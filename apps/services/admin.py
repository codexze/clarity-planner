from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, Addon, Staff, StaffService

class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'active']
    list_filter = ['type', 'active']
    search_fields = ['name', 'description']
    fieldsets = (
        (None, {'fields': ('type','name','description')}),
        ('Service Information', {'fields': ('duration', 'price', 'active')}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(Service, ServicesAdmin)

class AddonAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'active']
    list_filter = ['type', 'active']
    search_fields = ['name',]
    fieldsets = (
        (None, {'fields': ('type','name')}),
        ('Service Information', {'fields': ('additional_time', 'price', 'active')}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(Addon, AddonAdmin)
