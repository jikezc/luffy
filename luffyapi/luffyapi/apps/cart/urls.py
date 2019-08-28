from django.urls import path, re_path
from . import views
urlpatterns = []

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("course",views.CartAPIView,"cart")
urlpatterns += router.urls