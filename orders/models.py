from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    #This connects an order with the user who placed it
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()
    #I store the product price in OrderItem because product prices can change later.
    #The order should preserve the price that the customer actually paid.
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"