from django.urls import path
from .views import UsernameLoginView


app_name = "app_account"

# urlpatterns = [
#     path("login/",   LoginView.as_view(),   name="login_page"),
#     path("signup/",  SignUpView.as_view(),  name="signup_page"),
# ]




urlpatterns = [
    # path(
    #     'signup/',
    #     SignupView.as_view(),
    #     name='signup',
    # ),
    path(
        'login/',
        UsernameLoginView.as_view(),
        name='login',
    ),
    # path(
    #     'email/',
    #     EmailLoginView.as_view(),
    #     name='email',
    # ),
    # path(
    #     'email/otp/',
    #     OTPView.as_view(),
    #     name='otp',
    # ),
    # path(
    #     'logout/',
    #     CustomLogoutView.as_view(),
    #     name='logout',
    # ),
    # path('profile/<int:pid>/', Profile.as_view(), name='profile'),
]
