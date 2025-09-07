# AI Chatbot Backend with RAG Pipeline

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/your-username/ai-chatbot-backend)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](https://github.com/your-username/ai-chatbot-backend)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)

A backend-only AI chatbot service implementing Retrieval-Augmented Generation (RAG) for intelligent responses, JWT-based user authentication, persistent chat history, and automated background tasks for system maintenance.

## 🚀 Features

### Core Functionality
- **User Authentication**: JWT-based secure registration and login
- **Chat History**: Persistent storage of all user messages and AI responses
- **RAG Pipeline**: Intelligent response generation using document retrieval + AI
- **Background Tasks**: Automated cleanup of old chat history and email notifications
- **REST API**: Complete API for frontend integration

### Technical Features
- **RAG Implementation**: Document retrieval integrated with Mistral AI
- **Vector Search**: Pinecon-based semantic document search
- **JWT Security**: Access and refresh token management
- **Database**: SQLite for user data and chat history
- **Background Processing**: APScheduler for automated tasks
- **API Documentation**: Comprehensive Postman collection included

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login with JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token

### Chat Operations
- `GET /api/chat/history/` - Retrieve user's chat history
- `POST /api/chat/sessions/` - Create new chat session
- `POST /api/chat/messages/` - Send message to chatbot
- `DELETE /api/chat/sessions/{id}/` - Delete chat session

### Document Management
- `GET /api/rag/search/` - Search documents
- `POST /api/rag/index/` - Index new documents

## 🛠️ Tech Stack

- **Backend**: Django REST Framework
- **Database**: SQLite
- **AI Model**: Mistral AI for response generation and embeddings.
- **Vector DB**: Pinecone for document embeddings
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Background Tasks**: APScheduler
- **Testing**: Django Test Framework + pytest

## 🏗️ System Architecture

```
                    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
                    │   User Client   │────│   API Gateway   │────│   Auth Service  │
                    │   (Frontend)    │    │   (Django)      │    │   (JWT)         │
                    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                                    │
                                           ┌─────────────────┐
                                           │   Chat Service  │
                                           │   (RAG Pipeline)│
                                           └─────────────────┘
                                                    │
                                           ┌─────────────────┐
                                           │   Document      │
                                           │   Retrieval     │
                                           │   (Pinecone)    │
                                           └─────────────────┘
```

## 🚦 Quick Start

### Prerequisites
- Python 3.8+

- SQLite3

- Redis (optional, for caching)

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/ai-chatbot-backend.git
cd ai-chatbot-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Create and configure .env file

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Index initial documents
python manage.py populate_documents

# Start development server
python manage.py runserver
```

### Environment Variables

```bash
# Required
SECRET_KEY=your-secret-key
MISTRAL_API_KEY=your-mistral-api-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=your-pinecone-env

# Database (SQLite is used by default)
DATABASE_URL=sqlite:///db.sqlite3

# Optional
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

## 📖 API Documentation

### User Registration
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### User Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Send Chat Message
```http
POST /api/chat/messages/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "session_id": 1,
  "message": "What is machine learning?"
}
```

### Get Chat History
```http
GET /api/chat/history/
Authorization: Bearer <jwt-token>
```

## 🔄 Background Tasks

### Automated Cleanup
- **Chat History Cleanup**: Daily removal of messages older than 30 days
- **Token Cleanup**: Daily removal of expired verification tokens
- **Email Notifications**: User verification emails after registration

### Task Schedule
- **Daily at 2 AM**: Clean old chat history
- **Daily at 3 AM**: Clean expired tokens
- **On registration**: Send verification email

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test tests.test_auth
python manage.py test tests.test_chat
python manage.py test tests.test_rag

# Run with coverage
pytest --cov=chat --cov=users --cov=rag
```

## 📊 Database Schema

### User Model
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `is_active`: Account status
- `created_at`: Registration timestamp

### ChatSession Model
- `id`: Session identifier
- `user`: Foreign key to User
- `title`: Session title
- `created_at`: Creation timestamp

### ChatMessage Model
- `id`: Message identifier
- `session`: Foreign key to ChatSession
- `content`: Message content
- `sender`: User or AI
- `timestamp`: Message timestamp

### Document Model
- `id`: Document identifier
- `title`: Document title
- `content`: Document content
- `embedding`: Vector embedding
- `metadata`: Additional document info

## 🎯 Answers to README Questions

### 1. How did you integrate the RAG pipeline for the chatbot, and what role does document retrieval play in the response generation?

The RAG pipeline integrates document retrieval with AI generation through these steps:

1. **Document Storage**: Documents are chunked and stored with vector embeddings in Pinecone
2. **Query Processing**: User queries are converted to embeddings using Mistral AI's embedding model.
3. **Document Retrieval**: Semantic search finds the most relevant documents based on query similarity
4. **Context Assembly**: Retrieved documents provide relevant context for response generation
5. **AI Generation**: Mistral AI generates contextual responses using the retrieved information.

This approach ensures responses are grounded in accurate, relevant information while maintaining natural conversation flow.

### 2. What database and model structure did you use for storing user and chat history, and why did you choose this approach?

**Database Structure:**
- **SQLite**: Primary database for user data and chat history
- **Pinecone**: Vector database for document embeddings and semantic search
- **Redis**: Optional caching layer for session management

**Model Design:**
- **Normalized structure** with separate User, ChatSession, and ChatMessage models
- **Indexed fields** for fast query performance
- **Soft deletes** to preserve data integrity
- **JSON fields** for flexible metadata storage

This approach provides scalability, data integrity, and efficient querying capabilities.

### 3. How did you implement user authentication using JWT? What security measures did you take for handling passwords and tokens?

**JWT Implementation:**
- **Access tokens**: 15-minute lifetime for API access
- **Refresh tokens**: 7-day lifetime for session renewal
- **Token rotation**: Automatic refresh token rotation on use
- **Blacklisting**: Invalidated tokens after refresh

**Security Measures:**
- **Password hashing**: Django's built-in PBKDF2 algorithm
- **HTTPS enforcement**: All endpoints require HTTPS in production
- **Rate limiting**: API endpoint protection against brute force attacks
- **CORS configuration**: Strict origin policies for API access
- **Input validation**: Comprehensive request validation and sanitization

### 4. How does the chatbot generate responses using the AI model (GPT-3) after retrieving documents?

**Response Generation Process:**

1. **Query Embedding**: Convert user query to vector embedding
2. **Document Search**: Find top-k most relevant documents using cosine similarity
3. **Context Building**: Combine retrieved documents into context prompt
4. **AI Generation**: Use Mistral AI to generate contextual response
5. **Response Formatting**: Structure response for API consumption

The system uses a temperature-controlled generation approach to balance creativity with accuracy.

### 5. How did you schedule and implement background tasks for cleaning up old chat history, and how often do these tasks run?

**Background Task Implementation:**
- **APScheduler**: Python library for task scheduling
- **Database queries**: Efficient deletion using Django ORM
- **Error handling**: Comprehensive logging and failure recovery
- **Monitoring**: Task execution tracking and alerting

**Task Schedule:**
- **Daily at 2:00 AM UTC**: Clean messages older than 30 days
- **Daily at 3:00 AM UTC**: Clean expired verification tokens
- **Real-time**: Email verification on user registration

### 6. What testing strategies did you use to ensure the functionality of the chatbot, authentication, and background tasks?

**Testing Strategy:**
- **Unit tests**: Individual component testing (models, views, services)
- **Integration tests**: API endpoint testing with authentication
- **End-to-end tests**: Complete user flow testing
- **Performance tests**: Response time and load testing
- **Mock tests**: External API mocking for consistent testing

**Test Coverage:**
- **Authentication flow**: Registration, login, token refresh
- **Chat functionality**: Message sending, history retrieval
- **RAG pipeline**: Document retrieval, AI response generation
- **Background tasks**: Task scheduling and execution
- **Error handling**: Edge cases and failure scenarios

### 7. What external services (APIs, databases, search engines) did you integrate, and how did you set up and configure them?

**External Services:**

1. **Mistral AI**
   - **Purpose**: Provider for text embeddings and response generation
   - **Setup**: API key configuration in environment variables (MISTRAL_API_KEY)
   - **Integration**: use the Mistral SDK or HTTP client

2. **Pinecone**
   - **Purpose**: Vector database for document search
   - **Setup**: API key and environment configuration
   - **Integration**: pinecone-client library

3. **SQLite**
   - **Purpose**: Primary data storage
   - **Setup**: Default Django configuration
   - **Integration**: Django ORM

4. **Redis** (optional)
   - **Purpose**: Session caching and background task queue
   - **Setup**: Redis URL configuration
   - **Integration**: django-redis library

### 8. How would you expand this chatbot to support more advanced features, such as real-time knowledge base updates or multi-user chat sessions?

**Future Enhancements:**

1. **Real-time Updates**
   - **WebSocket integration**: Live document updates and notifications
   - **File upload API**: Automatic document indexing and embedding
   - **Version control**: Track document changes and updates

2. **Multi-user Features**
   - **Shared chat sessions**: Collaborative conversations
   - **Role-based access**: Different permission levels for users
   - **Real-time presence**: User activity indicators

3. **Advanced RAG**
   - **Multi-modal support**: Image and PDF processing
   - **Semantic search improvements**: Advanced embedding models
   - **Knowledge graphs**: Relationship mapping between documents

4. **Analytics & Monitoring**
   - **Usage analytics**: User interaction patterns
   - **Response quality metrics**: AI response evaluation
   - **Performance monitoring**: API response times and error rates

## 📁 Project Structure

```
ai-chatbot-backend/
├── config/                 # Django configuration
│   ├── settings.py         # Main settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI application
├── users/                  # User management
│   ├── models.py           # User models
│   ├── views.py            # Authentication views
│   └── serializers.py      # User serialization
├── chat/                   # Chat functionality
│   ├── models.py           # Chat models
│   ├── views.py            # Chat views
│   └── services.py         # Chat services
├── rag/                    # RAG pipeline
│   ├── models.py           # Document models
│   ├── views.py            # RAG views
│   └── services.py         # RAG services
├── background_tasks/       # Background processing
│   ├── scheduler.py        # Task scheduling
│   └── tasks.py            # Background tasks
├── tests/                  # Test suite
│   ├── test_auth.py        # Authentication tests
│   ├── test_chat.py        # Chat tests
│   └── test_rag.py         # RAG tests
├── SnapShots/              # API Documentation Screenshots
│   ├── GET/                # GET request screenshots
│   ├── POST/               # POST request screenshots
│   └── jwt_token.png       # JWT authentication example
├── requirements.txt        # Python dependencies
└── README.md               # This documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue on [GitHub Issues](https://github.com/your-username/ai-chatbot-backend/issues)
- Check the troubleshooting guide in the documentation
- Review API documentation at `http://localhost:8000/api/docs/`

## 📦 Postman Collection & API Documentation

A comprehensive Postman collection is included: `ai_chatbot_postman_collection.json`

Import this collection to test all API endpoints with pre-configured requests and environment variables.

### 📸 API Documentation Screenshots

The `SnapShots/` folder contains detailed screenshots demonstrating key API endpoints and their responses:

#### 🔍 GET Requests
- **Get Chat History** - Shows retrieval of user's complete chat history
- **Send Message to Session** - Displays GET request for session messages

#### 📮 POST Requests
- **User Registration** - Demonstrates new user signup process
- **User Login** - Shows JWT token generation and authentication
- **Email Verification** - Displays email verification flow
- **Create Chat Session** - Shows new chat session creation
- **Send Message to Session** - Demonstrates sending messages to specific sessions
- **Chat with RAG** - Shows RAG-powered intelligent response generation
- **Index Documents** - Displays document indexing for knowledge base updates

#### 🔐 Authentication
- **JWT Token** - Shows JWT token structure and usage in requests

### 🎯 Key API Demonstrations

**GET Request - Chat History Retrieval:**
![GET Chat History](SnapShots/GET/GET%20Get%20Chat%20History.png)

**POST Request - RAG Chat with AI:**
![POST RAG Chat](SnapShots/POST/POST%20Chat%20with%20Rag.png)

These screenshots provide visual documentation of:
- Request structure and headers
- JSON payloads and parameters
- Successful response formats
- Error handling examples
- Authentication token usage