from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control  font-17 fw-bold me-1 border border-dark",
            "placeholder":" نام کاربری ",
            "type": "email"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control  font-17 fw-bold me-1 border border-dark",
            "placeholder": "رمز عبور"
        })


class EmailCheckForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))

    error_messages = {
        "invalid_email": _(
            "Please enter a correct email!"
            "email may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


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


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."),
            )

        return cleaned_data
