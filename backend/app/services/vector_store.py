"""
Vector Store Service

Handles all interactions with Chroma vector database:
- Loading and indexing documents
- Semantic search and retrieval
- Managing embeddings
"""
import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Manages document storage and retrieval using Chroma vector database."""
    
    # Configuration constants
    DEFAULT_PERSIST_DIRECTORY = "./chroma_db"
    DEFAULT_COLLECTION_NAME = "documents"
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 50
    
    def __init__(
        self,
        persist_directory: str = DEFAULT_PERSIST_DIRECTORY,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):
        """
        Initialize the vector store service.
        
        Args:
            persist_directory: Directory to store Chroma database
            collection_name: Name of the Chroma collection
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chroma_client = None
        
        # Initialize HuggingFace embeddings (FREE, local)
        logger.info("Loading HuggingFace embedding model (all-MiniLM-L6-v2)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize or load vector store
        self.vectorstore = None
        self._load_or_create_vectorstore()
    
    def _load_or_create_vectorstore(self) -> None:
        """Load existing vector store or create new one."""
        try:
            # Ensure persist directory is absolute path
            persist_path = Path(self.persist_directory).resolve()
            self.persist_directory = str(persist_path)
            
            # Create directory if it doesn't exist
            persist_path.mkdir(parents=True, exist_ok=True)
            
            # Create ChromaDB client with proper settings (reusing if possible)
            if self.chroma_client is None:
                logger.info(f"Creating new ChromaDB client for {self.persist_directory}")
                self.chroma_client = chromadb.PersistentClient(
                    path=self.persist_directory,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True
                    )
                )
            
            if persist_path.exists() and any(persist_path.iterdir()):
                logger.info(f"Loading existing Chroma database from {self.persist_directory}")
                self.vectorstore = Chroma(
                    client=self.chroma_client,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                count = self.vectorstore._collection.count()
                logger.info(f"Loaded {count} documents")
            else:
                logger.info(f"Creating new Chroma database at {self.persist_directory}")
                self.vectorstore = Chroma(
                    client=self.chroma_client,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
        except (OSError, RuntimeError) as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def load_documents(self, docs_directory: str) -> List[Document]:
        """
        Load markdown documents from directory.
        
        Args:
            docs_directory: Path to directory containing markdown files
            
        Returns:
            List of loaded documents
            
        Raises:
            ValueError: If directory doesn't exist or is not a directory
        """
        # Validate input
        if not os.path.exists(docs_directory):
            raise ValueError(f"Directory not found: {docs_directory}")
        if not os.path.isdir(docs_directory):
            raise ValueError(f"Not a directory: {docs_directory}")
        
        logger.info(f"Loading documents from {docs_directory}...")
        
        loader = DirectoryLoader(
            docs_directory,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True
        )
        
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} markdown files")
        
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of document chunks
        """
        logger.info(f"Chunking {len(documents)} documents...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        return chunks
    
    def index_documents(self, docs_directory: str, force_reindex: bool = False) -> int:
        """
        Load, chunk, and index documents into vector store.
        
        Args:
            docs_directory: Path to directory containing markdown files
            force_reindex: If True, clear existing index before adding
            
        Returns:
            Number of chunks indexed
        """
        if force_reindex:
            logger.info("Clearing existing index...")
            if self.vectorstore is not None and self.chroma_client is not None:
                # Delete the collection instead of deleting directory
                try:
                    self.chroma_client.delete_collection(self.collection_name)
                    logger.info(f"Deleted collection '{self.collection_name}'")
                except Exception as e:
                    logger.warning(f"Could not delete collection (might not exist): {e}")
                
                # Recreate the collection
                self.vectorstore = Chroma(
                    client=self.chroma_client,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info("Created fresh collection")
        else:
            # If not force reindexing, check if documents already exist
            if self.vectorstore is not None:
                existing_count = self.vectorstore._collection.count()
                if existing_count > 0:
                    logger.info(f"Using existing index with {existing_count} documents. Use force_reindex=True to rebuild.")
                    return existing_count
        
        # Load and chunk documents
        documents = self.load_documents(docs_directory)
        chunks = self.chunk_documents(documents)
        
        if not chunks:
            logger.warning("No documents to index")
            return 0
        
        if self.vectorstore is None:
            raise RuntimeError("Vector store not initialized")
        
        # Add to vector store
        logger.info("Generating embeddings and indexing...")
        self.vectorstore.add_documents(chunks)
        
        logger.info(f"Successfully indexed {len(chunks)} chunks")
        return len(chunks)
    
    def search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search for relevant documents using semantic similarity.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of relevant document chunks
        """
        if self.vectorstore is None:
            logger.warning("Vector store not initialized")
            return []
        
        if filter_metadata:
            results = self.vectorstore.similarity_search(
                query, k=k, filter=filter_metadata
            )
        else:
            results = self.vectorstore.similarity_search(query, k=k)
        
        return results
    
    def search_with_scores(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """
        Search for relevant documents and return similarity scores.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of tuples (document, similarity_score)
        """
        if self.vectorstore is None:
            logger.warning("Vector store not initialized")
            return []
        
        if filter_metadata:
            results = self.vectorstore.similarity_search_with_score(
                query, k=k, filter=filter_metadata
            )
        else:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with stats (document count, etc.)
        """
        if self.vectorstore is None:
            return {"status": "not_initialized"}
        
        try:
            count = self.vectorstore._collection.count()
            return {
                "status": "ready",
                "document_count": count,
                "persist_directory": self.persist_directory,
                "collection_name": self.collection_name,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_sources(self) -> Dict[str, Any]:
        """
        Get information about all source documents in the vector store.
        
        Returns:
            Dictionary containing:
            - sources: List of source files with their metadata
            - total_files: Total number of unique source files
            - total_chunks: Total number of chunks across all files
        """
        if self.vectorstore is None:
            return {
                "sources": [],
                "total_files": 0,
                "total_chunks": 0
            }
        
        try:
            # Get all documents with metadata
            result = self.vectorstore._collection.get(include=["metadatas"])
            
            # Count chunks per source file
            source_chunks: Dict[str, int] = {}
            for metadata in result['metadatas']:
                if metadata and 'source' in metadata:
                    source_path = metadata['source']
                    source_chunks[source_path] = source_chunks.get(source_path, 0) + 1
            
            # Build source list with file names and paths
            sources = []
            for source_path, chunk_count in sorted(source_chunks.items()):
                # Extract just the filename from the full path
                file_name = Path(source_path).name
                sources.append({
                    "file_name": file_name,
                    "file_path": source_path,
                    "chunk_count": chunk_count
                })
            
            return {
                "sources": sources,
                "total_files": len(sources),
                "total_chunks": sum(source_chunks.values())
            }
        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            return {
                "sources": [],
                "total_files": 0,
                "total_chunks": 0,
                "error": str(e)
            }
    
    def close(self) -> None:
        """Close ChromaDB client and release resources."""
        try:
            # ChromaDB PersistentClient doesn't require explicit close
            # but we can clear references to help with garbage collection
            self.vectorstore = None
            self.chroma_client = None
            logger.info("Vector store closed")
        except Exception as e:
            logger.warning(f"Error closing vector store: {e}")
