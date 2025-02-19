import requests
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta


class PesapalAuthenticator:
    """
    Handles Pesapal authentication and token retrieval.
    """

    PESAPAL_AUTH_BASE_URL = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
    # PESAPAL_AUTH_BASE_URL = "https://pay.pesapal.com/v3/api/Auth/RequestToken"
    TOKEN_EXPIRY_SECONDS = 300  # 5 minutes
    TOKEN_EXPIRY_BUFFER = 30  # Refresh token 30 seconds before expiry

    # Store token and expiry as class variables for caching
    _token = None
    _expiry = None

    @classmethod
    def get_token(cls):
        """
        Fetch a new token from Pesapal if it is expired or not set.
        """
        # Reuse the token if it's still valid
        if (
            cls._token
            and cls._expiry
            and now() < cls._expiry - timedelta(seconds=cls.TOKEN_EXPIRY_BUFFER)
        ):
            return cls._token

        # Request new token
        headers = {"Content-Type": "application/json"}
        data = {
            "consumer_key": settings.PESAPAL_CONSUMER_KEY,
            "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
        }

        response = requests.post(cls.PESAPAL_AUTH_BASE_URL, json=data, headers=headers)

        try:
            response_data = response.json()
        except Exception as e:
            raise Exception(f"Error decoding Pesapal response: {str(e)}")

        if response.status_code == 200 and "token" in response_data:
            cls._token = response_data["token"]
            cls._expiry = now() + timedelta(seconds=cls.TOKEN_EXPIRY_SECONDS)
            return cls._token

        raise Exception(
            f"Pesapal Auth Error: {response_data.get('message', 'Unknown error')}"
        )
