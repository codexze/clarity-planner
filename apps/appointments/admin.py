from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["start", "end", "client", "service", "employee", "is_walkin", "arrived", "cancelation"]
    list_filter = ["service", "employee", "is_walkin", "arrived", "cancelation" ]
    search_fields = ["start", "end", "client"]
    fieldsets = (
        ("Appointment Information", {"fields": ("client", "service", "charges", "employee","is_walkin",)}),
        ("Arrival", {"fields": ("arrived", "arrived_time",)}),
        ("Cancelation", {"fields": ("cancelation", "cancelation_reason",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(Appointment, AppointmentAdmin)








