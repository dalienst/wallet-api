import uuid

from django.db import models
from accounts.utils import generate_reference, generate_slug


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniversalIdModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
    )

    class Meta:
        abstract = True


class ReferenceSlugModel(models.Model):
    reference = models.CharField(max_length=10, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug()
        if not self.reference:
            self.reference = generate_reference()
        super().save(*args, **kwargs)
