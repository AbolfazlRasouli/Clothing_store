from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model


class LoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

    # def get_success_url(self):
    #     return self.request.GET.get("next", reverse_lazy("app_home:home_page"))