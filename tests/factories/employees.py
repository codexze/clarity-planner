"""
Factory classes for creating test data - Employee related models
"""
import factory
from factory.django import DjangoModelFactory
from apps.employees.models import Employee, EmployeeService
from apps.services.models import ServiceType
from .auth import EmployeeUserFactory, UserFactory


class EmployeeFactory(EmployeeUserFactory):
    """Factory for creating employees (proxy model)"""
    class Meta:
        model = Employee


class ServiceTypeFactory(DjangoModelFactory):
    """Factory for creating service types"""
    class Meta:
        model = ServiceType
    
    name = factory.Faker('job')


class EmployeeServiceFactory(DjangoModelFactory):
    """Factory for creating employee-service relationships"""
    class Meta:
        model = EmployeeService
    
    employee = factory.SubFactory(EmployeeFactory)
    service_type = factory.SubFactory(ServiceTypeFactory)
    is_active = True