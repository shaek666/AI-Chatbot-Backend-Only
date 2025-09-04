from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
import django
import os
import redis
import logging

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from .tasks import (
    cleanup_old_chat_history,
    cleanup_expired_verification_tokens,
    send_daily_activity_report,
    backup_chat_data
)

# Set up logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.WARNING)

def check_redis_connection():
    """Check if Redis is available for background tasks."""
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD or None
        )
        r.ping()
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False

def start_scheduler():
    """Start the background task scheduler with Redis connection check."""
    scheduler = BackgroundScheduler()
    
    # Check Redis connection before starting
    if check_redis_connection():
        print("✓ Redis connection established. Background tasks will work properly.")
    else:
        print("⚠ Background tasks scheduler started but Redis is not available.")
        print("  Tasks will be scheduled but may fail to execute properly.")
    
    # Schedule cleanup tasks
    scheduler.add_job(
        cleanup_old_chat_history,
        trigger=CronTrigger(hour=2, minute=0),  # Run at 2 AM daily
        id='cleanup_old_chat_history',
        name='Clean up old chat history',
        replace_existing=True
    )
    
    scheduler.add_job(
        cleanup_expired_verification_tokens,
        trigger=CronTrigger(hour=3, minute=0),  # Run at 3 AM daily
        id='cleanup_expired_verification_tokens',
        name='Clean up expired verification tokens',
        replace_existing=True
    )
    
    # Schedule daily report
    scheduler.add_job(
        send_daily_activity_report,
        trigger=CronTrigger(hour=8, minute=0),  # Run at 8 AM daily
        id='send_daily_activity_report',
        name='Send daily activity report',
        replace_existing=True
    )
    
    # Schedule backup (weekly)
    scheduler.add_job(
        backup_chat_data,
        trigger=CronTrigger(day_of_week='sun', hour=1, minute=0),  # Run at 1 AM on Sunday
        id='backup_chat_data',
        name='Backup chat data',
        replace_existing=True
    )
    
    scheduler.start()
    print("Background scheduler started successfully")
    
    return scheduler

# Global scheduler instance
try:
    scheduler = start_scheduler()
except Exception as e:
    print(f"⚠ Error starting background scheduler: {e}")
    scheduler = None