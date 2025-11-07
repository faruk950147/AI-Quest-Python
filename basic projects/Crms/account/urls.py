from django.urls import path
from account.views import (
    SignUpView,
    SignInView,
    SignOutView,
    ChangesPasswordView,
    ProfileView,
    ActivationView,
    SendOTPView,
    ResetPasswordView,
)
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activationview/<uidb64>/<token>/', ActivationView.as_view(), name='activationview'),
    path('sign/', SignInView.as_view(), name='sign'),
    path('signout/', SignOutView.as_view(), name='signout'),
    path('changespassword/', ChangesPasswordView.as_view(), name='changespassword'),
    path('sendotpview/', SendOTPView.as_view(), name='sendotpview'),
    path('resetpasswordview/', ResetPasswordView.as_view(), name='resetpasswordview'),
    path('profileview/', ProfileView.as_view(), name='profileview'),
]
