from django.urls import path
from task.views import HomeView, ToggleTaskView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('toggle-task/<int:pk>/', ToggleTaskView.as_view(), name='toggle-task'),
]