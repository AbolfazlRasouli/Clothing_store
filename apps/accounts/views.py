# from django.shortcuts import render
# from django.views import View
# from django.shortcuts import render, redirect
# from django.contrib.auth.views import LoginView
# from .forms import LoginForm, SignUpForm
# from django.urls import reverse_lazy
# from django.contrib.auth.decorators import user_passes_test
# from django.utils.decorators import method_decorator
# from django.views.generic.edit import CreateView
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic import DetailView
# from django.shortcuts import get_object_or_404
# from django.contrib.auth import login, logout
# from django.contrib.auth import get_user_model


# class LoginView(LoginView):
#     form_class = LoginForm
#     template_name = "accounts/login.html"
#
#     # def get_success_url(self):
#     #     return self.request.GET.get("next", reverse_lazy("app_home:home_page"))
#
#
# class SignUpView(CreateView):
#     template_name = "accounts/register.html"
#     form_class = SignUpForm
#
#     def get_success_url(self):
#         return reverse_lazy("app_home:home_page")
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         login(self.request, self.object)
#         return response


# class LogoutView(View):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect("app_home:home_page")


from django.contrib.auth import get_user_model
from .forms import EmailCheckForm, LoginForm
from .backends import CustomModelBackend as CMB
from .utils import store_otp, check_otp
from .tasks import send_otp_by_email

from django.views import View

from django.views.generic.edit import CreateView, FormView

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy


User = get_user_model()


class UsernameLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("home"))

    # def get_success_url(self):
    #     username = self.request.POST.get("username")
    #     first_name = User.objects.get(username=username).first_name
    #
    #     messages.success(
    #         self.request,
    #         _(
    #             f"Login Successfuly. " \
    #             f"Welcome {first_name if first_name else username}."
    #         )
    #     )

        # next_url = self.request.GET.get('next')
        # if next_url:
        #     return next_url
        # return reverse_lazy('core:home')