from django.db import models
from apps.core.models import Subrecord
from apps.authorize.models import User, EmployeeUserManager

class ServiceType(models.TextChoices):
    HAIR = "HAIR"
    MAKEUP = "MAKEUP"
    MASSAGES = "MASSAGES"
    WAXING = "WAXING"
    FACIALS = "FACIALS"
    OTHER = "OTHER"
        
class Service(Subrecord):
    type = models.CharField(choices=ServiceType.choices, default=ServiceType.OTHER)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

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
    type = models.CharField(choices=ServiceType.choices)
    name = models.CharField(max_length=255)
    additional_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

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
        return f"{self.type} > {self.name} ({self.time_display})"

    def __str__(self):
        return self.display
    
class Employee(User):
    objects = EmployeeUserManager()

    class Meta:
        proxy = True  # This tells Django not to create a new table

    def __str__(self):
        return f"Staff: {self.username}"
    
class EmployeeService(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('employee', 'service')  
        
    def __str__(self):
        return f"{self.employee.name} ({self.service.display})"
