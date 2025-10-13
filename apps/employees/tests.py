"""
Unit tests for employees app models
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.employees.models import Employee, EmployeeService, EmployeeManager
from apps.services.models import ServiceType
from tests.factories.employees import EmployeeFactory, ServiceTypeFactory, EmployeeServiceFactory
from tests.factories.auth import UserFactory, EmployeeUserFactory, ManagerUserFactory
from tests.base import BaseTestCase


class EmployeeManagerTest(BaseTestCase):
    """Tests for EmployeeManager"""
    
    def setUp(self):
        super().setUp()
        # Create groups
        self.employee_group = Group.objects.create(name='employee')
        self.manager_group = Group.objects.create(name='manager')
        
    def test_employee_manager_filters_users_with_groups(self):
        """Test that EmployeeManager only returns users with groups"""
        # Create regular user without groups
        regular_user = UserFactory()
        
        # Create employee user with group
        employee_user = EmployeeUserFactory()
        
        # Create manager user with group  
        manager_user = ManagerUserFactory()
        
        # EmployeeManager should only return users with groups
        employees = Employee.objects.all()
        employee_usernames = [emp.username for emp in employees]
        
        self.assertIn(employee_user.username, employee_usernames)
        self.assertIn(manager_user.username, employee_usernames)
        self.assertNotIn(regular_user.username, employee_usernames)
        
    def test_employee_manager_role_filtering(self):
        """Test role-based filtering methods"""
        employee_user = EmployeeUserFactory()
        manager_user = ManagerUserFactory()
        
        # Test role filtering
        employees_only = Employee.objects.role('employee')
        managers_only = Employee.objects.role('manager')
        
        self.assertIn(employee_user.username, [emp.username for emp in employees_only])
        self.assertNotIn(manager_user.username, [emp.username for emp in employees_only])
        
        self.assertIn(manager_user.username, [mgr.username for mgr in managers_only])
        self.assertNotIn(employee_user.username, [mgr.username for mgr in managers_only])
        
    def test_employee_manager_convenience_methods(self):
        """Test managers() and employees() convenience methods"""
        employee_user = EmployeeUserFactory()
        manager_user = ManagerUserFactory()
        
        employees = Employee.objects.employees()
        managers = Employee.objects.managers()
        
        self.assertEqual(employees.count(), 1)
        self.assertEqual(managers.count(), 1)
        self.assertEqual(employees.first().username, employee_user.username)
        self.assertEqual(managers.first().username, manager_user.username)


class EmployeeModelTest(BaseTestCase):
    """Tests for Employee model (proxy)"""
    
    def test_employee_creation(self):
        """Test creating an employee"""
        employee = EmployeeFactory()
        self.assertTrue(isinstance(employee, Employee))
        self.assertIsNotNone(employee.username)
        
    def test_employee_str_representation(self):
        """Test employee string representation"""
        employee = EmployeeFactory(username="johndoe")
        expected_str = "Employee: johndoe"
        self.assertEqual(str(employee), expected_str)
        
    def test_employee_services_property(self):
        """Test employee services property"""
        employee = EmployeeFactory()
        service_type = ServiceTypeFactory()
        
        # Create employee-service relationship
        employee_service = EmployeeServiceFactory(
            employee=employee,
            service_type=service_type
        )
        
        services = employee.services
        self.assertEqual(services.count(), 1)
        self.assertEqual(services.first(), employee_service)
        
    def test_employee_inherits_user_properties(self):
        """Test that Employee inherits all User model properties"""
        employee = EmployeeFactory(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        
        self.assertEqual(employee.first_name, "John")
        self.assertEqual(employee.last_name, "Doe")
        self.assertEqual(employee.email, "john.doe@example.com")
        self.assertEqual(employee.name, "John Doe")


class EmployeeServiceTest(BaseTestCase):
    """Tests for EmployeeService model"""
    
    def test_employee_service_creation(self):
        """Test creating an employee-service relationship"""
        employee_service = EmployeeServiceFactory()
        
        self.assertTrue(isinstance(employee_service, EmployeeService))
        self.assertIsNotNone(employee_service.employee)
        self.assertIsNotNone(employee_service.service_type)
        self.assertTrue(employee_service.is_active)
        
    def test_employee_service_unique_together(self):
        """Test that employee-service_type combination is unique"""
        employee = EmployeeFactory()
        service_type = ServiceTypeFactory()
        
        # Create first relationship
        EmployeeServiceFactory(employee=employee, service_type=service_type)
        
        # Try to create duplicate - should raise IntegrityError
        with self.assertRaises(IntegrityError):
            EmployeeServiceFactory(employee=employee, service_type=service_type)
            
    def test_employee_service_different_combinations_allowed(self):
        """Test that different employee-service combinations are allowed"""
        employee1 = EmployeeFactory()
        employee2 = EmployeeFactory()
        service_type1 = ServiceTypeFactory()
        service_type2 = ServiceTypeFactory()
        
        # These should all be allowed
        es1 = EmployeeServiceFactory(employee=employee1, service_type=service_type1)
        es2 = EmployeeServiceFactory(employee=employee1, service_type=service_type2)
        es3 = EmployeeServiceFactory(employee=employee2, service_type=service_type1)
        es4 = EmployeeServiceFactory(employee=employee2, service_type=service_type2)
        
        self.assertEqual(EmployeeService.objects.count(), 4)
        
    def test_employee_service_cascade_delete_employee(self):
        """Test that EmployeeService is deleted when employee is deleted"""
        employee_service = EmployeeServiceFactory()
        employee = employee_service.employee
        
        employee.delete()
        
        with self.assertRaises(EmployeeService.DoesNotExist):
            employee_service.refresh_from_db()
            
    def test_employee_service_cascade_delete_service_type(self):
        """Test that EmployeeService is deleted when service_type is deleted"""
        employee_service = EmployeeServiceFactory()
        service_type = employee_service.service_type
        
        service_type.delete()
        
        with self.assertRaises(EmployeeService.DoesNotExist):
            employee_service.refresh_from_db()
            
    def test_employee_service_deactivation(self):
        """Test employee service can be deactivated"""
        employee_service = EmployeeServiceFactory()
        employee_service.is_active = False
        employee_service.save()
        
        employee_service.refresh_from_db()
        self.assertFalse(employee_service.is_active)


# Pytest-style tests
@pytest.mark.django_db
class TestEmployeeModel:
    """Pytest-style tests for Employee model"""
    
    def test_employee_factory_creates_valid_employee(self):
        """Test that factory creates a valid employee"""
        employee = EmployeeFactory()
        assert employee.pk is not None
        assert employee.groups.filter(name='employee').exists()
        
    def test_multiple_employees_can_exist(self):
        """Test creating multiple employees"""
        employees = EmployeeFactory.create_batch(3)
        assert len(employees) == 3
        assert all(emp.pk is not None for emp in employees)


@pytest.mark.django_db
class TestEmployeeServiceModel:
    """Pytest-style tests for EmployeeService model"""
    
    def test_employee_service_factory_creates_valid_relationship(self):
        """Test that factory creates a valid employee-service relationship"""
        employee_service = EmployeeServiceFactory()
        assert employee_service.pk is not None
        assert employee_service.is_active is True
        
    def test_employee_can_have_multiple_services(self):
        """Test that an employee can provide multiple services"""
        employee = EmployeeFactory()
        service1 = ServiceTypeFactory()
        service2 = ServiceTypeFactory()
        
        es1 = EmployeeServiceFactory(employee=employee, service_type=service1)
        es2 = EmployeeServiceFactory(employee=employee, service_type=service2)
        
        assert employee.services.count() == 2
