from django.urls import path

from . import views

app_name = 'api_transaction'
urlpatterns = [
    path('instansale-list/', views.InstanSaleListApiView.as_view(), name='list_instansale'),
    path('instansale/create/', views.InstanSaleCreateApiView.as_view(), name='create_instansale'),
    path('ppobsale/create/', views.PpobSaleCreateApiView.as_view(), name='create_ppobsale'),
    path('ppobsale/inquery/', views.PpobInqueryApiView.as_view(), name='inquery_ppob'),
]