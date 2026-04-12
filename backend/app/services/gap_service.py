"""
Documentation Gap Service

Tracks questions with low confidence scores to identify documentation gaps.
Automatically deduplicates similar questions and tracks frequency.
"""
import hashlib
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.database import get_db
from app.models.gap import DocumentationGap, GapStatus

logger = logging.getLogger(__name__)


class GapService:
    """Service for logging and managing documentation gaps."""
    
    # Similarity threshold for fuzzy matching (0-1)
    SIMILARITY_THRESHOLD = 0.90
    
    def __init__(self, db: Optional[Session] = None):
        """
        Initialize gap service.
        
        Args:
            db: Optional database session (for testing)
        """
        self._db = db
    
    @staticmethod
    def _normalize_question(question: str) -> str:
        """
        Normalize question for comparison.
        
        Args:
            question: Raw question string
            
        Returns:
            Normalized question (lowercase, trimmed)
        """
        return question.lower().strip()
    
    @staticmethod
    def _hash_question(question: str) -> str:
        """
        Create hash of normalized question for fast lookups.
        
        Args:
            question: Question text
            
        Returns:
            SHA256 hash of normalized question
        """
        normalized = GapService._normalize_question(question)
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def _get_db(self) -> Session:
        """Get database session."""
        if self._db:
            return self._db
        return next(get_db())
    
    def log_gap(
        self,
        question: str,
        confidence_score: float,
        retrieval_context: Optional[List[Dict[str, Any]]] = None
    ) -> DocumentationGap:
        """
        Log a documentation gap (low-confidence question).
        
        If the question already exists (exact or similar match), increments frequency.
        Otherwise, creates a new gap entry.
        
        Args:
            question: User's question that had low confidence
            confidence_score: Confidence score from RAG (0-1)
            retrieval_context: Optional list of retrieved chunks for debugging
            
        Returns:
            DocumentationGap: The created or updated gap entry
        """
        db = self._get_db()
        
        try:
            # Normalize question for comparison
            normalized_question = self._normalize_question(question)
            question_hash = self._hash_question(question)
            
            # Check for exact match by hash (fast lookup)
            existing_gap = db.query(DocumentationGap).filter(
                DocumentationGap.question_hash == question_hash
            ).first()
            
            if existing_gap:
                # Update existing gap
                logger.info(f"Incrementing frequency for existing gap: {question[:50]}...")
                existing_gap.frequency += 1
                existing_gap.confidence_score = confidence_score
                existing_gap.updated_at = datetime.utcnow()
                
                # Update retrieval context if provided
                if retrieval_context:
                    existing_gap.retrieval_context = retrieval_context
                
                db.commit()
                db.refresh(existing_gap)
                return existing_gap
            else:
                # Create new gap entry
                logger.info(f"Logging new documentation gap: {question[:50]}...")
                new_gap = DocumentationGap(
                    question=question,
                    question_hash=question_hash,
                    confidence_score=confidence_score,
                    retrieval_context=retrieval_context or [],
                    frequency=1,
                    status=GapStatus.NEW
                )
                
                db.add(new_gap)
                db.commit()
                db.refresh(new_gap)
                
                logger.info(f"Created gap entry with ID: {new_gap.id}")
                return new_gap
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error logging documentation gap: {e}")
            raise
    
    def get_all_gaps(
        self,
        status: Optional[GapStatus] = None,
        min_frequency: Optional[int] = None,
        limit: int = 100
    ) -> List[DocumentationGap]:
        """
        Retrieve documentation gaps with optional filtering.
        
        Args:
            status: Filter by gap status (NEW, REVIEWED, RESOLVED)
            min_frequency: Minimum frequency threshold
            limit: Maximum number of results
            
        Returns:
            List of DocumentationGap entries
        """
        db = self._get_db()
        
        query = db.query(DocumentationGap)
        
        # Apply filters
        if status:
            query = query.filter(DocumentationGap.status == status)
        
        if min_frequency:
            query = query.filter(DocumentationGap.frequency >= min_frequency)
        
        # Order by frequency (most common first), then by created date
        query = query.order_by(
            DocumentationGap.frequency.desc(),
            DocumentationGap.created_at.desc()
        )
        
        # Limit results
        query = query.limit(limit)
        
        return query.all()
    
    def get_gap_by_id(self, gap_id: str) -> Optional[DocumentationGap]:
        """
        Retrieve a specific gap by ID.
        
        Args:
            gap_id: UUID of the gap
            
        Returns:
            DocumentationGap or None if not found
        """
        db = self._get_db()
        return db.query(DocumentationGap).filter(
            DocumentationGap.id == gap_id
        ).first()
    
    def update_gap_status(
        self,
        gap_id: str,
        new_status: GapStatus
    ) -> Optional[DocumentationGap]:
        """
        Update the status of a documentation gap.
        
        Args:
            gap_id: UUID of the gap
            new_status: New status (REVIEWED, RESOLVED)
            
        Returns:
            Updated DocumentationGap or None if not found
        """
        db = self._get_db()
        
        # Fetch gap in the same session
        gap = db.query(DocumentationGap).filter(DocumentationGap.id == gap_id).first()
        if not gap:
            logger.warning(f"Gap not found: {gap_id}")
            return None
        
        logger.info(f"Updating gap {gap_id} status: {gap.status} → {new_status}")
        gap.status = new_status
        gap.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(gap)
        
        return gap
    
    def get_gap_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about documentation gaps.
        
        Returns:
            Dictionary with gap statistics
        """
        db = self._get_db()
        
        total_gaps = db.query(DocumentationGap).count()
        
        new_gaps = db.query(DocumentationGap).filter(
            DocumentationGap.status == GapStatus.NEW
        ).count()
        
        reviewed_gaps = db.query(DocumentationGap).filter(
            DocumentationGap.status == GapStatus.REVIEWED
        ).count()
        
        resolved_gaps = db.query(DocumentationGap).filter(
            DocumentationGap.status == GapStatus.RESOLVED
        ).count()
        
        # Total number of times low-confidence questions were asked
        total_frequency = db.query(
            func.sum(DocumentationGap.frequency)
        ).scalar() or 0
        
        # Most frequent gap
        most_frequent = db.query(DocumentationGap).order_by(
            DocumentationGap.frequency.desc()
        ).first()
        
        return {
            "total_gaps": total_gaps,
            "total_occurrences": total_frequency,
            "by_status": {
                "new": new_gaps,
                "reviewed": reviewed_gaps,
                "resolved": resolved_gaps
            },
            "most_frequent": {
                "question": most_frequent.question if most_frequent else None,
                "frequency": most_frequent.frequency if most_frequent else 0
            } if most_frequent else None
        }
