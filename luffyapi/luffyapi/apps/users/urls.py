from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    # rest_framework_jwt 提供的登录获取token的视图
    path(r'authorizations/', obtain_jwt_token, name='authorizations'),
    path(r'captcha/', views.CaptchaAPIView.as_view()),
    path(r'register/', views.UserAPIView.as_view()),
    re_path(r'sms/(?P<mobile>1[3-9]\d{9})/', views.SMSCodeAPIView.as_view()),
    path(r'orders/', views.UserOrderAPIView.as_view()),
]
