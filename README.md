# 🗓️ Clarity Planner

A modern, full-stack appointment scheduling and client management system built with Django REST Framework and Vue.js.

## 📋 Project Overview

Clarity Planner is a comprehensive business management solution designed for service-based businesses, providing:

- **Client Management** - Complete client profiles with company associations
- **Employee Management** - Staff scheduling and service assignments
- **Appointment Scheduling** - Interactive calendar with real-time updates
- **Service Management** - Configurable services with pricing and duration
- **Real-time Communication** - WebSocket integration for live updates
- **User Authentication** - JWT-based security with role-based permissions

## 🛠️ Tech Stack

### **Backend**

- **Django 5.1.5** - Web framework
- **Django REST Framework** - API development
- **Django Channels** - WebSocket support for real-time features
- **PostgreSQL** - Production database
- **Redis** - Session storage and WebSocket channel layer
- **JWT Authentication** - Secure token-based auth

### **Frontend**

- **Vue.js 3** - Progressive JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **FullCalendar** - Interactive calendar component
- **Axios** - HTTP client for API communication
- **FontAwesome** - Icon library
- **Flowbite** - UI components

### **Development & Testing**

- **pytest** - Python testing framework
- **Factory Boy** - Test data generation
- **Coverage.py** - Code coverage reporting
- **ESLint** - JavaScript linting

## 🏗️ Architecture

```
clarity/
├── 🐍 Backend (Django)
│   ├── apps/
│   │   ├── authorize/     # User authentication & permissions
│   │   ├── clients/       # Client & company management
│   │   ├── employees/     # Staff management
│   │   ├── planning/      # Appointments & scheduling
│   │   ├── services/      # Service definitions
│   │   └── core/          # Shared utilities
│   ├── config/            # Django settings & URLs
│   └── tests/             # Comprehensive test suite
├── 🌐 Frontend (Vue.js)
│   ├── src/
│   │   ├── components/    # Reusable Vue components
│   │   ├── views/         # Page components
│   │   ├── router/        # Vue Router configuration
│   │   └── store/         # Vuex state management
└── 📄 Documentation
```

## 🚀 Local Development Setup

### **Prerequisites**

- **Python 3.9+**
- **Node.js 16+** and npm
- **PostgreSQL 13+**
- **Redis 6+** (for WebSocket support)

### **1. Clone Repository**

```bash
git clone https://github.com/codexze/clarity-planner.git
cd clarity-planner
```

### **2. Backend Setup**

#### **Create Virtual Environment**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

#### **Install Dependencies**

```bash
# Install Python packages
pip install -r requirements.txt

# Install testing dependencies (optional)
pip install -r requirements-test.txt
```

#### **Environment Configuration**

```bash
# Create environment file
cp .env.example .env.local

# Edit .env.local with your settings:
DATABASE_URL=postgresql://username:password@localhost:5432/clarity_db
SECRET_KEY=your-secret-key-here
DEBUG=True
REDIS_URL=redis://localhost:6379/0
```

#### **Database Setup**

```bash
# Create PostgreSQL database
createdb clarity_db

# Generate secure key (optional for development)
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### **3. Frontend Setup**

#### **Install Dependencies**

```bash
# Install Node.js packages
npm install
```

#### **Environment Configuration**

```bash
# Create Vue environment file
echo "VUE_APP_API_BASE_URL=http://localhost:8000/api/v1/" > .env.local
```

### **4. Start Development Servers**

#### **Terminal 1 - Backend**

```bash
# Activate virtual environment
source .venv/bin/activate

# Start Django development server
python manage.py runserver
# Backend available at: http://localhost:8000
```

#### **Terminal 2 - Frontend**

```bash
# Start Vue development server
npm run serve
# Frontend available at: http://localhost:8080
```

#### **Terminal 3 - Redis (if needed)**

```bash
# Start Redis server
redis-server
# Redis available at: localhost:6379
```

### **5. Verify Setup**

1. **Backend API**: Visit `http://localhost:8000/admin/`
2. **Frontend App**: Visit `http://localhost:8080`
3. **API Documentation**: Visit `http://localhost:8000/api/v1/`

## 🧪 Testing

### **Backend Tests**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/clients/tests.py
pytest apps/clients/test_api.py

# Run model tests only
pytest -k "test_model"

# Run API tests only
pytest -k "test_api"
```

### **Frontend Tests**

```bash
# Run Vue tests (when implemented)
npm run test

# Lint JavaScript
npm run lint
```

## 🔧 Development Commands

### **Backend**

```bash
# Create new Django app
python manage.py startapp myapp

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run tests
python manage.py test
```

### **Frontend**

```bash
# Development server
npm run serve

# Production build
npm run build

# Lint and fix files
npm run lint

# Analyze bundle size
npm run build --report
```

## 📊 Key Features

### **🏢 Client Management**

- Complete client profiles with contact information
- Company associations and hierarchies
- Client history and notes
- Advanced search and filtering

### **👥 Employee Management**

- Staff profiles with service specializations
- Role-based permissions (Manager, Employee)
- Service assignments and availability
- Employee performance tracking

### **📅 Appointment Scheduling**

- Interactive calendar interface
- Drag-and-drop appointment management
- Real-time updates via WebSockets
- Appointment conflicts prevention
- Email notifications and reminders

### **🛍️ Service Management**

- Configurable service types
- Pricing and duration management
- Service categories and descriptions
- Employee service assignments

### **🔐 Security & Authentication**

- JWT-based authentication
- Role-based access control
- Password security policies
- Session management
- API rate limiting

## 📚 API Documentation

The API follows RESTful conventions with the following endpoints:

- **Authentication**: `/api/v1/auth/`
- **Clients**: `/api/v1/clients/`
- **Companies**: `/api/v1/companies/`
- **Employees**: `/api/v1/employees/`
- **Appointments**: `/api/v1/appointments/`
- **Services**: `/api/v1/services/`

Full API documentation available at: `http://localhost:8000/api/v1/docs/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Development Guidelines**

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- Create an issue in the GitHub repository
- Check the [API Testing Guide](API_TESTING_GUIDE.md) for testing examples
- Review the [Environment Configuration](ENVIRONMENT_CONFIG.md) for setup help

## 🚧 Roadmap

- [ ] Mobile application (React Native)
- [ ] Advanced reporting and analytics
- [ ] Multi-language support
- [ ] Payment processing integration
- [ ] Advanced calendar features (recurring appointments)
- [ ] Email marketing integration
