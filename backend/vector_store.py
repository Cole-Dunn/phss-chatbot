"""
Vector database operations using Pinecone.
This handles storing and searching through your knowledge base.
"""

import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from typing import List, Dict, Tuple
import hashlib

class VectorStore:
    def __init__(self):
        """Initialize Pinecone vector database and OpenAI client"""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize Pinecone (new API)
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        self.index_name = "chatbot-knowledge-base"
        self.embedding_model = "text-embedding-ada-002"
        
        # Create index if it doesn't exist
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)

    def _ensure_index_exists(self):
        """Create Pinecone index if it doesn't exist"""
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI ada-002 embedding dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"  # Free tier region
                )
            )

    def _create_embedding(self, text: str) -> List[float]:
        """Convert text to vector embedding using OpenAI"""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add documents to the vector database.
        
        Args:
            documents: List of dicts with 'content' and 'metadata' keys
        """
        vectors_to_upsert = []
        
        for doc in documents:
            content = doc['content']
            metadata = doc.get('metadata', {})
            
            # Create unique ID for document
            doc_id = hashlib.md5(content.encode()).hexdigest()
            
            # Create embedding
            embedding = self._create_embedding(content)
            
            # Prepare vector for upsert
            vectors_to_upsert.append({
                'id': doc_id,
                'values': embedding,
                'metadata': {
                    'content': content,
                    **metadata
                }
            })
        
        # Upsert vectors to Pinecone
        self.index.upsert(vectors=vectors_to_upsert)

    def search_similar(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for similar documents based on query.
        
        Args:
            query: User's question
            top_k: Number of similar documents to return
            
        Returns:
            List of relevant documents with metadata
        """
        # Create embedding for query
        query_embedding = self._create_embedding(query)
        
        # Search in Pinecone
        search_response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extract relevant documents
        relevant_docs = []
        for match in search_response['matches']:
            relevant_docs.append({
                'content': match['metadata']['content'],
                'score': match['score'],
                'metadata': {k: v for k, v in match['metadata'].items() if k != 'content'}
            })
        
        return relevant_docs

    def get_index_stats(self):
        """Get statistics about the vector database"""
        return self.index.describe_index_stats()