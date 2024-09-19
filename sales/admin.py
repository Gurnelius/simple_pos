from django.contrib import admin
from .models import Sale, SaleItem

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'created_at', 'cashier')  # Ensure these fields exist
    search_fields = ('id', 'cashier__username')
    list_filter = ('created_at',)  # Ensure this field exists

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price')  # Ensure these fields exist
    search_fields = ('product__name', 'sale__id')
