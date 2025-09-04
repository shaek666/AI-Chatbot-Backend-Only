# test_redis.py
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
import redis

def test_redis_connection():
    """Test Redis connection using Django settings."""
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD or None
        )
        result = r.ping()
        print(f"✓ Redis connection successful: {result}")
        return True
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        return False

if __name__ == "__main__":
    test_redis_connection()