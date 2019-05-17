from django.urls import path, include

from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)
extra_patterns = [
# API
    path('profile/', include('userprofile.api.urls')),
    path('product/', include('product.api.urls')),
    path('transaction/', include('transaction.api.urls')),
    path('billing/', include('billing.api.urls')),
    path('payment/', include('payment.api.urls')),
    path('bankrecon/', include('bankrecon.api.urls')),
    path('withdraw/', include('witdraw.api.urls')),
    path('app/', include('api_production.api.urls')),
]

app_name = 'v1'
urlpatterns = [
    # JWT AUTH
    path('jwt-token-auth/', obtain_jwt_token),
    path('jwt-token-refresh/', refresh_jwt_token),
    path('jwt-token-verify/', verify_jwt_token),
    path('v1/', include(extra_patterns)),
]