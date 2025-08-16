"""
Main FastAPI application for the RAG chatbot backend.
This handles incoming chat requests and returns AI-generated responses.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

from rag_system import RAGSystem

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="A RAG chatbot that answers questions based on your knowledge base",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Wix Studio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Wix domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = RAGSystem()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_history: List[dict] = []

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG Chatbot API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user messages and returns AI responses.
    """
    try:
        # Use RAG system to generate response
        response, sources = await rag_system.generate_response(
            question=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(response=response, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy", "rag_system": "initialized"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)