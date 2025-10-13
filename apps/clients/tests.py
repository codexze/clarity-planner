"""
Unit tests for clients app models
"""
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from freezegun import freeze_time
import datetime

from apps.clients.models import Company, Client, Gender
from tests.factories.clients import CompanyFactory, ClientFactory, ClientWithoutCompanyFactory
from tests.base import BaseTestCase


class CompanyModelTest(BaseTestCase):
    """Tests for Company model"""
    
    def test_company_creation(self):
        """Test creating a company with valid data"""
        company = CompanyFactory()
        self.assertTrue(isinstance(company, Company))
        self.assertTrue(company.is_active)
        self.assertIsNotNone(company.name)
        
    def test_company_str_representation(self):
        """Test company string representation"""
        company = CompanyFactory(name="Test Company Ltd")
        self.assertEqual(str(company), "Test Company Ltd")
        
    def test_company_optional_fields(self):
        """Test company with optional fields as None/blank"""
        company = CompanyFactory(
            address=None,
            email=None, 
            phone=None,
            website=None
        )
        self.assertIsNone(company.address)
        self.assertIsNone(company.email)
        self.assertIsNone(company.phone)
        self.assertIsNone(company.website)
        
    def test_company_deactivation(self):
        """Test company can be deactivated"""
        company = CompanyFactory()
        company.is_active = False
        company.save()
        
        company.refresh_from_db()
        self.assertFalse(company.is_active)


class ClientModelTest(BaseTestCase):
    """Tests for Client model"""
    
    def test_client_creation(self):
        """Test creating a client with valid data"""
        client = ClientFactory()
        self.assertTrue(isinstance(client, Client))
        self.assertTrue(client.is_active)
        self.assertIsNotNone(client.first_name)
        self.assertIsNotNone(client.surname)
        self.assertIsNotNone(client.date_of_birth)
        
    def test_client_without_company(self):
        """Test creating a client without a company"""
        client = ClientWithoutCompanyFactory()
        self.assertIsNone(client.company)
        
    def test_client_name_property(self):
        """Test client name property returns full name"""
        client = ClientFactory(first_name="John", surname="Doe")
        self.assertEqual(client.name, "John Doe")
        
    @freeze_time("2024-01-01")
    def test_client_age_property(self):
        """Test client age calculation"""
        # Client born on 1990-01-01, should be 34 years old on 2024-01-01
        client = ClientFactory(date_of_birth=datetime.date(1990, 1, 1))
        self.assertEqual(client.age, 34)
        
        # Client born on 1990-06-01, should be 33 years old on 2024-01-01
        client = ClientFactory(date_of_birth=datetime.date(1990, 6, 1))
        self.assertEqual(client.age, 33)
        
    def test_client_display_property(self):
        """Test client display property format"""
        with freeze_time("2024-01-01"):
            client = ClientFactory(
                first_name="Jane",
                surname="Smith", 
                date_of_birth=datetime.date(1985, 1, 1)
            )
            expected = "Jane Smith (39Y)"
            self.assertEqual(client.display, expected)
            
    def test_client_gender_choices(self):
        """Test client gender field accepts valid choices"""
        for gender_choice, _ in Gender.choices:
            client = ClientFactory(gender=gender_choice)
            self.assertEqual(client.gender, gender_choice)
            
    def test_client_cascade_delete_with_company(self):
        """Test client is deleted when company is deleted"""
        company = CompanyFactory()
        client = ClientFactory(company=company)
        
        company.delete()
        
        with self.assertRaises(Client.DoesNotExist):
            client.refresh_from_db()
            
    def test_client_deactivation(self):
        """Test client can be deactivated"""
        client = ClientFactory()
        client.is_active = False
        client.save()
        
        client.refresh_from_db()
        self.assertFalse(client.is_active)


# Pytest-style tests
@pytest.mark.django_db
class TestCompanyModel:
    """Pytest-style tests for Company model"""
    
    def test_company_factory_creates_valid_company(self):
        """Test that factory creates a valid company"""
        company = CompanyFactory()
        assert company.pk is not None
        assert company.is_active is True
        
    def test_multiple_companies_can_exist(self):
        """Test creating multiple companies"""
        companies = CompanyFactory.create_batch(5)
        assert len(companies) == 5
        assert all(company.pk is not None for company in companies)


@pytest.mark.django_db  
class TestClientModel:
    """Pytest-style tests for Client model"""
    
    def test_client_factory_creates_valid_client(self):
        """Test that factory creates a valid client"""
        client = ClientFactory()
        assert client.pk is not None
        assert client.is_active is True
        assert client.company is not None
        
    def test_client_age_calculation_edge_cases(self):
        """Test age calculation for edge cases"""
        with freeze_time("2024-02-29"):  # Leap year
            # Born on leap day
            client = ClientFactory(date_of_birth=datetime.date(1992, 2, 29))
            assert client.age == 32
            
    def test_client_email_generation(self):
        """Test that client email is generated properly"""
        client = ClientFactory(first_name="John", surname="Doe")
        assert "john.doe" in client.email.lower()
        
    def test_get_last_appointment_method(self):
        """Test the get_last_appointment method exists"""
        client = ClientFactory()
        # This method exists but needs appointments to test properly
        # We'll test this more thoroughly in integration tests
        assert hasattr(client, 'get_last_appointment')
        assert callable(getattr(client, 'get_last_appointment'))
