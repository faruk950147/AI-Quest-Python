from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import Profile
# Create your views here.
@method_decorator(never_cache, name='dispatch')
class CheckoutView(generic.View):
    def get(self, request):
        return render(request, 'checkout/checkout.html')
    
@method_decorator(never_cache, name='dispatch')
class CheckoutListView(generic.View):
    def get(self, request):
        return render(request, 'checkout/checkout_list.html')

