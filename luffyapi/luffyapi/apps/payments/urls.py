from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r"(?P<order_number>\d+)/alipay/", views.AlipayAPIView.as_view()),
    path(r"alipay/result/", views.AlipayResultAPIView.as_view()),
]

