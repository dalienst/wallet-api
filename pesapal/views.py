import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pesapal.models import PesapalIPN
from django.core.cache import cache
from pesapal.serializers import PesapalIPNSerializer
from pesapal.utils import PesapalAuthenticator
from wallet_api.settings import (
    PESAPAL_CONSUMER_KEY,
    PESAPAL_CONSUMER_SECRET,
    PESAPAL_GET_IPN_URLS,
)


class RegisterIPNView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate the request
        serializer = PesapalIPNSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        url = serializer.validated_data.get("url")
        ipn_notification_type = serializer.validated_data.get(
            "ipn_notification_type", "GET"
        )

        # Get consumer key and secret from request body
        consumer_key = PESAPAL_CONSUMER_KEY
        consumer_secret = PESAPAL_CONSUMER_SECRET

        if not consumer_key or not consumer_secret:
            return Response(
                {"error": "Consumer key and secret are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get the cached or new Bearer token
            bearer_token = PesapalAuthenticator.get_cached_bearer_token(
                consumer_key, consumer_secret
            )

            # Register the IPN URL with Pesapal
            # pesapal_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"
            pesapal_url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"

            payload = {"url": url, "ipn_notification_type": ipn_notification_type}

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}",
            }

            response = requests.post(pesapal_url, json=payload, headers=headers)

            if response.status_code == 200:
                # Extract the notification_id from the response
                notification_id = response.json().get("ipn_id")

                # Save the IPN registration details to the database
                pesapal_ipn = PesapalIPN(
                    url=url,
                    ipn_notification_type=ipn_notification_type,
                    notification_id=notification_id,
                )
                pesapal_ipn.save()

                # Return the serialized data
                return Response(
                    PesapalIPNSerializer(pesapal_ipn).data,
                    status=status.HTTP_201_CREATED,
                )
            elif response.status_code == 401:  # Unauthorized (token expired)
                # Clear the cached token and retry
                cache.delete("pesapal_bearer_token")
                return self.post(request, *args, **kwargs)  # Retry the request
            else:
                # If there's an error, return the error response from Pesapal
                return Response(response.json(), status=response.status_code)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetIPNUrlsView(APIView):
    def get(self, request, *args, **kwargs):
        # Get consumer key and secret from request body
        consumer_key = PESAPAL_CONSUMER_KEY
        consumer_secret = PESAPAL_CONSUMER_SECRET

        if not consumer_key or not consumer_secret:
            return Response(
                {"error": "Consumer key and secret are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the IPNs from PESAPAL_GET_IPN_URLS
        try:
            # Get the cached or new Bearer token
            bearer_token = PesapalAuthenticator.get_cached_bearer_token(
                consumer_key, consumer_secret
            )

            # Get the IPN URLs from Pesapal
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}",
            }

            response = requests.get(PESAPAL_GET_IPN_URLS, headers=headers)

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            elif response.status_code == 401:  # Unauthorized (token expired)
                # Clear the cached token and retry
                cache.delete("pesapal_bearer_token")
                return self.get(request, *args, **kwargs)  # Retry the request
            else:
                # If there's an error, return the error response from Pesapal
                return Response(response.json(), status=response.status_code)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
