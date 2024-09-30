from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'complete', 'get_cart_items', 'get_cart_total', 'shipping')
    list_display_links = ('id', 'user')
    list_filter = ('complete', 'created_at')
    list_editable = ('complete',)
    search_fields = ('id','complete')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
