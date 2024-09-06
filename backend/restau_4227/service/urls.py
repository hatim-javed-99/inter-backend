from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, SupplierViewSet, CategoryViewSet, SubCategoryViewSet, OrderViewSet

router = DefaultRouter()

router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
 path('', include(router.urls)),
]