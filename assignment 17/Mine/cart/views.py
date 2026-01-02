from django.views import generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from store.models import Product, ProductVariant
from cart.models import Coupon, Cart, Wishlist

# ==================================
# Add To Cart
# ==================================
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from store.models import Product, ProductVariant
from cart.models import Cart

# ==================================
# Add To Cart (Concurrency Safe)
@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        product_slug = request.POST.get("product_slug")
        product_id = request.POST.get("product_id")
        select_color = request.POST.get("color")   # optional
        select_size = request.POST.get("size")     # optional
        quantity = int(request.POST.get("quantity", 1))

        # Fetch product
        product = get_object_or_404(Product, slug=product_slug, id=product_id, status='active')

        variant = None
        with transaction.atomic():
            # Lock product row
            product.refresh_from_db(fields=["available_stock"])

            # Fetch variant if color or size is selected
            if select_color or select_size:
                variant_qs = ProductVariant.objects.select_for_update().filter(product=product)

                # Apply filters individually if selected
                if select_color:
                    variant_qs = variant_qs.filter(color_id=int(select_color))
                if select_size:
                    variant_qs = variant_qs.filter(size_id=int(select_size))

                # If no exact match, fallback logic:
                if not variant_qs.exists():
                    # If only color is selected
                    if select_color and not select_size:
                        variant_qs = ProductVariant.objects.filter(product=product, color_id=int(select_color))
                    # If only size is selected
                    elif select_size and not select_color:
                        variant_qs = ProductVariant.objects.filter(product=product, size_id=int(select_size))

                if not variant_qs.exists():
                    return JsonResponse({"status": "error", "message": "Selected variant does not exist."})

                variant = variant_qs[0]
                variant.refresh_from_db(fields=["available_stock"])

            # Determine max available stock
            max_stock = variant.available_stock if variant else product.available_stock
            if max_stock <= 0:
                message = "Selected variant is out of stock." if variant else "Product is out of stock."
                return JsonResponse({"status": "error", "message": message})

            # Handle cart
            cart_qs = Cart.objects.select_for_update().filter(user=request.user, product=product, variant=variant)
            if cart_qs.exists():
                cart_item = cart_qs[0]
                available_to_add = max_stock - cart_item.quantity
                if quantity > available_to_add:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Cannot add {quantity} more items. Only {available_to_add} left in stock."
                    })
                cart_item.quantity += quantity
                cart_item.save(update_fields=["quantity"])
            else:
                if quantity > max_stock:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Cannot add {quantity} items. Only {max_stock} left in stock."
                    })
                Cart.objects.create(user=request.user, product=product, variant=variant, quantity=quantity)

        return JsonResponse({
            "status": "success",
            "message": "Product added to cart successfully.",
            "product_title": product.title,
            "variant_id": variant.id if variant else None,
            "available_stock": max_stock
        })



# ================================
# Cart Detail Page
# ================================
@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        pass


# ================================
# Increase/Decrease Quantity
# ================================
@method_decorator(never_cache, name="dispatch")
class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        pass


# ================================
# Remove From Cart
# ================================
@method_decorator(never_cache, name='dispatch')
class CartRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        pass