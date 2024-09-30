from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from products.models import Product


from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from core.mpesa.mpesa_api import Mpesa

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .utils import cartData



class MpesaCallbackView(View):
    def post(self, request):
        # Handle the callback from the Mpesa class
        mpesa = Mpesa()
        callback_data = mpesa.handle_callback(request)
        # Update order status or payment confirmation based on the callback
        return JsonResponse({"status": "callback received"})
    
class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['items'] = data['items']
        context['order'] = data['order']
        context['cartItems'] = data['cartItems']
        return context

class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['items'] = data['items']
        context['order'] = data['order']
        context['cartItems'] = data['cartItems']
        return context


class StoreView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['products'] = Product.objects.all()
        context['cartItems'] = data['cartItems']
        return context

from django.views import View
from django.http import JsonResponse
import json
from .models import Product, Order, OrderItem

class UpdateItemView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)

from django.views import View
from django.http import JsonResponse
import datetime
import json
from .models import Order, ShippingAddress
from .utils import guestOrder

class ProcessOrderView(View):
    def post(self, request, *args, **kwargs):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            customer, order = guestOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        return JsonResponse('Payment complete!', safe=False)


from django.views.generic import ListView
from .models import Order

class SaleListView(ListView):
    model = Order
    template_name = 'sales/sale_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        # Filter only orders where complete is True
        return Order.objects.filter(complete=True).order_by('-created_at')
