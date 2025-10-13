"""
Factory classes for creating test data - User and Authorization related models
"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import Group, Permission
from apps.authorize.models import User, FrontendPermission
import datetime


class GroupFactory(DjangoModelFactory):
    """Factory for creating user groups"""
    class Meta:
        model = Group
    
    name = factory.Sequence(lambda n: f"group_{n}")


class UserFactory(DjangoModelFactory):
    """Factory for creating users"""
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    mobile = factory.Faker('phone_number')
    is_active = True
    is_staff = False
    is_superuser = False


class SuperUserFactory(UserFactory):
    """Factory for creating superusers"""
    is_staff = True
    is_superuser = True
    username = factory.Sequence(lambda n: f"admin_{n}")


class EmployeeUserFactory(UserFactory):
    """Factory for creating employee users with employee group"""
    
    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        
        employee_group, created = Group.objects.get_or_create(name='employee')
        self.groups.add(employee_group)


class ManagerUserFactory(UserFactory):
    """Factory for creating manager users with manager group"""
    
    @factory.post_generation  
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        
        manager_group, created = Group.objects.get_or_create(name='manager')
        self.groups.add(manager_group)


class FrontendPermissionFactory(DjangoModelFactory):
    """Factory for creating frontend permissions"""
    class Meta:
        model = FrontendPermission