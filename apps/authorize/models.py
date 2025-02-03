from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager


class FrontendPermission(models.Model):
    view_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    add_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    change_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    delete_permissions = models.ManyToManyField(Permission, related_name='+', blank=True)


class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
   
    class Meta:
        ordering = ('last_name', )
    
    @property
    def name(self):
        return self.get_full_name()

    def has_role(self, group):
        return self.groups.filter(name=group).exists()
    

class ManagerUserManager(UserManager):
    """Custom manager to return only manager users"""
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="manager")
    
class EmployeeUserManager(UserManager):
    """Custom manager to return only staff users"""
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="employee")
