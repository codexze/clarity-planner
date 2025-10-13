"""
Factory classes for creating test data - Client related models
"""
import factory
from factory.django import DjangoModelFactory
from apps.clients.models import Company, Client, Gender
from .auth import UserFactory
import datetime


class CompanyFactory(DjangoModelFactory):
    """Factory for creating companies"""
    class Meta:
        model = Company
    
    name = factory.Faker('company')
    address = factory.Faker('address')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')
    website = factory.Faker('url')
    is_active = True


class ClientFactory(DjangoModelFactory):
    """Factory for creating clients"""
    class Meta:
        model = Client
    
    company = factory.SubFactory(CompanyFactory)
    first_name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=16, maximum_age=90)
    gender = factory.Faker('random_element', elements=[choice[0] for choice in Gender.choices])
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name.lower()}.{obj.surname.lower()}@example.com")
    mobile = factory.Faker('phone_number')
    is_active = True


class ClientWithoutCompanyFactory(ClientFactory):
    """Factory for creating clients without company"""
    company = None


class InactiveClientFactory(ClientFactory):
    """Factory for creating inactive clients"""
    is_active = False