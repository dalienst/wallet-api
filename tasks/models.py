from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceSlugModel
from projects.models import Project

User = get_user_model()


class Task(UniversalIdModel, TimeStampedModel, ReferenceSlugModel):
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, related_name="tasks", blank=True, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_tasks", blank=True, null=True
    )
    title = models.CharField(max_length=255)
    date = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
