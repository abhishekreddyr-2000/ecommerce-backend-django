from django.db import models
from django.conf import settings
class Cart(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_items(self):
        return sum(i.quantity for i in self.items.all())

    @property
    def total_price(self):
        return sum(i.subtotal for i in self.items.all())


    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart=models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product=models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    quantity=models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity
    

    def __str__(self):
        return f"{self.quantity} X {self.product.title}"


        

