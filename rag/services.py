import os
import google.generativeai as genai
import pinecone
from django.conf import settings
from typing import List, Dict, Any
import json

class RAGService:
    def __init__(self):
        # Initialize Google Gemini
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.gemini_available = True
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            self.gemini_available = False
        
        # Initialize Pinecone with new API
        try:
            self.pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Get or create index
            self.index_name = settings.PINECONE_INDEX_NAME
            existing_indexes = self.pc.list_indexes().names()
            
            if self.index_name not in existing_indexes:
                # Create index with correct dimensions for Gemini
                self.pc.create_index(
                    name=self.index_name,
                    dimension=3072,  # Gemini embedding dimension
                    metric='cosine',
                    spec=pinecone.ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
            
            self.index = self.pc.Index(self.index_name)
            self.pinecone_available = True
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            self.pinecone_available = False
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using Gemini"""
        if not self.gemini_available:
            return []
        
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document",
                title="Embedding of single string"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []
    
    def add_document(self, doc_id: str, title: str, content: str, metadata: Dict[str, Any] = None):
        """Add document to vector database"""
        if not self.pinecone_available:
            return False
        
        embedding = self.get_embedding(content)
        if not embedding:
            return False
        
        metadata = metadata or {}
        metadata.update({
            'title': title,
            'content': content,
            'doc_id': doc_id
        })
        
        try:
            self.index.upsert(
                vectors=[(doc_id, embedding, metadata)]
            )
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        if not self.pinecone_available:
            return []
        
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
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
    
    def generate_response(self, query: str, context: str = "") -> str:
        """Generate response using Gemini"""
        if not self.gemini_available:
            return "I apologize, but the AI service is not available at the moment."
        
        try:
            if context:
                prompt = f"""Based on the following context, please answer the user's question. 
                If the context doesn't contain relevant information, please provide a helpful general response.
                
                Context:
                {context}
                
                User Question:
                {query}
                
                Please provide a comprehensive and helpful response."""
            else:
                prompt = f"""Please answer the following question to the best of your ability:
                
                {query}
                
                Please provide a helpful and informative response."""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again later."
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process user query with RAG pipeline"""
        # Search for relevant documents
        relevant_docs = self.search_documents(query)
        
        # Prepare context from relevant documents
        context = ""
        if relevant_docs:
            context_parts = []
            for doc in relevant_docs:
                if doc['score'] > 0.7:  # Relevance threshold
                    context_parts.append(f"Document: {doc['title']}\nContent: {doc['content']}")
            context = "\n\n".join(context_parts)
        
        # Generate response
        response = self.generate_response(query, context)
        
        return {
            'response': response,
            'relevant_documents': relevant_docs,
            'context_used': bool(context)
        }

# Initialize the service only if we have the required API keys
if hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY and hasattr(settings, 'PINECONE_API_KEY') and settings.PINECONE_API_KEY:
    try:
        rag_service = RAGService()
    except Exception as e:
        print(f"Error initializing RAG service: {e}")
        rag_service = None
else:
    print("Google API key or Pinecone API key not found. RAG service will not be available.")
    rag_service = None