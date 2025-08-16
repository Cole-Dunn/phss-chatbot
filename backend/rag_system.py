"""
RAG (Retrieval-Augmented Generation) system that combines search and AI generation.
This is the core logic that makes your chatbot intelligent.
"""

import os
from openai import OpenAI
from typing import List, Dict, Tuple
from vector_store import VectorStore

class RAGSystem:
    def __init__(self):
        """Initialize RAG system with vector store and OpenAI client"""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vector_store = VectorStore()
        self.llm_model = "gpt-4o-mini"
        
        # Chatbot personality settings
        self.chatbot_name = os.getenv("CHATBOT_NAME", "Assistant")
        self.company_name = os.getenv("CHATBOT_COMPANY", "Your Company")

    def _create_system_prompt(self, relevant_docs: List[Dict], user_question: str) -> str:
        """Create the system prompt that tells GPT how to behave"""
        
        # Combine relevant documents into context
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['content']}" 
            for i, doc in enumerate(relevant_docs)
        ])
        
        return f"""You are {self.chatbot_name}, a helpful customer service assistant for {self.company_name}.

Your role is to answer questions based ONLY on the provided context documents. Here are your guidelines:

1. Always be helpful, friendly, and professional
2. Only answer questions using information from the context provided below
3. If you cannot find relevant information in the context, politely say you don't have that information
4. Keep responses concise but complete
5. If asked about topics outside your knowledge base, redirect users to contact support

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {user_question}

Please provide a helpful response based on the context above."""

    async def generate_response(self, question: str, conversation_history: List[dict] = None) -> Tuple[str, List[str]]:
        """
        Generate AI response using RAG approach.
        
        Args:
            question: User's question
            conversation_history: Previous messages (optional)
            
        Returns:
            Tuple of (response_text, source_references)
        """
        try:
            # Step 1: Search for relevant documents in the knowledge base
            relevant_docs = self.vector_store.search_similar(question, top_k=3)
            
            if not relevant_docs:
                return (
                    f"I don't have information about that in my knowledge base. "
                    f"Please contact {self.company_name} support for more help.",
                    []
                )
            
            # Step 2: Create system prompt with relevant context
            system_prompt = self._create_system_prompt(relevant_docs, question)
            
            # Step 3: Prepare conversation for OpenAI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                # Insert history before the current question
                for msg in conversation_history[-4:]:  # Keep last 4 messages for context
                    messages.insert(-1, msg)
            
            # Step 4: Call OpenAI API to generate response
            response = self.openai_client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Step 5: Extract response and create source references
            ai_response = response.choices[0].message.content
            source_references = [
                doc.get('metadata', {}).get('source', f'Document {i+1}') 
                for i, doc in enumerate(relevant_docs)
            ]
            
            return (ai_response, source_references)
            
        except Exception as e:
            return (
                f"I'm sorry, I encountered an error processing your question. "
                f"Please try again or contact {self.company_name} support.",
                []
            )

    def add_knowledge_base(self, documents: List[Dict[str, str]]):
        """Add documents to the knowledge base"""
        self.vector_store.add_documents(documents)

    def get_knowledge_stats(self):
        """Get statistics about the knowledge base"""
        return self.vector_store.get_index_stats()