from rest_framework.generics import ListAPIView
from .models import CourseCategory, Course
from .serializers import CourseCategoryModelSerializer, CourseModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    """课程分类列表"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategoryModelSerializer


# 原来的课程列表
# class CourseListAPIView(ListAPIView):
#     """课程列表"""
#     queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
#     serializer_class = CourseModelSerializer


# 按条件筛选[分类]展示课程信息
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CustomPageNumberPagination


class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course_category',)
    ordering_fields = ("id", "students", "price")
    # # 指定分页器
    pagination_class = CustomPageNumberPagination


from .serializers import CourseDetailModelSerializer
from rest_framework.generics import RetrieveAPIView


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False)
    serializer_class = CourseDetailModelSerializer


from luffyapi.libs.polyv import PolyvPlayer
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PolyvAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取保利威云视频加密播放的token"""
        """接受客户端的请求参数"""
        vid = request.query_params.get("vid")  # 视频播放ID
        remote_addr = request.META.get("REMOTE_ADDR")  # 用户的IP
        user_id = request.user.id  # 用户ID
        user_name = request.user.username  # 用户名
        polyv = PolyvPlayer(
            settings.POLYV_CONFIG["userId"],
            settings.POLYV_CONFIG["secretkey"],
            settings.POLYV_CONFIG["tokenUrl"],
        )

        data = polyv.get_video_token(vid, remote_addr, user_id, user_name)
        print(data)
        return Response(data)
