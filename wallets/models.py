from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceSlugModel

User = get_user_model()


class Wallet(UniversalIdModel, TimeStampedModel, ReferenceSlugModel):
    """
    Wallet used to track payments
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default="KES")
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Suspended", "Suspended")],
        default="Active",
    )

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.currency} {self.balance}"
