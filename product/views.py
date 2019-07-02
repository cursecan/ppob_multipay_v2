from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import (
    Product, Operator
)
from django.utils import timezone

from .tasks import (
    scheduling_prod_status,
    product_operator_status
)

import datetime

# Create your views here.


def get_bulk_prodstatus(request):
    _op = request.GET.get('op', None)

    prod_obj = Product.objects.filter(type_product='IN')
    
    if _op:
        prod_obj = prod_obj.filter(operator__code=_op)

    for i in prod_obj:
        # Generate task status
        scheduling_prod_status(i.id, verbose_name='Produk status', creator=i, repeat=300, repeat_until=timezone.now() + datetime.timedelta(weeks=50))

    return HttpResponse('0')


def get_bulk_opstatus(request, op_code):
    op_obj = get_object_or_404(Operator, code=op_code)
    
    product_operator_status(op_obj.id, verbose_name=op_obj.operator_name, creator=op_obj, repeat=300, repeat_until=timezone.now() + datetime.timedelta(weeks=50))

    return HttpResponse('0')