from django.urls import path

from . import views

app_name = 'api_product'
urlpatterns = [
    path('instan-product/', views.ProductListApiView.as_view(), name='list_product'),
    path('ppob-product/', views.PpobProductListApiView.as_view(), name='list_ppob_product'),
    path('product-detail/<int:id>/', views.ProductDetailApiView.as_view(), name='detail_product'),
    path('operator/', views.OperatorListApiView.as_view(), name='list_operator'),
]