from django.urls import path
from cart.views import (
    AddToCartView, CartDetailView,
)
urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('detail/', CartDetailView.as_view(), name='cart-detail'),
]