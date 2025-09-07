from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q
from .models import ChatSession, Message, Document
from .serializers import (
    ChatSessionSerializer,
    ChatSessionCreateSerializer,
    MessageSerializer,
    DocumentSerializer
)
from rag.services import get_rag_service

class ChatSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatSessionCreateSerializer
        return ChatSessionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save(user=self.request.user)
        
        # Return the full session data with ID
        return Response(
            ChatSessionSerializer(session).data, 
            status=status.HTTP_201_CREATED
        )

class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        return Message.objects.filter(session_id=session_id, session__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        session_id = self.kwargs.get('session_id')
        try:
            session = ChatSession.objects.get(id=session_id, user=self.request.user)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Chat session not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Set the session and message type, then save
        user_message = serializer.save(session=session, message_type='user')

        # Generate AI response if RAG service is available
        rag_service = get_rag_service()
        if rag_service:
            try:
                ai_response_content = rag_service.process_query(user_message.content)['response']
                Message.objects.create(
                    session=session,
                    message_type='bot',
                    content=ai_response_content
                )
            except Exception as e:
                ai_response_content = f"Error generating AI response: {str(e)}"
                Message.objects.create(
                    session=session,
                    message_type='bot',
                    content=ai_response_content
                )
        else:
            ai_response_content = "I'm sorry, the AI service is currently unavailable." # Fallback message
            Message.objects.create(
                session=session,
                message_type='bot',
                content=ai_response_content
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChatHistoryView(generics.ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Get recent messages across all sessions
        recent_messages = Message.objects.filter(
            session__user=request.user
        ).order_by('-created_at')[:10]
        
        return Response({
            'sessions': serializer.data,
            'recent_messages': MessageSerializer(recent_messages, many=True).data,
            'total_sessions': queryset.count(),
            'total_messages': Message.objects.filter(session__user=request.user).count()
        })

class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]