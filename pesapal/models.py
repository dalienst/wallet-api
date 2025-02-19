from django.db import models

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceSlugModel


class PesapalIPN(TimeStampedModel, UniversalIdModel, ReferenceSlugModel):
    """
    Model to store Pesapal IPN data
    """

    url = models.URLField(
        max_length=255, help_text="The IPN URL to be registered with Pesapal."
    )
    notification_type = models.CharField(
        max_length=10,
        default="GET",
        help_text="The type of IPN notification (GET or POST).",
    )
    notification_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="The IPN ID returned by Pesapal after registration.",
    )

    class Meta:
        verbose_name = "Pesapal IPN"
        verbose_name_plural = "Pesapal IPNs"
        ordering = ("-created_at",)

    def __str__(self):
        return f"IPN: {self.url} (ID: {self.notification_id})"
