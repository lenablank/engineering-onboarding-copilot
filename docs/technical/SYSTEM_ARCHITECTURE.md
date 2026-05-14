# System Architecture & Implementation Guide

**Technical design and RAG pipeline details for Engineering Onboarding Copilot**

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (Web Browser)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FRONTEND (Next.js + TypeScript)                 │
│  ┌──────────┬────────────────┬──────────────────────────────┐   │
│  │ Ask Page │ Gaps Dashboard │ Global Layout & Navigation   │   │
│  └──────────┴────────────────┴──────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 BACKEND (Python + FastAPI)                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      API Endpoints                           ││
│  │  /ask, /api/gaps, /health                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Core Services                             ││
│  │  • Vector Store Service (local markdown → chunks)           ││
│  │  • RAG Service (query → answer + citations)                 ││
│  │  • Gap Detection Service (confidence → log gaps)            ││
│  └─────────────────────────────────────────────────────────────┘│
└───────────────┬─────────────────────────┬───────────────────────┘
                │                         │
                ▼                         ▼
┌───────────────────────────┐  ┌──────────────────────────────────┐
│  VECTOR DB (Chroma)       │  │  SQLite (embedded, gaps.db)      │
│  • Document chunks        │  │  • Documentation gaps            │
│  • Embeddings (1024-dim)  │  │  • Gap frequency tracking        │
│  • Metadata (file paths)  │  │  • Gap status (NEW/REVIEWED)     │
└───────────────────────────┘  └──────────────────────────────────┘
                ▲
                │
                │ LLM API (Sprint 1+)
                ▼
┌─────────────────────────────────────────────────────────────────┐
│     FREE STACK: Groq API (Llama-3.1-8b) + Cohere API            │
│  • Embeddings: Cohere embed-english-v3.0 (1024-dim, API, $0)    │
│  • LLM: Groq Llama-3.1-8b-instant (14,400 requests/day free)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagrams

### Question Answering Flow

```
User Question
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Question Preprocessing                                        │
│    • Clean input, detect intent                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Embedding Generation                                          │
│    • Cohere embed-english-v3.0 (API-based, FREE tier)            │
│    • Convert question → 1024-dim vector                          │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Semantic Search (Vector DB)                                   │
│    • Retrieve top-k chunks (k=5-10)                              │
│    • Get similarity scores + metadata                            │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Confidence Check                                              │
│    • If max_score < threshold (e.g., 0.7) → FLAG AS GAP         │
│    • If context insufficient → FLAG AS GAP                       │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
                    ┌───────┴────────┐
                    │                │
        HIGH CONFIDENCE              LOW CONFIDENCE
                    │                │
                    ▼                ▼
┌────────────────────────────┐  ┌──────────────────────────────┐
│ 5a. Answer Generation      │  │ 5b. Gap Logging              │
│ • Groq Llama-3-8b prompt   │  │ • Log question to gaps table │
│ • Include retrieved chunks │  │ • Return safe fallback       │
│ • Enforce citation format  │  │ • Suggest manual answer      │
└──────────┬─────────────────┘  └──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Response Assembly                                             │
│    • Answer text                                                 │
│    • Source citations (file paths, line ranges)                  │
│    • Retrieved snippets                                          │
│    • Confidence indicator                                        │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
                      Return to User
```

### Documentation Indexing Flow

```
Application Startup (Automatic)
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Local File Access                                             │
│    • Load markdown files from synthetic-docs/ directory          │
│    • Use LangChain DirectoryLoader with glob pattern **/*.md    │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Document Processing                                           │
│    • Read file contents with UTF-8 encoding                      │
│    • Preserve markdown formatting and structure                  │
│    • Extract file paths as metadata                              │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Chunking Strategy                                             │
│    • RecursiveCharacterTextSplitter (LangChain)                  │
│    • Chunk size: 500 characters                                  │
│    • Overlap: 50 characters                                      │
│    • Separators: ["\n\n", "\n", " ", ""]                        │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Embedding Generation                                          │
│    • Cohere embed-english-v3.0 (API-based, FREE tier)            │
│    • 1024-dimensional vectors                                    │
│    • Cost: $0 (free tier: 1000 requests/min)                     │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. Vector DB Indexing                                            │
│    • Store chunks + embeddings in ChromaDB                       │
│    • Store metadata: {source: file_path}                         │
│    • Create persistent searchable index                          │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
                  Indexing Complete ✓
                (Ready to answer questions)
```

