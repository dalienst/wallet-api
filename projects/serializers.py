from rest_framework import serializers

from projects.models import Project
from tasks.serializers import TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "user",
            "title",
            "tasks",
            "created_at",
            "updated_at",
            "reference",
            "slug",
        )
