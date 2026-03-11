from django.urls import path
from task.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]