from django.contrib import admin

from .models import Witdraw
from .forms import WitdrawForm


@admin.register(Witdraw)
class WitdrawAdmin(admin.ModelAdmin):
    list_display = [
        'amount', 'create_by', 'timestamp'
    ]
    form = WitdrawForm