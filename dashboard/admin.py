from django.contrib import admin

# Register your models here.
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass