from django.core.management.base import BaseCommand
from chat.models import Document
from rag.services import get_rag_service

class Command(BaseCommand):
    help = 'Populate database with predefined documents and FAQs for RAG system'

    def handle(self, *args, **options):
        documents = [
            {
                'title': 'AI Chatbot FAQ',
                'content': '''
                Q: What is an AI Chatbot?
                A: An AI chatbot is a computer program that uses artificial intelligence to simulate human conversation. It can understand user queries and provide relevant responses.

                Q: How does the RAG system work?
                A: RAG (Retrieval-Augmented Generation) combines document retrieval with AI generation. It first searches through relevant documents, then uses that information to generate more accurate and contextual responses.

                Q: What is the difference between traditional chatbots and AI chatbots?
                A: Traditional chatbots follow predefined rules and patterns, while AI chatbots use machine learning to understand context and provide more natural, intelligent responses.

                Q: How secure is the chat system?
                A: The system uses JWT authentication, encrypted passwords, and secure API endpoints. All user data is protected and chat history is automatically cleaned up after 30 days.

                Q: Can I upload my own documents?
                A: Yes, you can upload documents through the API. The system will index them and use them for future responses in the RAG pipeline.
                '''
            },
            {
                'title': 'API Documentation Guide',
                'content': '''
                API Endpoints:
                1. POST /api/auth/register/ - Register a new user
                2. POST /api/auth/login/ - Login and get JWT token
                3. GET /api/chat/history/ - Get chat history
                4. POST /api/chat/sessions/ - Create new chat session
                5. POST /api/chat/sessions/{id}/messages/ - Send message
                6. GET /api/chat/sessions/{id}/messages/ - Get session messages

                Authentication:
                - Use JWT tokens in Authorization header: "Bearer <token>"
                - Tokens expire after 60 minutes
                - Use refresh endpoint to get new tokens

                Error Handling:
                - 400: Bad Request (invalid data)
                - 401: Unauthorized (invalid/missing token)
                - 404: Not Found (resource doesn't exist)
                - 500: Internal Server Error
                '''
            },
            {
                'title': 'Technical Architecture',
                'content': '''
                System Components:
                1. Django REST Framework - Backend API
                2. SQLite Database - Data storage
                3. Mistral AI - Response generation
                4. Pinecone - Vector database for document search
                5. Redis/Fakeredis - Background task queue
                6. APScheduler - Task scheduling

                RAG Pipeline:
                1. User sends query
                2. System searches Pinecone for relevant documents
                3. Retrieved documents are combined with user query
                4. Mistral AI generates response using context
                5. Response is returned to user

                Background Tasks:
                - Daily cleanup of old chat history (30+ days)
                - Daily cleanup of expired verification tokens
                - Daily activity reports
                - Weekly data backups
                '''
            },
            {
                'title': 'User Guide',
                'content': '''
                Getting Started:
                1. Register an account using email and password
                2. Login to get your authentication token
                3. Create a new chat session
                4. Start sending messages to the AI chatbot

                Features:
                - Persistent chat history across sessions
                - Intelligent responses using RAG technology
                - Document search and retrieval
                - Secure user authentication
                - Automatic cleanup of old data

                Best Practices:
                - Keep your authentication tokens secure
                - Use descriptive session titles
                - Ask specific questions for better responses
                - The system learns from your interactions
                '''
            },
            {
                'title': 'Troubleshooting Guide',
                'content': '''
                Common Issues:
                1. "Token expired" - Login again to get a new token
                2. "Unauthorized" - Check your authentication header
                3. "AI service unavailable" - Check API key configuration
                4. "Document not found" - Upload documents first

                Performance Tips:
                - Keep messages concise for faster responses
                - Use specific keywords for better document retrieval
                - The system improves with more data

                Support:
                - Check API documentation at /api/docs/
                - Review error messages for specific issues
                - Ensure all environment variables are set correctly
                '''
            }
        ]

        # Clear existing documents
        Document.objects.all().delete()
        self.stdout.write('Cleared existing documents')

        # Create new documents
        created_count = 0
        for doc_data in documents:
            document = Document.objects.create(
                title=doc_data['title'],
                content=doc_data['content'].strip()
            )
            created_count += 1
            self.stdout.write(f'Created document: {document.title}')

        # Add documents to RAG system
        rag_service = get_rag_service()
        if rag_service:
            for document in Document.objects.all():
                success = rag_service.add_document(
                    doc_id=f"doc_{document.id}",
                    title=document.title,
                    content=document.content,
                    metadata={'source': 'predefined', 'category': 'faq'}
                )
                if success:
                    self.stdout.write(f'Added to RAG: {document.title}')
                else:
                    self.stdout.write(f'Failed to add to RAG: {document.title}')
        else:
            self.stdout.write('RAG service not available - documents not indexed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} documents')
        )
