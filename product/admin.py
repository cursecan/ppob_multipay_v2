from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

from .resources import *


from .models import (
    Product, Prefix, Operator, Group
)
from .forms import (
    GroupForm, OperatorForm, ProductForm
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
    list_filter = [
        'is_active',
        'type_product',
        'operator__operator_name',
        'group__group_name'
    ]
    list_display = [
        'display_product', 'operator', 'group',
        'nominal', 'price', 'commision',
        'is_active'
    ]
    form = ProductForm
    fieldsets = (
        (None, {
            'fields': ('type_product', 'code', 'product_name')
        }),
        (None, {
            'fields': (('group', 'operator'),)
        }),
        ('Price information', {
            'fields': ('nominal', 'price', 'commision'),
            'classes': ('collapse',)
        }),
        (None, {
            'fields' : ('is_active',)
        })
    )
    resource_class = ProductResource

    def display_product(self, instance):
        return format_html(
            '{} ({})',
            instance.product_name,
            instance.code
        )

    display_product.short_description = 'Product'


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
        'display_operator',
    ]
    inlines = [
        PrefixInline
    ]
    form = OperatorForm
    resource_class = OperatorResource

    fieldsets = (
        (None, {
            'fields': (('code', 'operator_name'),)
        }),
    )

    def display_operator(self, instance):
        return format_html(
            '{} ({})',
            instance.operator_name,
            instance.code
        )
    display_operator.short_description = 'Operator'


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
        'display_group'
    ]
    form = GroupForm
    resource_class = GroupResource

    def display_group(self, instance):
        return format_html(
            '{} ({})',
            instance.group_name,
            instance.code
        )

    display_group.short_description = 'Group'