from django.urls import path

from transactions.views import (
    TransactionListCreateAPIView,
    TrasactionDetailAPIView,
    IPNHandlerAPIView,
)

urlpatterns = [
    path("", TransactionListCreateAPIView.as_view(), name="transaction-list-create"),
    path("<str:slug>/", TrasactionDetailAPIView.as_view(), name="transaction-detail"),
    path("pesapal/ipn/", IPNHandlerAPIView.as_view(), name="ipn-handler"),
]
