"""
Chat and Document Models
=======================

This module contains models for chat functionality and document storage.
It handles chat sessions, messages, and documents for the RAG system.

Models:
- ChatSession: Groups messages into conversations
- Message: Individual messages in chat sessions
- Document: Documents stored for RAG retrieval
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatSession(models.Model):
    """
    Chat Session Model
    
    Represents a conversation session between a user and the AI chatbot.
    Groups related messages together for better organization.
    
    Fields:
        user: Foreign key to User model
        title: Optional title for the chat session
        created_at: Timestamp when session was created
        updated_at: Timestamp when session was last updated
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']  # Most recent sessions first
    
    def __str__(self):
        return f"{self.user.email} - {self.title or 'Untitled'}"


class Message(models.Model):
    """
    Message Model
    
    Represents individual messages in chat sessions.
    Can be user messages, bot responses, or system messages.
    
    Fields:
        session: Foreign key to ChatSession
        message_type: Type of message (user/bot/system)
        content: The actual message content
        metadata: JSON field for additional data (processing time, etc.)
        created_at: Timestamp when message was created
    """
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('bot', 'Bot Message'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='user')
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)  # Store processing time, relevant docs, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']  # Chronological order
    
    def __str__(self):
        return f"{self.session.title} - {self.message_type}: {self.content[:50]}..."


class Document(models.Model):
    """
    Document Model
    
    Stores documents that are indexed in the RAG system.
    These documents are used for retrieval and context generation.
    
    Fields:
        title: Document title
        content: Document content/text
        file_path: Optional path to original file
        file_type: Type of document (txt, pdf, etc.)
        created_at: Timestamp when document was created
        updated_at: Timestamp when document was last updated
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    file_path = models.CharField(max_length=500, blank=True)
    file_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'documents'
    
    def __str__(self):
        return self.title