from django.contrib import admin
from django.urls import path
from .views import AuthViewSet, WarehouseViewSet, VendorViewSet, ProductViewSet, StockViewSet, StockTransferViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'stock-transfers', StockTransferViewSet, basename='stock-transfer')

urlpatterns = router.urls