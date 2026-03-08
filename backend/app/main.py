"""
Engineering Onboarding Copilot API - Sprint 0
FastAPI backend for RAG-powered documentation assistant
"""
from typing import Any
from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

app = FastAPI(
    title="Engineering Onboarding Copilot API",
    description="RAG-powered documentation assistant with Gap Radar",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, Any]:
    """Return API information and available endpoints."""
    return {
        "name": "Engineering Onboarding Copilot API",
        "version": "0.1.0",
        "status": "Sprint 0 - Proving Pipeline",
        "endpoints": {
            "health": "/health",
            "prove_pipeline": "/prove-pipeline",
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/prove-pipeline")
def prove_pipeline() -> dict[str, Any]:
    """
    Prove the core RAG pipeline is functional.

    This Sprint 0 endpoint demonstrates:
    1. Loading markdown files from synthetic-docs/
    2. Splitting into chunks (500 chars, 50 overlap)
    3. Generating embeddings using OpenAI
    4. Storing in Chroma vector database
    5. Performing test retrieval query

    Returns:
        Pipeline statistics and sample results, or error details
    """
    try:
        # Validate synthetic docs directory exists
        docs_path = Path(__file__).parent.parent.parent / "synthetic-docs"
        if not docs_path.exists():
            return {
                "status": "error",
                "pipeline_proven": False,
                "error": f"Synthetic docs directory not found: {docs_path}",
            }

        # Load markdown documents
        loader = DirectoryLoader(
            str(docs_path),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents = loader.load()

        if not documents:
            return {
                "status": "error",
                "pipeline_proven": False,
                "error": "No documents loaded from synthetic-docs/",
            }

        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_documents(documents)

        # Generate embeddings using free local model (no API key needed)
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db_test",
        )

        # Test retrieval with sample query
        test_query = "How do I set up my development environment?"
        results = vectorstore.similarity_search(test_query, k=3)

        # Format response samples
        sample_chunks = [
            {
                "content": (
                    chunk.page_content[:200] + "..."
                    if len(chunk.page_content) > 200
                    else chunk.page_content
                ),
                "source": chunk.metadata.get("source", "unknown"),
                "chunk_length": len(chunk.page_content),
            }
            for chunk in chunks[:3]
        ]

        sample_results = [
            {
                "content": (
                    result.page_content[:200] + "..."
                    if len(result.page_content) > 200
                    else result.page_content
                ),
                "source": result.metadata.get("source", "unknown"),
                "relevance": "high",
            }
            for result in results
        ]

        return {
            "status": "success",
            "pipeline_proven": True,
            "message": "🎉 Core RAG pipeline is functional!",
            "stats": {
                "documents_loaded": len(documents),
                "chunks_created": len(chunks),
                "embeddings_generated": len(chunks),
                "test_query": test_query,
                "results_retrieved": len(results),
            },
            "samples": {
                "first_3_chunks": sample_chunks,
                "retrieved_results": sample_results,
            },
            "next_steps": [
                "Create GitHub repository",
                "Share repo with quantic-grader",
                "Sign up for free Groq API (for LLM in Sprint 1)",
                "Begin Sprint 1: Full RAG implementation",
            ],
        }

    except Exception as e:
        return {
            "status": "error",
            "pipeline_proven": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
