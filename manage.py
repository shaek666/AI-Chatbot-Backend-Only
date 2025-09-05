#!/usr/bin/env python
"""
AI Chatbot Django Management Script
===================================

This is Django's command-line utility for administrative tasks.
It sets up the Django environment and executes management commands.

Usage:
    python manage.py runserver    # Start development server
    python manage.py migrate      # Run database migrations
    python manage.py test         # Run test suite
    python manage.py populate_documents  # Add predefined documents
"""
import os
import sys

def main():
    """
    Main entry point for Django management commands.
    
    Sets up the Django environment and executes the requested command.
    """
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the management command
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()