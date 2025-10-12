from django.contrib import admin
from .models import  Employee, EmployeeService


class EmployeeServiceInline(admin.TabularInline):
    model = EmployeeService
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'name', 'age', 'is_active']
    list_filter = ['groups', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [EmployeeServiceInline]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
    )

    def name(self, obj):
        return obj.get_full_name()

admin.site.register(Employee, EmployeeAdmin)


