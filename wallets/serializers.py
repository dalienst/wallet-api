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
