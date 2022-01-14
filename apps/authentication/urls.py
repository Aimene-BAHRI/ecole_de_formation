# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from .views import login_view, register_user, PasswordsChangeView
from django.contrib.auth.views import LogoutView, PasswordChangeView
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('change/',PasswordsChangeView.as_view(
        template_name="registration/password_change_form.html"),name = 'password_change'),
]
