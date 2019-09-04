from django.urls import path

from . import views

app_nam = 'v2'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
]