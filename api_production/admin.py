from django.contrib import admin

from .models import ProductVersion

@admin.register(ProductVersion)
class ProductVersion(admin.ModelAdmin):
    list_display = [
        'version', 'description'
    ]