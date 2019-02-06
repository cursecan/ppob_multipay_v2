from django.urls import path

from . import views

app_name = 'api_product'
urlpatterns = [
    path('product-list/', views.ProductListApiView.as_view(), name='list_product'),
    path('product-detail/<int:id>/', views.ProductDetailApiView.as_view(), name='detail_product'),
]