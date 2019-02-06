from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Profile, Wallet
)

class WalletInline(admin.StackedInline):
    model = Wallet
    min = 1
    max = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username', 'user__email'
    ]
    list_filter = [
        'user__is_active'
    ]
    list_display = [
        'user', 'user_type', 'agen',
        'display_saldo', 'display_commision', 'display_loan', 'display_limit',
    ]
    inlines = [
        WalletInline
    ]

    def display_saldo(self, instance):
        return instance.wallet.saldo
    
    def display_commision(self, instance):
        return instance.wallet.commision

    def display_loan(self, instance):
        return instance.wallet.loan

    def display_limit(self, instance):
        return instance.wallet.limit

    display_saldo.short_description = 'Saldo'
    display_commision.short_description = 'Commision'
    display_loan.short_description = 'Loan'
    display_limit.short_description = 'Limit'

class UserAdminCustom(UserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)