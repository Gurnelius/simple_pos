from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from core.mixins import SearchMixin
from .models import Store
from .forms import StoreForm
from django.contrib.auth.mixins import LoginRequiredMixin

class StoreCreateView(CreateView):
    model = Store
    form_class = StoreForm
    template_name = 'stores/store_form.html'
    success_url = '/stores/'

class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreForm
    template_name = 'stores/store_form.html'
    success_url = '/stores/'


class StoreListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Store
    template_name = 'stores/store_list.html'
    context_object_name = 'stores'
    search_fields = ['name', 'location', 'contact_number', 'email', 'address']  # Fields to search

    def get_queryset(self):
        queryset = super().get_queryset()  # Call the mixin's get_queryset
        print("Query set: ",queryset)
        return queryset  # This will include search functionality




