import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from pesapal.utils import PesapalAuthenticator
from payments.utils import generate_merchant_reference
from wallet_api.settings import (
    PESAPAL_CONSUMER_KEY,
    PESAPAL_CONSUMER_SECRET,
    API_URL,
    PESAPAL_PAYMENT_URL,
)

# TODO: Store the consumer key and secret of users in the database.
# This way, we can link them to a user/vendor account and enable them receive payments.


class SubmitOrderView(APIView):
    def post(self, request, *args, **kwargs):
        # validate the request
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        wallet = serializer.validated_data.get("wallet")
        amount = serializer.validated_data.get("amount")
        currency = "KES"

        # Generate a unique merchant reference
        merchant_reference = generate_merchant_reference()

        # Get consumer key and secret
        consumer_key = PESAPAL_CONSUMER_KEY
        consumer_secret = PESAPAL_CONSUMER_SECRET

        if not consumer_key or not consumer_secret:
            return Response(
                {"error": "Consumer key and secret are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get the cached or new bearer token
            bearer_token = PesapalAuthenticator.get_cached_bearer_token(
                consumer_key, consumer_secret
            )

            # prepare the payload for Pesapal
            payload = {
                "id": merchant_reference,
                "currency": currency,
                "amount": float(amount),
                "description": "Payment for services",
                "callback_url": f"{API_URL}/api/payments/callback",
                "notification_id": "bf8e52da-c691-4611-8b23-dc23d6ed2fd4",
                "billing_address": {
                    "email_address": wallet.user.email,
                    "country_code": "KE",
                },
            }

            # Submit the order request to Pesapal
            pesapal_url = PESAPAL_PAYMENT_URL

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}",
            }

            response = requests.post(pesapal_url, json=payload, headers=headers)

            if response.status_code == 200:
                # Extract response data
                response_data = response.json()
                order_tracking_id = response_data.get("order_tracking_id")
                redirect_url = response_data.get("redirect_url")

                # Create a new transaction record
                transaction = Transaction(
                    wallet=wallet,
                    amount=amount,
                    status="PENDING",
                    transaction_id=order_tracking_id,
                )
                transaction.save()

                return Response(
                    {
                        "order_tracking_id": order_tracking_id,
                        "redirect_url": redirect_url,
                    },
                    status=status.HTTP_200_OK,
                )

            elif response.status_code == 401:
                cache.delete("pesapal_bearer_token")
                return self.post(request, *args, **kwargs)
            else:
                return Response(
                    response.json(),
                    status=response.status_code,
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CallbackView(APIView):
    def get(self, request, *args, **kwargs):
        order_tracking_id = request.query_params.get("OrderTrackingId")

        if not order_tracking_id:
            return Response(
                {"error": "Invalid callback params"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            transaction = Transaction.objects.get(transaction_id=order_tracking_id)

            # Update the transaction status
            transaction.status = "COMPLETED"
            transaction.save()

            return Response(
                {"message": "Transaction completed successfully"},
                status=status.HTTP_200_OK,
            )
        except Transaction.DoesNotExist:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
