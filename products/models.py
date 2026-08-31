from django.conf import settings
from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imageUrl = models.URLField(default="https://image-link.com/product.jpg")
    rating = models.IntegerField(default=0)
    category=models.CharField(max_length=100,null=True,blank=True)
    is_prime=models.BooleanField(default=False)
    seller=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return self.title
