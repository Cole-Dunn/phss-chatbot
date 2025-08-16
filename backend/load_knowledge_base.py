"""
Utility script to load knowledge base documents into the vector database.
Run this script whenever you add new content to your knowledge base.
"""

import os
from typing import List, Dict
from rag_system import RAGSystem
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_text_files(knowledge_base_dir: str) -> List[Dict[str, str]]:
    """Load all text files from the knowledge base directory"""
    documents = []
    
    for filename in os.listdir(knowledge_base_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(knowledge_base_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
                # Split content into sections (each section becomes a separate document)
                sections = content.split('\n\n')
                
                for i, section in enumerate(sections):
                    if section.strip():  # Skip empty sections
                        documents.append({
                            'content': section.strip(),
                            'metadata': {
                                'source': filename,
                                'section': i + 1,
                                'file_path': file_path
                            }
                        })
    
    return documents

def main():
    """Load knowledge base into vector database"""
    print("🚀 Loading knowledge base into vector database...")
    
    # Initialize RAG system
    rag_system = RAGSystem()
    
    # Load documents from knowledge_base directory
    knowledge_base_dir = os.path.join(os.path.dirname(__file__), 'knowledge_base')
    
    if not os.path.exists(knowledge_base_dir):
        print(f"❌ Knowledge base directory not found: {knowledge_base_dir}")
        return
    
    # Load text files
    documents = load_text_files(knowledge_base_dir)
    
    if not documents:
        print("❌ No documents found in knowledge base directory")
        return
    
    print(f"📚 Found {len(documents)} document sections to process...")
    
    # Add documents to vector database
    try:
        rag_system.add_knowledge_base(documents)
        print("✅ Knowledge base loaded successfully!")
        
        # Show statistics
        stats = rag_system.get_knowledge_stats()
        print(f"📊 Vector database stats: {stats}")
        
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")
        print("Make sure your API keys are set up correctly in .env file")

if __name__ == "__main__":
    main()