from django.urls import path
from account.views import (
    SignUpView,
    PasswordChangeView,
    PasswordResetView,
    ProfileView,
    
)
urlpatterns = [
    # Define your URL patterns here
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
