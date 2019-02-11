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
    search_fields = [
        'code', 'product_name'
    ]
    list_max_show_all = 100
    list_per_page = 20
    list_editable = [
        'price', 'commision'
    ]
    list_filter = [
        'is_active',
        'type_product',
        'operator__operator_name',
        'group__group_name'
    ]
    list_display = [
        'product_name',
        'code', 'operator', 'group',
        'nominal', 'price', 'commision',
        'is_active'
    ]
    resource_class = ProductResource


@admin.register(Operator)
class OperatorAdmin(ImportExportModelAdmin):
    search_fields = [
        'code', 'operator_name'
    ]
    list_max_show_all = 100
    list_per_page = 20
    list_filter = [
        'group__group_name'
    ]
    list_display = [
        'operator_name', 'code',
    ]
    inlines = [
        PrefixInline
    ]
    form = OperatorForm
    resource_class = OperatorResource


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    search_fields = [
        'code', 'group_name'
    ]
    list_max_show_all = 100
    list_per_page = 20
    list_filter = [
        'operator__operator_name'
    ]
    list_display = [
        'group_name', 'code',
    ]
    form = GroupForm
    resource_class = GroupResource