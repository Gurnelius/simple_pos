from django.urls import path
from .views import (
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
]
