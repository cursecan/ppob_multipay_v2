from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import *


from .models import (
    Product, Prefix, Operator, Group
)
from .forms import (
    GroupForm, OperatorForm
)


class PrefixInline(admin.TabularInline):
    model = Prefix
    extra = 1

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource


@admin.register(Operator)
class OperatorAdmin(ImportExportModelAdmin):
    inlines = [
        PrefixInline
    ]
    form = OperatorForm
    resource_class = OperatorResource


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    form = GroupForm
    resource_class = GroupResource