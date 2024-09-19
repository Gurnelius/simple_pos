from django.db import models
from core import settings

class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stores', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='store_images/', blank=True, null=True) 

    def __str__(self):
        return self.name
