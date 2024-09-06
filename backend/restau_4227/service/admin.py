from django.contrib import admin

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_category']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'total_price']


admin.site.register(Supplier)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
