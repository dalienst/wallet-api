from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.validators import (
    validate_password_digit,
    validate_password_uppercase,
    validate_password_lowercase,
    validate_password_symbol,
)
from verification.models import VerificationCode
from accounts.utils import send_verification_email

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["id"] = str(user.id)
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_verified"] = user.is_verified
        token["reference"] = user.reference
        token["slug"] = user.slug

        return token


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "is_superuser",
            "is_verified",
            "reference",
            "slug",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        # create user
        user = User.objects.create_user(**validated_data)
        user.save()

        # create verification code
        verification_code = VerificationCode.objects.create(user=user)

        # send verification email
        send_verification_email(user, verification_code.code)

        return user


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Account with this email does not exist!")

        try:
            verification = user.verification_codes.get(
                code=code, purpose="email_verification", used=False
            )
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired verification code!")

        if not verification.is_valid():
            raise serializers.ValidationError(
                "The code has expired or already been used!"
            )

        attrs["user"] = user
        attrs["verification"] = verification

        return attrs
