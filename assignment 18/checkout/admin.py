from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'variant', 'unit_price', 'quantity', 'subtotal')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'user', 'status', 'total', 'created_at', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('invoice_id', 'user__username', 'user__email')
    inlines = [OrderItemInline]
    readonly_fields = ('subtotal', 'discount_amount', 'total', 'created_at', 'paid_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'amount', 'paid', 'created_at')
    list_filter = ('payment_method', 'paid')
    search_fields = ('transaction_id', 'order__invoice_id')
