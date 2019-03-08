from django.contrib import admin

from .models import (
    Payment, LoanPayment, Transfer
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Transfer)
class TrasferAdmin(admin.ModelAdmin):
    pass