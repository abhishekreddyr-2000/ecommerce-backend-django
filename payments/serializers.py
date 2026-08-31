from rest_framework import serializers
from .models import Payment


# Converts Payment model data into JSON
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id','order','amount','payment_method','payment_status','transaction_id','created_at']

        # These values are controlled by the backend
        read_only_fields = ['amount','payment_status','transaction_id','created_at']

# Validates the payment status update request
class PaymentStatusSerializer(serializers.Serializer):

    # Status sent for the payment
    payment_status = serializers.ChoiceField(
        choices=['Success', 'Failed']
    )

            
           
            
            
        