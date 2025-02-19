from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


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
    """
    Implements creation of IPN data
    """

    permission_classes = [
        AllowAny,
    ]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests from pesapal
        """
        transaction_id = request.GET.get("OrderTrackingId")
        status = request.GET.get("OrderStatus")

        if not transaction_id or not status:
            return JsonResponse({"error": "Invalid request parameters"}, status=400)

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            transaction.status = status.upper()
            transaction.save()

            return JsonResponse(
                {"message": "Transaction status updated successfully"}, status=200
            )
        except Transaction.DoesNotExist:
            return JsonResponse({"error": "Transaction not found"}, status=404)

    def post(self, request, *args, **kwargs):
        transaction_id = request.data.get("pesapal_transaction_tracking_id")
        status = request.data.get("pesapal_notification_type")

        # Update the transaction status in the database
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            transaction.status = status
            transaction.save()
        except Transaction.DoesNotExist:
            # Handle the case where the transaction doesn't exist
            pass

        return Response(status=status.HTTP_200_OK)
