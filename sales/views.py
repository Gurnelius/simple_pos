from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Sale, SaleItem
from products.models import Product
from .forms import CreateSaleForm, RefundForm

class CreateSaleView(LoginRequiredMixin, FormView):
    template_name = 'sales/create_sale.html'
    form_class = CreateSaleForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        product_id = form.cleaned_data['product_id']
        quantity = form.cleaned_data['quantity']
        
        # Get the product
        product = get_object_or_404(Product, id=product_id)
        
        # Create the sale using the model method
        sale = Sale()
        sale.cashier = self.request.user  # Set the cashier
        sale.create_sale(product, quantity)  # Call the method to create the sale

        return super().form_valid(form)

    
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

from django.shortcuts import render, redirect
from django.views import View
from .models import Product

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST['product_id']
        quantity = int(request.POST['quantity'])
        product = get_object_or_404(Product, id=product_id)

        # Initialize the cart in session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}

        # Update cart
        cart = request.session['cart']
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        return redirect('product_list')  # Redirect to the product list

class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        products = []
        total_price = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total_price += product.price * quantity

        return render(request, 'sales/cart.html', {
            'products': products,
            'total_price': total_price
        })

