from django.contrib import admin
from .models import UserProfile, Vendor, Warehouse, Product, Stock, StockTransfer
# Register your models here.
admin.site.register({UserProfile, Vendor, Warehouse, Product, Stock, StockTransfer})