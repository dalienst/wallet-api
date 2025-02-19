from django.urls import path

from pesapal.views import RegisterIPNView, GetIPNUrlsView

urlpatterns = [
    path("register-ipn/", RegisterIPNView.as_view(), name="register-ipn"),
    path("get-ipn/", GetIPNUrlsView.as_view(), name="get-ipn"),
]
