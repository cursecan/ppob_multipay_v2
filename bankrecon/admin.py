from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Bank, BankAccount, Reconciliation,
)


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1
    fields = [
        'account'
    ]


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = [
        'display_bank',
    ]
    inlines = [
        BankAccountInline
    ]
    fields = [
        'bank_code', 'bank_name'
    ]

    def display_bank(self, instance):
        return format_html(
            '{} ({})',
            instance.bank_name,
            instance.bank_code
        )
    
    display_bank.short_description = 'Bank'


@admin.register(Reconciliation)
class ReconciliationAdmin(admin.ModelAdmin):
    list_display = [
        'reconid', 'nominal', 'identified', 'trans_date'
    ]