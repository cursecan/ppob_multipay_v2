from django.urls import path

from . import views


app_name = 'api_version'
urlpatterns = [
    path('version/', views.ProductVersionApiView.as_view(), name='version'),
]