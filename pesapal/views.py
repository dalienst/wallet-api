import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pesapal.models import PesapalIPN
from pesapal.serializers import PesapalIPNSerializer
from pesapal.utils import PesapalAuthenticator


class RegisterIPNView(APIView):
    """
    Registers the IPN URL with Pesapal and saves it to the database.
    """

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

        try:
            # Get Pesapal Bearer Token
            bearer_token = PesapalAuthenticator.get_token()

            # Register IPN with Pesapal
            pesapal_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"

            payload = {
                "url": url,
                "ipn_notification_type": ipn_notification_type,
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}",
            }

            response = requests.post(pesapal_url, json=payload, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                notification_id = response_data.get("ipn_id")

                # Save IPN to the database
                pesapal_ipn = PesapalIPN.objects.create(
                    url=url,
                    ipn_notification_type=ipn_notification_type,
                    notification_id=notification_id,
                )

                return Response(
                    PesapalIPNSerializer(pesapal_ipn).data,
                    status=status.HTTP_201_CREATED,
                )

            return Response(response.json(), status=response.status_code)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
