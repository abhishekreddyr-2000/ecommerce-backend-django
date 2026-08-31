from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer, PaymentStatusSerializer
from django.db import transaction



class PaymentAPIView(APIView):
    # Only logged-in users can create a payment
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate the payment request
        serializer = PaymentSerializer(data=request.data)

        # Stop if the request data is invalid
        serializer.is_valid(raise_exception=True)

        # Get the Order object from validated data
        order = serializer.validated_data['order']

        # Check whether the order belongs to the logged-in user
        if order.user != request.user:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # A cancelled order cannot be paid
        if order.status == 'Cancelled':
            return Response(
                {"detail": "Cancelled orders cannot be paid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check whether this order already has a payment
        if Payment.objects.filter(order=order).exists():
            return Response(
                {"detail": "Payment already exists for this order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the payment method selected by the user
        payment_method = serializer.validated_data['payment_method']

        # Create payment and update order safely in one transaction
        with transaction.atomic():

            # Create the payment using the order amount
            payment = Payment.objects.create(
                order=order,
                amount=order.total_amount,
                payment_method=payment_method
            )

            # COD does not require online payment confirmation
            if payment_method == 'COD':
                order.status = 'Confirmed'
                order.save()

        # Convert the payment into JSON
        response_serializer = PaymentSerializer(payment)

        # Return the created payment
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

class PaymentStatusAPIView(APIView):
    # Only logged-in users can update payment status
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        # Validate the payment status request
        serializer = PaymentStatusSerializer(data=request.data)

        # Stop if the request data is invalid
        serializer.is_valid(raise_exception=True)

        # Find the payment belonging to the logged-in user
        payment = Payment.objects.filter(
            id=payment_id,
            order__user=request.user
        ).first()

        # Check whether the payment exists
        if not payment:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # A cancelled order cannot be paid
        if payment.order.status == 'Cancelled':
            return Response(
                {"detail": "Cancelled orders cannot be paid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A payment can only be updated while it is Pending
        if payment.payment_status != 'Pending':
            return Response(
                {"detail": "Payment has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the requested payment status
        new_status = serializer.validated_data['payment_status']

        # Update payment and order together
        with transaction.atomic():

            # Update the payment status
            payment.payment_status = new_status
            payment.save()

            # Confirm the order when the payment succeeds
            if new_status == 'Success' and payment.order.status == 'Pending':
                payment.order.status = 'Confirmed'
                payment.order.save()

        # Convert the updated payment into JSON
        response_serializer = PaymentSerializer(payment)

        # Return the updated payment
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )      

class PaymentDetailAPIView(APIView):
    # Only logged-in users can view payment details
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        # Find the payment belonging to the logged-in user
        payment = Payment.objects.filter(
            id=payment_id,
            order__user=request.user
        ).first()

        # Return 404 if the payment does not exist
        if not payment:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Convert the payment into JSON
        serializer = PaymentSerializer(payment)

        # Return payment details
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )    