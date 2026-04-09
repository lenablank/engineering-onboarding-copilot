"""
Documentation Gap model for tracking questions that the system couldn't answer confidently.

This is the core of the "Documentation Gap Radar" feature - our capstone differentiator.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
import enum

from app.models.database import Base


class GapStatus(str, enum.Enum):
    """Status of a documentation gap."""
    NEW = "new"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"


class DocumentationGap(Base):
    """
    Model for storing documentation gaps.
    
    A documentation gap is logged when:
    - The system receives a question
    - The confidence score is below the threshold
    - The system returns a fallback response
    
    This helps identify:
    - What questions users are asking that aren't well answered
    - Which areas of documentation need improvement
    - What knowledge is missing from the system
    """
    __tablename__ = "documentation_gaps"
    
    # Primary key - using UUID for better scalability
    id = Column(
        String(36),  # UUID as string for SQLite compatibility
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    
    # The question that triggered low confidence
    question = Column(String(500), nullable=False, index=True)
    
    # Confidence score that was calculated (0.0 to 1.0)
    confidence_score = Column(Float, nullable=False)
    
    # How many times this question (or similar) has been asked
    # Incremented when duplicate/similar question is detected
    frequency = Column(Integer, default=1, nullable=False, index=True)
    
    # Status tracking for gap resolution
    status = Column(
        SQLEnum(GapStatus),
        default=GapStatus.NEW,
        nullable=False,
        index=True
    )
    
    # Optional: Store the retrieval context (what chunks were found)
    # This helps debug why confidence was low
    # Stored as JSON: [{"chunk_id": 1, "content": "...", "score": 0.5}, ...]
    retrieval_context = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of the gap."""
        return (
            f"<DocumentationGap(id={self.id}, "
            f"question='{self.question[:50]}...', "
            f"confidence={self.confidence_score:.2f}, "
            f"frequency={self.frequency}, "
            f"status={self.status})>"
        )
    
    def to_dict(self) -> dict:
        """Convert gap to dictionary for API responses."""
        return {
            "id": self.id,
            "question": self.question,
            "confidence_score": self.confidence_score,
            "frequency": self.frequency,
            "status": self.status.value,
            "retrieval_context": self.retrieval_context,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
