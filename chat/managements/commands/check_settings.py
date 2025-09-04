from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check Django settings for Redis configuration'

    def handle(self, *args, **options):
        self.stdout.write("Checking Redis settings...")
        
        # Check Redis settings
        self.stdout.write(f"REDIS_HOST: {settings.REDIS_HOST}")
        self.stdout.write(f"REDIS_PORT: {settings.REDIS_PORT}")
        self.stdout.write(f"REDIS_DB: {settings.REDIS_DB}")
        self.stdout.write(f"REDIS_PASSWORD: {'***' if settings.REDIS_PASSWORD else '(empty)'}")
        
        # Check Celery settings
        self.stdout.write(f"CELERY_BROKER_URL: {settings.CELERY_BROKER_URL}")
        self.stdout.write(f"CELERY_RESULT_BACKEND: {settings.CELERY_RESULT_BACKEND}")
        
        self.stdout.write(self.style.SUCCESS("Settings check complete"))