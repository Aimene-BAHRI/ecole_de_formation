# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
import imp
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash

from apps.home.forms import CustomPasswordChangeForm
from .forms import LoginForm, SignUpForm
from apps.home.views import staff_required

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

@staff_required(login_url="login")
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="{% "login" %}">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
class PasswordsChangeView(PasswordChangeView):
    form_class =  CustomPasswordChangeForm 
    success_url = reverse_lazy('home')           
