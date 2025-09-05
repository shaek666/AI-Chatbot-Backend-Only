"""
AI Chatbot Django Settings Configuration
=======================================

This file contains all Django settings for the AI Chatbot project.
It configures database, authentication, API keys, and other project settings.

Environment Variables:
- SECRET_KEY: Django secret key for security
- DEBUG: Enable/disable debug mode
- ALLOWED_HOSTS: List of allowed hostnames
- PINECONE_API_KEY: Pinecone vector database API key
- EMAIL_*: Email configuration for notifications
- REDIS_*: Redis configuration for background tasks
"""
import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(Path(BASE_DIR) / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing and should be kept secure
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode provides detailed error pages and should be disabled in production
DEBUG = config('DEBUG', default=True, cast=bool)

# List of allowed hostnames for the application
# In production, this should be set to your actual domain names
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local apps
    'users',
    'chat',
    'rag',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# DRF Spectacular configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'AI Chatbot API',
    'DESCRIPTION': 'API documentation for AI Chatbot',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Email settings (for verification emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# AI and RAG settings

PINECONE_API_KEY = config('PINECONE_API_KEY', default='')
PINECONE_ENVIRONMENT = config('PINECONE_ENVIRONMENT', default='')
PINECONE_INDEX_NAME = config('PINECONE_INDEX_NAME', default='ai-chatbot-docs')
MISTRAL_API_KEY = config('MISTRAL_API_KEY', default='')

# Background task settings
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

# Redis connection settings (using fakeredis for development)
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')

# Use fakeredis for development
USE_FAKE_REDIS = config('USE_FAKE_REDIS', default=True, cast=bool)

# Add this near the top of the file
AUTH_USER_MODEL = 'users.User'

# Enable background tasks for development
DISABLE_BACKGROUND_TASKS = False