from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model


def is_not_authenticated(user):
    return not user.is_authenticated


class LoginView(LoginView):
    pass


class SignUpView(CreateView):
    pass


class LogoutView(View):
    pass


class ProfileView(DetailView):
    pass



