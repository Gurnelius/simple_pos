from django.urls import path
from .views import ProductListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



