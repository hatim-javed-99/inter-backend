from django.contrib import admin
from django.utils.html import mark_safe

from .models import Supplier, Category, SubCategory, Product, Order, OrderItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier')
    search_fields = ('name',)
    list_filter = ('supplier',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'sub_category', 'image', 'status')
    search_fields = ('name',)
    list_filter = ('sub_category',)

    def image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'No Image'

    image.short_description = 'Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at',)
    list_filter = ('created_at', 'user__user__username')
    readonly_fields = ('total_price',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'total_price']
    list_filter = ['order__id', 'product']
