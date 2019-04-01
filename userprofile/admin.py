from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Profile, Wallet, UploadUser
)

from .resources import (
    WalletResource,
    UploadUserResource,
)

class WalletInline(admin.StackedInline):
    model = Wallet
    min = 1
    max = 1


@admin.register(UploadUser)
class UploadUserAdmin(ImportExportModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name'
    ]
    resource_class = UploadUserResource


@admin.register(Wallet)
class WalletAdmin(ImportExportModelAdmin):
    resource_class = WalletResource
    list_display = [
        'profile', 'saldo', 'limit', 'init_loan', 'commision'
    ]


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
        return '{} + {}'.format(instance.wallet.loan, instance.wallet.init_loan)

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