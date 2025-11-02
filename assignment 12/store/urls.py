from django.urls import path
from store.views import (
    HomeView, SingleProductView
)
urlpatterns = [
    # Define your URL patterns here
    path('', HomeView.as_view(), name='home'),
    path('single-product/', SingleProductView.as_view(), name='single-product'),
]
