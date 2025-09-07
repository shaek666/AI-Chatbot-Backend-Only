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
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://127.0.0.1:3000', cast=lambda v: [s.strip() for s in v.split(',')])

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



# Redis connection settings (using fakeredis for development)
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')

# Use fakeredis for development
USE_FAKE_REDIS = config('USE_FAKE_REDIS', default=True, cast=bool)

# Add this near the top of the file
AUTH_USER_MODEL = 'users.User'

# Background tasks configuration
DISABLE_BACKGROUND_TASKS = config('DISABLE_BACKGROUND_TASKS', default=False, cast=bool)

# Logging configuration
LOG_LEVEL = config('LOG_LEVEL', default='INFO')

# File upload settings
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE', default=10485760, cast=int)  # 10MB
ALLOWED_FILE_TYPES = config('ALLOWED_FILE_TYPES', default='txt,pdf,doc,docx,md', cast=lambda v: [s.strip() for s in v.split(',')])

# RAG pipeline settings
RAG_CHUNK_SIZE = config('RAG_CHUNK_SIZE', default=1000, cast=int)
RAG_MAX_DOCUMENTS = config('RAG_MAX_DOCUMENTS', default=5, cast=int)
RAG_RELEVANCE_THRESHOLD = config('RAG_RELEVANCE_THRESHOLD', default=0.7, cast=float)

# Rate limiting settings
RATE_LIMIT_REQUESTS_PER_MINUTE = config('RATE_LIMIT_REQUESTS_PER_MINUTE', default=1000, cast=int)
RATE_LIMIT_REQUESTS_PER_HOUR = config('RATE_LIMIT_REQUESTS_PER_HOUR', default=10000, cast=int)

# Cache settings
CACHE_TIMEOUT = config('CACHE_TIMEOUT', default=300, cast=int)
CACHE_KEY_PREFIX = config('CACHE_KEY_PREFIX', default='ai_chatbot')

# Feature flags
ENABLE_EMAIL_VERIFICATION = config('ENABLE_EMAIL_VERIFICATION', default=True, cast=bool)
ENABLE_PASSWORD_RESET = config('ENABLE_PASSWORD_RESET', default=True, cast=bool)
ENABLE_USER_PROFILES = config('ENABLE_USER_PROFILES', default=True, cast=bool)
ENABLE_CHAT_EXPORT = config('ENABLE_CHAT_EXPORT', default=True, cast=bool)
ENABLE_ANALYTICS = config('ENABLE_ANALYTICS', default=False, cast=bool)
ENABLE_ADMIN_PANEL = config('ENABLE_ADMIN_PANEL', default=True, cast=bool)

# Security settings for local development
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)