from rest_framework import serializers
from .models import User
from django_redis import get_redis_connection


class UserModelSerializer(serializers.ModelSerializer):
    """用户注册的序列化器"""
    # 字段声明
    sms_code = serializers.CharField(write_only=True, max_length=6, help_text="短信验证码")
    token = serializers.CharField(max_length=1024, read_only=True, help_text="jwt的token字符串")

    # 模型信息
    class Meta:
        model = User
        fields = ["id", "mobile", "password", "sms_code", "token"]
        extra_kwargs = {
            "id":{
              "read_only":True,
            },
            "mobile":{
                "max_length": 15,
                "required": True
            },
            "password":{
                "write_only": True,
                "max_length": 128,
                "required": True
            }
        }

    # 验证数据
    def validate(self, data):
        '''多字段的验证码'''
        mobile = data.get("mobile")
        sms_code = data.get("sms_code")
        redis = get_redis_connection("sms_code")
        # 在redis中存储的所有数据最终格式都是bytes类型，所以我们读取redis中的任何内容都要进行转换
        real_sms_code = redis.get("sms_%s" % mobile).decode()
        # print(real_sms_code)

        # 删除redis中的短信验证码
        try:
            redis.delete("sms_%s" % mobile)
        except:
            pass

        if real_sms_code !=  sms_code:
            raise serializers.ValidationError({"message":"短信验证码已过期或错误！"})

        return data

    # 保存信息
    def create(self, validated_data):
        """添加用户"""
        # 删除不存在于数据库的字段
        del validated_data["sms_code"]

        # 保存用户信息，设置一些字段的默认值
        validated_data["username"] = validated_data["mobile"]

        # 调用当前模型序列化器父类的create
        user = super().create(validated_data)

        # 对密码进行加密
        user.set_password(user.password)
        user.save()

        # 生成jwt的token值，用于记录登录状态
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)

        # 最终token作为user模型的一个字段返回给客户端
        user.token = jwt_encode_handler(payload)

        return user


from order.models import Order
class UserOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id","create_time","order_number","status","order_status","pay_time","course_list"]