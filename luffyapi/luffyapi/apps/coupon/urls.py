from django.urls import path
from . import views
urlpatterns = [
    path("",views.UserCouponAPIVew.as_view()),
]