---

## 🛠️ Technology Stack (Detailed)

### Frontend Stack

- **Framework**: Next.js 14 (App Router)
  - _Why_: Modern React framework with built-in routing, SSR capabilities, excellent Vercel integration
- **Language**: TypeScript
  - _Why_: Type safety, better IDE support, catches bugs at compile time
- **Styling**: Tailwind CSS
  - _Why_: Utility-first, fast prototyping, consistent design system
- **UI Components**: shadcn/ui (optional)
  - _Why_: Clean, accessible components without bloated dependencies
- **State Management**: React hooks (useState, useEffect)
  - _Why_: Simple state needs, no Redux overhead for MVP
- **API Client**: fetch or Axios
  - _Why_: Native or lightweight HTTP client for REST API calls

### Backend Stack

- **Framework**: FastAPI (Python 3.11+)
  - _Why_: Fast, async-capable, automatic API docs, excellent Python AI library ecosystem
- **API Design**: RESTful JSON APIs
  - _Why_: Simpler than GraphQL for small API surface, better for demo
- **CORS**: FastAPI CORS middleware
  - _Why_: Enable frontend-backend communication across origins
- **Logging**: Python logging module
  - _Why_: Built-in, sufficient for observability needs
- **Environment**: python-dotenv
  - _Why_: Secure environment variable management

### AI/ML Stack

- **LLM**: Groq Llama-3.1-8b-instant (FREE tier)
  - _Why_: FREE tier with 14,400 requests/day, extremely fast inference, cost-conscious engineering
  - _Cost_: $0 for entire project
  - _Note_: Demonstrates that production-quality AI systems can be built without expensive infrastructure
- **Embeddings**: Cohere embed-english-v3.0 (API-based, FREE tier)
  - _Why_: API-based, 1024 dimensions (better quality than 384-dim local models), free tier sufficient
  - _Cost_: FREE (1000 requests/min)
  - _Dimensions_: 1024 (vs 384 for local models, better semantic understanding)
- **Orchestration**: LangChain
  - _Why_: RAG chains, prompt templates, proven patterns for production RAG
- **Vector Database**: Chroma
  - _Why_: Local-first (easy development), persistent storage, Python-native, free
- **Chunking**: LangChain RecursiveCharacterTextSplitter
  - _Why_: Character-based chunking with recursive splitting, 500 char chunks, 50 char overlap

### Data Storage

- **Vector DB**: Chroma (persistent local → cloud)
  - _Why_: Embeddings optimized, semantic search, metadata filtering
- **Relational DB**: SQLite (embedded, gaps.db)
  - _Why_: Structured data (documentation gaps, frequency tracking), zero-config, easy to inspect
  - Tables: documentation_gaps (question, confidence, status, frequency)

### Infrastructure & DevOps

- **Frontend Hosting**: Vercel (free tier)
  - _Why_: Automatic Next.js deployment, global CDN, preview deployments, $0 cost
- **Backend Hosting**: Render (free tier)
  - _Why_: Free tier supports Python, auto-deploy from GitHub, health checks
- **Database**: SQLite (embedded)
  - _Why_: Zero-config, embedded database, no external service needed, $0 cost
- **CI/CD**: None (manual deployments)
  - _Why_: Automatic deployments via Vercel/Render GitHub integration
- **Version Control**: GitHub
  - _Why_: Industry standard, facilitates collaboration and CI/CD
- **Environment Secrets**: GitHub Secrets + hosting platform env vars
  - _Why_: Secure secret management, no hardcoded keys

### Development Tools

- **Package Management**: npm/pnpm (frontend), pip + venv (backend)
- **Linting**: ESLint (frontend), ruff or flake8 (backend)
- **Formatting**: Prettier (frontend), black (backend)
- **Testing**: Jest/Vitest (frontend), pytest (backend)
- **API Testing**: Postman or Thunder Client (manual testing)

---

## 📊 Data Models

### DocumentChunk (Chroma Vector DB)

```python
{
    "id": "unique_chunk_id",
    "text": "chunk text content...",
    "embedding": [0.123, -0.456, ...],  # 1024-dim vector (Cohere)
    "metadata": {
        "source": "synthetic-docs/2-architecture-overview.md"
    }
}
```

