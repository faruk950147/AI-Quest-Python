from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from accounts.mixing import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.db.models import Sum, F
User = get_user_model()
from accounts.models import Profile
from cart.models import Cart
from checkout.models import Checkout

@method_decorator(never_cache, name='dispatch')
class CheckoutView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def get(self, request):
        checkout_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
        summary = checkout_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))
        shipping_cost = 120
        grand_total = (summary['total_price'] or 0) + shipping_cost
        profiles = Profile.objects.filter(user=request.user)
        context = {
            "checkout_items": checkout_items,
            "shipping_cost": shipping_cost,
            "grand_total": grand_total,
            "profiles": profiles,
        }
        return render(request, 'checkout/checkout.html', context)

@method_decorator(never_cache, name='dispatch')
class CheckoutSuccessView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        # fetch address/profile
        address_id = request.POST.get('address-id')

        if not address_id:
            return redirect('checkout')

        # get profile
        profile = get_object_or_404(Profile, id=address_id, user=request.user)

        # cart items
        cart_items = Cart.objects.filter(user=request.user, paid=False)

        # save checkout orders
        for item in cart_items:
            Checkout.objects.create(
                user=request.user,
                profile=profile,
                product=item.product,
                quantity=item.quantity,
                status='Pending',
                is_ordered=True
            )

        # mark cart as paid
        cart_items.update(paid=True)

        # delete cart items
        cart_items.delete()

        return redirect('checkout-list')
 
@method_decorator(never_cache, name='dispatch')
class CheckoutListView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        checkout_confirm_items = Checkout.objects.filter(
            user=request.user,
            is_ordered=True
        ).order_by('-ordered_date').select_related('product', 'profile')

        return render(request, 'checkout/checkout_list.html', {
            'checkout_confirm_items': checkout_confirm_items
        })
