from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import create_wallet_view, load_wallet_view, get_wallet_balance_view
from . import views

router = DefaultRouter()



urlpatterns = [
    path('wallet_creation', views.WalletCreateView.as_view(), name='wallet_creation'),
]

