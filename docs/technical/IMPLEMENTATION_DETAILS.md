# Implementation Details

This document covers RAG pipeline implementation, testing strategy, and deployment plan.

---

## 🧪 RAG Pipeline Implementation Details

### Chunking Strategy

**Approach**: Semantic chunking by headers (better than fixed-size)

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Split by markdown headers to preserve structure
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

# Then split large sections further
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,      # ~2000 chars (roughly ~400-700 tokens depending on text)
    chunk_overlap=100,   # Preserve context across boundaries
    separators=["\n\n", "\n", " ", ""]
)
```

**Metadata preservation**:

```python
chunk_metadata = {
    "file_path": "docs/setup.md",
    "repo": "engineering-docs",
    "chunk_index": 0,
    "header_hierarchy": "Setup > Installation",  # Display-friendly format
    "last_sync": "2026-02-25T10:30:00Z"
}
```

### Retrieval Strategy

**Hybrid approach** (if time allows stretch goal):

- **Primary**: Semantic search (vector similarity)
- **Optional boost**: Keyword matching for exact terms (e.g., CLI commands, file names)

**Basic retrieval** (MVP):

```python
from chromadb import Client

# Query vector DB
results = chroma_collection.query(
    query_embeddings=[question_embedding],
    n_results=10,
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

### Confidence Detection Logic

```python
def detect_confidence(question: str, retrieved_chunks: list) -> str:
    """
    Determine if we have sufficient evidence to answer question.

    Returns: 'high', 'medium', 'low', 'gap'
    """
    if not retrieved_chunks:
        return 'gap'

    # Check relevance scores (normalized from distance, see retrieval section)
    max_relevance = max(chunk['relevance_score'] for chunk in retrieved_chunks)

    # Check context sufficiency (word count as token proxy)
    total_words = sum(len(chunk['text'].split()) for chunk in retrieved_chunks)

    # Check source diversity
    unique_sources = len(set(chunk['metadata']['file_path'] for chunk in retrieved_chunks))

    # Heuristic thresholds (calibrate on your evaluation set!)
    if max_relevance > 0.85 and total_words > 100 and unique_sources >= 2:
        return 'high'
    elif max_relevance > 0.7 and total_words > 50:
        return 'medium'
    elif max_relevance > 0.5:
        return 'low'
    else:
        return 'gap'
```

**Important Notes**:

- Distance thresholds depend on embedding model and metric (cosine vs. euclidean)
- `relevance_score = 1 - distance` assumes cosine distance; validate for your chosen metric
- Thresholds should be calibrated on your specific evaluation set
- This is a **risk reduction** strategy, not a guarantee of correctness
- Document chosen thresholds and empirical rationale in `DESIGN_AND_TESTING.md`

**Implementation Requirement**:

⚠️ **Before setting final thresholds**: Log raw retrieval outputs (similarity scores, distances) on 20 evaluation queries and calibrate thresholds empirically for your chosen Chroma distance metric. Do not use arbitrary values without validation.

### Gap Logging Service

```python
from datetime import datetime, timezone

async def log_documentation_gap(
    question: str,
    confidence_level: str,
    db: Session
):
    """Log question that couldn't be answered confidently."""

    # Normalize question for better duplicate detection
    question_normalized = question.lower().strip().replace("  ", " ").rstrip("?!.")

    # Check if similar question already exists
    existing_gap = db.query(DocumentationGap).filter(
        DocumentationGap.question_normalized == question_normalized
    ).first()

    if existing_gap:
        # Increment frequency
        existing_gap.frequency += 1
        existing_gap.last_asked = datetime.now(timezone.utc)
    else:
        # Create new gap entry
        new_gap = DocumentationGap(
            question=question,
            question_normalized=question_normalized,
            confidence_level=confidence_level,
            frequency=1,
            status='new',
            topic=extract_topic(question),  # Optional: LLM or rule-based
            created_at=datetime.now(timezone.utc),
            last_asked=datetime.now(timezone.utc)
        )
        db.add(new_gap)

    db.commit()
```

**Note**: Using `question_normalized` for duplicate detection improves frequency aggregation without expensive fuzzy matching. Exact string match on raw question would treat "How do I rotate API keys?" and "How do we rotate API keys in prod?" as separate gaps.

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

### `/sync` Endpoint Response

```json
{
  "status": "success",
  "files_processed": 23,
  "chunks_created": 187,
  "sync_timestamp": "2026-02-25T10:30:00Z",
  "errors": []
}
```

### `/gaps` Endpoint Response

```json
{
  "gaps": [
    {
      "id": 1,
      "question": "How do we rotate API keys in production?",
      "frequency": 5,
      "status": "new",
      "confidence_level": "gap",
      "last_asked": "2026-02-25T09:15:00Z",
      "created_at": "2026-02-20T14:30:00Z"
    }
  ],
  "total": 12
}
```

### `/metrics` Endpoint Response

```json
{
  "avg_latency_ms": 1650,
  "citation_rate": 0.94,
  "answerable_rate": 0.78,
  "total_queries": 342,
  "time_period": "last_7_days"
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
   - HuggingFace embeddings already working (Sprint 0)
   - Add Groq API calls (FREE tier)
   - Test with small corpus
   - Validate thresholds

5. **Gap logging + query logs**
   - Implement confidence detection
   - Add database models
   - Test gap frequency tracking

6. **UI integration** (Ask/Sources/Gaps pages)
   - Build frontend components
   - Wire up API calls
   - Handle loading/error states

7. **CI pipeline**
   - Add GitHub Actions workflow
   - Configure test runs
   - Set up linting

8. **Deployment** (Vercel + Render + Neon)
   - Deploy backend first
   - Then frontend
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
    mock_embed.return_value = [0.1] * 1536
    result = generate_embedding("test text")
    assert len(result) == 1536
    mock_embed.assert_called_once()

def test_github_sync_logic():
    """Test sync pipeline with fixture data."""
    test_docs = load_fixture('test-docs/')
    sync_result = sync_documents(test_docs)
    assert sync_result.success
    assert sync_result.chunks_created > 0
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
   - `DATABASE_URL` (Neon connection string)
   - `CHROMA_PERSIST_DIRECTORY` (e.g., `/opt/render/project/chroma_data`)

**Note**: No API key needed for embeddings (HuggingFace runs locally)

**Chroma Persistence Caveat**: Render free tier may have ephemeral filesystem behavior. If Chroma index is lost on redeploy/restart, use one of these mitigations:

- **MVP approach**: Manual re-sync after deploy via `/sync` endpoint
- **Automated**: Re-index on startup from configured docs source (adds startup latency)
- **Persistent disk**: Mount persistent volume if available (may not be free-tier)

5. **Deploy**: Auto-deploys on push to `main`

### Database Setup (Neon)

1. **Create Neon project** (free tier)
2. **Run migration SQL**:
   ```sql
   CREATE TABLE query_logs (...);
   CREATE TABLE documentation_gaps (...);
   CREATE TABLE sync_history (...);
   ```
3. **Copy connection string** to Render env vars

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
