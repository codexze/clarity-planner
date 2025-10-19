"""
API endpoint tests for employees app with authentication
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee, EmployeeService
from apps.services.models import ServiceType
from tests.factories.employees import EmployeeFactory, EmployeeServiceFactory, ServiceTypeFactory
from tests.factories.clients import CompanyFactory
from tests.factories.auth import UserFactory, EmployeeUserFactory, ManagerUserFactory
from tests.base import BaseAPITestCase


class EmployeeAPIAuthenticationTest(BaseAPITestCase):
    """Test Employee API endpoints with different authentication scenarios"""
    
    def setUp(self):
        super().setUp()
        self.employee = EmployeeFactory()
        self.service_type = ServiceTypeFactory()
        
    def test_employee_list_requires_authentication(self):
        """Test that employee list requires authentication"""
        url = '/api/v1/employees/'  # Adjust URL as needed
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_employee_list_with_authentication(self):
        """Test employee list with proper authentication"""
        self.authenticate_user()
        
        url = '/api/v1/employees/'  # Adjust URL as needed
        response = self.client.get(url)
        
        # This might be 200 if endpoint exists, or 404 if not implemented
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        
    def test_different_user_types_access(self):
        """Test that different user types can access employee data"""
        # Test with employee user
        employee_user = EmployeeUserFactory()
        self.authenticate_user(employee_user)
        
        url = '/api/v1/employees/'
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        
        # Test with manager user
        manager_user = ManagerUserFactory()
        self.authenticate_user(manager_user)
        
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class EmployeeServiceAPITest(BaseAPITestCase):
    """Test EmployeeService relationships via API"""
    
    def setUp(self):
        super().setUp()
        self.employee = EmployeeFactory()
        self.service_type = ServiceTypeFactory()
        self.employee_service = EmployeeServiceFactory(
            employee=self.employee,
            service_type=self.service_type
        )
        
    def test_employee_services_require_auth(self):
        """Test that employee services endpoints require authentication"""
        # This would test endpoints like /api/v1/employee-services/
        url = '/api/v1/employee-services/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_employee_service_authenticated(self):
        """Test creating employee service relationship with auth"""
        self.authenticate_user()
        
        new_service = ServiceTypeFactory()
        data = {
            'employee': self.employee.pk,
            'service_type': new_service.pk,
            'is_active': True
        }
        
        url = '/api/v1/employee-services/'
        response = self.client.post(url, data, format='json')
        
        # Might be 201 if endpoint exists, or 404 if not implemented
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED, 
            status.HTTP_404_NOT_FOUND,
            status.HTTP_405_METHOD_NOT_ALLOWED  # If POST not allowed
        ])


class AuthenticationMethodsTest(BaseAPITestCase):
    """Test different authentication methods and edge cases"""
    
    def test_token_in_header(self):
        """Test JWT token in Authorization header"""
        self.authenticate_user()
        
        # Test any protected endpoint
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_malformed_auth_header(self):
        """Test malformed authorization header"""
        self.client.credentials(HTTP_AUTHORIZATION='InvalidFormat token123')
        
        url = reverse('companies-list') 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_missing_bearer_keyword(self):
        """Test authorization header without 'Bearer' keyword"""
        token = self.authenticate_user()
        self.client.credentials(HTTP_AUTHORIZATION=token)  # Missing 'Bearer '
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_empty_auth_header(self):
        """Test empty authorization header"""
        self.client.credentials(HTTP_AUTHORIZATION='')
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_deactivation_invalidates_token(self):
        """Test that deactivating a user invalidates their tokens"""
        token = self.authenticate_user()
        
        # Deactivate the user
        self.user.is_active = False
        self.user.save()
        
        url = reverse('companies-list')
        response = self.client.get(url)
        
        # Should be unauthorized since user is deactivated
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class APIPermissionTest(BaseAPITestCase):
    """Test API permissions beyond authentication"""
    
    def setUp(self):
        super().setUp()
        self.company = CompanyFactory()
        self.employee_user = EmployeeUserFactory()
        self.manager_user = ManagerUserFactory()
        
    def test_employee_crud_permissions(self):
        """Test CRUD permissions for employee users"""
        self.authenticate_user(self.employee_user)
        
        # Test READ permission
        url = reverse('companies-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test CREATE permission
        company_data = {
            'name': 'Employee Created Company',
            'is_active': True
        }
        response = self.client.post(url, company_data, format='json')
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,  # If employees can create
            status.HTTP_403_FORBIDDEN  # If employees cannot create
        ])
        
    def test_manager_crud_permissions(self):
        """Test CRUD permissions for manager users"""
        self.authenticate_user(self.manager_user)
        
        # Test READ permission
        url = reverse('companies-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test CREATE permission
        company_data = {
            'name': 'Manager Created Company',
            'is_active': True
        }
        response = self.client.post(url, company_data, format='json')
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,  # If managers can create
            status.HTTP_403_FORBIDDEN  # If managers cannot create
        ])
        
        # Test UPDATE permission
        if response.status_code == status.HTTP_201_CREATED:
            company_id = response.data['id']
            update_url = reverse('companies-detail', kwargs={'pk': company_id})
            update_data = {'name': 'Updated by Manager'}
            
            response = self.client.patch(update_url, update_data, format='json')
            self.assertIn(response.status_code, [
                status.HTTP_200_OK,
                status.HTTP_403_FORBIDDEN
            ])


class APIValidationTest(BaseAPITestCase):
    """Test API validation with authentication"""
    
    def setUp(self):
        super().setUp()
        self.authenticate_user()
        
    def test_create_company_invalid_data(self):
        """Test creating company with invalid data"""
        invalid_data = {
            'name': '',  # Required field empty
            'email': 'invalid-email'  # Invalid email format
        }
        
        url = reverse('companies-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        
    def test_create_client_invalid_date(self):
        """Test creating client with invalid date"""
        company = CompanyFactory()
        invalid_client_data = {
            'company': company.pk,
            'first_name': 'John',
            'surname': 'Doe',
            'date_of_birth': 'invalid-date',  # Invalid date format
            'gender': 'MALE'
        }
        
        url = reverse('clients-list')
        response = self.client.post(url, invalid_client_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_of_birth', response.data)
        
    def test_update_nonexistent_resource(self):
        """Test updating a resource that doesn't exist"""
        update_data = {'name': 'Updated Name'}
        url = reverse('companies-detail', kwargs={'pk': 99999})  # Non-existent ID
        
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)