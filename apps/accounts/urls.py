from django.urls import path
from .views import (UsernameLoginView, EmailLoginView, OTPView, LoginView, SignUpView, VerifyUser, CustomLogoutView,
                    PasswordChange, PasswordReset, ResetPasswordDone, profile, show_address, detail_address,
                    AddressUpdateView, CheckShipping, AddressCreateView, code_copun)


app_name = "accounts"
urlpatterns = [
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path(
        'login/',
        UsernameLoginView.as_view(redirect_authenticated_user=True),
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
        CustomLogoutView.as_view(),
        name='logout',
    ),
    path('verify/<int:user_id>', VerifyUser.as_view(), name='verify'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    # path('password_reset/<str:hashed_user_id>/', PasswordReset.as_view(), name='password_reset')
    path('password_reset/<str:hashed_user_id>/', PasswordReset.as_view(), name='password_reset'),
    path('resetpassworddone/', ResetPasswordDone.as_view(), name='resetpassworddone'),
    path('profile/', profile, name='profile'),
    path('showaddress/', show_address, name='show_address'),
    # path('show-address-single/', detail_address, name='detail_address')
    path('shipingcart/', CheckShipping.as_view(), name='shiping_cart'),
    path('addresscreat/', AddressCreateView.as_view(), name='address_create_view'),
    path('updateaddress/<int:pk>/', AddressUpdateView.as_view(), name='update_address'),
    path('copun/', code_copun, name='code_copon')

]
