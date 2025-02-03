from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User


admin.site.unregister(Group)

class UserProfileAdmin(UserAdmin):
    list_display = ('username','first_name', 'last_name', 'date_of_birth', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ( 'first_name', 'last_name', 'date_of_birth', 'email',)}),
        ('Permissions', {'fields': ( 'is_active', 'is_staff', 'groups',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ( 'username', 'first_name', 'last_name', 'date_of_birth', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ( 'is_active', 'is_staff', 'groups', 'force_password_change',)})
    )

admin.site.register(User, UserProfileAdmin)