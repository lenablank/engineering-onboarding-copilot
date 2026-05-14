# Implementation Details

This document covers RAG pipeline implementation, testing strategy, and deployment plan.

---

## 🧪 RAG Pipeline Implementation Details

### Chunking Strategy

**Approach**: Character-based chunking with recursive splitting

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

**Why this approach:**
- Simple and reliable for mixed documentation formats
- Preserves sentence boundaries where possible
- Small overlap ensures context continuity
- No dependency on markdown structure consistency

**Metadata preservation**:

```python
# LangChain's DirectoryLoader automatically includes source file path
chunk_metadata = {
    "source": "synthetic-docs/2-architecture-overview.md"
}
```

### Retrieval Strategy

**Using LangChain + ChromaDB integration**:

```python
from langchain_chroma import Chroma

# Query using LangChain wrapper (handles embedding automatically)
docs_with_scores = vectorstore.similarity_search_with_score(
    question,
    k=5  # Top 5 most relevant chunks
)

# docs_with_scores is List[Tuple[Document, float]]
# where float is ChromaDB's distance metric (lower = more similar)

# Documents contain:
# - page_content: the chunk text
# - metadata: {"source": "synthetic-docs/file.md"}
```

**Why this approach:**
- LangChain handles embedding generation automatically
- ChromaDB computes cosine similarity
- Returns both content and relevance scores
- Simple, reliable, well-tested integration

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
"""

USER_PROMPT = """Question: {question}

Relevant documentation:
{context_chunks}

