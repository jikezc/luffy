# Create your views here.
from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import BannerInfo
from .serializers import BannerInfoSerializer


class BannerInfoListAPIView(ListAPIView):
    """轮播图列表"""
    queryset = BannerInfo.objects.filter( Q(is_show=True) & Q(is_delete=False)).order_by("-orders")
    serializer_class = BannerInfoSerializer

    # def get(self, request):
    #     print(BannerInfo.objects.filter(pk=1).first().image.url)
    #     return super().get(request)


from .models import NavInfo
from .serializers import NavInfoModelSerializer


class HeaderNavListAPIView(ListAPIView):
    """头部导航列表"""
    queryset = NavInfo.objects.filter(is_show=True,is_delete=False,opt=1).order_by("orders")
    serializer_class = NavInfoModelSerializer

class FooterNavListAPIView(ListAPIView):
    """脚部导航列表"""
    queryset = NavInfo.objects.filter(is_show=True,is_delete=False,opt=2).order_by("orders")
    serializer_class = NavInfoModelSerializer

