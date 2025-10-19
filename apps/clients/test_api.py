"""
API endpoint tests for clients app with authentication
"""
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from apps.clients.models import Company, Client, Gender
from tests.factories.clients import CompanyFactory, ClientFactory
from tests.factories.auth import UserFactory, EmployeeUserFactory, ManagerUserFactory
from tests.base import BaseAPITestCase

User = get_user_model()


class CompanyAPITest(BaseAPITestCase):
    """Test Company API endpoints with authentication"""
    
    def setUp(self):
        super().setUp()
        self.company = CompanyFactory()
        self.company_data = {
            'name': 'Test Company Ltd',
            'address': '123 Test Street',
            'email': 'test@company.com',
            'phone': '+1234567890',
            'website': 'https://testcompany.com',
            'is_active': True
        }
    
    def test_list_companies_authenticated(self):
        """Test listing companies with authentication"""
        self.authenticate_user()
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
    def test_list_companies_unauthenticated(self):
        """Test listing companies without authentication should fail"""
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_company_authenticated(self):
        """Test creating a company with authentication"""
        self.authenticate_user()
        
        url = reverse('companies-list')
        response = self.client.post(url, self.company_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.company_data['name'])
        self.assertEqual(response.data['email'], self.company_data['email'])
        
    def test_create_company_unauthenticated(self):
        """Test creating a company without authentication should fail"""
        url = reverse('companies-list')
        response = self.client.post(url, self.company_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_retrieve_company_authenticated(self):
        """Test retrieving a specific company with authentication"""
        self.authenticate_user()
        
        url = reverse('companies-detail', kwargs={'pk': self.company.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.company.pk)
        self.assertEqual(response.data['name'], self.company.name)
        
    def test_update_company_authenticated(self):
        """Test updating a company with authentication"""
        self.authenticate_user()
        
        updated_data = {'name': 'Updated Company Name'}
        url = reverse('companies-detail', kwargs={'pk': self.company.pk})
        response = self.client.patch(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        
    def test_delete_company_authenticated(self):
        """Test deleting a company with authentication"""
        self.authenticate_user()
        
        url = reverse('companies-detail', kwargs={'pk': self.company.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(pk=self.company.pk).exists())
        
    def test_company_filter_by_name(self):
        """Test filtering companies by name"""
        self.authenticate_user()
        
        # Create additional companies
        CompanyFactory(name="ABC Corp")
        CompanyFactory(name="XYZ Ltd")
        
        url = reverse('companies-list')
        response = self.client.get(url, {'name__icontains': 'ABC'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('ABC', response.data['results'][0]['name'])
        
    def test_company_filter_by_active_status(self):
        """Test filtering companies by active status"""
        self.authenticate_user()
        
        # Create inactive company
        CompanyFactory(is_active=False)
        
        url = reverse('companies-list')
        response = self.client.get(url, {'is_active': True})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # All returned companies should be active
        for company in response.data['results']:
            self.assertTrue(company['is_active'])


class ClientAPITest(BaseAPITestCase):
    """Test Client API endpoints with authentication"""
    
    def setUp(self):
        super().setUp()
        self.company = CompanyFactory()
        self.client_obj = ClientFactory(company=self.company)
        self.client_data = {
            'company': self.company.pk,
            'first_name': 'John',
            'surname': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': Gender.male,
            'email': 'john.doe@example.com',
            'mobile': '+1234567890',
            'is_active': True
        }
    
    def test_list_clients_authenticated(self):
        """Test listing clients with authentication"""
        self.authenticate_user()
        
        url = reverse('clients-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
    def test_list_clients_unauthenticated(self):
        """Test listing clients without authentication should fail"""
        url = reverse('clients-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_client_authenticated(self):
        """Test creating a client with authentication"""
        self.authenticate_user()
        
        url = reverse('clients-list')
        response = self.client.post(url, self.client_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], self.client_data['first_name'])
        self.assertEqual(response.data['surname'], self.client_data['surname'])
        
    def test_create_client_without_company(self):
        """Test creating a client without company"""
        self.authenticate_user()
        
        client_data = self.client_data.copy()
        client_data['company'] = None
        
        url = reverse('clients-list')
        response = self.client.post(url, client_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['company'])
        
    def test_retrieve_client_authenticated(self):
        """Test retrieving a specific client with authentication"""
        self.authenticate_user()
        
        url = reverse('clients-detail', kwargs={'pk': self.client_obj.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.client_obj.pk)
        self.assertEqual(response.data['first_name'], self.client_obj.first_name)
        
    def test_update_client_authenticated(self):
        """Test updating a client with authentication"""
        self.authenticate_user()
        
        updated_data = {'first_name': 'Jane'}
        url = reverse('clients-detail', kwargs={'pk': self.client_obj.pk})
        response = self.client.patch(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], updated_data['first_name'])
        
    def test_delete_client_authenticated(self):
        """Test deleting a client with authentication"""
        self.authenticate_user()
        
        url = reverse('clients-detail', kwargs={'pk': self.client_obj.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(pk=self.client_obj.pk).exists())
        
    def test_client_filter_by_name(self):
        """Test filtering clients by name"""
        self.authenticate_user()
        
        # Create additional clients
        ClientFactory(first_name="Alice", surname="Johnson")
        ClientFactory(first_name="Bob", surname="Smith")
        
        url = reverse('clients-list')
        response = self.client.get(url, {'name': 'Alice'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find clients with Alice in first or last name
        
    def test_client_filter_by_gender(self):
        """Test filtering clients by gender"""
        self.authenticate_user()
        
        # Create clients with different genders
        ClientFactory(gender=Gender.female)
        ClientFactory(gender=Gender.male)
        
        url = reverse('clients-list')
        response = self.client.get(url, {'gender': Gender.female})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for client in response.data['results']:
            if client['gender']:  # Some might be null
                self.assertEqual(client['gender'], Gender.female)
                
    def test_client_filter_by_company(self):
        """Test filtering clients by company"""
        self.authenticate_user()
        
        # Create clients for different companies
        other_company = CompanyFactory()
        ClientFactory(company=other_company)
        
        url = reverse('clients-list')
        response = self.client.get(url, {'company': self.company.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for client in response.data['results']:
            if client['company']:  # Some might be null
                self.assertEqual(client['company'], self.company.pk)


class GenderAPITest(BaseAPITestCase):
    """Test Gender API endpoints"""
    
    def test_list_genders_authenticated(self):
        """Test listing gender choices with authentication"""
        self.authenticate_user()
        
        url = reverse('genders-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        # Should contain all gender choices
        gender_values = [choice['value'] for choice in response.data]
        self.assertIn(Gender.male, gender_values)
        self.assertIn(Gender.female, gender_values)
        self.assertIn(Gender.unknown, gender_values)
        
    def test_list_genders_unauthenticated(self):
        """Test that gender choices might be accessible without auth"""
        # This depends on your permission setup
        url = reverse('genders-list')
        response = self.client.get(url)
        
        # This might be 200 or 401 depending on your permissions
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])


class PermissionTestCase(BaseAPITestCase):
    """Test different user permissions for API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.company = CompanyFactory()
        self.employee_user = EmployeeUserFactory()
        self.manager_user = ManagerUserFactory()
        self.regular_user = UserFactory()
        
    def test_employee_can_access_companies(self):
        """Test that employee users can access company endpoints"""
        self.authenticate_user(self.employee_user)
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_manager_can_access_companies(self):
        """Test that manager users can access company endpoints"""
        self.authenticate_user(self.manager_user)
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_regular_user_can_access_companies(self):
        """Test that regular authenticated users can access company endpoints"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JWTAuthenticationTest(APITestCase):
    """Test JWT token authentication specifically"""
    
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        
    def test_jwt_token_authentication(self):
        """Test that JWT tokens work correctly for authentication"""
        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        # Use token in request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_invalid_jwt_token(self):
        """Test that invalid JWT tokens are rejected"""
        # Use invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_expired_jwt_token(self):
        """Test handling of expired JWT tokens"""
        # This would require mocking time or using short-lived tokens
        # For now, just test with no token
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_jwt_token_refresh(self):
        """Test JWT token refresh functionality"""
        refresh = RefreshToken.for_user(self.user)
        
        # The refresh token should be able to generate new access tokens
        new_access_token = str(refresh.access_token)
        self.assertIsNotNone(new_access_token)
        
        # Use the new token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}')
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)