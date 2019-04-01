"""ppob_multipay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)

from core import views as core_views
from dashboard import views as dashboard_views
from transaction import views as transac_view

urlpatterns = [
    path('', dashboard_views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/custom-login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('activate/<slug:uidb64>/<slug:token>/', core_views.activate, name='activate'),
    path('activate-success/', core_views.activate_success, name='activate_success'),
    path('jwt-api-token-auth/', obtain_jwt_token),
    path('jwt-api-token-refresh/', refresh_jwt_token),
    path('jwt-api-token-verify/', verify_jwt_token),
    path('adminpanel/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('api/profile/', include('userprofile.api.urls')),
    path('api/product/', include('product.api.urls')),
    path('api/transaction/', include('transaction.api.urls')),
    path('api/billing/', include('billing.api.urls')),
    path('api/payment/', include('payment.api.urls')),

    path('trx-bulk-checking/', transac_view.bulk_update_trx),
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
