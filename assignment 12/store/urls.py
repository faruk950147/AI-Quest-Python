from django.urls import path
from store.views import (
    HomeView,
)
urlpatterns = [
    # Define your URL patterns here
    path('', HomeView.as_view(), name='home'),
]
