from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Q, Sum, Count, Value as V, Case, When, Max, Min
from django.db.models.functions import Coalesce, TruncDate, TruncMonth
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector

from billing.models import (
    BillingRecord, CommisionRecord, LoanRecord
)
from userprofile.models import Profile
from core.decorators import (
    user_is_agen, user_is_related_agen
)
from product.models import (
    Product, Group
)

from .models import Application


def get_pagination(obj, n=10, page=1):
    page_list = Paginator(obj, n)
    try:
        bill_list = page_list.page(page)
    except PageNotAnInteger:
        bill_list = page_list.page(1)
    except EmptyPage:
        bill_list = page_list.page(page_list.page_range)

    return bill_list


# VIEW APPLICATION ON HOME PAGE
def get_application_view(request):
    data = dict()
    app_obj = Application.objects.latest('timestamp')
    data['html'] = render_to_string(
        'dashboard/includes/partial-application.html', 
        {'app': app_obj},
        request=request
    ) 
    return JsonResponse(data)


# INDEX
@login_required
def index(request):
    commision_objs = CommisionRecord.objects.filter(
        agen = request.user, is_delete=False
    )

    content = {
        'commision_list': commision_objs[:5]
    }
    return render(request, 'dashboard/index.html', content)


# SALE VIEW
@login_required
def sale_view(request):
    """
        Sale for related user
        Pagination
        Search by customer
    """
    page = request.GET.get('page', None)
    q = request.GET.get('q', None)

    bill_objs = BillingRecord.objects.filter(
        sequence = 1
    ).filter(
        Q(instansale_trx__isnull=False) | Q(ppobsale_trx__isnull=False)
    )

    if not request.user.is_superuser:
        # Sales for related user
        bill_objs = bill_objs.filter(
            user=request.user
        )

    if q:
        # Sale search
        bill_objs = bill_objs.annotate(
            search = SearchVector(
                'instansale_trx__customer', 'ppobsale_trx__customer'
            )
        ).filter(search = q)

    # Pagination
    bill_list = get_pagination(bill_objs, n=20, page=page)

    content = {
        'bill_list': bill_list,
        'q': q
    }
    return render(request, 'dashboard/pg-sale.html', content)


# PRODUCT  VIEW
@login_required
def productView(request):
    group_objs = Group.objects.filter(
        active = True
    )
    product_objs = Product.objects.filter(
        group__code = 'PULSA', operator__code='TSEL'
    )
    content = {
        'group_list': group_objs,
        'product_list': product_objs,
    }
    return render(request, 'dashboard/pg-product.html', content)


# PRODUCT JS VIEW
@login_required
def productJsonView(request):
    data = dict()
    op = request.GET.get('op', 1)
    gr = request.GET.get('gr', 1)

    product_objs = Product.objects.filter(
        group_id=gr, operator_id=op
    )
    content = {
        'product_list': product_objs
    }
    data['html'] = render_to_string(
        'dashboard/includes/partial-product-list.html',
        content, request=request
    )
    return JsonResponse(data)


@login_required
def getMeView(request):
    return render(request, 'dashboard/pg-getme.html')

# LOAN VIEW
@login_required
@user_is_agen
def loanView(request):
    """
        Agen required
        Loan of member
        Loan Search
        pagination
    """
    page = request.GET.get('page', 1)

    loan_objs = LoanRecord.objects.filter(
        agen = request.user
    )

    loan_pages = get_pagination(loan_objs, 20, page)
    content = {
        'loan_list': loan_pages
    }

    return render(request, 'dashboard/pg-loan.html', content)


# COMMISISON VIEW
@login_required
@user_is_agen
def commisionView(request):
    """
        Commision agen
        Pagination
    """
    page = request.GET.get('page', 1)

    commision_objs = CommisionRecord.objects.filter(
        agen = request.user
    )

    resume_commision = commision_objs.aggregate(
        commision = Coalesce(
            Sum(F('debit')-F('credit')), V(0)
        )
    ) 
    
    commision_page = get_pagination(commision_objs, 20, page)
    content = {
        'commision_list': commision_page,
        'commision_resume': resume_commision,
    }

    return render(request, 'dashboard/pg_commision.html', content)


# USER LIST VIEW
@login_required
@user_is_agen
def user_profile_view(request):
    """
        Profile list related agen
        Search profile
        Pagination
    """
    page = request.GET.get('page', 1)
    q = request.GET.get('q', None)

    profile_objs = Profile.objects.select_related(
        'wallet'
    ).order_by('user__username')

    if not request.user.is_superuser:
        # Profile related agen
        profile_objs = profile_objs.filter(
            agen = request.user
        )
    
    if q:
        # Search profile
        profile_objs = profile_objs.annotate(
            search = SearchVector(
                'user__username', 'user__email', 'user__first_name', 'user__last_name'
            )
        ).filter(search=q)
    
    # Pagination
    profile_list = get_pagination(profile_objs, 20, page)

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

