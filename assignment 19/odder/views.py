from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Order, OrderItem, Payment, decimal_round
from carts.models import Cart
from coupons.models import Coupon
from .forms import CheckoutForm
import uuid
from decimal import Decimal

def gen_invoice():
    return uuid.uuid4().hex.upper()

class CheckoutView(View):
    def get(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user, paid=False)
        subtotal = Decimal('0.00')
        for c in carts:
            subtotal += decimal_round(Decimal(c.unit_price) * c.quantity)
        form = CheckoutForm()
        return render(request, 'orders/checkout.html', {
            'carts': carts, 'subtotal': subtotal, 'form': form
        })

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('account_login')  # change as per your auth url

        form = CheckoutForm(request.POST)
        if not form.is_valid():
            return render(request, 'orders/checkout.html', {'form': form, 'errors': form.errors})

        payment_method = form.cleaned_data['payment_method']
        coupon_code = form.cleaned_data.get('coupon_code') or None

        carts = Cart.objects.filter(user=user, paid=False).select_related('product', 'variant')
        if not carts.exists():
            return HttpResponseBadRequest("No items in cart.")

        with transaction.atomic():
            invoice = gen_invoice()
            order = Order.objects.create(user=user, invoice_id=invoice, payment_method=payment_method)

            # apply coupon if provided
            coupon = None
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code__iexact=coupon_code)
                    if not coupon.is_valid:
                        coupon = None
                except Coupon.DoesNotExist:
                    coupon = None
            order.coupon = coupon
            order.save()

            # create order items
            for cart in carts:
                unit_price = cart.unit_price
                OrderItem.objects.create(
                    order=order,
                    product=cart.product,
                    variant=cart.variant,
                    unit_price=unit_price,
                    quantity=cart.quantity
                )

            # recalc totals
            order.recalc_totals()
            order.save()

            # create payment record (not yet paid for non-COD)
            payment = Payment.objects.create(
                order=order,
                payment_method=payment_method,
                amount=order.total,
                paid=(payment_method == 'cod')  # mark paid immediately for COD
            )

            # If COD -> mark order as paid and deduct stock immediately
            if payment_method == 'cod':
                payment.mark_as_paid(txn_id=f'COD-{invoice}')
                # order.mark_paid will be invoked by payment.mark_as_paid -> which calls order.mark_paid

            # finally return success page
            return redirect('orders:success', invoice_id=order.invoice_id)

def apply_coupon_ajax(request):
    user = request.user
    code = request.GET.get('code', '').strip()
    if not code:
        return JsonResponse({'ok': False, 'error': 'No code provided'})

    try:
        coupon = Coupon.objects.get(code__iexact=code)
    except Coupon.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Coupon not found'})

    if not coupon.is_valid:
        return JsonResponse({'ok': False, 'error': 'Coupon invalid/expired'})

    # calculate subtotal
    carts = Cart.objects.filter(user=user, paid=False)
    subtotal = Decimal('0.00')
    for c in carts:
        subtotal += Decimal(c.unit_price) * c.quantity

    if subtotal < coupon.min_purchase:
        return JsonResponse({'ok': False, 'error': f'Minimum purchase {coupon.min_purchase} required'})

    if coupon.discount_type == 'percent':
        discount = (subtotal * coupon.discount_value) / Decimal('100')
    else:
        discount = min(subtotal, coupon.discount_value)

    return JsonResponse({
        'ok': True,
        'discount': str(decimal_round(discount)),
        'new_total': str(decimal_round(subtotal - discount))
    })

def success_view(request, invoice_id):
    order = get_object_or_404(Order, invoice_id=invoice_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})
