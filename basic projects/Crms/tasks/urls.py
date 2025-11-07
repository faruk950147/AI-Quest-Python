from django.urls import path
from tasks.views import (
    TasksView,
)
urlpatterns = [
    path('', TasksView.as_view(), name='taskview'),
]