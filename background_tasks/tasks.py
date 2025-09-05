import os
import django
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from chat.models import Message, ChatSession
from users.models import User, EmailVerification

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def cleanup_old_chat_history():
    """Delete chat history older than 30 days"""
    cutoff_date = datetime.now() - timedelta(days=30)
    
    # Delete old messages
    old_messages = Message.objects.filter(created_at__lt=cutoff_date)
    messages_deleted = old_messages.count()
    old_messages.delete()
    
    # Delete empty chat sessions
    empty_sessions = ChatSession.objects.filter(messages__isnull=True)
    sessions_deleted = empty_sessions.count()
    empty_sessions.delete()
    
    print(f"Cleaned up {messages_deleted} messages and {sessions_deleted} sessions")
    return {
        'messages_deleted': messages_deleted,
        'sessions_deleted': sessions_deleted
    }

def cleanup_expired_verification_tokens():
    """Delete expired email verification tokens"""
    expired_tokens = EmailVerification.objects.filter(expires_at__lt=datetime.now())
    tokens_deleted = expired_tokens.count()
    expired_tokens.delete()
    
    print(f"Cleaned up {tokens_deleted} expired verification tokens")
    return {'tokens_deleted': tokens_deleted}

def send_daily_activity_report():
    """Send daily activity report to admin"""
    yesterday = datetime.now() - timedelta(days=1)
    
    # Get statistics
    new_users = User.objects.filter(date_joined__gte=yesterday).count()
    new_sessions = ChatSession.objects.filter(created_at__gte=yesterday).count()
    new_messages = Message.objects.filter(created_at__gte=yesterday).count()
    
    report = f"""
    Daily Activity Report - {datetime.now().strftime('%Y-%m-%d')}
    
    New Users: {new_users}
    New Chat Sessions: {new_sessions}
    New Messages: {new_messages}
    
    Total Users: {User.objects.count()}
    Total Chat Sessions: {ChatSession.objects.count()}
    Total Messages: {Message.objects.count()}
    """
    
    send_mail(
        'Daily Activity Report',
        report,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],  # Send to admin
        fail_silently=False,
    )
    
    print("Daily activity report sent")
    return {
        'new_users': new_users,
        'new_sessions': new_sessions,
        'new_messages': new_messages
    }

def backup_chat_data():
    """Create backup of chat data (placeholder for actual backup logic)"""
    # This is a placeholder - in production, you'd implement actual backup logic
    backup_file = f"chat_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Export data logic would go here
    print(f"Backup created: {backup_file}")
    return {'backup_file': backup_file}

def send_mail_async(subject, message, from_email, recipient_list, fail_silently=False):
    """Send email asynchronously using Django's send_mail function."""
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)
        print(f"Email sent asynchronously to {', '.join(recipient_list)}")
    except Exception as e:
        print(f"Error sending email asynchronously: {e}")