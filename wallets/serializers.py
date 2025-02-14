from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Wallet
        fields = (
            "id",
            "user",
            "balance",
            "currency",
            "status",
            "created_at",
            "updated_at",
            "reference",
            "slug",
        )

    def update(self, instance, validated_data):
        instance.balance = validated_data.get("balance", instance.balance)
        instance.currency = validated_data.get("currency", instance.currency)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
