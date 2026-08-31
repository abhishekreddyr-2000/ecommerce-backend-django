from django.urls import path
from .views import PaymentAPIView,PaymentDetailAPIView,PaymentStatusAPIView

urlpatterns = [
    path('', PaymentAPIView.as_view(), name='create-payment'),  # Create a payment for an order
    path('<int:payment_id>/status/',PaymentStatusAPIView.as_view(),name='payment-status'),
    path('<int:payment_id>/',PaymentDetailAPIView.as_view(),name='payment-detail'),

]
