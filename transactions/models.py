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

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.wallet.user} {self.amount} {self.status}"
