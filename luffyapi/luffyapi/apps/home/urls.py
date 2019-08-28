from django.urls import path,re_path
from . import views
urlpatterns = [
    path(r'banner/', views.BannerInfoListAPIView.as_view()),
    path(r'nav/header/', views.HeaderNavListAPIView.as_view()),
    path(r'nav/footer/', views.FooterNavListAPIView.as_view()),
]

