from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

router = DefaultRouter()


urlpatterns = [
    path('register_user/', views.RegisterUserView.as_view(), name='register_user'),
    path('login/', views.LoginUserAPIView.as_view(), name='login'),
]