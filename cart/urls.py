from django.urls import path
from.views import CartView,AddToCartView,CartItemDetailView

urlpatterns=[
    path('cart/',CartView.as_view(),name='products_list'),               #GET
    path('add/',AddToCartView.as_view(),name='add_product'),             #POST
    path('items/<int:pk>/',CartItemDetailView.as_view(),name='item_detail'), #PATCH/DELETE 
]