from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart, CartItem
from decimal import Decimal


class CheckoutAPIView(APIView):
    # Only logged-in users can access checkout and their orders
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get only the logged-in user's orders
        orders = Order.objects.filter(
            user=request.user
        ).order_by('-created_at')

        # Convert orders into JSON
        serializer = OrderSerializer(orders,many=True)

        # Return the user's orders
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        # Validate the selected cart items
        checkout_serializer = CheckoutSerializer(data=request.data)

        # Stop if the request data is invalid
        checkout_serializer.is_valid(raise_exception=True)

        # Get the selected items from validated data
        selected_items = checkout_serializer.validated_data['items']

        # Get the logged-in user's cart
        cart = Cart.objects.filter(user=request.user).first()

        # Check whether the cart exists
        if not cart:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Store cart items that will become OrderItems
        order_items_data = []

        # Start the total amount
        total_amount = Decimal('0.00')

        # Validate every selected cart item
        for selected_item in selected_items:

            # Get cart item ID and requested quantity
            cart_item_id = selected_item['cart_item_id']
            requested_quantity = selected_item['quantity']

            # Find the cart item inside this user's cart
            cart_item = CartItem.objects.filter(id=cart_item_id,cart=cart).first()

            # Check whether the cart item exists
            if not cart_item:
                return Response(
                    {
                        "detail": (
                            f"Cart item {cart_item_id} not found."
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check whether enough quantity is available
            if requested_quantity > cart_item.quantity:
                return Response(
                    {
                        "detail": (
                            f"Only {cart_item.quantity} "
                            f"quantity available for "
                            f"{cart_item.product.title}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the current product price from the database
            price = cart_item.product.price

            # Calculate this cart item's subtotal
            subtotal = price * requested_quantity

            # Add subtotal to the total order amount
            total_amount += subtotal

            # Store data needed to create the OrderItem
            order_items_data.append({
                'cart_item': cart_item,
                'quantity': requested_quantity,
                'price': price
            })

        # Create Order, OrderItems and update Cart
        # as one database transaction
        with transaction.atomic():

            # Create the order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount
            )

            # Create OrderItems from selected cart items
            for item in order_items_data:

                OrderItem.objects.create(
                    order=order,
                    product=item['cart_item'].product,
                    quantity=item['quantity'],
                    price=item['price']
                )

                # Remove the CartItem if the full quantity was ordered
                if item['quantity'] == item['cart_item'].quantity:
                    item['cart_item'].delete()

                # Otherwise, reduce the remaining cart quantity
                else:
                    item['cart_item'].quantity -= item['quantity']
                    item['cart_item'].save()

        # Convert the created order into JSON
        serializer = OrderSerializer(order)

        # Return the created order
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    # Only logged-in users can view an order
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        # Find the order only if it belongs to this user
        order = Order.objects.filter(
            id=order_id,
            user=request.user
        ).first()

        # Return 404 if the order doesn't belong to the user
        if not order:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Convert the order into JSON
        serializer = OrderSerializer(order)

        # Return the order details
        return Response(serializer.data,status=status.HTTP_200_OK)


class CancelOrderAPIView(APIView):
    # Only logged-in users can cancel an order
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        # Find the order belonging to the logged-in user
        order = Order.objects.filter(
            id=order_id,
            user=request.user
        ).first()

        # Return 404 if the order doesn't exist
        if not order:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only Pending and Confirmed orders can be cancelled
        if order.status not in ['Pending', 'Confirmed']:
            return Response(
                {
                    "detail": (
                        f"Order cannot be cancelled because "
                        f"its status is {order.status}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Change the order status
        order.status = 'Cancelled'

        # Save the updated order
        order.save()

        # Convert the updated order into JSON
        serializer = OrderSerializer(order)

        # Return the cancelled order
        return Response(serializer.data,status=status.HTTP_200_OK)