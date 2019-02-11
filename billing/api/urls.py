from django.urls import path

from . import views

app_name = 'api_billing'
urlpatterns = [
    path('full-billing/', views.BillingRecordListApiView.as_view(), name='full_billing'),
    path('billing-trx/', views.BillingRecordTransactionApiListView.as_view(), name='billing_trx'),
    path('billing-trx/<int:id>/', views.BillingRecordTransactionDetailApiView.as_view(), name='detail_bill_trx'),
]