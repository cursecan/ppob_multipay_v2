from django.urls import path

from . import views

app_name = 'api_withdraw'
urlpatterns = [
    path('withdraw/create/', views.WitdrawApiCreateView.as_view(), name='create_withdraw'),
]