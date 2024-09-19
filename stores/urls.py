from django.urls import path
from .views import StoreCreateView, StoreUpdateView, StoreListView

urlpatterns = [
    path('', StoreListView.as_view(), name='store_list'),
    path('stores/add/', StoreCreateView.as_view(), name='store_add'),
    path('stores/update/<int:pk>', StoreUpdateView.as_view(), name='store_update'), 

]
