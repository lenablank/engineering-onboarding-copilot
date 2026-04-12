"""
API routes for Source Document Management

Provides endpoints to retrieve information about indexed documentation sources.
"""
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_store import VectorStoreService

router = APIRouter(prefix="/api/sources", tags=["sources"])


# Pydantic models for response
class SourceDocument(BaseModel):
    """Response model for a source document."""
    file_name: str
    file_path: str
    chunk_count: int


class SourcesResponse(BaseModel):
    """Response model for sources list."""
    sources: List[SourceDocument]
    total_files: int
    total_chunks: int


@router.get("/", response_model=SourcesResponse)
async def list_sources():
    """
    List all source documents in the vector store.
    
    Returns:
        List of source documents with their chunk counts, plus summary statistics
    """
    vector_store = VectorStoreService()
    sources_data = vector_store.get_sources()
    
    return SourcesResponse(**sources_data)
