"""
API routes for Documentation Gap Management

Provides endpoints to retrieve and manage logged documentation gaps.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.gap_service import GapService
from app.models.gap import GapStatus, DocumentationGap

router = APIRouter(prefix="/api/gaps", tags=["gaps"])


# Pydantic models for request/response
class GapResponse(BaseModel):
    """Response model for a documentation gap."""
    id: str
    question: str
    confidence_score: float
    frequency: int
    status: str
    retrieval_context: List[dict]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class GapStatusUpdate(BaseModel):
    """Request model for updating gap status."""
    status: GapStatus


class GapStatisticsResponse(BaseModel):
    """Response model for gap statistics."""
    total_gaps: int
    total_occurrences: int
    by_status: dict
    most_frequent: Optional[dict]


def _gap_to_response(gap: DocumentationGap) -> GapResponse:
    """Convert DocumentationGap model to GapResponse."""
    gap_dict = gap.to_dict()
    return GapResponse(**gap_dict)


@router.get("/", response_model=List[GapResponse])
async def list_gaps(
    status: Optional[GapStatus] = Query(None, description="Filter by status"),
    min_frequency: Optional[int] = Query(None, description="Minimum frequency threshold", ge=1),
    limit: int = Query(100, description="Maximum number of results", ge=1, le=500)
):
    """
    List documentation gaps with optional filtering.
    
    Args:
        status: Filter by gap status (NEW, REVIEWED, RESOLVED)
        min_frequency: Only return gaps asked at least this many times
        limit: Maximum number of results (1-500)
    
    Returns:
        List of documentation gaps ordered by frequency (most common first)
    """
    gap_service = GapService()
    gaps = gap_service.get_all_gaps(
        status=status,
        min_frequency=min_frequency,
        limit=limit
    )
    
    return [_gap_to_response(gap) for gap in gaps]


@router.get("/stats", response_model=GapStatisticsResponse)
async def get_gap_statistics():
    """
    Get statistics about documentation gaps.
    
    Returns:
        Statistics including total gaps, occurrences by status, most frequent gap
    """
    gap_service = GapService()
    stats = gap_service.get_gap_statistics()
    
    return GapStatisticsResponse(**stats)


@router.get("/{gap_id}", response_model=GapResponse)
async def get_gap(gap_id: str):
    """
    Get a specific documentation gap by ID.
    
    Args:
        gap_id: UUID of the gap
    
    Returns:
        Documentation gap details
        
    Raises:
        HTTPException: 404 if gap not found
    """
    gap_service = GapService()
    gap = gap_service.get_gap_by_id(gap_id)
    
    if not gap:
        raise HTTPException(status_code=404, detail=f"Gap {gap_id} not found")
    
    return _gap_to_response(gap)


@router.patch("/{gap_id}/status", response_model=GapResponse)
async def update_gap_status(gap_id: str, update: GapStatusUpdate):
    """
    Update the status of a documentation gap.
    
    Args:
        gap_id: UUID of the gap
        update: New status (NEW, REVIEWED, or RESOLVED)
    
    Returns:
        Updated gap details
        
    Raises:
        HTTPException: 404 if gap not found
    """
    gap_service = GapService()
    gap = gap_service.update_gap_status(gap_id, update.status)
    
    if not gap:
        raise HTTPException(status_code=404, detail=f"Gap {gap_id} not found")
    
    return _gap_to_response(gap)
