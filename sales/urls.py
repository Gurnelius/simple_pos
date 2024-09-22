from django.urls import path
from .views import (
    AddToCartView,
    CartView,
    SaleListView,
    SaleDetailView,
    RefundView,
    SalesReportView,
    CreateSaleView
)

urlpatterns = [
    path('create_sale/', CreateSaleView.as_view(), name='create_sale'),
    path('sales/', SaleListView.as_view(), name='sale_list'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale_detail'),
    path('sales/refund/', RefundView.as_view(), name='refund'),
    path('sales/reports/', SalesReportView.as_view(), name='sales_report'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
]
