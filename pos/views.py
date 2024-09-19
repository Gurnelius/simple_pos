from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Sale, SaleItem
from django.shortcuts import get_object_or_404

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'pos/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_sellable=True)



