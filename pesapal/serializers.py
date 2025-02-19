from rest_framework import serializers

from pesapal.models import PesapalIPN


class PesapalIPNSerializer(serializers.ModelSerializer):
    class Meta:
        model = PesapalIPN
        fields = (
            "id",
            "url",
            "notification_type",
            "notification_id",
            "created_at",
            "updated_at",
            "reference",
            "slug",
        )
