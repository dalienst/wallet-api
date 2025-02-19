import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

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

    def post(self, request, *args, **kwargs):
        transaction_id = request.data.get("pesapal_transaction_tracking_id")
        status = request.data.get("pesapal_notification_type")

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            transaction.status = status
            transaction.save()
            return Response(status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND
            )
