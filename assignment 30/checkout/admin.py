from django.contrib import admin
from checkout.models import Checkout
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile', 'product', 'quantity', 'status', 'ordered_date')
admin.site.register(Checkout, CheckoutAdmin)