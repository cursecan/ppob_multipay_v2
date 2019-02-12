from django.urls import path

from . import views

app_name = 'api_payment'
urlpatterns = [
    path('paylist/', views.PaymentListApiView.as_view(), name='list_payment'),
]