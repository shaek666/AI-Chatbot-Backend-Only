#!/usr/bin/env python
"""
Postman Collection Generator for AI Chatbot API
Generates a Postman collection JSON file for API documentation.
Run this script from the root directory: python postman_collection.py
"""

import json
import os
from datetime import datetime

def generate_postman_collection():
    """Generate Postman collection for the AI Chatbot API"""
    
    collection = {
        "info": {
            "name": "AI Chatbot Backend API",
            "description": "Complete API documentation for the AI Chatbot with RAG Pipeline, User Authentication, and Chat History",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{jwt_token}}",
                    "type": "string"
                }
            ]
        },
        "variable": [
            {
                "key": "BASE_URL",
                "value": "http://localhost:8000",
                "type": "string"
            },
            {
                "key": "jwt_token",
                "value": "",
                "type": "string"
            }
        ],
        "item": [
            {
                "name": "Authentication",
                "item": [
                    {
                        "name": "User Registration",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "username": "testuser",
                                    "email": "test@example.com",
                                    "password": "password123",
                                    "password_confirm": "password123",
                                    "first_name": "Test",
                                    "last_name": "User"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/auth/register/"
                            },
                            "description": "Register a new user account. User will be created as inactive until email verification."
                        },
                        "response": [
                            {
                                "name": "Success",
                                "originalRequest": {},
                                "status": "Created",
                                "code": 201,
                                "_postman_previewlanguage": "json",
                                "header": [
                                    {"key": "Content-Type", "value": "application/json"}
                                ],
                                "body": {
                                    "message": "User registered successfully. Please check your email for verification.",
                                    "user": {
                                        "id": 1,
                                        "username": "testuser",
                                        "email": "test@example.com",
                                        "first_name": "Test",
                                        "last_name": "User",
                                        "is_verified": False,
                                        "created_at": "2025-09-03T22:00:40.994338Z"
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "name": "User Login",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "email": "test@example.com",
                                    "password": "password123"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/auth/login/"
                            },
                            "description": "Login with email and password to receive JWT access and refresh tokens."
                        },
                        "response": [
                            {
                                "name": "Success",
                                "originalRequest": {},
                                "status": "OK",
                                "code": 200,
                                "_postman_previewlanguage": "json",
                                "header": [
                                    {"key": "Content-Type", "value": "application/json"}
                                ],
                                "body": {
                                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                    "user": {
                                        "id": 1,
                                        "username": "testuser",
                                        "email": "test@example.com",
                                        "first_name": "Test",
                                        "last_name": "User",
                                        "is_verified": True,
                                        "created_at": "2025-09-03T22:00:40.994338Z"
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "name": "Email Verification",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "token": "verification_token_here"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/auth/verify-email/"
                            },
                            "description": "Verify user email using the token sent to the user's email address."
                        }
                    }
                ]
            },
            {
                "name": "Chat Management",
                "item": [
                    {
                        "name": "Create Chat Session",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{jwt_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "title": "New Chat Session"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/chat/sessions/"
                            },
                            "description": "Create a new chat session for the authenticated user."
                        }
                    },
                    {
                        "name": "Get Chat History",
                        "request": {
                            "method": "GET",
                            "header": [
                                {"key": "Authorization", "value": "Bearer {{jwt_token}}"}
                            ],
                            "url": {
                                "raw": "{{BASE_URL}}/api/chat/history/"
                            },
                            "description": "Retrieve chat history for the authenticated user including all sessions and recent messages."
                        }
                    },
                    {
                        "name": "Send Message to Session",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{jwt_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "content": "Hello, how are you?"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/chat/sessions/1/messages/"
                            },
                            "description": "Send a message to a specific chat session."
                        }
                    }
                ]
            },
            {
                "name": "RAG Pipeline",
                "item": [
                    {
                        "name": "Index Documents",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{jwt_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "documents": [
                                        {
                                            "title": "AI Overview",
                                            "content": "Artificial Intelligence is a field of computer science focused on creating intelligent machines.",
                                            "metadata": {"category": "AI"}
                                        },
                                        {
                                            "title": "Machine Learning",
                                            "content": "Machine Learning is a subset of AI that enables systems to learn and improve from experience.",
                                            "metadata": {"category": "ML"}
                                        }
                                    ]
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/rag/index-documents/"
                            },
                            "description": "Index documents for retrieval in the RAG pipeline."
                        }
                    },
                    {
                        "name": "Chat with RAG",
                        "request": {
                            "method": "POST",
                            "header": [
                                {"key": "Content-Type", "value": "application/json"},
                                {"key": "Authorization", "value": "Bearer {{jwt_token}}"}
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "message": "What is Artificial Intelligence?",
                                    "session_id": None
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{BASE_URL}}/api/rag/chat/"
                            },
                            "description": "Send a message to the chatbot. The RAG pipeline will retrieve relevant documents and generate an AI response."
                        },
                        "response": [
                            {
                                "name": "Success with RAG",
                                "originalRequest": {},
                                "status": "OK",
                                "code": 200,
                                "_postman_previewlanguage": "json",
                                "header": [
                                    {"key": "Content-Type", "value": "application/json"}
                                ],
                                "body": {
                                    "session_id": 1,
                                    "user_message": {
                                        "id": 1,
                                        "message_type": "user",
                                        "content": "What is Artificial Intelligence?",
                                        "created_at": "2025-09-03T22:04:23.463702Z"
                                    },
                                    "bot_response": {
                                        "id": 2,
                                        "message_type": "bot",
                                        "content": "Artificial Intelligence is a field of computer science...",
                                        "metadata": {
                                            "context_used": True,
                                            "processing_time": 1.83,
                                            "relevant_docs_count": 1
                                        },
                                        "created_at": "2025-09-03T22:04:27.443309Z"
                                    },
                                    "relevant_documents": [
                                        {
                                            "id": "doc_1",
                                            "score": 0.85,
                                            "title": "AI Overview",
                                            "content": "Artificial Intelligence is a field of computer science..."
                                        }
                                    ],
                                    "processing_time": 1.83
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Save the collection to a JSON file
    output_file = "ai_chatbot_postman_collection.json"
    
    with open(output_file, 'w') as f:
        json.dump(collection, f, indent=2)
    
    print(f"✅ Postman collection generated: {output_file}")
    print(f"📁 File location: {os.path.abspath(output_file)}")
    print("🚀 Import this file into Postman to test the API")
    
    return output_file

if __name__ == "__main__":
    generate_postman_collection()