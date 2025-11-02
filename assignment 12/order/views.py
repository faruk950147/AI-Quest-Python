from django.shortcuts import render
from django.views import generic

# Create your views here.
class CheckoutView(generic.View):
    def get(self, request):
        return render(request, 'order/checkout.html')

class AddressView(generic.View):
    def get(self, request):
        return render(request, 'order/address.html')