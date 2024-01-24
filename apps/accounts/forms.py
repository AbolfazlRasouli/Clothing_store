from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control bg-transparent text-white font-17 fw-bold",
            "placeholder":" نام کاربری ",
            "type": "email"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control bg-transparent text-white font-17 fw-bold",
            "placeholder": "رمز عبور"
        })


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control  font-17 fw-bold me-1 border border-dark",
            "placeholder": "نام کاربری",
            "required": "",
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control  font-17 border border-dark",
            "placeholder": "ایمیل",
            "required": "",
            "type": "email",
        })
        self.fields["phone_number"].widget.attrs.update({
            "class": "form-control  font-17 fw-bold border border-dark",
            "placeholder": "شماره تلفن",
            "required": "",
            "type": "tel"
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control font-17 fw-bold ms-1 border border-dark",
            "placeholder": "رمز عبور",
            "required": "",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control  font-17 fw-bold me-1 border border-dark",
            "placeholder": "تکرار رمز عبور",
            "required": "",
        })
