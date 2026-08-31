from django.contrib import admin
from.models import Order,OrderItem
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
#I registered the Order and OrderItem models so that 
# I can manage and test their data through Django's built-in admin panel.