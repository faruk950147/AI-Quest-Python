from django.db.models import Min, Max
from cart.models import (
    Cart,
)
def get_filters(request):
    cart_count = Cart.objects.filter(user=request.user, paid=False)
    return {
        'cart_count': len(cart_count),
    }