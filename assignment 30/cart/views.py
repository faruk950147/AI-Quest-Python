from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.db.models import F, Sum
from django.urls import reverse_lazy
from store.models import Product
from .models import Cart

@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        product_id = request.POST.get("product-id")
        quantity = request.POST.get("quantity", "0")

        if not product_id or not quantity.isdigit() or int(quantity) < 1:
            return JsonResponse({"status": "error", "message": "Invalid request."})

        quantity = int(quantity)
        product = get_object_or_404(Product, id=product_id)

        if quantity > product.available_stock:
            return JsonResponse({
                "status": "error",
                "message": f"Quantity cannot exceed available stock! Maximum: {product.available_stock}."
            })

        # Update or create cart item
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            paid=False,
            defaults={'quantity': quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.available_stock:
                return JsonResponse({
                    "status": "error",
                    "message": f"You can't add more than {product.available_stock} units!"
                })
            cart_item.quantity = F('quantity') + quantity
            cart_item.save()
            cart_item.refresh_from_db()

        # Aggregate cart
        cart_calculations = Cart.objects.filter(user=request.user, paid=False)
        cart_summary = cart_calculations.aggregate(
            total_items=Sum('quantity'),
            total_price=Sum(F('quantity') * F('product__sale_price'))
        )

        return JsonResponse({
            "status": "success",
            "message": "Product added to cart successfully!",
            "quantity": cart_item.quantity,
            "cart_count": cart_calculations.count(),
            "cart_total_price": round(float(cart_summary['total_price'] or 0), 2),
            "product_title": product.title,
            "product_image": product.image.url if product.image else "",
            "product_price": float(product.sale_price)
        })


@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False)
        cart_summary = cart_items.aggregate(
            total_price=Sum(F('quantity') * F('product__sale_price'))
        )
        cart_total = float(cart_summary['total_price'] or 0)
        shipping_cost = 50

        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "shipping_cost": shipping_cost,
        }
        return render(request, 'cart/cart-detail.html', context)

class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def post(self, request):
        cart_item_id = request.POST.get("product-id")
        action = request.POST.get("action")

        if cart_item_id and action:
            try:
                cart_item = Cart.objects.get(id=cart_item_id, user=request.user, paid=False)
                if action == "inc":
                    cart_item.quantity += 1
                    cart_item.save()
                elif action == "dec" and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()

            except Cart.DoesNotExist:
                pass  # item not found, quietly ignore

        # quantity updated cart page redirect
        return redirect('cart-detail')