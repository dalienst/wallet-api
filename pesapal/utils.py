import requests
from django.core.cache import cache
from django.conf import settings


class PesapalAuthenticator:
    @staticmethod
    def get_bearer_token(consumer_key, consumer_secret):
        """
        Authenticate with Pesapal and retrieve the Bearer token.
        """
        # auth_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
        auth_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"

        payload = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}

        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        response = requests.post(auth_url, json=payload, headers=headers)

        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("token")
            expiry_date = token_data.get(
                "expiryDate"
            )  # Assuming Pesapal returns this field

            # Cache the token with its expiry time (5 minutes)
            cache.set(
                "pesapal_bearer_token", token, timeout=300
            )  # 300 seconds = 5 minutes
            return token
        else:
            raise Exception(f"Failed to authenticate with Pesapal: {response.text}")

    @staticmethod
    def get_cached_bearer_token(consumer_key, consumer_secret):
        """
        Retrieve the cached Bearer token or fetch a new one if expired.
        """
        token = cache.get("pesapal_bearer_token")
        if not token:
            token = PesapalAuthenticator.get_bearer_token(consumer_key, consumer_secret)
        return token
