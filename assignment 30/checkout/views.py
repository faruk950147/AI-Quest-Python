from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.db.models import Sum, F
User = get_user_model()
from accounts.models import Profile
from cart.models import Cart
@method_decorator(never_cache, name='dispatch')
class CheckoutView(generic.View):
    login_url = reverse_lazy('sign-in')
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
        summary = cart_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))
        cart_total = float(summary["total_price"] or 0)
        shipping_cost = 50
        grand_total = cart_total + shipping_cost
        
        return render(request, 'checkout/checkout.html')
    
@method_decorator(never_cache, name='dispatch')
class CheckoutListView(generic.View):
    def get(self, request):
        return render(request, 'checkout/checkout_list.html')

