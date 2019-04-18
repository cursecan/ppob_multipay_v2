from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Payment, LoanPayment, Transfer,
    # Bank, BankAccount
)

# from .forms import BankForm

# class BankAccountInline(admin.TabularInline):
#     model = BankAccount
#     extra = 1
#     fields = [
#         'rekening', 'name'
#     ]

# @admin.register(Bank)
# class BankAdmin(admin.ModelAdmin):
#     list_display = [
#         'display_bank',
#     ]
#     inlines = [
#         BankAccountInline
#     ]
#     form = BankForm
#     fields = [
#         'bank_code', 'bank_name'
#     ]

#     def display_bank(self, instance):
#         return format_html(
#             '{} ({})',
#             instance.bank_name,
#             instance.bank_code
#         )

#     display_bank.short_description = 'Bank'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Transfer)
class TrasferAdmin(admin.ModelAdmin):
    pass