"""
Tests for Documentation Gap Service

Tests gap logging, deduplication, frequency tracking, and statistics.
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.database import Base
from app.models.gap import DocumentationGap, GapStatus
from app.services.gap_service import GapService


# Test database setup
@pytest.fixture
def test_db():
    """Create a test database session."""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


@pytest.fixture
def gap_service(test_db):
    """Create a gap service with test database."""
    return GapService(db=test_db)


def test_log_new_gap(gap_service, test_db):
    """Test logging a new documentation gap."""
    question = "How do I configure SSL certificates?"
    confidence = 0.45
    context = [{"content": "SSL setup...", "source": "security.md"}]
    
    gap = gap_service.log_gap(question, confidence, context)
    
    assert gap is not None
    assert gap.question == question
    assert gap.confidence_score == confidence
    assert gap.frequency == 1
    assert gap.status == GapStatus.NEW
    assert len(gap.retrieval_context) == 1
    assert gap.question_hash is not None


def test_log_duplicate_gap_increments_frequency(gap_service, test_db):
    """Test that duplicate questions increment frequency."""
    question = "What is the API rate limit?"
    
    # Log first time
    gap1 = gap_service.log_gap(question, 0.55)
    assert gap1.frequency == 1
    
    # Log same question again
    gap2 = gap_service.log_gap(question, 0.58)
    assert gap2.id == gap1.id  # Same gap
    assert gap2.frequency == 2  # Frequency incremented
    
    # Log third time
    gap3 = gap_service.log_gap(question, 0.52)
    assert gap3.id == gap1.id
    assert gap3.frequency == 3


def test_log_duplicate_with_different_case(gap_service, test_db):
    """Test that questions with different casing are treated as duplicates."""
    question1 = "How do I deploy to production?"
    question2 = "HOW DO I DEPLOY TO PRODUCTION?"
    question3 = "how do i deploy to production?"
    
    gap1 = gap_service.log_gap(question1, 0.60)
    gap2 = gap_service.log_gap(question2, 0.61)
    gap3 = gap_service.log_gap(question3, 0.59)
    
    assert gap1.id == gap2.id == gap3.id
    assert gap3.frequency == 3


def test_log_duplicate_with_extra_whitespace(gap_service, test_db):
    """Test that questions with extra whitespace are treated as duplicates."""
    question1 = "How do I run tests?"
    question2 = "  How do I run tests?  "
    question3 = "How   do   I   run   tests?"
    
    gap1 = gap_service.log_gap(question1, 0.65)
    gap2 = gap_service.log_gap(question2, 0.66)
    
    assert gap1.id == gap2.id
    assert gap2.frequency == 2
    
    # Note: Multiple spaces within question will create different hash
    gap3 = gap_service.log_gap(question3, 0.64)
    assert gap3.id != gap1.id  # Different due to internal spacing


def test_get_all_gaps(gap_service, test_db):
    """Test retrieving all gaps."""
    # Log multiple gaps
    gap_service.log_gap("Question 1?", 0.45)
    gap_service.log_gap("Question 2?", 0.50)
    gap_service.log_gap("Question 3?", 0.55)
    
    gaps = gap_service.get_all_gaps()
    assert len(gaps) == 3


def test_get_gaps_filtered_by_status(gap_service, test_db):
    """Test filtering gaps by status."""
    # Create gaps with different statuses
    gap1 = gap_service.log_gap("Question 1?", 0.45)
    gap2 = gap_service.log_gap("Question 2?", 0.50)
    gap3 = gap_service.log_gap("Question 3?", 0.55)
    
    # Update statuses
    gap_service.update_gap_status(gap2.id, GapStatus.REVIEWED)
    gap_service.update_gap_status(gap3.id, GapStatus.RESOLVED)
    
    # Filter by status
    new_gaps = gap_service.get_all_gaps(status=GapStatus.NEW)
    assert len(new_gaps) == 1
    assert new_gaps[0].id == gap1.id
    
    reviewed_gaps = gap_service.get_all_gaps(status=GapStatus.REVIEWED)
    assert len(reviewed_gaps) == 1
    assert reviewed_gaps[0].id == gap2.id


def test_get_gaps_filtered_by_frequency(gap_service, test_db):
    """Test filtering gaps by minimum frequency."""
    # Create gaps with different frequencies
    question1 = "Common question?"
    question2 = "Rare question?"
    
    gap_service.log_gap(question1, 0.45)
    gap_service.log_gap(question1, 0.46)  # frequency = 2
    gap_service.log_gap(question1, 0.44)  # frequency = 3
    
    gap_service.log_gap(question2, 0.50)  # frequency = 1
    
    # Filter by minimum frequency
    frequent_gaps = gap_service.get_all_gaps(min_frequency=2)
    assert len(frequent_gaps) == 1
    assert frequent_gaps[0].question == question1
    assert frequent_gaps[0].frequency == 3


def test_gaps_ordered_by_frequency(gap_service, test_db):
    """Test that gaps are ordered by frequency (descending)."""
    q1 = "Low frequency question?"
    q2 = "High frequency question?"
    q3 = "Medium frequency question?"
    
    # Create different frequencies
    gap_service.log_gap(q1, 0.45)  # frequency = 1
    
    gap_service.log_gap(q2, 0.50)
    gap_service.log_gap(q2, 0.51)
    gap_service.log_gap(q2, 0.49)  # frequency = 3
    
    gap_service.log_gap(q3, 0.55)
    gap_service.log_gap(q3, 0.54)  # frequency = 2
    
    gaps = gap_service.get_all_gaps()
    
    assert len(gaps) == 3
    assert gaps[0].question == q2  # Highest frequency first
    assert gaps[0].frequency == 3
    assert gaps[1].question == q3
    assert gaps[1].frequency == 2
    assert gaps[2].question == q1
    assert gaps[2].frequency == 1


def test_get_gap_by_id(gap_service, test_db):
    """Test retrieving a gap by ID."""
    gap = gap_service.log_gap("Test question?", 0.60)
    
    retrieved = gap_service.get_gap_by_id(gap.id)
    
    assert retrieved is not None
    assert retrieved.id == gap.id
    assert retrieved.question == gap.question


def test_get_gap_by_invalid_id(gap_service, test_db):
    """Test retrieving a gap with non-existent ID."""
    retrieved = gap_service.get_gap_by_id("non-existent-id")
    assert retrieved is None


def test_update_gap_status(gap_service, test_db):
    """Test updating gap status."""
    gap = gap_service.log_gap("Test question?", 0.60)
    assert gap.status == GapStatus.NEW
    
    updated = gap_service.update_gap_status(gap.id, GapStatus.REVIEWED)
    
    assert updated is not None
    assert updated.status == GapStatus.REVIEWED
    
    # Update again
    updated2 = gap_service.update_gap_status(gap.id, GapStatus.RESOLVED)
    assert updated2.status == GapStatus.RESOLVED


def test_get_gap_statistics(gap_service, test_db):
    """Test getting gap statistics."""
    # Create gaps with different frequencies and statuses
    q1 = "Question 1?"
    gap_service.log_gap(q1, 0.45)
    gap_service.log_gap(q1, 0.46)
    gap_service.log_gap(q1, 0.44)  # frequency = 3
    
    q2 = "Question 2?"
    gap2 = gap_service.log_gap(q2, 0.50)
    gap_service.log_gap(q2, 0.51)  # frequency = 2
    
    q3 = "Question 3?"
    gap3 = gap_service.log_gap(q3, 0.55)  # frequency = 1
    
    # Update statuses
    gap_service.update_gap_status(gap2.id, GapStatus.REVIEWED)
    gap_service.update_gap_status(gap3.id, GapStatus.RESOLVED)
    
    stats = gap_service.get_gap_statistics()
    
    assert stats["total_gaps"] == 3
    assert stats["total_occurrences"] == 6  # 3 + 2 + 1
    assert stats["by_status"]["new"] == 1
    assert stats["by_status"]["reviewed"] == 1
    assert stats["by_status"]["resolved"] == 1
    assert stats["most_frequent"]["question"] == q1
    assert stats["most_frequent"]["frequency"] == 3


def test_question_hash_generation():
    """Test that question hashes are generated correctly."""
    q1 = "How do I deploy?"
    q2 = "how do i deploy?"
    q3 = "  HOW DO I DEPLOY?  "
    
    hash1 = GapService._hash_question(q1)
    hash2 = GapService._hash_question(q2)
    hash3 = GapService._hash_question(q3)
    
    # All should produce same hash (normalized)
    assert hash1 == hash2 == hash3
    assert len(hash1) == 64  # SHA256 hex length


def test_question_normalization():
    """Test question normalization."""
    assert GapService._normalize_question("Test?") == "test?"
    assert GapService._normalize_question("  TEST  ") == "test"
    assert GapService._normalize_question("MiXeD CaSe") == "mixed case"


def test_retrieval_context_stored(gap_service, test_db):
    """Test that retrieval context is stored correctly."""
    context = [
        {"content": "Chunk 1", "source": "doc1.md", "distance": 0.5},
        {"content": "Chunk 2", "source": "doc2.md", "distance": 0.7}
    ]
    
    gap = gap_service.log_gap("Test?", 0.60, context)
    
    assert gap.retrieval_context == context
    assert len(gap.retrieval_context) == 2


def test_confidence_updated_on_duplicate(gap_service, test_db):
    """Test that confidence is updated when duplicate is logged."""
    question = "Test question?"
    
    gap1 = gap_service.log_gap(question, 0.45)
    assert gap1.confidence_score == 0.45
    
    gap2 = gap_service.log_gap(question, 0.62)
    assert gap2.id == gap1.id
    assert gap2.confidence_score == 0.62  # Updated with latest


def test_limit_results(gap_service, test_db):
    """Test limiting number of results returned."""
    # Create 10 gaps
    for i in range(10):
        gap_service.log_gap(f"Question {i}?", 0.50)
    
    # Get with limit
    gaps = gap_service.get_all_gaps(limit=5)
    assert len(gaps) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
