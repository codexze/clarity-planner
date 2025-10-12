from django.contrib import admin
from .models import CalendarSettings, Appointment, BlockedTime


class CalendarSettingsAdmin(admin.ModelAdmin):
    list_display = ["user","default_view", "enable_weekends"]
    list_filter = ["enable_weekends", "default_view"]
    search_fields = ["user__first_name", "user__last_name"]
    fieldsets = (
        ("", {"fields": ("user", )}),
        ("Schedule Settings", {"fields": ("enable_weekends", "business_hours", )}),
        ("Calendar Settings", {"fields": ("default_view", "event_slots", )}),
        ("Color Settings", {"fields": ("inhouse_appointment_bgcolor", "inhouse_appointment_textcolor", "onsite_appointment_bgcolor", "onsite_appointment_textcolor", "blocked_bgcolor", "blocked_textcolor", "reminder_bgcolor", "reminder_textcolor", "processed_bgcolor", "processed_textcolor", "arrived_bgcolor", "arrived_textcolor",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["start", "end", "client", "service", "employee", "is_onsite", "arrived", "cancelation"]
    list_filter = ["service", "employee", "is_onsite", "arrived", "cancelation" ]
    search_fields = ["start", "end", "client"]
    fieldsets = (
        ("Appointment Information", {"fields": ("client", "service", "addons", "charges", "employee","is_onsite",)}),
        ("Arrival", {"fields": ("arrived", "arrived_time",)}),
        ("Cancelation", {"fields": ("cancelation", "cancelation_reason",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

class BlockedTimeAdmin(admin.ModelAdmin):
    list_display = ["start", "end", "employee", "reason"]
    list_filter = ["employee"]
    search_fields = ["start", "end", "employee", "reason"]
    fieldsets = (
        ("Blocked Time Information", {"fields": ("employee", "start", "end", "reason")}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_record(request.user, change)
        super().save_model(request, obj, form, change)

admin.site.register(CalendarSettings, CalendarSettingsAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(BlockedTime, BlockedTimeAdmin)





