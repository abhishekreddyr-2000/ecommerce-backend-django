from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework. generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from.models import Product
from.serializers import ProductSerializers
from.pagination import ProductPagination
from.permissions import IsSellerOrReadOnly

class ProductListView(ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializers

    filter_backends=[filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    search_fields=['title','brand']    #search
    ordering_fields=['price','rating'] #sort
    filterset_fields=['brand','category','is_prime']   #filter
    pagination_class=ProductPagination #pages
    permission_classes=[IsSellerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset         = Product.objects.all()
    serializer_class = ProductSerializers

    permission_classes=[IsSellerOrReadOnly]

    