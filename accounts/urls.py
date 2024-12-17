from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    UserCreateView,
    UserDetailView,
    CustomTokenObtainPairView,
    VerifyEmailView,
    RequestPasswordResetView,
    PasswordResetView,
)

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", UserCreateView.as_view(), name="user-create"),
    path("verify-account/", VerifyEmailView.as_view(), name="verify-email"),
    path("<str:id>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "reset/",
        RequestPasswordResetView.as_view(),
        name="request-password-reset",
    ),
    path("reset-password/", PasswordResetView.as_view(), name="password-reset"),
]
