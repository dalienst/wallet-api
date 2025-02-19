import secrets
import string


def generate_merchant_reference(length=10):
    """Generates a unique merchant reference ID."""
    random_string = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
    return f"CT-Wallet-{random_string}"
