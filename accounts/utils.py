import string
import secrets
from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from wallet.settings import EMAIL_USER


current_year = datetime.now().year


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
            "current_year": current_year,
        },
    )

    send_mail(
        "Verify your account",
        email_body,
        EMAIL_USER,
        [user.email],
        fail_silently=False,
    )


def send_password_reset_email(user, verification_code):
    """
    A function to send a password reset email
    """
    email_body = render_to_string(
        "password_reset.html",
        {
            "user": user,
            "verification_code": verification_code,
            "current_year": current_year,
        },
    )

    send_mail(
        "Reset your password",
        email_body,
        EMAIL_USER,
        [user.email],
        fail_silently=False,
    )
