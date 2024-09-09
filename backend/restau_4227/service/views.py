from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import Product, Category, SubCategory, Supplier, Order
from .serializers import SupplierSerializer, CategorySerializer, ProductSerializer, OrderSerializer, \
    SubCategorySerializer, OrderCreateSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        query_params = self.request.query_params.get('category')
        if query_params:
            queryset = SubCategory.objects.filter(category=query_params)
        else:
            queryset = SubCategory.objects.all()
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_params = self.request.query_params.get('sub_category')
        if query_params:
            queryset = Product.objects.filter(sub_category=query_params)
        else:
            queryset = Product.objects.all()
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        query_params = self.request.query_params.get('user_id')
        if query_params:
            queryset = Order.objects.filter(user=query_params)
        else:
            queryset = Order.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

