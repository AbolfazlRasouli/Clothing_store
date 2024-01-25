from django.contrib.auth import get_user_model
from .forms import EmailCheckForm, LoginForm, SignUpForm
from .backends import CustomModelBackend as CMB
from .utils import store_otp, check_otp
from .tasks import send_otp_by_email, verify_link
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from config.celery import app


User = get_user_model()


class SignUpView(CreateView):
    template_name = "accounts/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:signup')

    # @app.task(name='form_valid', bind=True)
    def form_valid(self, form):
        response = super().form_valid(form)
        url = reverse_lazy('accounts:verify', kwargs={'user_id': self.object.id})
        # user_id = self.object.id
        email = self.object.email
        status = verify_link(email, url)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        if status:
            messages.success(
                self.request,
                _(
                    f"verfiy link sent Successfuly. " \
                    f"Check {email}."
                )
            )
            print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        else:
            messages.error(self.request, _("Opss! some truble happend! please try again!"))
            print('ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
        return response

    # @app.task(name='get_success_url', bind=True)
    # def get_success_url(self):
    #     return reverse_lazy("accounts:verify", )


class VerifyUser(TemplateView):
    template_name = 'accounts/verified.html'
    def get(self, request, user_id, **kwargs):
        q = get_user_model().objects.get(id=user_id)
        q.is_active = True
        q.save()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



class UsernameLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("home"))


class EmailLoginView(FormView):
    template_name = 'accounts/email.html'
    form_class = EmailCheckForm

    def post(self, request):
        if user_email := request.POST.get('email', None):
            form = self.form_class(request.POST)
            if form.is_valid():
                user = CMB().authenticate(request=request, email=user_email)
                if user:
                    otp_code = store_otp(user_email)
                    status = send_otp_by_email(user_email, otp_code)
                    if status:
                        request.session['email'] = user_email
                        messages.success(
                            self.request,
                            _(
                                f"Code sent Successfuly. " \
                                f"Check {user_email}."
                            )
                        )
                        return redirect("accounts:otp")
                    else:
                        messages.error(request, _("Opss! some truble happend! please try again!"))
                else:
                    messages.error(request, _("you didn't define email or you need to signup!"))
            else:
                messages.error(request, _(form.errors))
        else:
            messages.error(request, _("email field cant Empty!"))

        return self.render_to_response(self.get_context_data())


class OTPView(TemplateView):
    template_name = 'accounts/otp_code.html'

    def post(self, request, *args, **kwargs):
        if otp_code := request.POST.get('otp'):
            email = request.session.get('email')
            if email:
                otp_status = check_otp(email=email, send_otp=otp_code)
                if otp_status:
                    if otp_status != -1:
                        user = User.objects.get(email=email)
                        login(request, user)

                        username = user.username
                        first_name = user.first_name

                        messages.success(
                            self.request,
                            _(
                                f"Login Successfuly. " \
                                f"Welcome {first_name if first_name else username}."
                            )
                        )

                        return redirect('home')

                    else:
                        messages.error(request, _("The entered code does not match!!!"))
                else:
                    messages.error(request, _("The OTP code has expired!!!"))
            else:
                messages.error(request, _("Email didn't save in session!"))
        else:
            messages.error(request, _("Sent OTP code can't Empty!"))

        return self.render_to_response(self.get_context_data())


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")

