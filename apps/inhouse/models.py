import datetime
from django.db import models
from apps.core.models import Subrecord
from apps.authorize.models import User, UserManager

class ServiceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Service(Subrecord):
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    @property
    def time_display(self):
        time = ""
        if self.duration.hour > 0:
            time += f"{self.duration.hour} hour"

        if self.duration.minute > 0:
            time += f"{self.duration.minute} minutes"
        return time

    @property
    def display(self):
        return f"{self.name} ({self.time_display})"

    def __str__(self):
        return self.display

class Addon(models.Model):
    type = models.ManyToManyField(ServiceType, related_name="addon")
    name = models.CharField(max_length=255)
    additional_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    @property
    def time_display(self):
        time = ""
        if self.additional_time.hour > 0:
            time += f"{self.additional_time.hour} hour"

        if self.additional_time.minute > 0:
            time += f"{self.additional_time.minute} minutes"
        return time

    @property
    def display(self):
        return f"{self.name} ({self.time_display})"

    def __str__(self):
        return self.display

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
    
class Staff(User):
    objects = StaffManager()

    class Meta:
        proxy = True  # This tells Django not to create a new table
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"Staff: {self.username}"
    
    @property
    def services(self):
        return self.staffservice_set.all()

class StaffService(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('staff', 'service_type')