from rest_framework import serializers
from.models import Cart,CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_title=serializers.CharField(source='product.title',read_only=True)
    product_price=serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2,read_only=True)

    subtotal=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    class Meta:
        model=CartItem
        fields=['id','product','product_title','product_price','quantity','subtotal']

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)

    total_items=serializers.IntegerField(read_only=True)
    total_price=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    class Meta:
        model=Cart
        fields=['id','user','created_at','items','total_items','total_price']        