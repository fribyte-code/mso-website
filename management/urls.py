from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "login/",
        LoginView.as_view(template_name="management/login.html"),
        name="wagtail_login"
    ),
    path("logout/", views.logout_view, name="wagtailadmin_logout"),
]