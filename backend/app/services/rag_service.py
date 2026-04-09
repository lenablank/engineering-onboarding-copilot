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
    DEFAULT_MAX_TOKENS = 1000
    DEFAULT_RETRIEVAL_TOP_K = 5
    DEFAULT_CONFIDENCE_THRESHOLD = 0.7
    
    # Confidence calculation thresholds
    MIN_CONTEXT_WORDS = 50  # Minimum words in retrieved context
    MIN_SOURCES = 1  # Minimum unique source files (1 comprehensive source is fine)
    MIN_SIMILARITY_SCORE = 0.3  # Minimum similarity for any chunk
    
    # Fallback response message
    FALLBACK_MESSAGE = "I can only answer questions about the engineering documentation and processes in this knowledge base. This question appears to be outside that scope."
    
    # System prompt - sources are displayed separately in the UI
    SYSTEM_PROMPT = """You are a helpful engineering documentation assistant for an onboarding system.

Your role is to answer questions about engineering processes, tools, and practices using ONLY the provided documentation context.

CRITICAL RULES:
1. **USE THE PROVIDED CONTEXT** - The documentation chunks below contain the information you need
2. For BROAD questions, provide a comprehensive overview with key details from the context
3. For SPECIFIC questions, provide complete step-by-step answers with all relevant details
4. If the question is COMPLETELY outside the documentation scope (e.g., weather, sports), respond EXACTLY: "I can only answer questions about the engineering documentation and processes in this knowledge base. This question appears to be outside that scope."
5. **NEVER say "not provided in the context" if information IS in the context** - read carefully!
6. **NEVER make up or reference documents that aren't provided** - stick to what's in the context
7. **NEVER mention document numbers** - no "Document 1", "Documents 1-5", "across multiple documents", etc.
8. **NO meta-commentary about sources** - focus on the answer content only; the UI shows sources separately
9. Include all relevant commands, examples, and configuration details from the documentation
10. Structure multi-step answers clearly with numbered lists
11. Be CONFIDENT and COMPLETE when answering from the provided context

Example - GOOD answer for "How do I deploy?":
"We maintain three environments:
- Development (localhost:3000) for local development
- Staging (staging.company.com) auto-deploys on merge to develop
- Production (app.company.com) requires manual promotion

Deployment process:
1. Development → Staging (Automatic): Merge to develop triggers GitHub Actions, runs tests, builds Docker images...
2. Staging → Production (Manual): Verify staging, create release PR, get 2 approvals, merge to main, run deployment workflow..."

Example - BAD answer (DO NOT DO THIS):
"The documentation does not provide details... you would need to refer to [some-other-doc.md] not provided..."
"This is mentioned in Documents 1-3..."
"According to the provided context..."

Remember: If information IS in the context, present it confidently and completely!

Example of a complete answer:
"To set up PostgreSQL for local development:

1. Install PostgreSQL 15:
   - macOS: `brew install postgresql@15 && brew services start postgresql@15`
   - Windows: Download installer from https://postgresql.org/download/windows/

2. Create database user:
   ```bash
   createuser -P appuser
   # Enter password when prompted
   ```

3. Create database:
   ```bash
   createdb -O appuser engineering_copilot_dev
   ```

4. Add to your `.env` file:
   ```bash
   DATABASE_URL=postgresql://appuser:password@localhost:5432/engineering_copilot_dev
   DB_POOL_SIZE=5
   DB_MAX_OVERFLOW=10
   ```

5. Verify connection:
   ```bash
   psql -U appuser -d engineering_copilot_dev -h localhost
   ```"

Remember: Be confident with documented information. Only use the fallback when the question truly cannot be answered from the context.
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

Answer:""")
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
        # ChromaDB distance calibration (empirically: 0.0=perfect, ~0.9=moderate, 2.0=no match)
        # Convert to similarity percentage: similarity = max(0, (2 - distance) / 2)
        raw_distances = [score for _, score in documents_with_scores]
        similarities = [max(0, (2 - score) / 2) for _, score in documents_with_scores]
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
        # - Similarity: 50% (primary - how well docs match question)  
        # - Source diversity: 25% (having relevant sources)
        # - Context sufficiency: 25% (enough context for complete answer)
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
    
    def _create_fallback_response(
        self,
        question: str,
        documents: Optional[List[Document]] = None,
        confidence: float = 0.0
    ) -> RAGResponse:
        """
        Create a fallback response when unable to answer confidently.
        
        Args:
            question: Original question
            documents: Retrieved documents (if any) - not used in fallback
            confidence: Calculated confidence score
            
        Returns:
            RAGResponse with fallback message and no sources
        """
        # Don't show sources for fallback responses - they're irrelevant
        return RAGResponse(
            question=question,
            answer=self.FALLBACK_MESSAGE,
            sources=[],  # Empty sources - question is out of scope
            confidence=confidence,
            retrieved_chunks=0
        )
    
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
            return self._create_fallback_response(question)
        
        # Extract documents and calculate confidence
        documents = [doc for doc, _ in docs_with_scores]
        confidence = self._calculate_confidence(docs_with_scores)
        
        logger.info(f"Retrieved {len(documents)} chunks, confidence: {confidence:.2f}")
        for idx, (doc, score) in enumerate(docs_with_scores):
            filename = os.path.basename(doc.metadata.get("source", "unknown"))
            logger.debug(f"  [{idx+1}] {filename} (distance: {score:.3f})")
        
        # Step 2: Check confidence threshold (gating mechanism)
        if confidence < self.confidence_threshold:
            logger.info(
                f"Confidence {confidence:.2f} below threshold {self.confidence_threshold}. "
                "Returning fallback response to prevent hallucination."
            )
            # Set confidence to near-zero for fallback (question is out of scope)
            fallback_confidence = 0.05  # 5% - signals complete uncertainty
            return self._create_fallback_response(
                question=question,
                documents=documents,
                confidence=fallback_confidence
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
