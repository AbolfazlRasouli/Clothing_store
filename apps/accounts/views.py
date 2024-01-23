from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model



# class LoginView(LoginView):
#     form_class    = LoginForm
#     template_name = "accounts/login.html"
#
#     # def get_success_url(self):
#     #     return self.request.GET.get("next", reverse_lazy("app_home:home_page"))