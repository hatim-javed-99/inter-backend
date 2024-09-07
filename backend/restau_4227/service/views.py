from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import Product, Category, SubCategory, Supplier, Order
from .serializers import SupplierSerializer, CategorySerializer, ProductSerializer, OrderSerializer, \
    SubCategorySerializer


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
            queryset = SubCategory.objects.filter(sub_category=query_params)
        else:
            queryset = SubCategory.objects.all()
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_params = self.request.query_params.get('sub_category')
        if query_params:
            queryset = Product.objects.filter(category=query_params)
        else:
            queryset = Product.objects.all()
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        orders_data = request.data
        if isinstance(orders_data, list):
            created_orders = []
            for order_data in orders_data:
                serializer = self.get_serializer(data=order_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                created_orders.append(serializer.data)
            return Response(created_orders, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "Request data must be a list of orders."},
                status=status.HTTP_400_BAD_REQUEST
            )

