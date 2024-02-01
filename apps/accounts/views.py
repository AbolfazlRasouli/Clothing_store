from django.contrib.auth import get_user_model
from .forms import EmailCheckForm, LoginForm, SignUpForm, PasswordResetForm
from .backends import CustomModelBackend as CMB
from .utils import store_otp, check_otp
from .tasks import send_otp_by_email, verify_link, send_by_email
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
from django.contrib.auth.decorators import login_required
import hashlib
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from passlib.hash import pbkdf2_sha256

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
        return self.request.GET.get("next", reverse_lazy("product:home_page"))


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

                        return redirect('product:home_page')

                    else:
                        messages.error(request, _("The entered code does not match!!!"))
                else:
                    messages.error(request, _("The OTP code has expired!!!"))
            else:
                messages.error(request, _("Email didn't save in session!"))
        else:
            messages.error(request, _("Sent OTP code can't Empty!"))

        return self.render_to_response(self.get_context_data())


# class LogoutView(View):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect("product:home_page")

class CustomLogoutView(LogoutView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('product:home_page')


class PasswordChange(FormView):
    template_name = 'accounts/email.html'
    form_class = EmailCheckForm

    def post(self, request):
        if email := request.POST.get('email', None):
            form = self.form_class(request.POST)
            if form.is_valid():
                user = CMB().authenticate(request=request, email=email)
                if user:
                    user_id = user.id
                    # print('***************************************', user_id)
                    hashed_user_id = pbkdf2_sha256.hash(str(user_id))
                    # print('***************************************', hashed_user_id)
                    url = reverse_lazy('accounts:password_reset', kwargs={'hashed_user_id': hashed_user_id})
                    request.session['user_email'] = user.email
                    status = send_by_email(email, url)
                    if status:
                        messages.success(
                            self.request,
                            _(
                                f"email sent Successfuly. " \
                                f"Check {email}."
                            )
                        )
                        return redirect("accounts:password_change")
                    else:
                        messages.error(request, _("Opss! some truble happend! please try again!"))
                else:
                    messages.error(request, _("you didn't define email or you need to signup!"))
            else:
                messages.error(request, _(form.errors))
        else:
            messages.error(request, _("email field cant Empty!"))

        return self.render_to_response(self.get_context_data())


class PasswordReset(View):
    template_name = 'accounts/reset_password.html'
    form_class = PasswordResetForm

    def get(self, request, hashed_user_id):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, hashed_user_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            result = form.cleaned_data
            password1 = result['password1']
            password2 = result['password2']
            email = request.session.get('user_email')
            user = get_object_or_404(get_user_model(), email=email)
            # print(user.id, '****************************************************')
            # a = pbkdf2_sha256.verify(str(user.id), hashed_user_id)
            # print(a)
            if pbkdf2_sha256.verify(str(user.id), hashed_user_id):
                new_password = password1
                user.set_password(new_password)
                user.save()
                return redirect('accounts:resetpassworddone')
            else:
                return HttpResponse('Unauthorized', status=401)


class ResetPasswordDone(TemplateView):
    template_name = 'accounts/reset_password_done.html'