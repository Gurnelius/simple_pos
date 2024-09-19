from django.contrib import admin
from .models import Store

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_number', 'email')
    search_fields = ('name', 'location')

admin.site.register(Store, StoreAdmin)
