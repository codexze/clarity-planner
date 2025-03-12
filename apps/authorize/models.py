import datetime
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
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.date.today()
            born = self.date_of_birth
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return None
    
    @property
    def display(self):
        return f"{self.name} ({self.age}Y)" if self.age else f"{self.name} -Y)"
    
    def __str__(self):
        return self.name

    def has_role(self, group):
        return self.groups.filter(name=group).exists()
    
class StaffManager(UserManager):
    """Custom manager to return only staff users"""
    def get_queryset(self):
        return super().get_queryset().filter(groups__isnull=False)
    
    def role(self, role):
        return self.get_queryset().filter(groups__name=role)
    
    def managers(self):
        return self.role('manager')

    def employees(self):
        return self.role('employee')
