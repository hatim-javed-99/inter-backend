from rest_framework import serializers

from .models import Product, Category, SubCategory, Supplier, Order, OrderItem


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    supplier_detail = SupplierSerializer(source="supplier", read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    sub_category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_detail = SubCategorySerializer(source="sub_category", read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'total_price', 'product_detail']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'items', 'total_price']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items', 'user']

    def create(self, validated_data):
        # Extract items data
        items_data = validated_data.pop('items')

        # Create the Order instance
        order = Order.objects.create(**validated_data)

        # Create OrderItem instances and link them to the order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
