from django.urls import path
from home.views import StudentRegistrationPost, StudentRegistrationGet, CustomMiddlewareView
urlpatterns = [
    path('', StudentRegistrationPost.as_view(), name = 'StudentRegistrationPost'),
    path('get', StudentRegistrationGet.as_view(), name = 'StudentRegistrationGet'),
    path('middleware', CustomMiddlewareView.as_view(), name = 'CustomMiddlewareView')
]
