from django.contrib import admin

from .models import InstanSale


@admin.register(InstanSale)
class InstanSaleAdmin(admin.ModelAdmin):
    pass