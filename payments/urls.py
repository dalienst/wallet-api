from django.urls import path

from payments.views import SubmitOrderView, PesapalCallbackView, GetPaymentStatus

urlpatterns = [
    path("submit-order/", SubmitOrderView.as_view(), name="submit-order"),
    path("callback/", PesapalCallbackView.as_view(), name="callback"),
    path("payment-status/", GetPaymentStatus.as_view(), name="payment-status"),
]
