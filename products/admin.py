from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_sellable')  # Ensure these fields exist
    search_fields = ('name', 'description')
    list_filter = ('is_sellable',)  # Ensure this field exists