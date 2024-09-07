from django.contrib import admin
from .models import Supplier, Category, SubCategory, Product, Order

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    search_fields = ('name',)
    list_filter = ('supplier',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_category')
    search_fields = ('name',)
    list_filter = ('sub_category',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'created_at')
    search_fields = ('user__user__username', 'product__name')
    list_filter = ('created_at',)
    readonly_fields = ('total_price',)
