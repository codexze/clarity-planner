from django.contrib import admin
from .models import ServiceType, Service, Addon

admin.site.register(ServiceType)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'description']
    fieldsets = (
        (None, {'fields': ('type', 'name', 'description')}),
        ('Service Information', {'fields': ('duration', 'price', 'is_active')}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(Service, ServicesAdmin)

class AddonAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_types', 'price', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name',]
    fieldsets = (
        (None, {'fields': ('type','name')}),
        ('Service Information', {'fields': ('additional_time', 'price', 'is_active')}),
    )

    def get_types(self, obj):
        return ", ".join([t.name for t in obj.type.all()])
    get_types.short_description = 'Types'

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(Addon, AddonAdmin)
