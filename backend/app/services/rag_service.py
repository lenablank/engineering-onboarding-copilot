"""
RAG (Retrieval-Augmented Generation) Service

Handles the core RAG pipeline:
- Question answering using retrieved documentation
- Citation generation
- Confidence scoring
"""
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from .vector_store import VectorStoreService

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    """Response from RAG pipeline."""
    question: str
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    retrieved_chunks: int


class RAGService:
    """RAG service for answering questions using documentation."""
    
    # Configuration constants
    MAX_QUESTION_LENGTH = 500
    DEFAULT_TEMPERATURE = 0.1
    DEFAULT_MAX_TOKENS = 500
    DEFAULT_RETRIEVAL_TOP_K = 5
    DEFAULT_CONFIDENCE_THRESHOLD = 0.7
    
    # Confidence calculation thresholds
    MIN_CONTEXT_WORDS = 50  # Minimum words in retrieved context
    MIN_SOURCES = 2  # Minimum unique source files
    MIN_SIMILARITY_SCORE = 0.3  # Minimum similarity for any chunk
    
    # System prompt with citation instructions
    SYSTEM_PROMPT = """You are a helpful engineering documentation assistant for an onboarding system.

Your role is to answer questions about engineering processes, tools, and practices using ONLY the provided documentation context.

CRITICAL RULES:
1. ONLY use information from the provided documentation context
2. If the answer is in the context, provide a clear, concise answer
3. ALWAYS cite your sources using the format [source: filename]
4. If information is NOT in the context, respond: "I cannot answer this confidently from the current documentation."
5. Do NOT make up information or use external knowledge
6. Be specific and include relevant details from the documentation

Example with citations:
"To set up the development environment, install PostgreSQL 15 [source: 7-database-setup.md] and run 'brew install postgresql@15' on macOS [source: 7-database-setup.md]."
"""
    
    def __init__(
        self,
        vector_store: Optional[VectorStoreService] = None,
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        retrieval_top_k: int = DEFAULT_RETRIEVAL_TOP_K,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    ):
        """
        Initialize RAG service.
        
        Args:
            vector_store: Vector store service instance
            model: LLM model name (defaults to env var)
            temperature: LLM temperature
            max_tokens: Maximum tokens in response
            retrieval_top_k: Number of chunks to retrieve
            confidence_threshold: Minimum confidence for answering
        """
        # Initialize vector store
        self.vector_store = vector_store or VectorStoreService()
        
        # LLM configuration
        self.model = model or os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retrieval_top_k = retrieval_top_k
        self.confidence_threshold = confidence_threshold
        
        # Initialize Groq LLM
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        logger.info(f"Initializing Groq LLM ({self.model})...")
        try:
            self.llm = ChatGroq(
                api_key=api_key,  # type: ignore
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        except (ValueError, RuntimeError) as e:
            raise RuntimeError(f"Failed to initialize Groq LLM: {e}")
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", """Context from documentation:
{context}

Question: {question}

Answer (with source citations):""")
        ])
        
        logger.info("RAG service initialized successfully")
    
    def _format_sources(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """
        Format retrieved documents as sources.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            List of source dictionaries
        """
        sources = []
        for idx, doc in enumerate(documents):
            source = {
                "chunk_id": idx,
                "content": doc.page_content,
                "metadata": doc.metadata,
                "file_path": doc.metadata.get("source", "unknown")
            }
            sources.append(source)
        
        return sources
    
    def _calculate_confidence(
        self,
        documents_with_scores: List[Tuple[Document, float]]
    ) -> float:
        """
        Calculate confidence score based on retrieval quality.
        
        Factors considered:
        1. Similarity scores (higher = better)
        2. Number of unique sources (more = better)
        3. Context sufficiency (enough words retrieved)
        
        Args:
            documents_with_scores: List of (document, similarity_score) tuples
            
        Returns:
            Confidence score between 0 and 1
        """
        if not documents_with_scores:
            return 0.0
        
        # Factor 1: Average similarity score
        # Convert distance to similarity: similarity = 1 / (1 + distance)
        similarities = [1 / (1 + score) for _, score in documents_with_scores]
        avg_similarity = sum(similarities) / len(similarities)
        
        # Check minimum similarity threshold
        if avg_similarity < self.MIN_SIMILARITY_SCORE:
            logger.debug(f"Low similarity: {avg_similarity:.2f} < {self.MIN_SIMILARITY_SCORE}")
            return round(avg_similarity * 0.5, 2)  # Penalize low similarity
        
        # Factor 2: Unique sources count (diversity of information)
        unique_sources = set(
            doc.metadata.get("source", "unknown") 
            for doc, _ in documents_with_scores
        )
        source_diversity = min(len(unique_sources) / self.MIN_SOURCES, 1.0)
        
        # Factor 3: Context sufficiency (total words retrieved)
        total_words = sum(
            len(doc.page_content.split()) 
            for doc, _ in documents_with_scores
        )
        context_sufficiency = min(total_words / self.MIN_CONTEXT_WORDS, 1.0)
        
        # Weighted combination:
        # - Similarity: 50% (most important)
        # - Source diversity: 25%
        # - Context sufficiency: 25%
        confidence = (
            0.5 * avg_similarity +
            0.25 * source_diversity +
            0.25 * context_sufficiency
        )
        
        logger.debug(
            f"Confidence calculation: sim={avg_similarity:.2f}, "
            f"sources={len(unique_sources)}, words={total_words}, "
            f"final={confidence:.2f}"
        )
        
        return round(confidence, 2)
    
    def _build_context(self, documents: List[Document]) -> str:
        """
        Build context string from retrieved documents.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for idx, doc in enumerate(documents):
            filename = os.path.basename(doc.metadata.get("source", "unknown"))
            content = doc.page_content.strip()
            context_parts.append(f"[Document {idx + 1} - {filename}]\n{content}\n")
        
        return "\n".join(context_parts)
    
    def ask(self, question: str) -> RAGResponse:
        """
        Answer a question using RAG pipeline.
        
        Args:
            question: User question
            
        Returns:
            RAGResponse with answer, sources, and metadata
            
        Raises:
            ValueError: If question is empty or too long
        """
        # Input validation
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        question = question.strip()
        
        # Limit question length to prevent abuse
        if len(question) > self.MAX_QUESTION_LENGTH:
            raise ValueError(
                f"Question too long ({len(question)} chars). "
                f"Maximum {self.MAX_QUESTION_LENGTH} characters."
            )
        
        logger.info(f"Processing question: {question[:100]}...")
        
        # Step 1: Retrieve relevant documents with scores
        logger.debug(f"Retrieving top {self.retrieval_top_k} relevant chunks...")
        docs_with_scores = self.vector_store.search_with_scores(
            query=question,
            k=self.retrieval_top_k
        )
        
        if not docs_with_scores:
            logger.warning("No relevant documents found")
            return RAGResponse(
                question=question,
                answer="I cannot answer this confidently from the current documentation.",
                sources=[],
                confidence=0.0,
                retrieved_chunks=0
            )
        
        # Extract documents and calculate confidence
        documents = [doc for doc, _ in docs_with_scores]
        confidence = self._calculate_confidence(docs_with_scores)
        
        logger.info(f"Retrieved {len(documents)} chunks, confidence: {confidence:.2f}")
        for idx, (doc, score) in enumerate(docs_with_scores):
            filename = os.path.basename(doc.metadata.get("source", "unknown"))
            logger.debug(f"  [{idx+1}] {filename} (distance: {score:.3f})")
        
        # Step 2: Check confidence threshold
        if confidence < self.confidence_threshold:
            logger.info(f"Confidence {confidence:.2f} below threshold {self.confidence_threshold}")
            return RAGResponse(
                question=question,
                answer="I cannot answer this confidently from the current documentation.",
                sources=self._format_sources(documents),
                confidence=confidence,
                retrieved_chunks=len(documents)
            )
        
        # Step 3: Build context and generate answer
        context = self._build_context(documents)
        
        logger.debug("Generating answer with Groq LLM...")
        try:
            messages = self.prompt.format_messages(
                context=context,
                question=question
            )
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Ensure answer is a string
            if not isinstance(answer, str):
                answer = str(answer)
            
            logger.info(f"Answer generated ({len(answer)} chars)")
        except (ValueError, RuntimeError) as e:
            logger.error(f"Error generating answer: {e}")
            return RAGResponse(
                question=question,
                answer="Error generating answer. Please try again.",
                sources=self._format_sources(documents),
                confidence=confidence,
                retrieved_chunks=len(documents)
            )
        
        # Step 4: Format response
        return RAGResponse(
            question=question,
            answer=answer,
            sources=self._format_sources(documents),
            confidence=confidence,
            retrieved_chunks=len(documents)
        )
    
    def index_documents(self, docs_directory: str, force_reindex: bool = False) -> int:
        """
        Index documents into vector store.
        
        Args:
            docs_directory: Path to directory containing markdown files
            force_reindex: If True, clear existing index first
            
        Returns:
            Number of chunks indexed
        """
        return self.vector_store.index_documents(docs_directory, force_reindex)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get RAG service statistics.
        
        Returns:
            Dictionary with stats
        """
        vector_stats = self.vector_store.get_stats()
        
        return {
            "llm_model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "retrieval_top_k": self.retrieval_top_k,
            "confidence_threshold": self.confidence_threshold,
            "vector_store": vector_stats
        }
    
    def close(self) -> None:
        """Clean up resources."""
        if self.vector_store:
            self.vector_store.close()
            logger.info("RAG service closed")
