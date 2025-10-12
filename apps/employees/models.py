import datetime
from django.db import models
from apps.core.models import Subrecord
from apps.authorize.models import User, UserManager
from apps.services.models import ServiceType

class EmployeeManager(UserManager):
    """Custom manager to return only employee users"""
    def get_queryset(self):
        return super().get_queryset().filter(groups__isnull=False)
    
    def role(self, role):
        return self.get_queryset().filter(groups__name=role)
    
    def managers(self):
        return self.role('manager')

    def employees(self):
        return self.role('employee')
    
class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True 
        verbose_name_plural = "Employee"

    def __str__(self):
        return f"Employee: {self.username}"
    
    @property
    def services(self):
        return self.employeeservice_set.all()

class EmployeeService(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('employee', 'service_type')