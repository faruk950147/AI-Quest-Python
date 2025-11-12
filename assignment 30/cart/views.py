from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from accounts.mixing import LoginRequiredMixin
from store.models import Product
# Create your views here.
@method_decorator(never_cache, name='dispatch')
class AddToCartView(generic.View):
    def post(self, request):
        product_id = request.POST.get("product-id")
        quantity = int(request.POST.get("quantity"))

        if not product_id or not quantity:
            messages.error(request, "Invalid request.")
            return redirect('home')  

        product = get_object_or_404(Product, id=product_id)
        
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1!")
            return redirect('single-product', slug=product.slug, id=product.id)

        if quantity > product.available_stock:
            messages.error(
                request,
                f"Quantity cannot exceed available stock! Maximum available: {product.available_stock}."
            )
            return redirect('single-product', slug=product.slug, id=product.id)

        # add to cart logic
        messages.success(request, "Product added to cart successfully!")
        return redirect('single-product', slug=product.slug, id=product.id)

        
@method_decorator(never_cache, name='dispatch')
class CartDetailView(generic.View):
    def get(self, request):
        # Logic to display cart details
        return render(request, 'cart/cart-detail.html')
