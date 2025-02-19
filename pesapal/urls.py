from django.urls import path

from pesapal.views import RegisterIPNView

urlpatterns = [
    path("register-ipn/", RegisterIPNView.as_view(), name="register-ipn"),
]
