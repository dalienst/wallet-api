from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "user",
            "title",
            "date",
            "created_at",
            "updated_at",
            "reference",
            "slug",
        )
