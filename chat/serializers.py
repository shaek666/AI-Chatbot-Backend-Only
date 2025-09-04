from rest_framework import serializers
from .models import ChatSession, Message, Document

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message_type', 'content', 'metadata', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def validate_content(self, value):
        """Validate message content"""
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty")
        return value

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'created_at', 'updated_at', 'messages', 'message_count')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_message_count(self, obj):
        return obj.messages.count()

class ChatSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ('id', 'title')  # Add 'id' field here
    
    def validate_title(self, value):
        """Validate session title"""
        if value and not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'file_path', 'file_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')