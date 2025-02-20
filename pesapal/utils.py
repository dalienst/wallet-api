import requests
from django.core.cache import cache
from wallet_api.settings import PESAPAL_QUERY_PAYMENT_STATUS


class PesapalAuthenticator:
    @staticmethod
    def get_bearer_token(consumer_key, consumer_secret):
        """
        Authenticate with Pesapal and retrieve the Bearer token.
        """
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


class PesapalTransactionStatus:
    @staticmethod
    def get_transaction_status(order_tracking_id, bearer_token):
        """
        Get the status of a transaction from Pesapal.
        """
        pesapal_url = (
            f"{PESAPAL_QUERY_PAYMENT_STATUS}?orderTrackingId={order_tracking_id}"
        )

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }

        response = requests.get(pesapal_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to get transaction status from Pesapal: {response.text}"
            )
