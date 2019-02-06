from django.urls import path

from . import views

app_name = 'api_transaction'
urlpatterns = [
    path('instansale-list/', views.InstanSaleListApiView.as_view(), name='list_instansale'),
    path('instansale/create/', views.InstanSaleCreateApiView.as_view(), name='create_instansale'),
]