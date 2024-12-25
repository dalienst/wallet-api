from rest_framework import serializers

from projects.models import Project
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field="slug", queryset=Project.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "date",
            "is_completed",
            "created_at",
            "updated_at",
            "reference",
            "slug",
        )
