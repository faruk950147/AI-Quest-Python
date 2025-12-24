from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum, F
import logging

from cart.models import Cart
from store.models import Product, ProductVariant

logger = logging.getLogger('project')

# ==================================
# Add To Cart
# ==================================
@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        product_slug = request.POST.get("product_slug")
        product_id = request.POST.get("product_id")
        select_color = request.POST.get("color")       # optional
        select_size = request.POST.get("size")         # optional
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            return JsonResponse({"status": "error", "message": "Quantity must be at least 1."})

        # Fetch product
        product = get_object_or_404(Product, slug=product_slug, id=product_id, status='active')
        product.refresh_from_db(fields=["available_stock"])

        # Convert variant selection to int (if exists)
        if select_color:
            select_color = int(select_color)
        if select_size:
            select_size = int(select_size)

        # Handle variant
        variant = None
        if select_color or select_size:
            filters = {}
            if select_color:
                filters["color_id"] = select_color
            if select_size:
                filters["size_id"] = select_size
            variant = ProductVariant.objects.filter(product=product, **filters).first()
            if not variant:
                return JsonResponse({"status": "error", "message": "Selected variant does not exist."})
            variant.refresh_from_db(fields=["available_stock"])

        # Determine available stock
        max_stock = variant.available_stock if variant else product.available_stock
        if max_stock <= 0:
            message = "Selected variant is out of stock." if variant else "Product is out of stock."
            return JsonResponse({"status": "error", "message": message})

        # Add/update cart in transaction
        with transaction.atomic():
            cart_item_qs = Cart.objects.filter(user=request.user, product=product, variant=variant)
            if cart_item_qs.exists():
                cart_item = cart_item_qs.select_for_update()[0]  # fix: parentheses added
                new_quantity = cart_item.quantity + quantity
                if new_quantity > max_stock:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Cannot add {quantity} more items. Only {max_stock - cart_item.quantity} left in stock."
                    })
                cart_item.quantity = new_quantity
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