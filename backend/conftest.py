"""
Pytest configuration for backend tests.

Mocking strategy:
- Uses pytest_configure hook to install mocks BEFORE test collection
- Mocks external dependencies: ChromaDB, Groq LLM, HuggingFace embeddings
- Makes tests fast, deterministic, and CI-friendly
"""
import os
import sys
from unittest.mock import Mock


def pytest_configure(config):
    """Install mocks before pytest collects tests."""
    # Set test mode
    os.environ["TESTING"] = "true"
    os.environ.setdefault("GROQ_API_KEY", "test-fake-key-for-ci")
    
    # Don't mock if modules already imported (allows local dev with real deps)
    if 'chromadb' in sys.modules:
        return
    
    # Create ChromaDB mock with proper structure
    mock_chromadb = type(sys)('chromadb')
    mock_chromadb.config = type(sys)('config')
    mock_chromadb.config.Settings = type('Settings', (), {})
    
    # Mock collection
    mock_collection = Mock()
    mock_collection.count.return_value = 0
    mock_collection.get.return_value = {'documents': [], 'metadatas': [], 'ids': []}
    
    # Mock client
    mock_client = Mock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_chromadb.PersistentClient = Mock(return_value=mock_client)
    
    sys.modules['chromadb'] = mock_chromadb
    sys.modules['chromadb.config'] = mock_chromadb.config
    
    # Mock Groq
    mock_groq = Mock()
    mock_llm = Mock()
    mock_llm.invoke.return_value = Mock(content="Mocked LLM response")
    mock_groq.ChatGroq = Mock(return_value=mock_llm)
    sys.modules['langchain_groq'] = mock_groq
    
    # Mock HuggingFace
    mock_hf = Mock()
    mock_embeddings = Mock()
    mock_embeddings.embed_documents.return_value = [[0.1] * 384]
    mock_embeddings.embed_query.return_value = [0.1] * 384
    mock_hf.HuggingFaceEmbeddings = Mock(return_value=mock_embeddings)
    sys.modules['langchain_community.embeddings'] = mock_hf
    sys.modules['langchain_community.embeddings.huggingface'] = mock_hf
    
    # Mock Chroma vectorstore
    mock_vs = Mock()
    mock_vs_instance = Mock()
    mock_vs_instance.similarity_search_with_score.return_value = []
    mock_vs_instance._collection = mock_collection
    mock_vs.Chroma = Mock(return_value=mock_vs_instance)
    sys.modules['langchain_community.vectorstores'] = mock_vs
    sys.modules['langchain_community.vectorstores.chroma'] = mock_vs
