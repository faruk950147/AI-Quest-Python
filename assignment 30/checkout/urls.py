from django.urls import path

from checkout.views import (
    CheckoutView,
    CheckoutListView,
)
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-list/', CheckoutListView.as_view(), name='checkout-list'),
]