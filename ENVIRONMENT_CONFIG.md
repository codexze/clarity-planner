# Environment Configuration Guide

This project uses environment-specific configuration files to manage settings for different deployment environments.

## Environment Files

- `.env.local` - Development environment (used by default)
- `.env.production` - Production environment
- `.env` - Fallback environment file
- `.env.example` - Template file with all available options

## How It Works

The application automatically loads the appropriate environment file based on the `DJANGO_ENV` environment variable:

### Development (Default)

```bash
# No DJANGO_ENV set, or DJANGO_ENV=development
# Loads .env.local
python manage.py runserver
```

### Production

```bash
# Set DJANGO_ENV=production
# Loads .env.production
export DJANGO_ENV=production
python manage.py runserver
```

### Custom/Fallback

```bash
# Any other DJANGO_ENV value
# Loads .env
export DJANGO_ENV=staging
python manage.py runserver
```

## Environment Variables

| Variable               | Description          | Development Default     | Production Notes                   |
| ---------------------- | -------------------- | ----------------------- | ---------------------------------- |
| `SECRET_KEY`           | Django secret key    | Development key         | **MUST** be changed for production |
| `DEBUG`                | Debug mode           | `True`                  | Should be `False` in production    |
| `DATABASE_URL`         | Database connection  | Local PostgreSQL        | Production database URL            |
| `ALLOWED_HOSTS`        | Allowed hosts        | `localhost,127.0.0.1`   | Your production domains            |
| `CORS_ALLOWED_ORIGINS` | CORS origins         | `http://localhost:8080` | Production HTTPS URLs              |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins | `http://localhost:8080` | Production HTTPS URLs              |

## Setup Instructions

### Development Setup

1. Copy `.env.example` to `.env.local`
2. Update database credentials and other settings as needed
3. Run the application (it will use `.env.local` by default)

### Production Setup

1. Copy `.env.example` to `.env.production`
2. Update all production-specific values:
   - Generate a new `SECRET_KEY`
   - Set `DEBUG=False`
   - Configure production database URL
   - Set production domains in `ALLOWED_HOSTS`
   - Use HTTPS URLs for CORS settings
3. Set `DJANGO_ENV=production` in your deployment environment
4. Deploy the application

## Security Notes

- Never commit actual environment files (`.env*`) to version control
- Always use HTTPS in production
- Generate a strong, unique `SECRET_KEY` for production
- Keep production credentials secure and rotate them regularly
