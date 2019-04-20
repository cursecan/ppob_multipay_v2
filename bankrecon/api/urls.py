from django.urls import path

from . import views

app_name = 'api_bankrecon'
urlpatterns = [
    path('bank/', views.BankAccountListApiView.as_view(), name='bank'),
    path('bank/<int:id>/', views.BankAccountDetailApiView.as_view(), name='bank_detail'),
    path('catatan/', views.CatatanListApiView.as_view(), name='catatan'),
    path('catatan/new/', views.CatatanCreateApiView.as_view(), name='create_catatan'),
]