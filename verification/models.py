from django.db import models

from accounts.abstracts import UniversalIdModel, TimeStampedModel


class VerificationCode(UniversalIdModel, TimeStampedModel):
    code = models.CharField(max_length=6)
