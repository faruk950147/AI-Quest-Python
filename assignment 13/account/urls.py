from django.urls import path
from account.views import SignUpView, SignInView, ChangesPasswordView
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('change-password/', ChangesPasswordView.as_view(), name='change-password'),
]