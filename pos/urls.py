from django.urls import path
from .views import ProductListView, CreateSaleView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('create_sale/', CreateSaleView.as_view(), name='create_sale'),
]
