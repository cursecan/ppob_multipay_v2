from django.shortcuts import render
from django.http.response import HttpResponse

from .tasks import send_invois_email_api

# Create your views here.

def sending_email_tunggakan(request):
    send_invois_email_api()

    return HttpResponse("0")
