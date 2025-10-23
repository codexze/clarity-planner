# 🔐 API Testing with Authentication - Complete Guide

This guide demonstrates comprehensive API endpoint testing with JWT authentication for your Django REST Framework project.

## 🎯 What We're Testing

### **Authentication Scenarios**

- ✅ **Authenticated Requests** - Valid JWT tokens
- ✅ **Unauthenticated Requests** - No token (should fail)
- ✅ **Invalid Tokens** - Malformed/expired tokens
- ✅ **Different User Types** - Employee, Manager, Regular users
- ✅ **Permission Levels** - CRUD operations by user role

### **API Endpoint Coverage**

- ✅ **CRUD Operations** - Create, Read, Update, Delete
- ✅ **List/Filter Endpoints** - Pagination, filtering, search
- ✅ **Custom Actions** - Special endpoints like `/companies/all/`
- ✅ **Validation Testing** - Invalid data handling
- ✅ **Error Responses** - 401, 403, 404, 400 status codes

## 🔧 Key Testing Patterns

### **1. Basic Authentication Test Pattern**

```python
class MyAPITest(BaseAPITestCase):
    def test_endpoint_requires_auth(self):
        """Test endpoint fails without authentication"""
        url = reverse('my-endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_endpoint_with_auth(self):
        """Test endpoint succeeds with authentication"""
        self.authenticate_user()  # Adds JWT token

        url = reverse('my-endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### **2. CRUD Testing Pattern**

```python
def test_create_resource(self):
    """Test creating a resource via API"""
    self.authenticate_user()

    data = {'name': 'Test Resource'}
    url = reverse('resources-list')
    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['name'], data['name'])

def test_update_resource(self):
    """Test updating a resource via API"""
    self.authenticate_user()
    resource = MyModelFactory()

    update_data = {'name': 'Updated Name'}
    url = reverse('resources-detail', kwargs={'pk': resource.pk})
    response = self.client.patch(url, update_data, format='json')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], update_data['name'])
```

### **3. Permission Testing Pattern**

```python
def test_different_user_permissions(self):
    """Test different user types have appropriate permissions"""

    # Test employee user
    employee = EmployeeUserFactory()
    self.authenticate_user(employee)

    url = reverse('sensitive-endpoint')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test regular user (might not have access)
    regular_user = UserFactory()
    self.authenticate_user(regular_user)

    response = self.client.get(url)
    self.assertIn(response.status_code, [
        status.HTTP_200_OK,    # If allowed
        status.HTTP_403_FORBIDDEN  # If not allowed
    ])
```

### **4. Filtering/Search Testing Pattern**

```python
def test_filter_by_field(self):
    """Test API filtering functionality"""
    self.authenticate_user()

    # Create test data
    MyModelFactory(name="ABC Company")
    MyModelFactory(name="XYZ Company")

    url = reverse('my-list-endpoint')
    response = self.client.get(url, {'name__icontains': 'ABC'})

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['results']), 1)
    self.assertIn('ABC', response.data['results'][0]['name'])
```

### **5. JWT Token Testing Pattern**

```python
def test_jwt_token_authentication(self):
    """Test JWT token handling"""
    # Generate token manually
    refresh = RefreshToken.for_user(self.user)
    access_token = str(refresh.access_token)

    # Set token in client
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('protected-endpoint')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_invalid_token_rejected(self):
    """Test invalid tokens are properly rejected"""
    self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')

    url = reverse('protected-endpoint')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

## 🚀 Running Your API Tests

### **Run All API Tests**

```bash
# Run all API tests
pytest apps/clients/test_api.py apps/employees/test_api.py -v

# Run with coverage
pytest apps/clients/test_api.py --cov=apps.clients.views

# Run specific test class
pytest apps/clients/test_api.py::CompanyAPITest -v

# Run specific test method
pytest apps/clients/test_api.py::CompanyAPITest::test_create_company_authenticated -v
```

### **Django Test Runner Alternative**

```bash
# Run API tests with Django
python manage.py test apps.clients.test_api --settings=config.settings_test

# Run specific test
python manage.py test apps.clients.test_api.CompanyAPITest.test_create_company_authenticated --settings=config.settings_test
```

## 🔍 Test Structure Overview

### **Test Classes Created:**

#### **`apps/clients/test_api.py`**

- **`CompanyAPITest`** - Complete CRUD testing for Company endpoints
- **`ClientAPITest`** - Complete CRUD testing for Client endpoints
- **`GenderAPITest`** - Testing choice field endpoints
- **`PermissionTestCase`** - Testing user role permissions
- **`JWTAuthenticationTest`** - JWT-specific authentication testing

#### **`apps/employees/test_api.py`**

- **`EmployeeAPIAuthenticationTest`** - Employee endpoint auth testing
- **`EmployeeServiceAPITest`** - Relationship endpoint testing
- **`AuthenticationMethodsTest`** - Edge cases and auth methods
- **`APIPermissionTest`** - Advanced permission testing
- **`APIValidationTest`** - Data validation testing

## 💡 Best Practices Implemented

### **1. Test Isolation**

- Each test uses fresh factory-generated data
- Tests don't depend on each other
- Database is reset between tests

### **2. Realistic Test Data**

- Factory Boy generates realistic test data
- Relationships are properly handled
- Edge cases are covered (null values, invalid data)

### **3. Comprehensive Coverage**

- All HTTP methods tested (GET, POST, PATCH, DELETE)
- Both success and failure scenarios
- Authentication and authorization separated
- Validation and error handling tested

### **4. Maintainable Code**

- Reusable base classes
- Clear test method names
- Descriptive assertions
- Proper setup/teardown

## 🛠️ Customizing for Your Endpoints

### **Add New Endpoint Tests**

```python
class MyNewAPITest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.my_model = MyModelFactory()

    def test_my_custom_endpoint(self):
        self.authenticate_user()

        url = reverse('my-custom-action')  # Adjust URL name
        response = self.client.post(url, {'param': 'value'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add specific assertions for your endpoint
```

### **Test Custom Permissions**

```python
def test_custom_permission_class(self):
    """Test your custom permission classes"""
    # Create user that should NOT have permission
    unauthorized_user = UserFactory(some_field=False)
    self.authenticate_user(unauthorized_user)

    url = reverse('restricted-endpoint')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Create user that SHOULD have permission
    authorized_user = UserFactory(some_field=True)
    self.authenticate_user(authorized_user)

    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
```

## 🎯 Next Steps

1. **Run the existing tests** to verify your API setup
2. **Add tests for remaining apps** (services, planning, etc.)
3. **Test WebSocket endpoints** (for Channels functionality)
4. **Add integration tests** for complex workflows
5. **Performance testing** for high-load scenarios

Your API testing setup is now production-ready with comprehensive authentication coverage! 🚀
