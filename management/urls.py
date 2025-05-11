from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from management.views import *

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_jobs/", views.my_assigned_jobs, name="my_assigned_jobs"),
    path(
        "login/",
        LoginView.as_view(template_name="management/login.html"),
        name="wagtail_login"
    ),
    path("logout/", views.logout_view, name="wagtailadmin_logout"),
    path("profile/edit/", views.profile_edit, name="profile_edit.html"),
    path("profile/", views.profile, name="profile.html"),
    path("jobs/", views.jobs, name="jobs"),
    path("admin/profile_edit/<int:pk>/", views.admin_profile_edit, name="admin-profile-edit"),
    path("admin/", views.admin, name="admin"),
]