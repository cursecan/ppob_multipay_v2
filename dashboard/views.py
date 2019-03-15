from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Q, Sum, Count, Value as V, Case, When, Max, Min
from django.db.models.functions import Coalesce, TruncDate, TruncMonth
from django.template.loader import render_to_string
from django.http import JsonResponse

from billing.models import (
    BillingRecord, CommisionRecord, LoanRecord
)
from userprofile.models import Profile
from core.decorators import (
    user_is_agen, user_is_related_agen
)

def get_pagination(obj, n=10, page=1):
    page_list = Paginator(obj, n)
    try:
        bill_list = page_list.page(page)
    except PageNotAnInteger:
        bill_list = page_list.page(1)
    except EmptyPage:
        bill_list = page_list.page(page_list.page_range)

    return bill_list


# INDEX
@login_required
def index(request):
    bill_objs = BillingRecord.objects.filter(
        sequence = 1
    ).filter(
        Q(instansale_trx__isnull=False) | Q(ppobsale_trx__isnull=False)
    )

    if not request.user.is_superuser:
        bill_objs = bill_objs.filter(
            Q(user__profile__agen = request.user) | Q(user=request.user)
        )

    content = {
        'bill_list': bill_objs[:5]
    }
    return render(request, 'dashboard/index.html', content)


# SALE VIEW
@login_required
def sale_view(request):
    page = request.GET.get('page', None)
    q = request.GET.get('q', None)

    bill_objs = BillingRecord.objects.filter(
        sequence = 1
    ).filter(
        Q(instansale_trx__isnull=False) | Q(ppobsale_trx__isnull=False)
    )

    if not request.user.is_superuser:
        bill_objs = bill_objs.filter(
            Q(user__profile__agen = request.user) | Q(user=request.user)
        )

    # Search value
    if q:
        bill_objs = bill_objs.filter(
            Q(instansale_trx__customer__contains=q) | Q(ppobsale_trx__customer__contains=q)
        )

    bill_list = get_pagination(bill_objs, page=page)

    content = {
        'bill_list': bill_list,
        'q': q
    }
    return render(request, 'dashboard/pg-sale.html', content)


# USER LIST VIEW
@login_required
@user_is_agen
def user_profile_view(request):
    page = request.GET.get('page', None)
    profile_objs = Profile.objects.select_related(
        'wallet'
    ).order_by('user__username')

    if not request.user.is_superuser:
        profile_objs = profile_objs.filter(
            agen = request.user
        )
    
    profile_list = get_pagination(profile_objs, page=page)

    content = {
        'profile_list': profile_list
    }
    return render(request, 'dashboard/pg-user.html', content)


# PROFIL DETAIL
@login_required
@user_is_agen
@user_is_related_agen
def user_profile_detail_view(request, id):
    profile_obj = get_object_or_404(Profile, pk=id)
    sum_loan = LoanRecord.objects.filter(
        user__profile__id=profile_obj.id
    )
    if not request.user.is_superuser:
        sum_loan = sum_loan.filter(
            agen = request.user
        )

    sum_loan = sum_loan.aggregate(
        t = Sum(F('credit')-F('debit'))
    )

    content = {
        'profile': profile_obj,
        'loan': sum_loan,
    }
    return render(request, 'dashboard/pg-user-detail.html', content)


# SALE PROFILE
@login_required
@user_is_agen
@user_is_related_agen
def json_user_billing_view(request, id):
    data = dict()
    page = request.GET.get('page', 1)
    profile_obj = get_object_or_404(Profile, pk=id)

    bill_objs = profile_obj.user.billingrecord_set.filter(
        sequence = 1
    ).filter(
        Q(instansale_trx__isnull=False) | Q(ppobsale_trx__isnull=False) 
    )

    bill_list = get_pagination(bill_objs, page=page)

    content = {
        'bill_list': bill_list
    }
    
    data['html'] = render_to_string(
        'dashboard/includes/partial-user-billing.html', content, request=request
    )
    return JsonResponse(data)


# COMMISION PROFILE
@login_required
@user_is_agen
@user_is_related_agen
def json_user_commision_view(request, id):
    data = dict()
    page = request.GET.get('page', 1)

    profile_obj = get_object_or_404(Profile, pk=id)
    
    commision_objs = CommisionRecord.objects.select_related(
        'instansale_trx', 'ppobsale_trx'
    ).filter(
        agen = request.user
    ).filter(
        Q(instansale_trx__create_by__profile__id=profile_obj.id) | Q(ppobsale_trx__create_by__profile__id=profile_obj.id)
    )

    # PAGINATION METHOD
    commision_list = get_pagination(commision_objs, page=page)
    
    content = {
        'commision_list': commision_list,
    }

    data['html'] = render_to_string(
        'dashboard/includes/partial-user-commision.html', content,
        request=request
    )
    return JsonResponse(data)


# LOAN PROFILE
@login_required
@user_is_agen
@user_is_related_agen
def json_user_loan_view(request, id):
    data = dict()
    page = request.GET.get('page', 1)
    profile_obj = get_object_or_404(
        Profile, pk=id
    )

    loan_objs = LoanRecord.objects.filter(
        user__profile__id=profile_obj.id, agen=request.user, is_paid=False
    ).annotate(
        trx = Case(
            When(instansale_trx__isnull=False, then=F('instansale_trx')),
            When(ppobsale_trx__isnull=False, then=F('ppobsale_trx')),
            default=F('loan_payment')
        )
    )

    # PAGINATION METHOD
    loan_list = get_pagination(loan_objs, page=page)
    content = {
        'loan_list': loan_list
    }

    data['html'] = render_to_string(
        'dashboard/includes/partial-user-loan.html', content,
        request=request
    )
    return JsonResponse(data)