### QueryLog (Not Implemented)

_Future enhancement: Query logging for analytics and observability._

### DocumentationGap (SQLite)

```python
from sqlalchemy import String, Float, Integer, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from datetime import datetime
import uuid

class GapStatus(str, enum.Enum):
    """Status of a documentation gap."""
    NEW = "new"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"

class DocumentationGap(Base):
    """Model for storing documentation gaps in SQLite."""
    __tablename__ = "documentation_gaps"
    
    # Primary key - UUID as string for SQLite
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    
    # The question that triggered low confidence
    question: Mapped[str] = mapped_column(String(500), index=True)
    
    # Hash of normalized question for fast duplicate detection
    question_hash: Mapped[Optional[str]] = mapped_column(String(64), index=True, default=None)
    
    # Confidence score (0.0 to 1.0)
    confidence_score: Mapped[float] = mapped_column(Float)
    
    # Frequency counter
    frequency: Mapped[int] = mapped_column(Integer, default=1, index=True)
    
    # Status tracking
    status: Mapped[GapStatus] = mapped_column(
        SQLEnum(GapStatus),
        default=GapStatus.NEW,
        index=True
    )
    
    # Optional: Store retrieval context as JSON
    retrieval_context: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON, default=None)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```



---

## 🧪 RAG Pipeline Implementation Details

### Chunking Strategy

**Character-based chunking with recursive splitting**:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split documents into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # 500 characters per chunk
    chunk_overlap=50,     # 50 character overlap between chunks
    length_function=len,
    separators=["\n\n", "\n", " ", ""]  # Try paragraph, then line, then word, then character
)
```

**Metadata preservation**:

```python
# LangChain's DirectoryLoader automatically includes source file path
chunk_metadata = {
    "source": "synthetic-docs/2-architecture-overview.md"
}
```

---

### Retrieval Strategy

**Semantic search using LangChain + ChromaDB**:

```python
from langchain_chroma import Chroma

# Query using LangChain wrapper (handles embedding automatically)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}  # Top 5 chunks
)

# Retrieve with scores
docs_with_scores = vectorstore.similarity_search_with_score(
    question,
    k=5
)

# docs_with_scores is List[Tuple[Document, float]]
# where float is ChromaDB's distance metric (lower = more similar)
```

---

### Answer Generation Prompt

```python
SYSTEM_PROMPT = """You are an engineering onboarding assistant for a software company.

Your role:
- Answer questions about engineering processes, setup, and workflows
- Use ONLY the provided documentation chunks
- Cite sources for every claim (use [file_path] format)
- If the documentation doesn't contain the answer, say "I cannot answer this confidently from the current documentation"
- Do NOT make up information
- Be concise but complete

Format your answer:
1. Direct answer to the question
2. Supporting details with citations
3. List of sources used at the end

Citation requirement: Include at least one supporting citation and cite key factual claims inline.
"""

USER_PROMPT = """Question: {question}

Relevant documentation:
{context_chunks}

Answer the question using ONLY the information above. Cite your sources.
"""
```

---

### Confidence Calculation

```python
def _calculate_confidence(
    self,
    documents_with_scores: List[Tuple[Document, float]]
) -> float:
    """
    Calculate confidence score based on retrieval quality.
    
    Factors:
    1. Similarity scores (higher = better)
    2. Number of unique sources (more = better)
    3. Context sufficiency (enough words retrieved)
    
    Returns:
        Confidence score between 0 and 1
    """
    if not documents_with_scores:
        return 0.0
    
    # ChromaDB distance calibration: 0.0=perfect, ~0.9=moderate, 2.0=no match
    # Convert to similarity: similarity = max(0, (2 - distance) / 2)
    similarities = [max(0, (2 - score) / 2) for _, score in documents_with_scores]
    avg_similarity = sum(similarities) / len(similarities)
    
    # Check minimum similarity threshold
    if avg_similarity < 0.3:  # MIN_SIMILARITY_SCORE
        return round(avg_similarity * 0.5, 2)  # Penalize low similarity
    
    # Unique sources count
    unique_sources = set(
        doc.metadata.get("source", "unknown") 
        for doc, _ in documents_with_scores
    )
    source_diversity = min(len(unique_sources) / 1, 1.0)  # MIN_SOURCES = 1
    
    # Context sufficiency (total words)
    total_words = sum(
        len(doc.page_content.split()) 
        for doc, _ in documents_with_scores
    )
    context_sufficiency = min(total_words / 50, 1.0)  # MIN_CONTEXT_WORDS = 50
    
    # Weighted combination:
    # - Similarity: 50% (how well docs match question)
    # - Source diversity: 25%
    # - Context sufficiency: 25%
    confidence = (
        0.5 * avg_similarity +
        0.25 * source_diversity +
        0.25 * context_sufficiency
    )
    
    return round(confidence, 2)
