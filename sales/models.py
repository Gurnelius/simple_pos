from django.db import models
from core import settings
from products.models import Product
from django.conf import settings
from django.shortcuts import get_object_or_404

class Sale(models.Model):
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Sale {self.id} by {self.cashier.username}'

    def create_sale(self, product, quantity):
        """Creates a sale and updates stock."""
        # Calculate total price
        total_price = product.price * quantity
        
        # Create the sale instance
        sale = Sale.objects.create(cashier=self.cashier, total_price=total_price)
        
        # Create sale item
        SaleItem.objects.create(sale=sale, product=product, quantity=quantity, unit_price=product.price)
        
        # Update product stock
        product.stock -= quantity
        product.save()
        
        return sale

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.quantity} x {self.product.name} for Sale {self.sale.id}'
