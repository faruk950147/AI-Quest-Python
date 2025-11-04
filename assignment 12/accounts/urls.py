from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import SignUpView, PasswordChangeView, ProfileView
from accounts.forms import SignInForm

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', auth_views.LoginView.as_view(template_name='accounts/sign-in.html', authentication_form=SignInForm), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='sign-in'), name='sign-out'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password-reset.html'
    ), name='password-reset'),
]
