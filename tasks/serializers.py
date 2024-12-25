from rest_framework import serializers
from datetime import date

from projects.models import Project
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field="slug", queryset=Project.objects.all()
    )
    date = serializers.DateField()

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

    def validate_date(self, value):
        """
        Ensure the date is not in the past.
        """
        if value < date.today():
            raise serializers.ValidationError("The date cannot be in the past.")
        return value


class ProgresOverviewSerializer(serializers.Serializer):
    date = serializers.DateField()
    completed = serializers.IntegerField()
    incomplete = serializers.IntegerField()
