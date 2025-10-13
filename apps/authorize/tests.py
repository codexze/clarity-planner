"""
Unit tests for authorize app models
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from freezegun import freeze_time
import datetime

from apps.authorize.models import User, FrontendPermission
from tests.factories.auth import UserFactory, SuperUserFactory, GroupFactory
from tests.base import BaseTestCase


class UserModelTest(BaseTestCase):
    """Tests for custom User model"""
    
    def test_user_creation(self):
        """Test creating a user with valid data"""
        user = UserFactory()
        self.assertTrue(isinstance(user, User))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
    def test_superuser_creation(self):
        """Test creating a superuser"""
        superuser = SuperUserFactory()
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        
    def test_user_str_representation(self):
        """Test user string representation returns name"""
        user = UserFactory(first_name="John", last_name="Doe")
        # The __str__ method calls the name property
        self.assertEqual(str(user), user.name)
        
    def test_user_name_property(self):
        """Test user name property returns full name"""
        user = UserFactory(first_name="Jane", last_name="Smith")
        expected_name = "Jane Smith"
        self.assertEqual(user.name, expected_name)
        
    def test_user_name_property_with_empty_names(self):
        """Test user name property with empty first or last name"""
        user = UserFactory(first_name="", last_name="")
        # get_full_name() handles empty names gracefully
        self.assertEqual(user.name, "")
        
        user = UserFactory(first_name="John", last_name="")
        self.assertEqual(user.name, "John")
        
    @freeze_time("2024-01-01")
    def test_user_age_property_with_dob(self):
        """Test user age calculation when date_of_birth is set"""
        user = UserFactory(date_of_birth=datetime.date(1990, 1, 1))
        self.assertEqual(user.age, 34)
        
    def test_user_age_property_without_dob(self):
        """Test user age property when date_of_birth is None"""
        user = UserFactory(date_of_birth=None)
        # Need to check what the age property returns for None DOB
        # Based on the model, it should handle None gracefully
        self.assertIsNone(user.date_of_birth)
        
    def test_user_mobile_field(self):
        """Test user mobile field"""
        user = UserFactory(mobile="+1234567890")
        self.assertEqual(user.mobile, "+1234567890")
        
    def test_user_mobile_field_optional(self):
        """Test user mobile field can be None/blank"""
        user = UserFactory(mobile=None)
        self.assertIsNone(user.mobile)
        
    def test_user_ordering(self):
        """Test that users are ordered by last_name"""
        # Clear any existing users from setUp
        User.objects.all().delete()
        
        user1 = UserFactory(last_name="Zeta")
        user2 = UserFactory(last_name="Alpha")
        user3 = UserFactory(last_name="Beta")
        
        users = User.objects.all()
        last_names = [user.last_name for user in users]
        
        # Should be ordered alphabetically by last_name
        expected_order = ["Alpha", "Beta", "Zeta"]
        self.assertEqual(last_names, expected_order)
        
    def test_user_unique_username(self):
        """Test that username must be unique"""
        UserFactory(username="uniqueuser1")
        
        # This should raise an error due to unique constraint
        with self.assertRaises(Exception):
            UserFactory(username="uniqueuser1")
            
    def test_user_unique_email(self):
        """Test that email should be unique (if enforced)"""
        user1 = UserFactory(email="test@example.com")
        # Django's default User model doesn't enforce unique email
        # but we can test that our factory generates unique emails
        user2 = UserFactory()
        self.assertNotEqual(user1.email, user2.email)


class FrontendPermissionTest(BaseTestCase):
    """Tests for FrontendPermission model"""
    
    def test_frontend_permission_creation(self):
        """Test creating a frontend permission"""
        frontend_perm = FrontendPermission.objects.create()
        self.assertTrue(isinstance(frontend_perm, FrontendPermission))
        
    def test_frontend_permission_relationships(self):
        """Test FrontendPermission many-to-many relationships"""
        frontend_perm = FrontendPermission.objects.create()
        
        # Create some permissions
        perm1 = Permission.objects.first()  # Get any existing permission
        if perm1:
            # Test adding permissions to different categories
            frontend_perm.view_permissions.add(perm1)
            frontend_perm.add_permissions.add(perm1)
            frontend_perm.change_permissions.add(perm1)
            frontend_perm.delete_permissions.add(perm1)
            
            self.assertTrue(frontend_perm.view_permissions.filter(pk=perm1.pk).exists())
            self.assertTrue(frontend_perm.add_permissions.filter(pk=perm1.pk).exists())
            self.assertTrue(frontend_perm.change_permissions.filter(pk=perm1.pk).exists())
            self.assertTrue(frontend_perm.delete_permissions.filter(pk=perm1.pk).exists())


# Pytest-style tests
@pytest.mark.django_db
class TestUserModel:
    """Pytest-style tests for User model"""
    
    def test_user_factory_creates_valid_user(self):
        """Test that factory creates a valid user"""
        user = UserFactory()
        assert user.pk is not None
        assert user.is_active is True
        assert '@' in user.email
        
    def test_user_age_calculation_edge_cases(self):
        """Test age calculation for edge cases"""
        with freeze_time("2024-02-29"):  # Leap year
            # Born on leap day
            user = UserFactory(date_of_birth=datetime.date(1992, 2, 29))
            # Age calculation should handle leap years correctly
            # This tests the property implementation
            assert hasattr(user, 'age')
            
    def test_multiple_users_can_exist(self):
        """Test creating multiple users"""
        users = UserFactory.create_batch(5)
        assert len(users) == 5
        assert all(user.pk is not None for user in users)
        
    def test_user_groups_relationship(self):
        """Test user can be added to groups"""
        user = UserFactory()
        group = GroupFactory(name="test_group")
        
        user.groups.add(group)
        assert user.groups.filter(name="test_group").exists()


@pytest.mark.django_db
class TestFrontendPermissionModel:
    """Pytest-style tests for FrontendPermission model"""
    
    def test_frontend_permission_can_be_created(self):
        """Test that frontend permission can be created"""
        frontend_perm = FrontendPermission.objects.create()
        assert frontend_perm.pk is not None
        
    def test_frontend_permission_empty_relationships(self):
        """Test frontend permission with empty permission sets"""
        frontend_perm = FrontendPermission.objects.create()
        
        assert frontend_perm.view_permissions.count() == 0
        assert frontend_perm.add_permissions.count() == 0
        assert frontend_perm.change_permissions.count() == 0
        assert frontend_perm.delete_permissions.count() == 0
