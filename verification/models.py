from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from accounts.abstracts import UniversalIdModel, TimeStampedModel
from verification.utils import generate_code

User = get_user_model()


class VerificationCode(UniversalIdModel, TimeStampedModel):
    PURPOSE_CHOICES = (
        ("email_verification", "Email Verification"),
        ("password_reset", "Password Reset"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verification_codes"
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    code = models.CharField(max_length=6, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a random 6-digit code
            self.code = generate_code()
        if not self.expires_at:
            # Set the expiration time to 30 minutes from now
            self.expires_at = now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_valid(self):
        return now() < self.expires_at and not self.used

    def __str__(self):
        return f"Verification Code for {self.user.email}"
