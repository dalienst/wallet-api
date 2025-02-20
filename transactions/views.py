import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from pesapal.utils import PesapalAuthenticator, PesapalTransactionStatus
from wallet_api.settings import (
    PESAPAL_CONSUMER_KEY,
    PESAPAL_CONSUMER_SECRET,
)

logger = logging.getLogger(__name__)


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return super().get_queryset().filter(wallet__user=self.request.user)


class TrasactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return super().get_queryset().filter(wallet__user=self.request.user)


"""
Creating IPN
"""


class IPNHandlerAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Extract IPN parameters
        order_tracking_id = request.data.get("OrderTrackingId")
        order_merchant_reference = request.data.get("OrderMerchantReference")

        # Get consumer key and secret
        consumer_key = PESAPAL_CONSUMER_KEY
        consumer_secret = PESAPAL_CONSUMER_SECRET

        if not consumer_key or not consumer_secret:
            return Response(
                {"error": "Consumer key and secret are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Fetch the transaction from the database
            transaction = Transaction.objects.get(transaction_id=order_tracking_id)

            # Fetch the transaction status from Pesapal
            bearer_token = PesapalAuthenticator.get_cached_bearer_token(
                consumer_key, consumer_secret
            )
            transaction_status = PesapalTransactionStatus.get_transaction_status(
                order_tracking_id, bearer_token
            )

            # Update the transaction details
            transaction.payment_method = transaction_status.get("payment_method")
            transaction.confirmation_code = transaction_status.get("confirmation_code")
            transaction.payment_status_description = transaction_status.get(
                "payment_status_description"
            )
            transaction.payment_account = transaction_status.get("payment_account")
            transaction.currency = transaction_status.get("currency")
            transaction.payment_date = transaction_status.get("payment_date")
            transaction.merchant_reference = transaction_status.get(
                "merchant_reference"
            )
            transaction.callback_url = transaction_status.get("callback_url")
            transaction.status = transaction_status.get(
                "payment_status_description", "PENDING"
            ).upper()
            transaction.save()

            # Respond to Pesapal with a success status
            response_data = {
                "orderNotificationType": "IPNCHANGE",
                "orderTrackingId": order_tracking_id,
                "orderMerchantReference": order_merchant_reference,
                "status": 200,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get("OrderTrackingId")
        status = request.GET.get("OrderStatus")

        if not transaction_id or not status:
            logger.error("Invalid request parameters: transaction_id or status missing")
            return JsonResponse({"error": "Invalid request parameters"}, status=400)

        # Validate status
        valid_statuses = [choice[0] for choice in Transaction.STATUS_CHOICES]
        if status.upper() not in valid_statuses:
            logger.error(f"Invalid status received: {status}")
            return JsonResponse({"error": "Invalid status"}, status=400)

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            if transaction.status == status.upper():
                logger.info(f"Transaction {transaction_id} status is already {status}")
                return JsonResponse(
                    {"message": "Transaction status is already up-to-date"}, status=200
                )
            transaction.status = status.upper()
            transaction.save()
            logger.info(f"Transaction {transaction_id} status updated to {status}")
            return JsonResponse(
                {"message": "Transaction status updated successfully"}, status=200
            )
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return JsonResponse({"error": "Transaction not found"}, status=404)
