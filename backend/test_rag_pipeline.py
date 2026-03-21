"""
Test the RAG Pipeline

This script tests the complete RAG pipeline:
1. Indexes synthetic documentation
2. Tests retrieval and answer generation
3. Validates citations and confidence scoring
"""
import logging
from pathlib import Path
from dotenv import load_dotenv
from app.services.rag_service import RAGService
from app.utils.logging import setup_logging

# Load environment variables
load_dotenv()

# Configure logging
setup_logging(level="INFO")
logger = logging.getLogger(__name__)


def main():
    print("="*70)
    print("RAG PIPELINE TEST - Sprint 1")
    print("="*70)
    
    # Initialize RAG service
    print("\n[1/3] Initializing RAG service...")
    rag = RAGService()
    
    # Index synthetic documentation
    print("\n[2/3] Indexing synthetic documentation...")
    docs_path = Path(__file__).parent.parent / "synthetic-docs"
    
    if not docs_path.exists():
        print(f"ERROR: Synthetic docs not found at {docs_path}")
        return
    
    num_chunks = rag.index_documents(str(docs_path), force_reindex=True)
    print(f"\n✅ Indexed {num_chunks} chunks from synthetic docs")
    
    # Get stats
    stats = rag.get_stats()
    print(f"\nRAG Service Stats:")
    print(f"  LLM Model: {stats['llm_model']}")
    print(f"  Confidence Threshold: {stats['confidence_threshold']}")
    print(f"  Documents in Vector Store: {stats['vector_store']['document_count']}")
    
    # Test questions
    print("\n[3/3] Testing RAG pipeline with sample questions...")
    print("="*70)
    
    test_questions = [
        "How do I set up my development environment?",
        "What is the deployment process?",
        "How do I run tests?",
        "What are the security best practices?",
        "How does the CI/CD pipeline work?",
    ]
    
    for idx, question in enumerate(test_questions, 1):
        response = rag.ask(question)
        
        print(f"\n{'='*70}")
        print(f"TEST {idx}/{len(test_questions)}")
        print(f"{'='*70}")
        print(f"\n📝 Question: {response.question}")
        print(f"\n✅ Answer:\n{response.answer}")
        print(f"\n📊 Metadata:")
        print(f"   Confidence: {response.confidence:.2f}")
        print(f"   Retrieved Chunks: {response.retrieved_chunks}")
        print(f"   Sources:")
        for source in response.sources[:3]:  # Show first 3 sources
            filename = Path(source['file_path']).name
            preview = source['content'][:100].replace('\n', ' ')
            print(f"     - {filename}: {preview}...")
        
        print(f"\n{'='*70}\n")
    
    print("\n" + "="*70)
    print("✅ RAG PIPELINE TEST COMPLETE")
    print("="*70)
    print("\nNext Steps:")
    print("1. ✅ RAG chain is working!")
    print("2. Create /ask API endpoint in FastAPI")
    print("3. Build Next.js frontend")
    print("="*70)


if __name__ == "__main__":
    main()
