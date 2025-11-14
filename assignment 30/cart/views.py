from django.shortcuts import get_object_or_404, render
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

        if product.available_stock < 1:
            return JsonResponse({"status": "error", "message": "Out of stock!"})

        if quantity > product.available_stock:
            return JsonResponse({
                "status": "error",
                "message": f"Max available stock: {product.available_stock}"
            })

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            paid=False,
            defaults={"quantity": quantity}
        )

        if not created:
            if cart_item.quantity + quantity > product.available_stock:
                return JsonResponse({
                    "status": "error",
                    "message": f"You can't add more than {product.available_stock} units!"
                })

            cart_item.quantity = F("quantity") + quantity
            cart_item.save()
            cart_item.refresh_from_db()

        cart_items = Cart.objects.filter(user=request.user, paid=False)
        summary = cart_items.aggregate(
            total_items=Sum("quantity"),
            total_price=Sum(F("quantity") * F("product__sale_price"))
        )

        return JsonResponse({
            "status": "success",
            "message": "Product added to cart!",
            "quantity": cart_item.quantity,
            "cart_count": summary["total_items"] or 0,
            "cart_total_price": float(summary["total_price"] or 0),
            "product_title": product.title,
            "product_image": product.image.url if product.image else "",
            "product_price": float(product.sale_price),
        })


@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False)

        summary = cart_items.aggregate(
            total_price=Sum(F("quantity") * F("product__sale_price"))
        )

        cart_total = float(summary["total_price"] or 0)
        shipping_cost = 50
        grand_total = cart_total + shipping_cost

        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "shipping_cost": shipping_cost,
            "grand_total": grand_total,
        }
        return render(request, 'cart/cart-detail.html', context)


@method_decorator(never_cache, name="dispatch")
class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        cart_id = request.POST.get("cart-id")
        action = request.POST.get("action")

        cart_item = get_object_or_404(Ccart, id=cart_id, user=request.user, paid=False)
        product = cart_item.product

        if action == "inc":
            if cart_item.quantity < product.available_stock:
                cart_item.quantity = F("quantity") + 1
                cart_item.save()
                cart_item.refresh_from_db()

        elif action == "dec":
            if cart_item.quantity > 1:
                cart_item.quantity = F("quantity") - 1
                cart_item.save()
                cart_item.refresh_from_db()

        cart_items = Cart.objects.filter(user=request.user, paid=False)
        summary = cart_items.aggregate(
            total_items=Sum("quantity"),
            total_price=Sum(F("quantity") * F("product__sale_price"))
        )

        cart_total = float(summary["total_price"] or 0)
        shipping_cost = 50
        grand_total = cart_total + shipping_cost

        return JsonResponse({
            "status": "success",
            "quantity": cart_item.quantity,
            "cart_total": round(cart_total, 2),
            "grand_total": round(grand_total, 2),
            "cart_count": summary["total_items"] or 0,
        })


@method_decorator(never_cache, name="dispatch")
class CartRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        cart_id = request.POST.get("cart-id")
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user, paid=False)
        cart_item.delete()

        cart_items = Cart.objects.filter(user=request.user, paid=False)
        summary = cart_items.aggregate(
            total_items=Sum("quantity"),
            total_price=Sum(F("quantity") * F("product__sale_price"))
        )

        return JsonResponse({
            "status": "success",
            "message": "Item removed!",
            "cart_count": summary["total_items"] or 0,
            "cart_total_price": float(summary["total_price"] or 0)
        })
