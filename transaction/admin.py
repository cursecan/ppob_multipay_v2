from django.contrib import admin

from .models import (
    InstanSale, Status
)


@admin.register(InstanSale)
class InstanSaleAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass