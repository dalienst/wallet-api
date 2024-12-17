import string
import secrets

from django.core.mail import send_mail
from django.template.loader import render_to_string
from wallet.settings import DOMAIN, EMAIL_USER


def generate_slug():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(16))
    return random_string


def generate_reference():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(10))
    return random_string.upper()


def send_verification_email(user, verification_code):
    """
    A function to send a verification email
    """
    email_body = render_to_string(
        "account_verification.html",
        {
            "user": user,
            "verification_code": verification_code,
        },
    )

    send_mail(
        "Verify your account",
        email_body,
        EMAIL_USER,
        [user.email],
        fail_silently=False,
    )
