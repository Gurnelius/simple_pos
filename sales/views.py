from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Sale, SaleItem
from products.models import Product
from .forms import RefundForm

class CreateSaleView(LoginRequiredMixin, FormView):
    template_name = 'pos/create_sale.html'
    success_url = reverse_lazy('product_list')

    def post(self, request, *args, **kwargs):
        product_id = request.POST['product_id']
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST['quantity'])

        # Create sale and deduct stock
        sale = Sale.objects.create(total_amount=product.price * quantity)
        SaleItem.objects.create(sale=sale, product=product, quantity=quantity, unit_price=product.price)

        product.stock -= quantity
        product.save()
        return super().form_valid(request)
    
# View for listing all sales
class SaleListView(ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    ordering = ['-date']  # Order by date descending

# View for viewing detailed sale information
class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'

# View for processing refunds
class RefundView(FormView):
    template_name = 'sales/refund_form.html'
    form_class = RefundForm
    success_url = reverse_lazy('sale_list')

    def form_valid(self, form):
        sale_id = form.cleaned_data['sale_id']
        refund_amount = form.cleaned_data['refund_amount']
        sale = get_object_or_404(Sale, id=sale_id)
        
        # Process the refund (custom logic needed here)
        sale.refund(refund_amount)
        sale.save()
        
        messages.success(self.request, 'Refund processed successfully.')
        return super().form_valid(form)

# Example view for sales reports (if needed)
class SalesReportView(ListView):
    model = Sale
    template_name = 'sales/sales_report.html'
    context_object_name = 'sales'

    def get_queryset(self):
        # Implement your logic for filtering/sorting sales reports
        return Sale.objects.all()
