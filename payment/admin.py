from django.contrib import admin

from .models import (
    Payment, LoanPayment
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(LoanPayment)
class LoanPayment(admin.ModelAdmin):
    pass