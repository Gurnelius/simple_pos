from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from core.mixins import SearchMixin
from .models import Product
from django.shortcuts import get_object_or_404
    
class ProductListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    
    # Define search fields for this view
    search_fields = ['name', 'description']

    def get_queryset(self):
        return super().get_queryset().filter(is_sellable=True)

