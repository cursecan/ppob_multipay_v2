from django.contrib import admin

from .models import (
    InstanSale, Status, PpobSale,
    ResponseInSale, ResponsePpobSale
)
from .forms import (
    InstanSaleForm,
    PpobSaleForm
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

@admin.register(ResponseInSale)
class ResponseInSaleAdmin(admin.ModelAdmin):
    list_display = [
        'sale', 'kode_produk', 'no_hp',
        'ref2', 'ket', 'saldo_terpotong', 'display_status'
    ]

    def display_status(self, instance):
        return instance.sale.instansale_status.latest('timestamp')

@admin.register(ResponsePpobSale)
class ResponsePpobSaleAdmin(admin.ModelAdmin):
    pass