from django.urls import path
from account.views import (
    SignInView,
    SignUpView,
    SignOutView,
    PasswordChangeView,
    PasswordResetView,
    ProfileView,
    
)
urlpatterns = [
    # Define your URL patterns here
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
