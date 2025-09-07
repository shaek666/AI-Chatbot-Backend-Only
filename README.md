# AI Chatbot Backend with RAG Pipeline

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
- **Vector Search**: Pinecone-based semantic document search
- **JWT Security**: Access and refresh token management
- **Database**: SQLite for user data and chat history
- **Background Processing**: APScheduler for automated tasks
- **API Documentation**: Comprehensive Postman collection included

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login with JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/verify-email/` - Verify user email
- `POST /api/auth/verify-email/<str:token>/` - Verify user email with token

### Chat Operations
- `GET, POST /api/chat/sessions/` - List and create chat sessions
- `GET, PUT, PATCH, DELETE /api/chat/sessions/<int:pk>/` - Retrieve, update, and delete a chat session
- `GET, POST /api/chat/sessions/<int:session_id>/messages/` - List and send messages in a session
- `GET /api/chat/history/` - Retrieve user's chat history

### Document Management
- `GET, POST /api/chat/documents/` - List and create documents
- `POST /api/rag/index-documents/` - Index new documents
- `POST /api/rag/chat/` - Chat with RAG pipeline

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
git clone https://github.com/shaek666/AI-Chatbot-Backend-Only.git
cd AI-Chatbot-Backend-Only

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Create .env file with your configuration (see Environment Variables section below)

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Index initial documents (pre-defined FAQs, etc.)
python manage.py populate_documents

# Index your own documents from a directory
python manage.py populate_index /path/to/your/documents

# Start development server
python manage.py runserver
```

### Environment Variables

Create a `.env` file in the project root with the following configuration:

```bash
# Create .env file
touch .env  # Linux/Mac
# or
echo. > .env  # Windows

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Required Configuration:**
- **Mistral AI API Key**: Get from https://console.mistral.ai/
- **Pinecone API Key**: Get from https://app.pinecone.io/
- **Email Credentials**: For user verification (optional)

**Complete .env Configuration:**
```bash
# Django Core
SECRET_KEY=django-insecure-local-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# AI Services
MISTRAL_API_KEY=your-mistral-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment-here
PINECONE_INDEX_NAME=ai-chatbot-docs

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
USE_FAKE_REDIS=True

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Background Tasks
DISABLE_BACKGROUND_TASKS=False
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Development Settings
LOG_LEVEL=DEBUG
MAX_UPLOAD_SIZE=10485760
ALLOWED_FILE_TYPES=txt,pdf,doc,docx,md
RAG_CHUNK_SIZE=1000
RAG_MAX_DOCUMENTS=5
RAG_RELEVANCE_THRESHOLD=0.7
RATE_LIMIT_REQUESTS_PER_MINUTE=1000
RATE_LIMIT_REQUESTS_PER_HOUR=10000
CACHE_TIMEOUT=300
CACHE_KEY_PREFIX=ai_chatbot_local

# Feature Flags
ENABLE_EMAIL_VERIFICATION=True
ENABLE_PASSWORD_RESET=True
ENABLE_USER_PROFILES=True
ENABLE_CHAT_EXPORT=True
ENABLE_ANALYTICS=False
ENABLE_ADMIN_PANEL=True

# Security
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
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
POST /api/chat/sessions/1/messages/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "content": "What is machine learning?"
}
```

### Get Chat History
```http
GET /api/chat/history/
Authorization: Bearer <jwt-token>
```

## 🔄 Background Tasks

### Automated Cleanup
- **Chat History Cleanup**: Daily removal of messages older than 30 days.
- **Token Cleanup**: Daily removal of expired verification tokens.
- **Daily Activity Report**: Sends a daily report of platform activity to the admin.
- **Weekly Backup**: Performs a weekly backup of chat data.
- **Email Notifications**: User verification emails after registration.

### Task Schedule
- **Daily at 2 AM**: Clean old chat history.
- **Daily at 3 AM**: Clean expired tokens.
- **Daily at 8 AM**: Send a daily activity report.
- **Weekly on Sunday at 1 AM**: Backup chat data.
- **On registration**: Send verification email.

## 🧪 Testing

The project includes comprehensive tests covering:

- **Authentication**: User registration, login, email verification, JWT tokens
- **Chat functionality**: Session management, message handling, history retrieval
- **RAG pipeline**: Document indexing, retrieval, AI response generation
- **Background tasks**: Cleanup operations, email notifications
- **API endpoints**: All REST endpoints with proper error handling
- **Performance**: Response time and latency testing

Run tests with:

```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test tests.test_auth
python manage.py test tests.test_chat
python manage.py test tests.test_rag
python manage.py test tests.test_rag_functionality

