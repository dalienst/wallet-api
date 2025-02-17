from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from wallets.models import Wallet
from wallets.serializers import WalletSerializer

class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)