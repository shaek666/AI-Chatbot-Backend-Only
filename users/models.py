"""
User Management Models
=====================

This module contains the User model and EmailVerification model for handling
user authentication and email verification functionality.

Models:
- User: Custom user model extending Django's AbstractUser
- EmailVerification: Model for storing email verification tokens
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User Model
    
    Extends Django's AbstractUser to add email verification functionality.
    Uses email as the primary identifier for authentication.
    
    Fields:
        email: Unique email address (used as username)
        is_verified: Boolean indicating if email has been verified
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    """
    Email Verification Model
    
    Stores verification tokens for email verification process.
    Each user can have one verification token at a time.
    
    Fields:
        user: One-to-one relationship with User model
        token: Unique verification token
        created_at: Timestamp when token was created
        expires_at: Timestamp when token expires
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'email_verifications'
    
    def is_expired(self):
        """Check if the verification token has expired."""
        return timezone.now() > self.expires_at


class PasswordResetToken(models.Model):
    """
    Password Reset Token Model

    Stores tokens for password reset process.
    Each user can have one password reset token at a time.

    Fields:
        user: One-to-one relationship with User model
        token: Unique password reset token
        created_at: Timestamp when token was created
        expires_at: Timestamp when token expires
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'password_reset_tokens'

    def is_expired(self):
        """Check if the password reset token has expired."""
        return timezone.now() > self.expires_at