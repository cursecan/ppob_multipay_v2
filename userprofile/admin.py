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

class WalletInline(admin.TabularInline):
    model = Wallet
    fields = [
        'saldo', 'commision', 'limit', 'init_loan'
    ]
    min_num = 1
    max_num = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name'
    ]
    list_filter = [
        'user__is_active'
    ]
    list_display = [
        'user', 'user_type', 'agen', 'display_status',
        'display_saldo', 'display_commision', 'display_limit',
    ]

    fieldsets = (
        (
            None, {
                'fields': ('user', 'ponsel'),
            }
        ),
        (
            'Advance options', {
                'fields': ('agen', 'user_type', 'email_confirmed'),
                'classes': ('collapse',)
            }
        )
    )

    inlines = [
        WalletInline
    ]

    def display_saldo(self, instance):
        return instance.wallet.saldo
    
    def display_commision(self, instance):
        return instance.wallet.commision

    def display_limit(self, instance):
        return instance.wallet.limit

    def display_status(self, instance):
        return instance.user.is_active

    display_saldo.short_description = 'Saldo'
    display_commision.short_description = 'Commision'
    display_limit.short_description = 'Limit'
    display_status.short_description = 'is_Active'
    display_status.boolean = True

    admin.site.unregister(User)