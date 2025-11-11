from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01. Carts'
        unique_together = ('user', 'product')

    @property
    def subtotal(self):
        return self.product.sale_price * self.quantity

    def __str__(self):
        return f'{self.user.username} - {self.product.title} ({self.quantity})'
