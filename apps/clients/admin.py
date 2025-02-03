from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'surname', 'date_of_birth', 'gender', 'emailaddress', 'mobile', 'active']
    list_filter = [ 'gender', 'active']
    search_fields = ['first_name', 'surname', 'date_of_birth', 'mobile']
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'surname', 'date_of_birth', 'gender',)}),
        ('Contact Information', {'fields': ('emailaddress', 'mobile',)}),
        (None, {'fields': ('active',)}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(Client, ClientAdmin)