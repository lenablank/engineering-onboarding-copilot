"""
Engineering Onboarding Copilot API - Sprint 1
FastAPI backend for RAG-powered documentation assistant
"""
from typing import Any, Optional
from pathlib import Path
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from app.services.vector_store import VectorStoreService
from app.services.rag_service import RAGService
from app.utils.logging import setup_logging
from app.models.database import init_db
from app.routes import gaps
import logging

# Load environment variables and setup logging
load_dotenv()
setup_logging(level="INFO")

logger = logging.getLogger(__name__)


# Pydantic models for /ask endpoint
class AskRequest(BaseModel):
    """Request model for /ask endpoint."""
    question: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        description="User's question about the documentation",
        examples=["How do I set up my development environment?"]
    )


class AskResponse(BaseModel):
    """Response model for /ask endpoint."""
    answer: str = Field(..., description="Generated answer to the question")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    sources: list[dict[str, Any]] = Field(..., description="List of source documents with content")
    chunks_used: int = Field(..., description="Number of document chunks retrieved")


# Global RAG service instance (initialized on startup)
rag_service: Optional[RAGService] = None


app = FastAPI(
    title="Engineering Onboarding Copilot API",
    description="RAG-powered documentation assistant with Gap Radar",
    version="1.0.0",
)

# Configure CORS - allow origins from environment variable
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
logger.info(f"CORS enabled for origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(gaps.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database and RAG service on application startup."""
    global rag_service
    
    # Initialize database first
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        logger.warning("Gap Radar features will be unavailable but RAG still works")
    
    # Then initialize RAG service
    try:
        logger.info("Initializing RAG service...")
        
        # Path to synthetic documentation
        docs_path = Path(__file__).parent.parent.parent / "synthetic-docs"
        
        # Initialize vector store service
        vector_store = VectorStoreService(
            persist_directory="./chroma_db",
            collection_name="onboarding_docs"
        )
        
        # Index documents from synthetic docs directory
        logger.info(f"Indexing documents from {docs_path}")
        num_chunks = vector_store.index_documents(
            docs_directory=str(docs_path),
            force_reindex=False  # Set to True to rebuild the entire index
        )
        logger.info(f"Indexed {num_chunks} document chunks")
        
        # Initialize RAG service with production confidence threshold
        rag_service = RAGService(
            vector_store=vector_store,
            confidence_threshold=0.7  # Production: 70% minimum confidence
        )
        
        logger.info("RAG service initialized successfully!")
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
        logger.warning("Application will start but RAG features may be unavailable")
        # Don't raise - allow app to start so we can access health endpoint and debug


@app.get("/")
def root() -> dict[str, Any]:
    """Return API information and available endpoints."""
    return {
        "name": "Engineering Onboarding Copilot API",
        "version": "1.0.0",
        "status": "Sprint 2 - Gap Radar Implementation",
        "endpoints": {
            "health": "/health",
            "ask": "/ask (POST)",
            "gaps": "/api/gaps (GET)",
            "gap_details": "/api/gaps/{id} (GET)",
            "gap_stats": "/api/gaps/stats (GET)",
            "update_gap": "/api/gaps/{id}/status (PATCH)",
            "docs": "/docs (Swagger UI)",
            "prove_pipeline": "/prove-pipeline",
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> AskResponse:
    """
    Answer questions using the RAG pipeline.

    This endpoint:
    1. Takes a user question
    2. Retrieves relevant document chunks from ChromaDB
    3. Generates an answer using Groq LLM (llama-3.1-8b-instant)
    4. Returns the answer with confidence score and sources

    Args:
        request: AskRequest containing the user's question

    Returns:
        AskResponse with answer, confidence, sources, and chunk count

    Raises:
        HTTPException: If RAG service is not initialized or if question processing fails
    """
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service not initialized. Please wait for startup to complete."
        )
    
    try:
        result = rag_service.ask(request.question)
        
        return AskResponse(
            answer=result.answer,
            confidence=result.confidence,
            sources=result.sources,  # Return full source objects with content
            chunks_used=result.retrieved_chunks
        )
    except ValueError as e:
        # Input validation errors (question too long, empty, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Other errors (LLM API failure, vector DB issues, etc.)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )


@app.get("/docs/{filename}")
def get_document(filename: str) -> dict[str, Any]:
    """
    Retrieve the full content of a documentation file.
    
    Args:
        filename: Name of the markdown file (e.g., "7-database-setup.md")
    
    Returns:
        Dictionary with filename and content
    
    Raises:
        HTTPException: 404 if file not found, 400 if invalid filename
    """
    # Security: Only allow filenames without path traversal
    if "/" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Only allow .md files
    if not filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only markdown files are supported")
    
    docs_path = Path(__file__).parent.parent.parent / "synthetic-docs"
    file_path = docs_path / filename
    
    # Check if file exists
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"Document '{filename}' not found")
    
    try:
        content = file_path.read_text(encoding="utf-8")
        return {
            "filename": filename,
            "content": content,
            "path": str(file_path)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read document: {str(e)}"
        )


@app.post("/prove-pipeline")
def prove_pipeline() -> dict[str, Any]:
    """
    DEPRECATED: Sprint 0 test endpoint - replaced by /ask endpoint.
    
    Use the /ask endpoint to test the RAG pipeline with actual questions.
    """
    return {
        "status": "deprecated",
        "message": "This Sprint 0 test endpoint has been replaced by the production /ask endpoint",
        "alternative": "POST /ask with {'question': 'your question here'}",
        "docs": "/docs"
    }


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on application shutdown."""
    global rag_service
    
    import logging
    logger = logging.getLogger(__name__)
    
    if rag_service is not None:
        logger.info("Shutting down RAG service...")
        rag_service.close()
        rag_service = None
        logger.info("RAG service shutdown complete")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
