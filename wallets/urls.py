from django.urls import path

from wallets.views import WalletListCreateView, WalletDetailView

urlpatterns = [
    path("", WalletListCreateView.as_view(), name="wallet-list-create"),
    path("<str:slug>/", WalletDetailView.as_view(), name="wallet-detail"),
]
