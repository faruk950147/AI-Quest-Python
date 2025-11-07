from django.urls import path
from account.views import SignupView
urlpatterns = [
    path('sign_up/', SignupView.as_view(), name='sign_up'),
]