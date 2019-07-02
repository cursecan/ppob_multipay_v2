from django.urls import path
from . import views


app_name = 'produck'
urlpatterns = [
    path('product-stat/', views.get_bulk_prodstatus, name='bulks_status'),
    path('op-status/<str:op_code>/', views.get_bulk_opstatus, name='bulk_op_status'),
]