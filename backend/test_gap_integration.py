"""
Integration test for Gap Logging with RAG Service

Tests that low-confidence questions are automatically logged to the database.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.database import Base
from app.models.gap import DocumentationGap, GapStatus
from app.services.rag_service import RAGService
from app.services.gap_service import GapService


@pytest.fixture
def test_db():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


@pytest.fixture
def rag_service(test_db):
    """Create a RAG service instance with test database."""
    service = RAGService()
    # Replace the gap_service with one using test database
    service.gap_service = GapService(db=test_db)
    return service, test_db


def test_gap_logged_on_low_confidence(rag_service):
    """Test that gaps are logged when confidence is below threshold."""
    service, test_db = rag_service
    
    # Ask a question that should have low confidence (irrelevant to docs)
    question = "What is the weather like today?"
    
    response = service.ask(question)
    
    # Verify fallback response was returned
    assert "I can only answer questions" in response.answer
    assert response.confidence < 0.70
    
    # Verify gap was logged
    gaps = test_db.query(DocumentationGap).all()
    assert len(gaps) == 1
    
    gap = gaps[0]
    assert gap.question == question
    assert gap.confidence_score < 0.70
    assert gap.frequency == 1
    assert gap.status == GapStatus.NEW
    assert len(gap.retrieval_context) > 0  # Should have retrieval chunks


def test_gap_frequency_incremented(rag_service):
    """Test that asking the same low-confidence question increments frequency."""
    service, test_db = rag_service
    
    question = "What is the capital of France?"
    
    # Ask same question 3 times
    service.ask(question)
    service.ask(question)
    service.ask(question)
    
    # Verify only one gap entry exists
    gaps = test_db.query(DocumentationGap).all()
    assert len(gaps) == 1
    
    # Verify frequency is 3
    gap = gaps[0]
    assert gap.frequency == 3
    assert gap.question == question


def test_no_gap_logged_for_high_confidence(rag_service):
    """Test that gaps are NOT logged when confidence is above threshold."""
    service, test_db = rag_service
    
    # Ask a question that should have high confidence (relevant to docs)
    question = "How do I set up the database?"
    
    response = service.ask(question)
    
    # Should get a real answer (if docs are indexed)
    # Note: This test assumes synthetic-docs are indexed
    
    # Check if confidence is high enough
    if response.confidence >= 0.70:
        # Verify NO gap was logged
        gaps = test_db.query(DocumentationGap).all()
        assert len(gaps) == 0
    else:
        # If confidence was low, gap should be logged
        gaps = test_db.query(DocumentationGap).all()
        assert len(gaps) == 1


def test_gap_retrieval_context_structure(rag_service):
    """Test that retrieval context is stored with correct structure."""
    service, test_db = rag_service
    
    question = "Tell me about quantum physics?"
    
    service.ask(question)
    
    gaps = test_db.query(DocumentationGap).all()
    assert len(gaps) == 1
    
    gap = gaps[0]
    
    # Verify retrieval_context structure
    assert isinstance(gap.retrieval_context, list)
    
    if len(gap.retrieval_context) > 0:
        chunk = gap.retrieval_context[0]
        
        # Should have these keys
        assert "content" in chunk
        assert "source" in chunk
        assert "distance" in chunk
        
        # Content should be truncated to 200 chars
        assert len(chunk["content"]) <= 200


def test_multiple_different_gaps(rag_service):
    """Test that different low-confidence questions create separate gaps."""
    service, test_db = rag_service
    
    questions = [
        "What is the weather?",
        "Who won the World Cup?",
        "What is the stock price of Apple?",
    ]
    
    for question in questions:
        service.ask(question)
    
    gaps = test_db.query(DocumentationGap).all()
    assert len(gaps) == 3
    
    # Verify all questions are different
    logged_questions = {g.question for g in gaps}
    assert logged_questions == set(questions)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
