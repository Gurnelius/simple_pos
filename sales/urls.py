from django.urls import path
from .views import (
    CartView,
    CheckoutView,
    MpesaCallbackView,

    CartView,
    CheckoutView,
    StoreView,
    UpdateItemView,
    ProcessOrderView,

    SaleListView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),

    # Mpesa
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('mpesa/callback/', MpesaCallbackView.as_view(), name='mpesa_callback'),

    # Process order view
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('store/', StoreView.as_view(), name='store'),
    path('update_item/', UpdateItemView.as_view(), name='update_item'),
    path('process_order/', ProcessOrderView.as_view(), name='process_order'),

    # Sales
    path('sales/', SaleListView.as_view(), name='sales_list'),

]

