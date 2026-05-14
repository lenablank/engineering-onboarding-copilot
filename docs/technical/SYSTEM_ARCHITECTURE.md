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
- **Chunking**: LangChain text splitters
  - MarkdownHeaderTextSplitter (semantic chunking by headers)
  - RecursiveCharacterTextSplitter (split large sections further)

### Data Storage

- **Vector DB**: Chroma (persistent local → cloud)
  - _Why_: Embeddings optimized, semantic search, metadata filtering
- **Relational DB**: SQLite (embedded, gaps.db)
  - _Why_: Structured data (documentation gaps, frequency tracking), zero-config, easy to inspect
  - Tables: documentation_gaps (question, confidence, status, frequency)

### Infrastructure & DevOps

- **Frontend Hosting**: Vercel (free tier)
  - _Why_: Automatic Next.js deployment, global CDN, preview deployments, $0 cost
- **Backend Hosting**: Render or Railway (free tier)
  - _Why_: Free tier supports Python, auto-deploy from GitHub, health checks
- **Database**: Neon Postgres (free tier)
  - _Why_: Serverless Postgres, $0 cost, auto-scaling (within limits)
- **CI/CD**: GitHub Actions
  - _Why_: Native GitHub integration, free for public repos, flexible workflows
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

### QueryLog (Future Enhancement - Not Implemented)

```sql
CREATE TABLE query_logs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT,
    confidence VARCHAR(20),  -- 'high', 'medium', 'low', 'gap'
    sources_used JSONB,      -- [{file_path, snippet}, ...]
    latency_ms INTEGER,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_logs_timestamp (timestamp)
);
```

### DocumentationGap (SQLite)

```sql
CREATE TABLE documentation_gaps (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    question_normalized TEXT NOT NULL,  -- Lowercase, trimmed, for deduplication
    status VARCHAR(20) DEFAULT 'new',  -- 'new', 'reviewed', 'resolved'
    topic_tag VARCHAR(100),             -- 'Local Setup', 'Testing', etc.
    frequency INTEGER DEFAULT 1,        -- Count of times asked
    created_at TIMESTAMPTZ DEFAULT NOW(),
    first_asked TIMESTAMPTZ DEFAULT NOW(),
    last_asked TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT,
    INDEX idx_gaps_status (status),
    INDEX idx_gaps_last_asked (last_asked)
);
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

**Basic semantic search (MVP)**:

```python
from chromadb import Client

# Query vector DB
results = chroma_collection.query(
    query_embeddings=[question_embedding],
    n_results=10,  # Top-k chunks
    include=["documents", "metadatas", "distances"]
)

# Normalize Chroma results into structured objects
rows = []
for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
):
    rows.append({
        "text": doc,
        "metadata": meta,
        "distance": dist,
        "relevance_score": 1 - dist  # Convert distance to score (validate for your metric!)
    })

# Filter by confidence threshold
threshold = 0.3  # Distance threshold (lower = more similar)
confident_results = [
    r for r in rows
    if r['distance'] < threshold
]
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

### Confidence Detection Logic

```python
from datetime import datetime, timezone

def detect_confidence(question: str, retrieved_chunks: list) -> str:
    """
    Evidence-based confidence heuristic for answering question.

    This is NOT a guarantee of correctness, but a gating mechanism
    to reduce unsupported answers by routing low-evidence queries
    to safe fallback behavior.

    Returns: 'high', 'medium', 'low', or 'gap'
    """
    if not retrieved_chunks:
        return 'gap'

    # Normalize Chroma distances to relevance scores
    # Note: Assumes cosine distance metric; validate for your configuration
    for chunk in retrieved_chunks:
        chunk['relevance_score'] = 1 - chunk.get('distance', 0)

    max_score = max(chunk['relevance_score'] for chunk in retrieved_chunks)

    # Check context sufficiency (character count as token proxy)
    total_context_chars = sum(len(chunk['text']) for chunk in retrieved_chunks)
    num_distinct_sources = len(set(chunk['metadata']['file_path'] for chunk in retrieved_chunks))

    # Heuristic decision logic (tune thresholds on eval set)
    if max_score > 0.85 and total_context_chars > 200 and num_distinct_sources >= 1:
        return 'high'
    elif max_score > 0.7 and total_context_chars > 100:
        return 'medium'
    elif max_score > 0.5:
        return 'low'
    else:
        return 'gap'  # Route to gap logging
```

