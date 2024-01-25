from django.urls import path
from .views import UsernameLoginView, EmailLoginView, OTPView, LoginView, SignUpView, VerifyUser


app_name = "accounts"
urlpatterns = [
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path(
        'login/',
        UsernameLoginView.as_view(),
        name='login',
    ),
    path(
        'email/',
        EmailLoginView.as_view(),
        name='email',
    ),
    path(
        'email/otp/',
        OTPView.as_view(),
        name='otp',
    ),
    path(
        'logout/',
        LoginView.as_view(),
        name='logout',
    ),
    path('verify/<int:user_id>', VerifyUser.as_view(), name='verify')
]
