from django.urls import path

from . import views

app_name = 'api_payment'
urlpatterns = [
    path('paylist/', views.PaymentListApiView.as_view(), name='list_payment'),
    path('flag/', views.LoanPaymentFlagApiView.as_view(), name='flag'),
    path('transfer/', views.TransferCreateApiView.as_view(), name='transfer'),
    path('bank-list/', views.BankAccountListApiView.as_view(), name='list_bank'),
]