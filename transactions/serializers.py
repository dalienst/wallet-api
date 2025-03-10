from rest_framework import serializers

from transactions.models import Transaction
from wallets.models import Wallet


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(
        slug_field="reference",
        queryset=Wallet.objects.all(),
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "wallet",
            "amount",
            "status",
            "transaction_id",
            "payment_method",
            "confirmation_code",
            "payment_status_description",
            "payment_account",
            "currency",
            "payment_date",
            "merchant_reference",
            "callback_url",
            "reference",
            "slug",
            "created_at",
            "updated_at",
        )
