from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', views.sale_view, name='sale_list'),
    path('members/', views.user_profile_view, name='member_list' ),
    path('profile/<int:id>/', views.user_profile_detail_view, name='profile'),

    path('api/billing-profile-<int:id>/', views.json_user_billing_view, name='json_billing_profile'),
    path('api/commision-profile-<int:id>/', views.json_user_commision_view, name='json_commision_profile'),
    path('api/loan-profile-<int:id>/', views.json_user_loan_view, name='json_loan_profile'),
]