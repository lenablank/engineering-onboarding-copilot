"""Test enhanced confidence detection - Sprint 2 Task #1"""
from dotenv import load_dotenv
load_dotenv()

from app.services.rag_service import RAGService

print("=== Testing Enhanced Confidence Detection ===\n")

# Initialize RAG service
print("Initializing RAG service...")
rag = RAGService(confidence_threshold=0.4)  # Lower threshold for testing

# Get stats
stats = rag.get_stats()
print(f"✓ RAG Service initialized")
print(f"  - Confidence threshold: {stats['confidence_threshold']}")
print(f"  - Retrieval top-K: {stats['retrieval_top_k']}")
print(f"  - Min context words: {rag.MIN_CONTEXT_WORDS}")
print(f"  - Min sources: {rag.MIN_SOURCES}")
print(f"  - Min similarity: {rag.MIN_SIMILARITY_SCORE}")

# Index documents
print("\nIndexing documents...")
docs_dir = "../synthetic-docs"
num_chunks = rag.index_documents(docs_dir)
print(f"✓ Indexed {num_chunks} chunks")

# Test questions with different confidence levels
test_questions = [
    "How do I set up PostgreSQL?",  # Should have good confidence (documented)
    "What is the CI/CD pipeline process?",  # Should have good confidence
    "What's the weather today?",  # Should have low confidence (not documented)
    "How do I configure monitoring?"  # May have medium confidence
]

print("\n=== Testing Confidence Calculation ===\n")
for question in test_questions:
    print(f"Question: {question}")
    response = rag.ask(question)
    print(f"Confidence: {response.confidence:.2f}")
    print(f"Sources: {response.retrieved_chunks} chunks from {len(response.sources)} docs")
    print(f"Answer: {response.answer[:100]}...")
    print()

print("✓ Enhanced confidence detection test complete!")

rag.close()
