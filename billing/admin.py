from django.contrib import admin

from .models import (
    BillingRecord, CommisionRecord, LoanRecord,
    ProfitRecord,
)

@admin.register(BillingRecord)
class BillingRecordAdmin(admin.ModelAdmin):
    list_display = [
        'display_sale', 'display_product',
        'user',
        'debit', 'credit', 'balance',
        'display_status'
    ]

    def get_sale(self, instance):
        if instance.instansale_trx:
            return instance.instansale_trx
        return None

    def display_sale(self, instance):
        return self.get_sale(instance).code

    def display_product(self, instance):
        return self.get_sale(instance).product.product_name

    def display_status(self, instance):
        return self.get_sale(instance).get_status()


@admin.register(CommisionRecord)
class CommisionRecordAdmin(admin.ModelAdmin):
    list_display = [
        'agen',
        'debit', 'credit', 'balance'
    ]

@admin.register(LoanRecord)
class LoanRecordAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'agen',
        'debit', 'credit', 'balance',
    ]

@admin.register(ProfitRecord)
class ProfitRecordAdmin(admin.ModelAdmin):
    pass