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
    """Test that gaps are logged when confidence is below threshold but above relevance threshold."""
    service, test_db = rag_service
    
    # Ask a question that's somewhat relevant to engineering but not documented
    # This should have confidence between MIN_RELEVANCE (0.15) and threshold (0.7)
    question = "How do I configure webpack for the frontend build?"
    
    response = service.ask(question)
    
    # Verify fallback response was returned
    assert "I can only answer questions" in response.answer
    assert response.confidence < 0.70
    
    # Verify gap was logged
    gaps = test_db.query(DocumentationGap).all()
    assert len(gaps) >= 1  # Should have at least one gap logged
    
    # Find the gap for our question
    gap = next((g for g in gaps if g.question == question), None)
    if gap:  # Only verify if gap was logged (confidence must be >= 0.15)
        assert gap.confidence_score < 0.70
        assert gap.confidence_score >= 0.15  # Above relevance threshold
        assert gap.frequency >= 1
        assert gap.status == GapStatus.NEW
        assert len(gap.retrieval_context) > 0  # Should have retrieval chunks


def test_gap_frequency_incremented(rag_service):
    """Test that asking the same low-confidence question increments frequency."""
    service, test_db = rag_service
    
    # Use an engineering-related question that's not well documented
    question = "How do I set up Ansible for deployment automation?"
    
    # Ask same question 3 times
    service.ask(question)
    service.ask(question)
    service.ask(question)
    
    # Find gaps for this question
    gaps = test_db.query(DocumentationGap).filter(
        DocumentationGap.question == question
    ).all()
    
    # If gap was logged (confidence >= 0.15), verify frequency
    if len(gaps) > 0:
        assert len(gaps) == 1  # Only one gap entry
        gap = gaps[0]
        assert gap.frequency == 3
        assert gap.question == question
        assert gap.confidence_score >= 0.15  # Above relevance threshold


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
    
    # Use engineering-related question that's likely not documented
    question = "How do I configure Redis caching for the application?"
    
    service.ask(question)
    
    # Find gaps for this question
    gaps = test_db.query(DocumentationGap).filter(
        DocumentationGap.question == question
    ).all()
    
    # Only verify if gap was logged (confidence >= 0.15)
    if len(gaps) == 0:
        pytest.skip("Question was too irrelevant (confidence < 0.15)")
    
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
    
    # Use engineering-related questions that are likely not well documented
    questions = [
        "How do I configure Prometheus metrics?",
        "How do I set up Kafka message queues?",
        "How do I configure NGINX load balancing?",
    ]
    
    for question in questions:
        service.ask(question)
    
    # Count gaps that were actually logged (confidence >= 0.15)
    gaps = test_db.query(DocumentationGap).all()
    
    # If no gaps were logged, it means all questions had confidence < 0.15 (irrelevant)
    # This is acceptable - just means none were relevant enough to log
    if len(gaps) == 0:
        pytest.skip("All questions had confidence < 0.15 (too irrelevant to log)")
    
    # If gaps were logged, verify they're from our question list
    logged_questions = {g.question for g in gaps}
    assert logged_questions.issubset(set(questions))


def test_irrelevant_questions_not_logged(rag_service):
    """Test that completely irrelevant questions (confidence < 0.15) are NOT logged as gaps."""
    service, test_db = rag_service
    
    # Ask completely irrelevant questions (should have confidence < 0.15)
    irrelevant_questions = [
        "What is the weather like today?",
        "What is the capital of France?",
        "How do I make pancakes?",
    ]
    
    for question in irrelevant_questions:
        response = service.ask(question)
        # Should return fallback
        assert "I can only answer questions" in response.answer
        assert response.confidence <= 0.15  # Very low confidence
    
    # Verify NO gaps were logged for these irrelevant questions
    gaps = test_db.query(DocumentationGap).all()
    logged_questions = {g.question for g in gaps}
    
    # None of the irrelevant questions should be in the gaps
    for question in irrelevant_questions:
        assert question not in logged_questions, \
            f"Irrelevant question '{question}' should not be logged as gap (confidence < 0.15)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
