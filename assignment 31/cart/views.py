from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.db.models import F, Sum
from django.db import transaction
from django.urls import reverse_lazy
from store.models import Product
from cart.models import Cart



# Add To Cart
@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def post(self, request):
        product_id = request.POST.get("product-id")
        quantity = int(request.POST.get("quantity", 1))

        # Quantity validation
        if quantity < 1:
            return JsonResponse({"status": "error", "message": "Quantity must be at least 1."})

        # Load product & refresh stock
        product = get_object_or_404(Product, id=product_id)
        product.refresh_from_db(fields=["available_stock"])

        # Stock check
        if quantity > product.available_stock:
            return JsonResponse({"status": "error", "message": f"Only {product.available_stock} units available."})

        # Atomic block
        with transaction.atomic():
            # Existing cart check
            cart_items = Cart.objects.filter(user=request.user, product=product, paid=False)
            if cart_items.exists():
                cart_item = cart_items[0]
                new_quantity = cart_item.quantity + quantity

                # Stock validation again
                if new_quantity > product.available_stock:
                    return JsonResponse({ "status": "error", "message": f"Cannot exceed available stock ({product.available_stock})."})
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                cart_item = Cart.objects.create(user=request.user, product=product, quantity=quantity, paid=False)

        # Cart summary
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
        cart_count = cart_items.count()
        summary = cart_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))

        return JsonResponse({
            "status": "success",
            "message": "Product added to cart successfully.",
            "quantity": cart_item.quantity,
            "cart_count": cart_count,
            "cart_total_price": summary["total_price"] or 0,
            "product_title": product.title,
            "product_image": product.image.url if product.image else "",
            "product_price": product.sale_price,
        })

# Cart Detail Page
@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
        summary = cart_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))

        cart_total = float(summary["total_price"] or 0)
        shipping_cost = 50
        grand_total = cart_total + shipping_cost

        return render(request, 'cart/cart-detail.html', {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "shipping_cost": shipping_cost,
            "grand_total": grand_total,
        })

# Increase/Decrease Quantity
@method_decorator(never_cache, name="dispatch")
class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        cart_id = request.POST.get("cart-id")
        action = request.POST.get("action")

        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user, paid=False)
        cart_item.product.refresh_from_db(fields=["available_stock"])

        # Use atomic transaction
        with transaction.atomic():
            # Increase
            if action == "inc" and cart_item.quantity < cart_item.product.available_stock:
                cart_item.quantity = F("quantity") + 1
                cart_item.save()
                cart_item.refresh_from_db()

            # Decrease
            elif action == "dec" and cart_item.quantity > 1:
                cart_item.quantity = F("quantity") - 1
                cart_item.save()
                cart_item.refresh_from_db()

        # Item subtotal
        item_subtotal = cart_item.quantity * cart_item.product.sale_price

        # Cart summary
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
        summary = cart_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))
        cart_total = summary["total_price"] or 0
        shipping_cost = 50
        grand_total = cart_total + shipping_cost

        return JsonResponse({
            "status": "success",
            "quantity": cart_item.quantity,
            "item_subtotal": float(round(item_subtotal, 2)),
            "cart_total": float(round(cart_total, 2)),
            "grand_total": float(round(grand_total, 2)),
        })

# Remove From Cart
@method_decorator(never_cache, name='dispatch')
class CartRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        cart_id = request.POST.get("cart-id")

        with transaction.atomic():
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user, paid=False)
            cart_item.delete()

            cart_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
            summary = cart_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))
            cart_total = summary["total_price"] or 0
            shipping_cost = 50
            grand_total = cart_total + shipping_cost
            cart_count = cart_items.count()

        return JsonResponse({
            "status": "success",
            "message": "Product removed from cart.",
            "cart_count": cart_count,
            "cart_total": float(round(cart_total, 2)),
            "grand_total": float(round(grand_total, 2)),
        })
