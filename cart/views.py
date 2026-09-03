from rest_framework.views import APIView
from rest_framework.response import Response
from.models import Cart,CartItem
from.serializers import CartItemSerializer,CartSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CartView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cart, _ =Cart.objects.get_or_create(user=request.user)
        serializer=CartSerializer(cart)
        return Response(serializer.data)
    
class AddToCartView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        cart,_ =Cart.objects.get_or_create(user=request.user)
        product_id=request.data.get('product')
        quantity=int(request.data.get('quantity',1))
        item,created=CartItem.objects.get_or_create(
            cart=cart,product_id=product_id,
            defaults={'quantity':quantity})

        if not created:
            item.quantity+=quantity
            item.save()
        return Response(
            CartSerializer(cart).data,
            status=201
        )

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,pk):
        item=CartItem.objects.get(pk=pk)
        item.quantity=request.data.get('quantity',item.quantity)
        item.save()
        return Response(CartItemSerializer(item).data)
    def delete(self,request,pk):
        item = CartItem.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

