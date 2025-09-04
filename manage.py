#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import redis

def check_redis_connection():
    """Check if Redis is available for background tasks."""
    try:
        r = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            password=None
        )
        result = r.ping()
        print(f"✓ Redis/Valkey connection successful: {result}")
        return True
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Check Redis connection for specific commands that need it
    if len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'shell', 'test']:
        check_redis_connection()
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()