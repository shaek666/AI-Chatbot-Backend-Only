"""
RAG (Retrieval-Augmented Generation) Service
===========================================

This module implements the RAG pipeline that combines document retrieval
with AI response generation using Mistral AI for embeddings and generation,
and Pinecone for vector storage and retrieval.

The RAG pipeline:
1. Convert user query to embedding using Mistral AI
2. Search similar documents in Pinecone vector database
3. Retrieve relevant documents
4. Generate AI response using retrieved context
5. Return response with relevant documents

Dependencies:
- mistralai: For embeddings and response generation
- pinecone-client: For vector database operations
"""
import os

import pinecone
from django.conf import settings
from typing import List, Dict, Any
import json
import time
from mistralai.client import MistralClient
from mistralai.exceptions import MistralAPIStatusException



class RAGService:
    MAX_RETRIES = 5
    BASE_DELAY = 2  # seconds

    def __init__(self):
        """Initialize RAG service with Mistral and Pinecone connections."""


        # Initialize Mistral AI for response generation
        try:
            self.mistral_client = MistralClient(api_key=settings.MISTRAL_API_KEY)
            self.mistral_model = "mistral-large-latest" # Or another suitable Mistral model
            self.mistral_available = True
        except Exception as e:
            print(f"Error initializing Mistral AI: {e}")
            self.mistral_available = False
        
        # Initialize Pinecone vector database for document storage and retrieval
        try:
            self.pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Get or create index for document storage
            self.index_name = settings.PINECONE_INDEX_NAME
            existing_indexes = self.pc.list_indexes().names()
            
            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1024,  # Updated to match Mistral embeddings
                    metric='cosine'
                )
            else:
                # Check if existing index has correct dimension
                try:
                    index_stats = self.pc.describe_index(self.index_name)
                    if index_stats.dimension != 1024:
                        # Delete and recreate with correct dimension for testing
                        self.pc.delete_index(self.index_name)
                        time.sleep(2)  # Wait for deletion
                        self.pc.create_index(
                            name=self.index_name,
                            dimension=1024,
                            metric='cosine'
                        )
                        time.sleep(2)  # Wait for creation
                except Exception as e:
                    print(f"Error checking index dimension: {e}")
            
            self.index = self.pc.Index(self.index_name)
            self.pinecone_available = True
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            self.pinecone_available = False
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text.
        
        Args:
            text: Input text to convert to embedding
            
        Returns:
            List of floats representing the text embedding
        """
        if not self.mistral_available:
            print("Error: No AI service available for embedding.")
            return []
        
        retries = 0
        delay = self.BASE_DELAY
        
        while retries < self.MAX_RETRIES:
            try:
                embedding_response = self.mistral_client.embeddings(model="mistral-embed", input=[text])
                embedding = embedding_response.data[0].embedding
                return embedding
            except MistralAPIStatusException as e:
                # Check if it's a rate limit error (429)
                status_code = getattr(e, 'status_code', None) or getattr(e, 'code', None)
                if status_code == 429:
                    retries += 1
                    if retries < self.MAX_RETRIES:
                        print(f"Mistral embedding rate limit exceeded. Retrying in {delay} seconds... (attempt {retries}/{self.MAX_RETRIES})")
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                    else:
                        print(f"Mistral embedding failed after {self.MAX_RETRIES} retries: {e}")
                        return []
                else:
                    print(f"Mistral embedding error: {e}")
                    return []
            except Exception as e:
                print(f"Mistral embedding error: {e}")
                return []
    
    def add_document(self, doc_id: str, title: str, content: str, metadata: Dict[str, Any] = None):
        """
        Add document to vector database
        
        Args:
            doc_id: Unique identifier for the document
            title: Document title
            content: Document content/text
            metadata: Additional metadata for the document
            
        Returns:
            Boolean indicating success/failure
        """
        if not self.pinecone_available:
            return False
        
        # Generate embedding for document content
        embedding = self.get_embedding(content)
        if not embedding:
            return False
        
        # Prepare metadata
        metadata = metadata or {}
        metadata.update({
            'title': title,
            'content': content,
            'doc_id': doc_id
        })
        
        try:
            # Store document in Pinecone vector database
            self.index.upsert(
                vectors=[(doc_id, embedding, metadata)]
            )
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with metadata
        """
        if not self.pinecone_available:
            return []
        
        # Generate embedding for search query
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        try:
            # Search for similar documents in vector database
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            documents = []
            for match in results['matches']:
                documents.append({
                    'id': match['id'],
                    'score': match['score'],
                    'title': match['metadata'].get('title', ''),
                    'content': match['metadata'].get('content', ''),
                    'metadata': match['metadata']
                })
            
            return documents
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def generate_response(self, query, context):
        """
        Generate response using Mistral AI
        
        Args:
            query: User's question
            context: Retrieved document context
            
        Returns:
            Generated response text
        """
        if not self.mistral_available:
            return "I apologize, but no AI service is available at the moment."

        retries = 0
        delay = self.BASE_DELAY
        
        while retries < self.MAX_RETRIES:
            try:
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Use the provided context to answer questions accurately."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}\n\nPlease provide a helpful and accurate response based on the given context."}
                ]
                
                chat_response = self.mistral_client.chat(model=self.mistral_model, messages=messages)
                response = chat_response.choices[0].message.content
                return response
            except MistralAPIStatusException as e:
                # Check if it's a rate limit error (429)
                status_code = getattr(e, 'status_code', None) or getattr(e, 'code', None)
                if status_code == 429:
                    retries += 1
                    if retries < self.MAX_RETRIES:
                        print(f"Mistral chat rate limit exceeded. Retrying in {delay} seconds... (attempt {retries}/{self.MAX_RETRIES})")
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                    else:
                        print(f"Mistral chat failed after {self.MAX_RETRIES} retries: {e}")
                        return "I apologize, but I'm having trouble generating a response at the moment due to high demand."
                else:
                    print(f"Mistral chat error: {e}")
                    return "I apologize, but I'm having trouble generating a response at the moment."
            except Exception as e:
                print(f"Mistral chat error: {e}")
                return "I apologize, but I'm having trouble generating a response at this time."
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process user query with complete RAG pipeline
        
        Args:
            query: User's question
            
        Returns:
            Dictionary containing response, relevant documents, and context usage
        """
        # Step 1: Search for relevant documents
        relevant_docs = self.search_documents(query)
        
        # Step 2: Prepare context from relevant documents
        context = ""
        if relevant_docs:
            context_parts = []
            for doc in relevant_docs:
                if doc['score'] > 0.7:  # Relevance threshold
                    context_parts.append(f"Document: {doc['title']}\nContent: {doc['content']}")
            context = "\n\n".join(context_parts)
        
        # Step 3: Generate AI response
        response = self.generate_response(query, context)
        
        return {
            'response': response,
            'relevant_documents': relevant_docs,
            'context_used': bool(context)
        }


rag_service_instance = None

def get_rag_service():
    """Return singleton RAGService instance if Mistral + Pinecone configured."""
    global rag_service_instance
    if rag_service_instance is None:
        pinecone_api_key = getattr(settings, 'PINECONE_API_KEY', None)
        mistral_api_key = getattr(settings, 'MISTRAL_API_KEY', None)

        if mistral_api_key and pinecone_api_key:
            try:
                rag_service_instance = RAGService()
            except Exception as e:
                print(f"Error initializing RAGService: {e}")
                rag_service_instance = None
        else:
            print("RAG service not available. Missing MISTRAL_API_KEY or PINECONE_API_KEY.")
            rag_service_instance = None
    return rag_service_instance