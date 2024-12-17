from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    VerifyCodeSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            verification = serializer.validated_data.get("verification")

            # Verify the account
            user.is_verified = True
            user.save()

            # Mark code as used
            verification.used = True
            verification.save()

            return Response(
                {"message": "Account verified successfully!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
