from django.urls import path
from task.views import HomeView, ToggleTaskView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('toggle-task/', ToggleTaskView.as_view(), name='toggle-task'),
]