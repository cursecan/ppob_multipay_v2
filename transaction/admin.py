from django.contrib import admin

from .models import (
    InstanSale, Status, PpobSale
)
from .forms import (
    InstanSaleForm,
    PpobSaleForm
)


@admin.register(InstanSale)
class InstanSaleAdmin(admin.ModelAdmin):
    form = InstanSaleForm

@admin.register(PpobSale)
class PpobSaleAdmin(admin.ModelAdmin):
    form = PpobSaleForm

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass