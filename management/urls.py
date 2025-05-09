from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from management.views import *

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "login/",
        LoginView.as_view(template_name="management/login.html"),
        name="wagtail_login"
    ),
    path("logout/", views.logout_view, name="wagtailadmin_logout"),
    path("profile/", views.profile, name="profile.html"),
    path("profile/edit/", views.profile_edit, name="profile_edit.html"),
    path("jobs/", views.jobs, name="jobs.html"),
]