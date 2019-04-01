from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

import datetime

from .models import ResponseInSale
from .tasks import daily_instansale_bulk_update

def bulk_update_trx(request):
    if ResponseInSale.objects.filter(sale__closed=False).exists():
        daily_instansale_bulk_update(repeat=3600, repeat_until=timezone.now() + datetime.timedelta(weeks=50))
    return JsonResponse({'return': 0})