**Important**: Thresholds should be calibrated on your evaluation set. Document chosen values and rationale in `DESIGN_AND_TESTING.md`.

---

### Gap Logging Service

```python
from datetime import datetime, timezone

async def log_documentation_gap(
    question: str,
    confidence: str,
    db: Session
):
    """Log question that couldn't be answered confidently."""

    # Normalize question for better duplicate detection
    question_normalized = question.lower().strip().replace("  ", " ").rstrip("?!.")

    # Check if similar gap already exists (using normalized key)
    existing_gap = db.query(DocumentationGap).filter(
        DocumentationGap.question_normalized == question_normalized
    ).first()

    if existing_gap:
        # Increment frequency
        existing_gap.frequency += 1
        existing_gap.last_asked = datetime.now(timezone.utc)
    else:
        # Create new gap
        new_gap = DocumentationGap(
            question=question,
            question_normalized=question_normalized,
            status='new',
            topic_tag=extract_topic_tag(question),  # Optional
            frequency=1,
            created_at=datetime.now(timezone.utc),
            last_asked=datetime.now(timezone.utc)
        )
        db.add(new_gap)

    db.commit()
```

**Note**: Using `question_normalized` for exact match dedupe improves frequency counts without expensive fuzzy matching. Alternative fuzzy approaches (e.g., `ilike("%...")`) can produce unreliable matches.

---

## 📁 API Endpoints

**Backend REST API**:

- `GET /health` - Health check
- `POST /ask` - Submit question, get answer + citations
- `POST /sync` - Trigger documentation sync
- `GET /sources` - List indexed documents
- `GET /gaps` - List documentation gaps
- `PATCH /gaps/{id}` - Update gap status
- `GET /metrics` - Get observability metrics
- `GET /query-logs` - Get recent query logs (or include in `/metrics`)

### API Response Contracts

#### `POST /ask` Response

```json
{
  "answer": "To run the backend locally, install dependencies with `pip install -r requirements.txt`, then run `uvicorn app.main:app --reload`. [docs/setup.md]",
  "confidence": "high",
  "sources": [
    {
      "file_path": "docs/setup.md",
      "snippet": "## Local Development\n\nInstall dependencies: `pip install -r requirements.txt`",
      "header_hierarchy": "Setup > Local Development"
    },
    {
      "file_path": "README.md",
      "snippet": "Run backend: `uvicorn app.main:app --reload`",
      "header_hierarchy": "Getting Started"
    }
  ],
  "retrieved_chunks": [
    {
      "file_path": "docs/setup.md",
      "relevance_score": 0.87
    },
    {
      "file_path": "README.md",
      "relevance_score": 0.82
    }
  ],
  "latency_ms": 1840,
  "gap_logged": false
}
```

#### Error Responses

**Validation Error** (400):

```json
{
  "error": "validation_error",
  "message": "Question must be between 1 and 500 characters"
}
```

**Index Not Ready** (503):

```json
{
  "error": "index_not_ready",
  "message": "Documentation not yet synced. Please run /sync first."
}
```

**LLM Failure** (500):

```json
{
  "error": "upstream_failure",
  "message": "Unable to generate answer. Please try again."
}
```

---

## 🚀 Deployment Notes

### Chroma Persistence on Render

**Important Caveat**: Render free tier may have ephemeral filesystem behavior. The Chroma vector index stored in `CHROMA_PERSIST_DIRECTORY` may be lost on redeploy/restart.

**MVP Mitigations**:

- **Manual re-sync**: Trigger `/sync` endpoint after each deploy to rebuild index
- **Startup re-index**: Check if index exists on startup; if missing, auto-trigger sync from configured docs source
- **Accepted tradeoff**: Document this as a free-tier limitation in `DESIGN_AND_TESTING.md`

**Note**: Backend writes to Chroma and Postgres synchronously in MVP (no async/best-effort logging to keep implementation simple).

---

**See [SPRINT_PLAN.md](SPRINT_PLAN.md) for week-by-week implementation schedule and [TESTING_AND_EVALUATION_GUIDE.md](TESTING_AND_EVALUATION_GUIDE.md) for testing strategy.**
