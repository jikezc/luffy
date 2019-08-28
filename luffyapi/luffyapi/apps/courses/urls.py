from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'category/', views.CourseCategoryListAPIView.as_view()),
    path(r'', views.CourseListAPIView.as_view()),
    re_path(r'(?P<pk>\d+)', views.CourseRetrieveAPIView.as_view()),
    path(r"polyv/token/", views.PolyvAPIView.as_view()),
]
