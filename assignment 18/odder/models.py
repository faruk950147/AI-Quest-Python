from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from store.models import Product, ProductVariant
from carts.models import Cart  # adjust import path if your Cart is in other app
from coupons.models import Coupon  # adjust if your Coupon is in same file as Cart
User = settings.AUTH_USER_MODEL if isinstance(settings.AUTH_USER_MODEL, str) else settings.AUTH_USER_MODEL

def decimal_round(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('cancelled', 'Cancelled'),
    ('shipped', 'Shipped'),
    ('completed', 'Completed'),
)

PAYMENT_METHOD_CHOICES = (
    ('cod', 'Cash On Delivery'),
    ('paypal', 'PayPal'),
    # add others: 'sslcommerz', 'stripe', etc.
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.invoice_id} ({self.user}) - {self.get_status_display()}"

    def clean(self):
        if self.coupon and not self.coupon.is_valid:
            raise ValidationError("Coupon is not valid or expired.")

    def recalc_totals(self):
        subtotal = Decimal('0.00')
        for item in self.items.all():
            subtotal += decimal_round(item.unit_price * item.quantity)
        self.subtotal = decimal_round(subtotal)

        discount = Decimal('0.00')
        if self.coupon and self.coupon.is_valid and self.subtotal >= self.coupon.min_purchase:
            if self.coupon.discount_type == 'percent':
                discount = decimal_round(self.subtotal * self.coupon.discount_value / Decimal('100'))
            else:
                discount = min(self.subtotal, self.coupon.discount_value)
        self.discount_amount = decimal_round(discount)
        self.total = decimal_round(self.subtotal - self.discount_amount)

    def mark_paid(self, payment_instance=None):
        """
        Mark order as paid: set status, paid_at, optionally link payment.
        Also deduct stocks if not yet deducted.
        """
        if self.status == 'paid':
            return
        with transaction.atomic():
            # reduce stock for each item
            for item in self.items.select_for_update():
                if item.variant:
                    if item.variant.available_stock < item.quantity:
                        raise ValidationError(f"Not enough stock for variant {item.variant}")
                    item.variant.available_stock -= item.quantity
                    item.variant.save()
                else:
                    if item.product.available_stock < item.quantity:
                        raise ValidationError(f"Not enough stock for product {item.product.title}")
                    item.product.available_stock -= item.quantity
                    item.product.save()

            self.status = 'paid'
            self.paid_at = timezone.now()
            self.save()
            if payment_instance:
                payment_instance.order = self
                payment_instance.save()
            # mark related carts as paid (optional)
            Cart.objects.filter(user=self.user, paid=False, product__in=self.items.values_list('product', flat=True)).update(paid=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name_plural = "Order Items"
        ordering = ['id']

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.unit_price = decimal_round(self.unit_price)
        self.subtotal = decimal_round(self.unit_price * Decimal(self.quantity))
        super().save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.payment_method} - {self.amount} - paid: {self.paid}"

    def mark_as_paid(self, txn_id=None):
        if self.paid:
            return
        self.paid = True
        if txn_id:
            self.transaction_id = txn_id
        self.save()
        if self.order:
            self.order.mark_paid(payment_instance=self)
