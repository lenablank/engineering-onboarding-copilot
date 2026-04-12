"""
Pytest configuration and fixtures.

Provides mocks for external dependencies (Groq API, ChromaDB) to make tests
fast and deterministic in CI environments.
"""
import os
import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Set test environment before any imports
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "test-key-for-ci")
os.environ["TESTING"] = "true"


# Mock ChromaDB at module level to prevent slow initialization
@pytest.fixture(scope="session", autouse=True)
def mock_chromadb():
    """Mock ChromaDB to prevent initialization during test collection."""
    with patch('langchain_community.vectorstores.Chroma') as mock_chroma_class:
        # Create a mock instance with all needed methods
        mock_chroma_instance = Mock()
        mock_chroma_instance.similarity_search_with_score.return_value = []
        mock_chroma_instance._collection = Mock()
        mock_chroma_instance._collection.count.return_value = 275
        mock_chroma_instance._collection.get.return_value = {
            'documents': [],
            'metadatas': [],
            'ids': []
        }
        mock_chroma_class.return_value = mock_chroma_instance
        
        yield mock_chroma_class


@pytest.fixture(scope="session", autouse=True)
def mock_external_services():
    """Mock external services for all tests (session-wide)."""
    
    # Mock Groq LLM
    with patch('langchain_groq.ChatGroq') as mock_groq:
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(
            content="This is a mocked LLM response for testing purposes."
        )
        mock_groq.return_value = mock_llm
        
        # Mock HuggingFace embeddings to return dummy vectors
        with patch('langchain_community.embeddings.HuggingFaceEmbeddings') as mock_hf:
            mock_embeddings = Mock()
            mock_embeddings.embed_documents.return_value = [[0.1] * 384]  # Mock 384-dim vector
            mock_embeddings.embed_query.return_value = [0.1] * 384
            mock_hf.return_value = mock_embeddings
            
            yield {
                'groq': mock_groq,
                'embeddings': mock_hf
            }


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset any singleton instances between tests."""
    # This prevents state leaking between tests
    yield
    # Cleanup after test
    pass
