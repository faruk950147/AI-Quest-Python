from django.urls import path

from order.views import(
    CheckoutView, AddressView,
)
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('address/', AddressView.as_view(), name='address'),
]