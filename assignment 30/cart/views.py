from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.
@method_decorator(never_cache, name='dispatch')
class AddToCartView(generic.View):
    def post(self, request):
        # Logic to add item to cart
        pass
@method_decorator(never_cache, name='dispatch')
class CartDetailView(generic.View):
    def get(self, request):
        # Logic to display cart details
        return render(request, 'cart/cart-detail.html')
