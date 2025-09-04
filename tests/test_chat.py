from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import ChatSession, Message
import json

User = get_user_model()

class ChatTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.is_active = True
        self.user.is_verified = True
        self.user.save()
        
        # Login and get token
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_chat_session(self):
        """Test creating a chat session"""
        data = {'title': 'Test Session'}
        response = self.client.post('/api/chat/sessions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Session')
    
    def test_send_message(self):
        """Test sending a message"""
        # Create session first
        data = {'title': 'Test Session'}
        response = self.client.post('/api/chat/sessions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        session_id = response.data['id']
        
        # Send message
        data = {'content': 'Hello, how are you?'}
        response = self.client.post(f'/api/chat/sessions/{session_id}/messages/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Hello, how are you?')
        self.assertEqual(response.data['message_type'], 'user')
    
    def test_chat_history(self):
        """Test retrieving chat history"""
        # Create session and messages
        session = ChatSession.objects.create(user=self.user, title='Test Session')
        Message.objects.create(session=session, message_type='user', content='Hello')
        Message.objects.create(session=session, message_type='bot', content='Hi there!')
        
        response = self.client.get('/api/chat/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sessions', response.data)
        self.assertIn('recent_messages', response.data)
        self.assertEqual(len(response.data['sessions']), 1)