"""
Base test classes and utilities for the Clarity project
"""
import pytest
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class BaseTestCase(TestCase):
    """
    Base test case with common setup and utilities
    """
    
    def setUp(self):
        super().setUp()
        self.user = self.create_test_user()
        
    def create_test_user(self, **kwargs):
        """Create a test user with default values"""
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    
    def create_test_superuser(self, **kwargs):
        """Create a test superuser"""
        defaults = {
            'username': 'admin',
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
        }
        defaults.update(kwargs)
        return User.objects.create_superuser(**defaults)


class BaseAPITestCase(APITestCase):
    """
    Base API test case with authentication utilities
    """
    
    def setUp(self):
        super().setUp()
        self.user = self.create_test_user()
        self.client = APIClient()
        
    def create_test_user(self, **kwargs):
        """Create a test user with default values"""
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com', 
            'first_name': 'Test',
            'last_name': 'User',
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    
    def authenticate_user(self, user=None):
        """Authenticate a user and return JWT token"""
        if user is None:
            user = self.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return access_token
    
    def unauthenticate(self):
        """Remove authentication credentials"""
        self.client.credentials()


class BaseTransactionTestCase(TransactionTestCase):
    """
    Base test case for tests requiring database transactions
    """
    
    def setUp(self):
        super().setUp()
        self.user = self.create_test_user()
        
    def create_test_user(self, **kwargs):
        """Create a test user with default values"""
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test', 
            'last_name': 'User',
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)


# Pytest fixtures
@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def superuser(db):
    """Create a test superuser"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def api_client():
    """Create an API client"""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Create an authenticated API client"""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client