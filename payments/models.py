from django.db import models
from orders.models import Order


class Payment(models.Model):
    # Payment methods available in our application
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
    ]

    # Payment status used to track the payment result
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    # Connect the payment to the order being paid for
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    # Store the amount paid for the order
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    # Store the method used to make the payment
    payment_method = models.CharField(max_length=10,choices=PAYMENT_METHOD_CHOICES)

    # Store the current payment status
    payment_status = models.CharField(max_length=10,choices=PAYMENT_STATUS_CHOICES,default='Pending')

    # Store the payment transaction reference
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    # Store when the payment record was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"