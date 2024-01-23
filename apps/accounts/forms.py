from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control bg-transparent text-white font-17 fw-bold",
            "placeholder":"ایمیل یا شماره تلفن",
            "type": "email"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control bg-transparent text-white font-17 fw-bold",
            "placeholder": "رمز عبور"
        })

