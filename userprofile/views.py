from django.shortcuts import render
from django.http.response import HttpResponse

from .tasks import send_email_invois

# Create your views here.

def sending_email_tunggakan(request):
    send_email_invois()

    return HttpResponse("0")
