from django import forms
from .models import PAYMENT_METHOD_CHOICES
from store.models import Product, ProductVariant
from cart.models import Coupon

class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    coupon_code = forms.CharField(max_length=50, required=False)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=20, required=True)
