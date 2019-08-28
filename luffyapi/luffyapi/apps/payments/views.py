from rest_framework.views import APIView
from alipay import AliPay
from django.conf import settings
from order.models import Order
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from coupon.models import UserCoupon
from django.db import transaction
from users.models import UserCourse
from courses.models import CourseExpire
from users.models import User
import logging

log = logging.getLogger("django")


class AlipayAPIView(APIView):
    def post(self, request, order_number):
        """生成支付宝支付链接的地址"""
        # 接受订单信息
        try:
            # order_status=0 表示未支付宝
            order = Order.objects.get(order_number=order_number, order_status=0)
        except Order.DoesNotExist:
            return Response({"message": "对不起当前订单不存在或者已经支付了！"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建支付宝的sdk对象
        alipay = AliPay(
            appid=settings.ALIPAY_CONFIG["appid"],
            app_notify_url=settings.ALIPAY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIPAY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIPAY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIPAY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIPAY_CONFIG["debug"],  # 默认False
        )

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,  # 订单号
            total_amount=float(order.real_price),  # 订单总金额[单位：元]
            subject=order.order_title,  # 订单标题
            return_url=settings.ALIPAY_CONFIG["return_url"],  # 同步通知地址
            notify_url=settings.ALIPAY_CONFIG["notify_url"],  # 异步通知地址
        )

        pay_url = settings.ALIPAY_CONFIG["gateway_url"] + order_string

        return Response({"pay_url": pay_url})


class AlipayResultAPIView(APIView):
    """
    支付宝支付结果的通知处理
    """

    def get(self, request):
        # for rest_framework users
        data = request.query_params.dict()
        return self.result(data)

    def post(self, request):
        """处理异步通知结果
        1. 线下开发是不起作用的，因为外网的支付宝服务器无法访问我们的局域网地址
        2. 如果使用了代理服务器，通过代理方式提供对外访问时，异步通知会在转发请求的过程中存在丢失数据的可能
        """
        data = request.data.dict()
        return self.result(data)

    def result(self, data):
        signature = data.pop("sign")

        # 创建支付宝的sdk对象
        alipay = AliPay(
            appid=settings.ALIPAY_CONFIG["appid"],
            app_notify_url=settings.ALIPAY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIPAY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIPAY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIPAY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIPAY_CONFIG["debug"],  # 默认False
        )

        # verification
        success = alipay.verify(data, signature)
        if success:

            # 修改订单状态
            out_trade_no = data.get("out_trade_no")
            try:
                order = Order.objects.get(order_number=out_trade_no, order_status=0)
            except Order.DoesNotExist:
                return Response({"message": "对不起当前订单不存在或者已经支付了！"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                # 记录事务的回滚点
                save_id = transaction.savepoint()

                order.order_status = 1
                order.pay_time = datetime.now()
                order.save()

                # 如果订单中使用了优惠券，则优惠券的使用状态要调整
                if order.coupon > 0:
                    user_coupon_id = order.coupon
                    try:
                        user_coupon = UserCoupon.objects.get(pk=user_coupon_id, is_use=False)
                        user_coupon.is_use = True
                        user_coupon.save()

                    except UserCoupon.DoesNotExist:
                        log.error("生成订单支付结果有误！优惠券发生异常！")
                        transaction.savepoint_rollback(save_id)

                # 如果用户使用了积分，则扣除相应积分
                user = User.objects.get(pk=order.user_id)
                if order.credit > 0:
                    user.credit = user.credit - order.credit
                    if user.credit > 0:
                        user.save()
                    else:
                        log.error("生成订单支付结果有误！积分计算有误！")
                        transaction.savepoint_rollback(save_id)

                # 记录用户购买商品的记录信息
                order_course = order.order_courses.all()
                course_list = []
                for item in order_course:

                    # 获取本次购买课程的有效期选项
                    try:
                        """有效期选项"""
                        course_expire = CourseExpire.objects.get(expire_time=item.expire, course=item.course)
                        expire = course_expire.expire_time
                        timer = expire * 24 * 60 * 60
                        out_timestamp = order.pay_time.timestamp() + timer
                        # 把数值时间戳转变成日期对象
                        out_time = datetime.fromtimestamp(out_timestamp)

                    except CourseExpire.DoesNotExist:
                        """永久有效，默认过期时间200年后"""
                        out_time = "2199-01-01 00:00:00"

                    """
                        判断之前当前用户是否购买过同一商品，如果购买了同一商品，则在前面的过期时间基础上增加时间
                        过期时间，也需要判断，如果现在已经过期了，则购买完课程以后的过期时间 = 现在 + 有效期
                                          如果现在没有过期，则购买完课程以后的过期时间 = 过期时间 + 有效期

                        购买完成，我们扣除了积分，但是我们也要针对本次消费的积分进行积分流水记录！ Credit
                    """
                    UserCourse.objects.create(
                        user=user,
                        course=item.course,
                        trade_no=data.get("trade_no"),
                        buy_type=1,
                        pay_time=order.pay_time,
                        out_time=out_time,
                        orders=0,

                    )
                    course_list.append({
                        "id": item.course.id,
                        "name": item.course.name
                    })

            data = {
                "order_number": order.order_number,
                "pay_time": order.pay_time,
                "real_price": order.real_price,
                "user_credit": user.credit,
                "course_list": course_list,
            }

            return Response(data)

        else:
            return Response({"message": "支付失败！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
