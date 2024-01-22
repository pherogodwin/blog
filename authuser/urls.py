from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

app_name = "authuser"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="authuser/login.html", authentication_form=LoginForm),
         name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]