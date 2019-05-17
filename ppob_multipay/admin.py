from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    site_header = 'Warungid Administrator'
    site_title = 'Warungid site admin'