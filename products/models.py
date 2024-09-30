from django.db import models
from django.contrib.auth.models import User
from stores.models import Store
from core import settings

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sellable = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    digital = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return self.name
    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return 'product_default.jpg'