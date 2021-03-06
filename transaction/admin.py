from django.contrib import admin
from django.utils.html import format_html


from .models import (
    InstanSale, Status, PpobSale,
    ResponseInSale, ResponsePpobSale,
    RefundRequest, RefundApproval
)
from .forms import (
    InstanSaleForm,
    PpobSaleForm,
    RefundRequestForm, RefundApprovalForm
)


# @admin.register(InstanSale)
# class InstanSaleAdmin(admin.ModelAdmin):
#     form = InstanSaleForm

@admin.register(PpobSale)
class PpobSaleAdmin(admin.ModelAdmin):
    form = PpobSaleForm

# @admin.register(Status)
# class StatusAdmin(admin.ModelAdmin):
#     pass

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = [
        'display_trx', 'comment'
    ]
    form = RefundRequestForm

    def display_trx(self, instance):
        return instance.__str__()

    display_trx.short_description = 'Trx'

@admin.register(RefundApproval)
class RefundApprovalAdmin(admin.ModelAdmin):
    list_display = [
        'refund', 'approve'
    ]
    form = RefundApprovalForm

@admin.register(ResponseInSale)
class ResponseInSaleAdmin(admin.ModelAdmin):
    search_fields = [
        'sale__code', 'sale__customer'
    ]
    list_display = [
        'sale', 'display_product', 'display_customer',
        'ref2', 'ket', 'saldo_terpotong', 'display_status', 'buyer'
    ]

    def display_status(self, instance):
        return instance.sale.instansale_status.latest('timestamp')

    def display_product(self, instance):
        return instance.sale.product.product_name

    def display_customer(self, instance):
        return instance.sale.customer

    def buyer(self, instance):
        return instance.sale.create_by

@admin.register(ResponsePpobSale)
class ResponsePpobSaleAdmin(admin.ModelAdmin):
    search_fields = [
        'sale__code', 'sale__customer'
    ]
    list_display = [
        'sale', 'display_product', 'display_customer',
        'ref2', 'ket', 'saldo_terpotong', 'display_status', 'buyer'
    ]

    def display_status(self, instance):
        return instance.sale.ppobsale_status.latest('timestamp')

    def display_product(self, instance):
        return instance.sale.product.product_name

    def display_customer(self, instance):
        return instance.sale.customer

    def buyer(self, instance):
        return instance.sale.create_by