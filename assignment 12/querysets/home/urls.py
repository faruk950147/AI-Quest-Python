from django.urls import path
from home.views import StudentRegistrationPost
urlpatterns = [
    path('', StudentRegistrationPost.as_view(), name = 'StudentRegistrationPost'),
]
