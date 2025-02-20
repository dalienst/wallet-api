from django.db import models

from accounts.abstracts import UniversalIdModel, ReferenceSlugModel, TimeStampedModel
from wallets.models import Wallet


class Transaction(UniversalIdModel, TimeStampedModel, ReferenceSlugModel):
    """
    Transaction Model
    """

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REVERSED", "Reversed"),
    ]

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="The unique transaction ID from Pesapal.",
    )
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)
    payment_status_description = models.CharField(max_length=100, blank=True, null=True)
    payment_account = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, default="KES")
    payment_date = models.DateTimeField(blank=True, null=True)
    merchant_reference = models.CharField(max_length=50, blank=True, null=True)
    callback_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.wallet.user} {self.amount} {self.status}"
