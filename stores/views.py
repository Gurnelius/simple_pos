from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .models import Store
from .forms import StoreForm

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



class StoreListView(ListView):
    model = Store
    template_name = 'stores/store_list.html'
    context_object_name = 'stores'
    paginate_by = 10  # Number of stores per page

    def get_queryset(self):
        """
        Optionally customize the query to filter or sort stores.
        """
        queryset = super().get_queryset()
        # Add custom filtering or sorting if needed
        return queryset