Answer the question using ONLY the information above. Cite your sources.
"""
```

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
        Confidence score between 0.0 and 1.0
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

**Confidence Thresholds**:

- `confidence >= 0.70` (70%) → Generate answer with LLM
- `0.11 <= confidence < 0.70` → Log as documentation gap
- `confidence < 0.11` (11%) → Spam filter (generic response, not logged)

**Spam Filtering**: The 11% threshold filters out completely unrelated questions ("What's the weather?", "asdfasdf") while capturing legitimate operational questions that lack documentation ("What's the on-call schedule?").

### Gap Logging Service

```python
import hashlib
from datetime import datetime

def log_gap(
    question: str,
    confidence_score: float,
    retrieval_context: Optional[List[Dict[str, Any]]] = None
) -> None:
    """Log documentation gap to SQLite database."""
    
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

**Gap Status Lifecycle**:
- `NEW` → Newly detected gap
- `REVIEWED` → Acknowledged by team
- `RESOLVED` → Documentation added to address gap

**Note**: Using SHA-256 hash of normalized question for fast duplicate detection and frequency tracking.

---

## 📋 API Data Contracts

**Frontend/Backend Integration Schemas**

### `/ask` Endpoint Response

```json
{
  "answer": "To run the backend locally, first install dependencies with `pip install -r requirements.txt`, then run `uvicorn app.main:app --reload`.",
  "confidence": "high",
  "sources": [
    {
      "file_path": "docs/setup.md",
      "snippet": "## Local Development\n\nInstall dependencies: `pip install -r requirements.txt`"
    },
    {
      "file_path": "README.md",
      "snippet": "Run backend: `uvicorn app.main:app --reload`"
    }
  ],
  "retrieved_chunks": [
    {
      "file_path": "docs/setup.md",
      "relevance_score": 0.87,
      "header_hierarchy": "Setup > Local Development"
    },
    {
      "file_path": "README.md",
      "relevance_score": 0.82,
      "header_hierarchy": "Getting Started"
    }
  ],
  "latency_ms": 1840,
  "gap_logged": false
}
```

### `/api/gaps/` Endpoint Response

```json
[
  {
    "id": "uuid-string",
    "question": "How do we rotate API keys in production?",
    "confidence_score": 0.45,
    "frequency": 5,
    "status": "new",
    "retrieval_context": null,
    "created_at": "2026-02-20T14:30:00Z",
    "updated_at": "2026-02-25T09:15:00Z"
  }
]
```

### `/health` Endpoint Response

```json
{
  "status": "healthy",
  "vector_store_ready": true
}
```

---

## 🛠️ Implementation Sequencing

**Recommended build order to minimize dependency issues:**

1. **Local markdown parsing + chunking** (no LLM calls yet)
   - Read files from `synthetic-docs/`
   - Test chunking logic with fixtures
   - Verify metadata extraction

2. **Chroma indexing + retrieval** (mocked embeddings initially)
   - Set up local Chroma instance
   - Store test embeddings
   - Verify semantic search works

3. **Mocked answer pipeline + citation formatting**
   - Build RAG service with mocked LLM responses
   - Implement citation extraction
   - Test end-to-end with fixtures

4. **Real embeddings + real LLM integration**
   - Cohere embeddings API integration (FREE tier)
   - Add Groq API calls (FREE tier)
   - Test with small corpus
   - Validate thresholds

5. **Gap logging + query logs**
   - Implement confidence detection
   - Add database models
   - Test gap frequency tracking

6. **UI integration** (Ask page, Gap Radar page, Home page)
   - Build frontend components
   - Wire up API calls
   - Handle loading/error states
   - Add Framer Motion animations

7. **CI pipeline**
   - Add GitHub Actions workflow
   - Configure test runs
   - Set up linting

8. **Deployment** (Vercel + Render with SQLite)
   - Deploy backend first (Render with embedded SQLite)
   - Then frontend (Vercel)
   - Test end-to-end on production URLs

---

## 🧪 Testing Strategy

### Test Architecture (Recommended Approach)

**Use test doubles to avoid flaky/expensive live API calls in CI**

### Test Categories

#### **1. Unit Tests (Mocked LLM/Embedding)** - _Fast, Reliable, CI-Safe_

```python
def test_markdown_parsing():
    """Test markdown file parsing."""
    raw_text = "# Header\n\nContent here."
    chunks = parse_and_chunk_markdown(raw_text)
    assert len(chunks) > 0
    assert all(len(chunk) < 2000 for chunk in chunks)

@patch('app.services.embeddings.generate_embedding')  # Mock your wrapper, not vendor SDK
def test_embedding_generation_mocked(mock_embed):
    """Test embedding generation with mocked API."""
    mock_embed.return_value = [0.1] * 1024  # Cohere 1024-dim
    result = generate_embedding("test text")
    assert len(result) == 1024
    mock_embed.assert_called_once()

def test_document_indexing():
    """Test document loading and chunking pipeline."""
    test_docs = load_test_documents('test-docs/')
    index_result = index_documents(test_docs)
    assert index_result.success
    assert index_result.chunks_created > 0
```

#### **2. Integration Tests (Local Chroma + Test Corpus)** - _Real Retrieval Logic_

```python
def test_semantic_search():
    """Test vector search retrieval with real embeddings."""
    # Use test Chroma instance with pre-indexed test corpus
    test_db = setup_test_chroma()

    query = "How do I run tests?"
    results = semantic_search(query, test_db, k=5)

    assert len(results) > 0
    assert all('score' in r for r in results)

@pytest.mark.integration
def test_full_rag_pipeline():
    """Test end-to-end RAG with test corpus."""
    question = "What is our deployment process?"

    response = ask_question(
        question=question,
        vector_db=test_chroma_db,
        llm=mocked_llm  # Still mock LLM to avoid costs
    )

    assert response.answer is not None
    assert len(response.sources) > 0
```

#### **3. Smoke Tests (Optional Live API)** - _Limited, Manual/CI-Skipped_

```python
@pytest.mark.smoke
@pytest.mark.skip_ci
def test_live_groq_call():
    """Test actual Groq API (run manually before deploy, FREE tier)."""
    question = "How do I run the backend locally?"
    response = ask_question_live(question)
    assert response is not None
```

### Regression Test Set

**Maintain canonical test cases** in `tests/fixtures/evaluation_questions.json`:

```json
{
  "answerable": [
    {
      "question": "How do I run the backend locally?",
      "expected_sources": ["README.md", "docs/setup.md"],
      "expected_confidence": "high"
    }
  ],
  "ambiguous": [
    {
      "question": "How do we handle secrets?",
      "expected_confidence": "medium"
    }
  ],
  "gaps": [
    {
      "question": "How do we rotate API keys in production?",
      "expected_behavior": "gap_logged"
    }
  ],
  "failure_modes": [
    {
      "question": "",
      "expected_behavior": "validation_error"
    },
    {
      "question": "[500+ char overlength question...]",
      "expected_behavior": "validation_error"
    },
    {
      "question": "Valid question before sync",
      "expected_behavior": "empty_results_or_safe_error"
    }
  ]
}
```

**Run regression tests in CI**: `pytest -m regression`

**Run smoke tests locally only**: `pytest -m smoke` (skipped in CI with `pytest -m "not smoke"`)

---

### Testing Rationale (For DESIGN_AND_TESTING.md)

**Why This Testing Strategy:**

**1. Mocking LLM calls prevents $50+ CI costs** from 100s of test runs  
**2. Regression set demonstrates production thinking** (metrics-driven quality)  
**3. Multiple test levels catch different bug types** (unit vs integration vs E2E)  
**4. CI-safe by default**: Fast, deterministic, cost-free automated tests  
**5. Manual smoke tests validate production deployment** without blocking CI

### Testing Approach and Rationale

**1. Unit Tests with Mocked LLM/Embedding APIs**

- **What**: Test chunking, validation, business logic in isolation
- **Why**: Avoid flaky/expensive API calls in CI; fast feedback; deterministic results
- **Tool**: pytest with unittest.mock
- **Coverage Target**: >70% backend coverage (focus on business logic, not boilerplate)

**2. Integration Tests with Real Vector DB**

- **What**: Test RAG pipeline end-to-end with local Chroma
- **Why**: Validate retrieval logic works correctly; catch integration bugs between components
- **Tool**: pytest with test fixtures

**3. Frontend Component Tests**

- **What**: React component rendering, user interactions
- **Why**: Ensure UI components work in isolation before integration
- **Tool**: Jest + React Testing Library

**4. End-to-End Smoke Tests**

- **What**: Full user flow testing (Ask → Answer → Gap logging)
- **Why**: Validate complete system integration; catch deployment issues
- **Tool**: Playwright or manual testing

**5. Regression Test Set (20-30 Questions)**

- **What**: Predefined questions with expected behaviors (answerable/gap/citation)
- **Why**: Measure quality metrics (citation rate, latency); detect regressions between sprints; demonstrate systematic evaluation
- **Tool**: Custom evaluation script with automated assertions
- **Citation Requirement**: Answerable responses must include at least one supporting citation and should include inline citations for key factual claims (not strictly every single claim, but major facts)

**6. Optional Live API Smoke Tests**

- **What**: Limited tests with real Groq API (not in CI to avoid free tier rate limits)
- **Why**: Verify production deployment works with real services; validate response quality
- **When**: Manual pre-demo validation only (skipped in CI to preserve free tier quota)

---

## 🚀 Deployment Plan

### Frontend Deployment (Vercel)

1. **Connect GitHub repo to Vercel**
2. **Configure build settings**:
   - Framework: Next.js
   - Build command: `npm run build`
   - Output directory: `.next`
3. **Set environment variables**:
   - `NEXT_PUBLIC_API_URL`: Backend URL (e.g., `https://your-backend.onrender.com`)
4. **Deploy**: Auto-deploys on push to `main`

### Backend Deployment (Render)

1. **Create new Web Service on Render**
2. **Connect GitHub repo**
3. **Configure settings**:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Set environment variables**:
   - `GROQ_API_KEY` (get from console.groq.com, FREE tier)
   - `COHERE_API_KEY` (get from dashboard.cohere.com/api-keys, FREE tier)
   - `CORS_ORIGINS` (frontend URL for production)

**Note**: Both API keys are FREE tier (Groq: 14,400 req/day, Cohere: 1000 req/min)

**Data Persistence**:
- **SQLite database** (`gaps.db`): Persists on Render's disk (documentation gaps with frequency tracking)
- **ChromaDB index**: Re-indexes automatically on startup from `synthetic-docs/` directory (~10-15 seconds)
- **No external database needed**: Zero-config embedded storage, $0 cost

5. **Deploy**: Auto-deploys on push to `main`

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -m "not smoke" --cov --cov-report=xml
      - run: ruff check .

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: npm install
        working-directory: frontend
      - run: npm run lint
        working-directory: frontend
      - run: npm run test
        working-directory: frontend
      - run: npm run build
        working-directory: frontend
```

---

## 🔗 Related Documentation

- [System Architecture](SYSTEM_ARCHITECTURE.md) - Technical design and data models
- [MVP Features](../planning/MVP_FEATURES.md) - What to build
- [Sprint Plan](../planning/SPRINT_PLAN.md) - When to build it
- [Evaluation & Demo](../evaluation/EVALUATION_AND_DEMO.md) - How to validate and present
