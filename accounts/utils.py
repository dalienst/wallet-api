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
    return random_string.upper()


def generate_reference():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(10))
    return random_string.upper()


def send_verification_email(user, verification_code):
    """
    A function to send a verification email
    """
    current_year = datetime.now().year
    email_body = render_to_string(
        "account_verification.html",
        {
            "user": user,
            "verification_code": verification_code,
            "current_year": current_year,
        },
    )

    send_mail(
        subject="Verify your account",
        message="",  # Leave plain text empty if you're only sending HTML
        from_email=EMAIL_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=email_body,  # Provide the rendered HTML template here
    )


def send_password_reset_email(user, verification_code):
    """
    A function to send a password reset email
    """
    current_year = datetime.now().year
    email_body = render_to_string(
        "password_reset.html",
        {
            "user": user,
            "verification_code": verification_code,
            "current_year": current_year,
        },
    )

    send_mail(
        subject="Reset your password",
        message="",  # Leave plain text empty if you're only sending HTML
        from_email=EMAIL_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=email_body,  # Provide the rendered HTML template here
    )
