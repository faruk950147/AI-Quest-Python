from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (
    SignUpView,
    # SignInView, 
    # SignOutView, 
    PasswordChangeView, 
    PasswordResetView,
    ProfileView
)
from accounts.forms import SignInForm

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    # The custom SignInView and SignOutView are commented out in favor of using Django's built-in auth views with custom forms and templates.
    # path('sign-in/', SignInView.as_view(), name='sign-in'),
    # path('sign-out/', SignOutView.as_view(), name='sign-out'),
    # probational way using django built-in auth views
    path('sign-in/', auth_views.LoginView.as_view(template_name='accounts/sign-in.html', 
    authentication_form=SignInForm), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='sign-in'), name='sign-out'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
