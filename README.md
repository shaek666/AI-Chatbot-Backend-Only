# AI Chatbot Backend with RAG Pipeline

A comprehensive backend-only AI chatbot system with user authentication, chat history, and Retrieval-Augmented Generation (RAG) pipeline using Django REST Framework.

## Features

### Core Features
- **User Authentication**: JWT-based authentication with email verification
- **Chat History**: Persistent storage of chat sessions and messages
- **RAG Pipeline**: Integration with Pinecone for document retrieval and Gemini for response generation
- **Background Tasks**: Automated cleanup and maintenance tasks
- **RESTful API**: Complete API with documentation

### Advanced Features
- **Document Indexing**: Index and search through custom documents
- **Context-Aware Responses**: AI responses based on retrieved documents
- **Real-time Processing**: Efficient query processing with latency tracking
- **Admin Dashboard**: Comprehensive admin interface for management
- **Automated Maintenance**: Scheduled cleanup of old data

## Technology Stack

### Backend
- **Framework**: Django 4.2.7 with Django REST Framework 3.14.0
- **Database**: PostgreSQL with psycopg2-binary
- **Authentication**: JWT tokens with djangorestframework-simplejwt
- **Background Tasks**: APScheduler for task scheduling

### AI and RAG
- **AI Model**: Google Gemini 2.0 Flash
- **Vector Database**: Pinecone for document storage and retrieval
- **Embeddings**: Gemini embeddings for semantic search

### Additional Tools
- **API Documentation**: drf-spectacular with Swagger UI
- **Environment Management**: python-decouple
- **Email**: SMTP for email verification

## Project Structure
AI-Chatbot/
├── config/                 # Django project configuration
├── users/                  # User authentication and management
├── chat/                   # Chat functionality and history
├── rag/                    # RAG pipeline implementation
├── background_tasks/       # Background task scheduling
├── utils/                  # Utility functions
├── tests/                  # Test cases
├── venv/                   # Virtual environment
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md               # This file