from django.db import models

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceSlugModel
from projects.models import Project


class Task(UniversalIdModel, TimeStampedModel, ReferenceSlugModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    date = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
