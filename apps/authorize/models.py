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
    mobile = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ('last_name', )

    def __str__(self):
        return self.name
    
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
        return f"{self.name} ({self.age}Y)" if self.age else f"{self.name} (-Y)"
    

    def has_role(self, group):
        return self.groups.filter(name=group).exists()

