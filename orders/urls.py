from django.urls import path
from .views import CheckoutAPIView,OrderDetailAPIView,CancelOrderAPIView


urlpatterns = [
    path('', CheckoutAPIView.as_view(), name='checkout'), # Create an order from the user's cart
    path('<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),# View one order belonging to the logged-in user
    path('<int:order_id>/cancel/',CancelOrderAPIView.as_view(),name='cancel-order'),
]