# rag/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from chat.models import ChatSession, Message
from chat.serializers import MessageSerializer
from .services import get_rag_service
import time

class ChatBotView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        session_id = request.data.get('session_id')
        
        if not user_message:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create chat session
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(
                user=request.user,
                title=user_message[:50] + ('...' if len(user_message) > 50 else '')
            )
        
        # Save user message
        user_message_obj = Message.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # Process with RAG pipeline (mock response if no API keys)
        start_time = time.time()
        
        # Check if we have API keys for real processing
        if hasattr(settings, 'MISTRAL_API_KEY') and settings.MISTRAL_API_KEY and hasattr(settings, 'PINECONE_API_KEY') and settings.PINECONE_API_KEY:
            rag_service = get_rag_service()
            if rag_service:
                rag_result = rag_service.process_query(user_message)
            else:
                # Fallback if RAG service is not available
                bot_response = f"This is a mock response to: {user_message}. RAG service not initialized."
                relevant_documents = []
                context_used = False
                processing_time = time.time() - start_time
                # Skip saving bot response and return early if service is not available
                return Response({
                    'session_id': session.id,
                    'user_message': MessageSerializer(user_message_obj).data,
                    'bot_response': MessageSerializer({'content': bot_response}).data,
                    'relevant_documents': relevant_documents,
                    'processing_time': processing_time
                })
            bot_response = rag_result['response']
            relevant_documents = rag_result['relevant_documents']
            context_used = rag_result['context_used']
        else:
            # Mock response for testing without API keys
            bot_response = f"This is a mock response to: {user_message}. In production, this would use the RAG pipeline with Mistral and Pinecone."
            relevant_documents = []
            context_used = False
        
        processing_time = time.time() - start_time
        
        # Save bot response
        bot_message_obj = Message.objects.create(
            session=session,
            message_type='bot',
            content=bot_response,
            metadata={
                'processing_time': processing_time,
                'relevant_docs_count': len(relevant_documents),
                'context_used': context_used
            }
        )
        
        return Response({
            'session_id': session.id,
            'user_message': MessageSerializer(user_message_obj).data,
            'bot_response': MessageSerializer(bot_message_obj).data,
            'relevant_documents': relevant_documents,
            'processing_time': processing_time
        })

class DocumentIndexView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        documents = request.data.get('documents', [])
        
        if not documents:
            return Response(
                {'error': 'Documents are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if we have API keys for real processing
        if hasattr(settings, 'PINECONE_API_KEY') and settings.PINECONE_API_KEY:
            rag_service = get_rag_service()
            indexed_count = 0
            if rag_service:
                for doc in documents:
                    doc_id = doc.get('id') or f"doc_{int(time.time())}_{indexed_count}"
                    title = doc.get('title', '')
                    content = doc.get('content', '')
                    
                    if title and content:
                        success = rag_service.add_document(
                            doc_id=doc_id,
                            title=title,
                            content=content,
                            metadata=doc.get('metadata', {})
                        )
                        if success:
                            indexed_count += 1
        else:
            # Mock indexing for testing without API keys
            indexed_count = len(documents)
        
        return Response({
            'message': f'Successfully indexed {indexed_count} documents',
            'indexed_count': indexed_count
        })