# Run with coverage (requires pytest-cov)
pytest --cov=chat --cov=users --cov=rag --cov-report=html
```

## 📊 Database Schema

### User Model (`users.User`)
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `is_verified`: Boolean indicating if email has been verified
- `is_active`: Account status
- `created_at`: Registration timestamp

### ChatSession Model (`chat.ChatSession`)
- `id`: Session identifier
- `user`: Foreign key to User
- `title`: Session title
- `created_at`: Creation timestamp
- `updated_at`: Timestamp of the last update

### Message Model (`chat.Message`)
- `id`: Message identifier
- `session`: Foreign key to ChatSession
- `message_type`: Type of message ('user', 'bot', 'system')
- `content`: Message content
- `metadata`: JSON field for additional data
- `created_at`: Message timestamp

### Document Model (`chat.Document`)
- `id`: Document identifier
- `title`: Document title
- `content`: Document content
- `file_path`: Optional path to the original file
- `file_type`: Type of document (e.g., 'txt', 'pdf')
- `created_at`: Timestamp when document was created
- `updated_at`: Timestamp of the last update

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
- **Normalized structure** with separate User, ChatSession, and Message models
- **JSON fields** for flexible metadata storage
- **Foreign key relationships** for data integrity
- **Timestamp fields** for tracking creation and updates

This approach provides scalability, data integrity, and efficient querying capabilities.

### 3. How did you implement user authentication using JWT? What security measures did you take for handling passwords and tokens?

**JWT Implementation:**
- **Access tokens**: 60-minute lifetime for API access
- **Refresh tokens**: 7-day lifetime for session renewal
- **Token rotation**: Automatic refresh token rotation on use
- **Blacklisting**: Invalidated tokens after refresh

**Security Measures:**
- **Password hashing**: Django's built-in PBKDF2 algorithm
- **Rate limiting**: API endpoint protection against brute force attacks
- **CORS configuration**: Configurable origin policies for API access
- **Input validation**: Comprehensive request validation and sanitization
- **JWT token security**: Token rotation and blacklisting

### 4. How does the chatbot generate responses using the AI model (Mistral AI) after retrieving documents?

**Response Generation Process:**

1. **Query Embedding**: Convert user query to vector embedding
2. **Document Search**: Find top-k most relevant documents using cosine similarity
3. **Context Building**: Combine retrieved documents into context prompt
4. **AI Generation**: Use Mistral AI to generate contextual response
5. **Response Formatting**: Structure response for API consumption

The system uses Mistral AI's default generation parameters for consistent and accurate responses.

### 5. How did you schedule and implement background tasks for cleaning up old chat history, and how often do these tasks run?

**Background Task Implementation:**
- **APScheduler**: Python library for task scheduling
- **Database queries**: Efficient deletion using Django ORM
- **Error handling**: Comprehensive logging and failure recovery
- **Monitoring**: Task execution tracking and alerting

**Task Schedule:**
- **Daily at 2:00 AM UTC**: Clean messages older than 30 days
- **Daily at 3:00 AM UTC**: Clean expired verification tokens
- **Daily at 8:00 AM UTC**: Send daily activity report
- **Weekly on Sunday at 1:00 AM UTC**: Backup chat data
- **Real-time**: Email verification on user registration

### 6. What testing strategies did you use to ensure the functionality of the chatbot, authentication, and background tasks?

**Testing Strategy:**
- **Unit tests**: Individual component testing (models, views, services)
- **Integration tests**: API endpoint testing with authentication
- **End-to-end tests**: Complete user flow testing
- **Performance tests**: Response time and load testing
- **Mock tests**: External API mocking for consistent testing

**Test Coverage:**
- **Authentication flow**: Registration, login, token refresh, email verification
- **Chat functionality**: Message sending, history retrieval, session management
- **RAG pipeline**: Document retrieval, AI response generation, fallback responses
- **Background tasks**: Task scheduling and execution, cleanup operations
- **Error handling**: Edge cases and failure scenarios
- **API endpoints**: All REST endpoints with proper authentication
- **Performance**: Response time and latency testing
- **Integration tests**: Complete user flow testing

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
   - **Purpose**: Background task coordination and caching
   - **Setup**: Redis connection configuration
   - **Integration**: redis library with fakeredis for development

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
├── config/                        # Django configuration
│   ├── settings.py                # Main settings
│   ├── urls.py                    # URL routing
│   └── wsgi.py                    # WSGI application
├── users/                         # User management
│   ├── models.py                  # User models
│   ├── views.py                   # Authentication views
│   └── serializers.py             # User serialization
├── chat/                          # Chat functionality
│   ├── models.py                  # Chat and Document models
│   ├── views.py                   # Chat views
│   └── urls.py                    # Chat URL routing
├── rag/                           # RAG pipeline
│   ├── models.py                  # Empty models file
│   ├── views.py                   # RAG views
│   ├── services.py                # RAG services
│   └── urls.py                    # RAG URL routing
├── background_tasks/              # Background processing
│   ├── scheduler.py               # Task scheduling
│   └── tasks.py                   # Background tasks
├── tests/                         # Test suite
│   ├── test_auth.py               # Authentication tests
│   ├── test_chat.py               # Chat tests
│   ├── test_rag.py                # RAG tests
│   └── test_rag_functionality.py  # RAG functionality tests
├── SnapShots/                     # API Documentation Screenshots
│   ├── GET/                       # GET request screenshots
│   ├── POST/                      # POST request screenshots
│   └── jwt_token.png              # JWT authentication example
├── requirements.txt               # Python dependencies
└── README.md                      # This documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test tests.test_auth
python manage.py test tests.test_chat
python manage.py test tests.test_rag
python manage.py test tests.test_rag_functionality

# Run with coverage (requires pytest-cov)
pytest --cov=chat --cov=users --cov=rag --cov-report=html
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Check the troubleshooting guide in the documentation
- Review API documentation at `http://localhost:8000/api/docs/`
- Test API endpoints using the included Postman collection

## 📦 Postman Collection & API Documentation

A comprehensive Postman collection is included: `ai_chatbot_postman_collection.json`

Import this collection to test all API endpoints with pre-configured requests and environment variables.

### Interactive API Documentation

Visit `http://localhost:8000/api/docs/` for interactive Swagger UI documentation when the server is running.

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