```

**Confidence gating**:
- If `confidence >= 0.70` (70%) → Generate answer with LLM
- If `0.11 <= confidence < 0.70` → Check if engineering-related, log as gap
- If `confidence < 0.11` (11%) → Spam filter, generic response

---

### Gap Logging

```python
import hashlib
from datetime import datetime

def log_gap(
    question: str,
    confidence_score: float,
    retrieval_context: Optional[List[Dict[str, Any]]] = None
) -> None:
    """
    Log documentation gap to SQLite database.
    
    Uses question_hash for deduplication - increments frequency if exists.
    """
    # Create hash for deduplication
    question_hash = hashlib.sha256(
        question.lower().strip().encode('utf-8')
    ).hexdigest()
    
    # Check if gap already exists
    existing_gap = db.query(DocumentationGap).filter(
        DocumentationGap.question_hash == question_hash
    ).first()
    
    if existing_gap:
        # Increment frequency
        existing_gap.frequency += 1
        existing_gap.updated_at = datetime.utcnow()
    else:
        # Create new gap
        new_gap = DocumentationGap(
            question=question,
            question_hash=question_hash,
            confidence_score=confidence_score,
            status=GapStatus.NEW,
            frequency=1,
            retrieval_context=retrieval_context,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_gap)
    
    db.commit()
```

---

## 📁 API Endpoints

**Backend REST API**:

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `POST /ask` - Submit question, get answer with citations
- `GET /api/gaps/` - List all documentation gaps
- `GET /api/gaps/{id}` - Get specific gap
- `GET /api/gaps/stats` - Get gap statistics
- `PATCH /api/gaps/{id}/status` - Update gap status
- `DELETE /api/gaps/{id}` - Delete gap
- `GET /docs/{filename}` - Retrieve documentation file

### API Response Contracts

#### `POST /ask` Response

```json
{
  "question": "How do I run the backend locally?",
  "answer": "To run the backend locally:\n\n1. Install dependencies: `pip install -r requirements.txt`\n2. Create .env file with API keys\n3. Run: `uvicorn app.main:app --reload`\n\nThe backend will be available at http://localhost:8000",
  "sources": [
    {
      "source": "synthetic-docs/1-getting-started.md",
      "content": "## Local Development\n\nInstall dependencies: `pip install -r requirements.txt`...",
      "score": 0.87
    }
  ],
  "confidence": 0.85,
  "retrieved_chunks": 3
}
```

#### Error Responses

**Validation Error** (422):

```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Service Error** (500):

```json
{
  "detail": "Internal server error"
}
```

---

## 🚀 Deployment

### Architecture

- **Frontend**: Vercel (Next.js, automatic deployments from main branch)
- **Backend**: Render (FastAPI, automatic deployments from main branch)
- **Database**: SQLite (embedded in backend, `gaps.db` file)
- **Vector DB**: ChromaDB (embedded in backend, `chroma_db/` directory)

### Data Persistence

**Important**: Both Render and Vercel free tiers have ephemeral filesystems:

- **ChromaDB index**: Regenerated on application startup (indexing happens automatically)
- **SQLite database**: Persistent on Render (stored in persistent volume)

### Environment Variables

Required on Render:

```bash
COHERE_API_KEY=your_cohere_api_key
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///./gaps.db
```

### Cold Start Behavior

On first request after deploy:
1. Backend initializes ChromaDB
2. Indexes all files from `synthetic-docs/` directory (automatic)
3. Creates SQLite database if doesn't exist
4. System ready to answer questions

Indexing takes ~10-15 seconds on startup.
