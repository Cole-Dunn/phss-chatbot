# RAG Chatbot for Wix Studio

A custom RAG (Retrieval-Augmented Generation) chatbot that integrates with Wix Studio websites.

## What This Project Does

This chatbot will:
1. **Store your knowledge base** in a vector database (Pinecone)
2. **Search through your content** when users ask questions
3. **Generate intelligent responses** using OpenAI's GPT model
4. **Integrate seamlessly** with your Wix Studio website

## Project Structure

```
chatbot-project/
├── backend/              # Python API server
│   ├── main.py          # FastAPI application
│   ├── rag_system.py    # RAG logic (search + generate)
│   ├── vector_store.py  # Vector database operations
│   └── knowledge_base/  # Your content files
├── frontend/            # Wix integration files
│   ├── chatbot.html    # Chat widget HTML
│   ├── chatbot.js      # Chat functionality
│   └── chatbot.css     # Styling
├── requirements.txt     # Python dependencies
└── .env                # API keys (keep secret!)
```

## Quick Start

1. **Set up your environment** (Python, API keys)
2. **Add your knowledge base** (documents, FAQs, etc.)
3. **Run the backend server**
4. **Embed the chat widget** in your Wix Studio site

## Technologies Used

- **Python + FastAPI**: Backend API server
- **Pinecone**: Vector database for knowledge storage
- **OpenAI GPT-4o-mini**: AI language model
- **HTML/CSS/JavaScript**: Frontend chat widget
- **Wix Studio**: Website integration

## Learning Goals

Through this project, you'll learn:
- How RAG systems work (search + AI generation)
- Vector databases and semantic search
- API development with Python
- Frontend-backend communication
- Wix Studio custom integrations
- basics of using a terminal
