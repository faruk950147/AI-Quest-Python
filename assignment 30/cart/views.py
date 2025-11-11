from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from accounts.mixing import LoginRequiredMixin
# Create your views here.
@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
     login_url = reverse_lazy('sign-in')
     def post(self, request):
        # Logic to add item to cart
        product_id = request.POST.get('product-id')
        
        
@method_decorator(never_cache, name='dispatch')
class CartDetailView(generic.View):
    def get(self, request):
        # Logic to display cart details
        return render(request, 'cart/cart-detail.html')
