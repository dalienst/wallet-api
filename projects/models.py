from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import UniversalIdModel, ReferenceSlugModel, TimeStampedModel

User = get_user_model()


class Project(UniversalIdModel, ReferenceSlugModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    date = models.DateField()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
