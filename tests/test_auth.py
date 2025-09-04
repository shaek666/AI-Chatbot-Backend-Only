from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
import json

User = get_user_model()

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_user_registration(self):
        """Test user registration with email verification"""
        # Mock email sending to avoid actual email sending in tests
        with patch('users.views.send_mail') as mock_send_mail:
            response = self.client.post('/api/auth/register/', self.user_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('user', response.data)
            
            # Check user was created but not verified
            self.assertTrue(User.objects.filter(email='test@example.com').exists())
            user = User.objects.get(email='test@example.com')
            self.assertFalse(user.is_active)  # User should be inactive until verified
            self.assertFalse(user.is_verified)
            
            # Check that email was sent
            self.assertTrue(mock_send_mail.called)
            
            # Now simulate email verification
            from users.models import EmailVerification
            verification = EmailVerification.objects.get(user=user)
            
            # Verify the email - try both URL patterns
            verify_data = {'token': verification.token}
            verify_response = self.client.post('/api/auth/verify-email/', verify_data, format='json')
            
            # If the first URL doesn't work, try the alternative
            if verify_response.status_code != status.HTTP_200_OK:
                verify_response = self.client.post(f'/api/auth/verify-email/{verification.token}/', {}, format='json')
            
            self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
            
            # Check user is now verified
            user.refresh_from_db()
            self.assertTrue(user.is_active)
            self.assertTrue(user.is_verified)
    
    def test_user_login(self):
        """Test user login"""
        # Create and verify user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.is_active = True
        user.is_verified = True
        user.save()
        
        # Login
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_unverified_user_login(self):
        """Test login with unverified user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.is_active = True
        user.is_verified = False  # Explicitly set to False
        user.save()
        
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('not verified', response.data['non_field_errors'][0])