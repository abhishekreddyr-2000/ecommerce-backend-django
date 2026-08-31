from rest_framework import serializers
from .models import Order, OrderItem


# Converts OrderItem model data into JSON
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


# Converts Order model data into JSON
class OrderSerializer(serializers.ModelSerializer):
    # Include the order items inside the order response
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user','total_amount','status','created_at','items']
        # User is automatically taken from the logged-in user along with total_amount.These values are controlled by the backend
        read_only_fields = ['user', 'total_amount','status', 'items']



# Validates one item selected for checkout
class CheckoutItemSerializer(serializers.Serializer):

    # ID of the item from the user's cart
    cart_item_id = serializers.IntegerField()

    # Quantity the user wants to order
    quantity = serializers.IntegerField(min_value=1)



# Validates the complete checkout request
class CheckoutSerializer(serializers.Serializer):

    # List of cart items selected by the user
    items = CheckoutItemSerializer(many=True)

    def validate_items(self, value):
        # Make sure at least one item is selected
        if not value:
            raise serializers.ValidationError(
                "At least one item is required for checkout."
            )

        # Get all cart item IDs from the request
        cart_item_ids = [item['cart_item_id'] for item in value]

        # Check whether the same cart item was sent more than once
        if len(cart_item_ids) != len(set(cart_item_ids)):
            raise serializers.ValidationError(
                "The same cart item cannot be selected more than once."
            )

        # Return the validated items
        return value