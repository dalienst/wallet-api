from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import UserCreateView, UserDetailView, CustomTokenObtainPairView

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", UserCreateView.as_view(), name="user-create"),
    path("<str:id>/", UserDetailView.as_view(), name="user-detail"),
]
