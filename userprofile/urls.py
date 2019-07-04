from django.urls import path

from . import views

app_name = 'userprofile'
urlpatterns = [
    path('sending-mail-tunggakan/', views.sending_email_tunggakan, name='sending_mail_tgk'),
]