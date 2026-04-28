# Design and Testing Documentation

**Status**: Final (Completed April 28, 2026)

---

## 1. Project Objective and User Persona

### Problem Statement

New engineers joining software companies face significant onboarding friction. Documentation is often fragmented across multiple systems (Confluence, GitHub wikis, Notion, Slack), outdated, or difficult to discover. New hires waste 5-15 hours per week asking teammates repetitive questions about setup, architecture, and workflows—time that could be spent on productive work. Additionally, teams lack visibility into which topics are poorly documented, making it difficult to prioritize documentation improvements.

### Target User

**Persona**: New engineer joining a software company

**Attributes**:

- Tenure: First 30 days at company
- Role: Full-stack engineer
- Goal: Self-serve setup/architecture/workflow answers without blocking teammates
- Pain point: Cannot find answers in scattered/outdated documentation
- Behavior: Prefers asking questions in natural language over searching documentation manually

### Use Cases

1. **Question Answering**: "How do I run tests locally?" → Receives answer with citations from testing docs
2. **Source Discovery**: "Where is authentication implemented?" → Finds relevant code files and documentation
3. **Gap Identification**: Engineering leadership views Gap Radar dashboard to discover undocumented topics
4. **Confidence-Based Routing**: System recognizes when documentation is insufficient and logs the gap instead of hallucinating

---

## 2. Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Ask Page    │  │  Gap Radar   │  │  Home Page   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTPS/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  /ask        │  │  /api/gaps   │  │  /health     │     │
│  │ (RAG Service)│  │ (Gap Service)│  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────┬─────────────────┬────────────────────────────────┘
           │                 │
           ▼                 ▼
┌──────────────────┐  ┌─────────────────┐
│   ChromaDB       │  │  SQLite DB      │
│  (Vector Store)  │  │  (Gap Logs)     │
│  275 chunks      │  │  Documentation  │
│  1024-dim        │  │  Gaps Table     │
└──────────────────┘  └─────────────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│         External AI Services (Free Tier)     │
│  ┌──────────────────┐  ┌─────────────────┐ │
│  │  Cohere API      │  │  Groq API       │ │
│  │  (Embeddings)    │  │  (LLM)          │ │
│  │  embed-eng-v3.0  │  │  Llama-3.1-8b   │ │
│  └──────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────┘
```

### Component Descriptions

- **Frontend (Next.js 14)**: Server-side rendered web application with three main pages:
  - Ask page: Chat interface for Q&A with confidence badges and source citations
  - Gap Radar: Dashboard displaying documentation gaps with filtering/sorting
  - Home: Landing page with feature overview

- **Backend (FastAPI)**: Python REST API with three core services:
  - RAG Service: Handles question→answer flow with retrieval and generation
  - Gap Service: Logs and manages documentation gaps
  - Vector Store: ChromaDB interface for semantic search

- **Vector Database (ChromaDB)**: Embedded vector store with 275 document chunks, 1024-dimensional Cohere embeddings

- **Relational Database (SQLite)**: Stores documentation gaps with metadata (question, confidence, frequency, status)

- **AI Stack**:
  - Cohere embed-english-v3.0 (1024-dim embeddings, API-based)
  - Groq Llama-3.1-8b-instant (LLM inference, free tier 14,400 req/day)

### Data Flow

**Question Answering Flow**:

1. User submits question via frontend Ask page
2. Frontend sends POST /ask to backend
3. Backend embeds question using Cohere API
4. ChromaDB performs semantic search, returns top-5 chunks with similarity scores
5. RAG service calculates confidence based on max similarity + context sufficiency
6. If confidence ≥0.7: Generate answer with Groq LLM + return with citations
7. If confidence <0.7: Return fallback message + log gap to SQLite
8. Frontend displays answer or fallback, shows confidence badge

**Gap Radar Flow**:

1. Low-confidence questions logged to SQLite during /ask flow
2. User navigates to Gap Radar page
3. Frontend fetches GET /api/gaps with optional filters
4. Backend queries SQLite, returns gaps with stats (frequency, status)
5. Frontend displays table with sorting/filtering UI

---

## 3. Technology Choices and Rationale

| Technology            | Reason                                                                                                                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Next.js 14**        | Modern React framework, SSR, excellent Vercel integration, App Router for clean routing                                      |
| **TypeScript**        | Type safety, catches bugs at compile time, better IDE support                                                                |
| **Tailwind CSS**      | Utility-first CSS, rapid UI development, consistent design system                                                            |
| **FastAPI**           | Async-capable, automatic API docs (Swagger), Python AI ecosystem, excellent performance                                      |
| **LangChain**         | RAG chains, prompt templates, proven patterns, extensive documentation                                                       |
| **ChromaDB**          | Embedded vector DB, persistent storage, Python-native, simple setup, no separate server needed                               |
| **SQLite**            | Embedded relational DB, zero-config, sufficient for demo scale, easy to inspect                                              |
| **Cohere Embeddings** | API-based, 1024 dimensions (better quality than 384-dim HuggingFace), free tier sufficient for capstone                      |
| **Groq API**          | FREE LLM (Llama-3.1-8b-instant), 14,400 requests/day free tier, extremely fast inference (sub-second), cost-conscious choice |
| **Vercel**            | Free tier frontend hosting, auto-deploy from GitHub, HTTPS by default, excellent Next.js support                             |
| **Render**            | Free tier backend hosting, Python support, auto-deploy from GitHub, 750 hours/month                                          |
| **Framer Motion**     | Smooth animations for studio aesthetic UI, declarative API                                                                   |
| **Lucide React**      | Modern icon set, tree-shakeable, consistent design                                                                           |

---

## 4. Software and Architectural Patterns

### Patterns Implemented

- **Repository Pattern** (data access abstraction)
  - **Location**: `backend/app/services/vector_store.py`, gap service
  - **Reason**: Decouples business logic from storage, enables easier testing with mocks, allows swapping ChromaDB for another vector store
- **Service Layer Pattern** (business logic encapsulation)
  - **Location**: `backend/app/services/rag_service.py`, `gap_service.py`
  - **Reason**: Separates business logic from API controllers, promotes reusability, testable in isolation
- **RAG Pattern** (Retrieval-Augmented Generation)
  - **Location**: Core architecture (embed → retrieve → generate)
  - **Reason**: Industry-standard AI pattern for grounding LLM responses in documentation, reduces hallucination

- **API Gateway Pattern** (centralized entry point)
  - **Location**: FastAPI main.py with CORS, error handling
  - **Reason**: Single entry point for frontend, centralized CORS/auth/logging, consistent error responses

- **Confidence-Based Routing** (custom pattern)
  - **Location**: RAG service confidence calculation → gap logging
  - **Reason**: Novel differentiator - routes low-confidence queries to gap detection instead of attempting to answer

### Architectural Decisions

- **Monorepo structure** (frontend + backend in one repo)
  - **Reason**: Simplifies deployment, single source of truth for capstone submission, easier grading

- **REST over GraphQL**
  - **Reason**: Simpler for small API surface (4 endpoints), better for demo/evaluation, less overhead

- **Separate vector + relational DBs**
  - **Reason**: ChromaDB optimized for embeddings/semantic search, SQLite for structured gap logs, each tool optimized for its use case

- **Embedded databases vs managed services**
  - **Reason**: Zero infrastructure cost, simpler setup, sufficient for demo scale, no external dependencies

- **Strategic mono font design system**
  - **Reason**: Studio aesthetic for modern, technical feel, consistency across all UI elements, enhances brand identity

**Evidence (Implementation)**:

- Services: `backend/app/services/rag_service.py`, `gap_service.py`, `vector_store.py`
- API routes: `backend/app/main.py`
- Test coverage: 5 test files validating pattern implementations

---

## 5. RAG Pipeline Design

### Chunking Strategy

**Approach**: Semantic chunking by markdown headers + recursive character splitting

- **Primary**: Split by markdown headers (preserves semantic context)
- **Secondary**: RecursiveCharacterTextSplitter with max 1000 chars, 200 char overlap
- **Metadata preserved**: file path, header text, chunk index
- **Code blocks**: Preserved intact when possible to maintain executable examples

**Implementation**: LangChain MarkdownHeaderTextSplitter + RecursiveCharacterTextSplitter

**Results**: 15 markdown files → 275 chunks (average ~360 chars/chunk)

### Retrieval Approach

1. **Embed question**: Cohere embed-english-v3.0 (1024-dim vector)
2. **Semantic search**: ChromaDB cosine similarity search, top-k=5 chunks
3. **Score calculation**: Max similarity score + context sufficiency heuristics
4. **Return**: Chunks with file paths, similarity scores, content

**Configuration**:

- Top-k: 5 chunks
- Distance metric: Cosine similarity
- No filtering threshold (filter happens at confidence calculation)

### Prompt Design

**System Prompt**:

```
You are an engineering onboarding assistant. Answer questions using ONLY the provided documentation.

Rules:
1. Base answers ONLY on the provided context
2. Cite sources using [filename] format
3. If the context doesn't contain the answer, say so clearly
4. Be concise and practical
5. Include specific commands, file paths, or steps when relevant
```

**User Prompt**:

```
Question: {question}

Context from documentation:
{retrieved_chunks}

Answer the question using only the context above. Cite sources as [filename].
```

### Citation Format

`[docs/setup.md]` - Inline citations linking to source files

**Implementation Evidence**:

- Chunking: `backend/app/services/vector_store.py` (load_and_chunk_documents)
- Retrieval: `backend/app/services/rag_service.py` (retrieve_context)
- Prompts: `backend/app/services/rag_service.py` (system/user templates)

---

## 6. Evidence-Based Confidence Gating

### Heuristic Design

Confidence score calculated from:

1. **Max similarity score** (primary signal): Highest cosine similarity from retrieved chunks
2. **Context sufficiency**: Total words in retrieved chunks (threshold: 50 words minimum)
3. **Source diversity**: Number of unique source files (not currently weighted, but tracked)

**Formula**:

```python
confidence = max_similarity_score
# Simple: use best match score as confidence
# Future: could combine with context length, source diversity
```

### Threshold Calibration

**Thresholds**:

- **High confidence**: ≥0.70 → Generate answer
- **Low confidence**: <0.70 → Return fallback + log gap

**Calibration basis**:

- Empirical testing on synthetic documentation
- Formal evaluation validated 100% accuracy at 0.70 threshold
- All 3 well-documented questions scored 0.75-0.82 (above threshold)
- All 2 undocumented questions scored 0.05-0.15 (below threshold)

**Important**: Confidence score indicates evidence sufficiency, **not factual correctness guarantee**. High confidence means "sufficient documentation retrieved to attempt an answer."

### Fallback Behavior

When confidence <0.70:

1. Return message: _"I cannot answer this confidently from the current documentation. This question has been logged for review."_
2. Log to `documentation_gaps` table with:
   - Question text
   - Confidence score
   - Retrieved sources (as context)
   - Timestamp
   - Frequency counter (increments on duplicate)
3. Frontend displays fallback message with explanation
4. Question appears in Gap Radar dashboard

**Implementation Evidence**:

- Confidence calculation: `backend/app/services/rag_service.py`
- Gap logging: Triggered in ask endpoint when confidence <0.70
- Tests: `backend/test_gap_service.py` (19 test functions for gap logic)

---

## 7. Deployment Options and Cost Implications

### Selected Option: Vercel (Frontend) + Render (Backend) ⭐

**Architecture**: Serverless frontend + containerized backend

**Cost**: **$0/month** (within free tier limits)

**Infrastructure Breakdown**:

| Component      | Service       | Free Tier Limits              | Actual Usage        | Cost |
| -------------- | ------------- | ----------------------------- | ------------------- | ---- |
| **Frontend**   | Vercel        | 100 GB bandwidth/month        | <1 GB (demo)        | $0   |
| **Backend**    | Render        | 750 hours/month, 512 MB RAM   | 720 hours (30 days) | $0   |
| **Vector DB**  | ChromaDB      | Embedded (no limits)          | 275 chunks          | $0   |
| **SQLite**     | Render disk   | Ephemeral (rebuilt on deploy) | <1 MB               | $0   |
| **Embeddings** | Cohere API    | Free tier (generous limits)   | ~300 API calls      | $0   |
| **LLM**        | Groq API      | 14,400 requests/day           | <100 requests       | $0   |
| **DNS/SSL**    | Vercel+Render | Free subdomains + auto-SSL    | 2 domains           | $0   |

**Total Monthly Cost: $0**

**Deployment Workflow**:

1. Push to `main` branch on GitHub
2. Vercel auto-builds frontend → Live at https://engineering-onboarding-copilot.vercel.app
3. Render auto-builds backend → Live at https://engineering-onboarding-copilot.onrender.com
4. ChromaDB re-indexes on startup (~30 seconds)

**Tradeoffs Accepted**:

1. **Backend cold starts**: 30-60 seconds after 15 min inactivity
   - **Mitigation**: Acceptable for capstone demo; mentioned in presentation
2. **Ephemeral filesystem**: ChromaDB/SQLite rebuilt on redeploy
   - **Mitigation**: Auto-rebuild from synthetic-docs/ on startup
3. **Single backend instance**: No horizontal scaling
   - **Mitigation**: Sufficient for evaluation load (<50 concurrent users)

**Deployment Status**: ✅ Live and operational (deployed April 27, 2026)

---

## 8. Testing Strategy and Rationale

### Testing Philosophy

The testing strategy prioritizes **deterministic, fast, cost-free automated tests** while maintaining high confidence in system correctness. This approach balances thorough validation against practical constraints (API costs, CI runtime, development velocity).

### Testing Approach and Rationale

#### 1. Unit Tests (Isolation Testing)

**What**: Test individual components and functions in isolation with mocked external dependencies

**Why**:

- Fast execution (milliseconds per test)
- No API costs (mocked LLM/embedding calls)
- Deterministic results (no network flakiness)
- Enables rapid development feedback loop
- High coverage of business logic

**Tool**: pytest with unittest.mock

**Coverage**: Gap detection logic, database operations, utility functions

**Example**: Testing gap normalization (whitespace/case handling) without database

**Test Files**:

- `test_gap_service.py`: 19 unit tests for gap logging, deduplication, statistics
- `test_database_setup.py`: Database initialization and schema validation
- Total: ~530 lines of unit test code

#### 2. Integration Tests (Component Interaction)

**What**: Test multiple components working together with real databases (SQLite, ChromaDB)

**Why**:

- Catch integration bugs between components
- Validate database queries and transactions
- Test RAG pipeline end-to-end with real vector store
- More realistic than pure unit tests, still fast enough for CI

**Tool**: pytest with test fixtures (in-memory SQLite, temporary ChromaDB)

**Coverage**: RAG service + vector store, Gap service + database, full sync pipeline

**Example**: Testing full question → embed → retrieve → confidence flow with test corpus

**Test Files**:

- `test_rag_pipeline.py`: RAG flow integration (92 lines)
- `test_gap_integration.py`: Gap service with real database (289 lines)
- Total: ~381 lines of integration test code

#### 3. Edge Case Testing (Robustness)

**What**: Test system behavior with unusual, malformed, or boundary-case inputs

**Why**:

- Ensure graceful degradation
- Validate input validation
- Prevent crashes from unexpected user behavior
- Document expected behavior for edge cases

**Tool**: pytest with parametrized test cases

**Coverage**: Empty queries, very long queries, special characters, concurrent requests

**Example**: Testing 500-character limit enforcement, empty string handling

**Test Files**:

- `test_edge_cases.py`: 463 lines testing boundary conditions, malformed input, error handling

#### 4. End-to-End Evaluation (System Validation)

**What**: Formal evaluation with 10 predefined test cases against deployed production system

**Why**:

- Validate complete user flows in production environment
- Measure accuracy, latency, confidence calibration
- Demonstrate system meets requirements
- Provide quantitative metrics for capstone evaluation
- Detect deployment-specific issues (CORS, cold starts, etc.)

**Tool**: Manual testing with documented test cases

**Coverage**: 3 well-documented, 2 partially-documented, 2 undocumented, 2 edge cases, 1 irrelevant

**Example**: "How do I set up my development environment?" → Expected answer with citations

**Documentation**: `docs/evaluation/sprint-3-formal-evaluation.md`

**Results**:

- 10/10 test cases passed (100% accuracy)
- Average response time: 1.4s (excluding cold start)
- Confidence calibration validated (high confidence = correct answers)

#### 5. Test Execution Environments

**Tests Run in Local Development** (before each commit):

- All unit tests (fast feedback)
- Integration tests (validate changes)
- Edge case tests (ensure robustness)

**Tests Skipped in CI/CD** (cost/complexity):

- Live API tests with real Groq/Cohere (would incur costs + rate limits)
- End-to-end browser tests (Playwright setup not included for capstone scope)
- Full regression suite (manual pre-demo validation sufficient)

**Tests Run Pre-Deployment** (manual):

- End-to-end evaluation (10 test cases)
- Production smoke tests (health check, sample queries)
- UI validation (all pages load, no console errors)

### Testing Actually Executed (Completion Summary)

**Test Execution Summary**:

- **Test suites executed**: pytest (backend), manual evaluation (production)
- **Dates**: Sprint 2 (April 20-26, 2026), Sprint 3 formal evaluation (April 27, 2026)
- **Environment**: Local macOS (pytest), Production Render+Vercel (evaluation)
- **Results**: All tests passing, 100% accuracy on evaluation
- **Test files**: 5 files, 1,374 lines of test code
- **Test functions**: 40+ test functions across all suites

**Test File Breakdown**:

| Test File                 | Lines | Purpose                                    | Test Count |
| ------------------------- | ----- | ------------------------------------------ | ---------- |
| `test_gap_service.py`     | 304   | Gap logging, deduplication, statistics     | 19         |
| `test_edge_cases.py`      | 463   | Boundary conditions, error handling        | 12+        |
| `test_gap_integration.py` | 289   | Gap service with database integration      | 8          |
| `test_database_setup.py`  | 226   | Database initialization, schema validation | 3          |
| `test_rag_pipeline.py`    | 92    | RAG flow end-to-end                        | 4          |
| **Total**                 | 1,374 | **Comprehensive test coverage**            | **46+**    |

**Coverage Analysis**:

- **Gap Detection**: Extensively tested (19 unit tests + 8 integration tests)
- **RAG Pipeline**: Core flow validated (4 integration tests)
- **Edge Cases**: Robust validation (12+ edge case tests)
- **Database**: Schema and initialization verified (3 tests)
- **End-to-End**: Production validation (10 evaluation test cases)

**Known Test Limitations**:

- No automated browser E2E tests (Playwright not implemented)
- No security penetration testing (lightweight threat model sufficient)
- Frontend tests limited (TypeScript type checking only, no Jest/RTL)

**Why This Testing Strategy**:

1. **Cost-conscious**: Mocking LLM calls prevents $50+ in API costs during development
2. **Fast feedback**: Unit tests run in <1 second, enables rapid iteration
3. **High confidence**: Integration tests catch real bugs without excessive complexity
4. **Production validation**: Formal evaluation ensures deployed system works
5. **Capstone-appropriate**: Balances thoroughness with time/budget constraints

### Evidence (Implementation)

**Test Files**:

- `backend/test_gap_service.py`: Gap detection unit tests
- `backend/test_gap_integration.py`: Gap service integration tests
- `backend/test_rag_pipeline.py`: RAG pipeline integration tests
- `backend/test_edge_cases.py`: Boundary condition tests
- `backend/test_database_setup.py`: Database schema tests

**Evaluation Documentation**:

- `docs/evaluation/sprint-3-formal-evaluation.md`: 10 test cases, 100% accuracy
- Test case categories: well-documented, partially-documented, undocumented, edge cases, irrelevant

**Test Execution**:

- Command: `pytest backend/test*.py -v`
- Results: All tests passing locally and in pre-deployment validation
- Production validation: 10/10 test cases passed with expected behavior

---

## 9. Security and AI Safety Considerations

### Lightweight Threat Model

1. **Accidental API cost spikes** from abuse or runaway loops
2. **Prompt injection** via malicious content in documents
3. **Information leakage** of sensitive data or internal errors
4. **Data ingestion risks** (secrets/keys accidentally indexed)
5. **CORS misconfiguration** allowing unauthorized frontend access

### Controls Implemented for MVP

**Implemented and Verified (✅)**:

1. ✅ **Secrets management**: API keys in environment variables, `.env` in `.gitignore`, `.env.example` provided
2. ✅ **Input validation**: Max question length (500 chars), empty/malformed request rejection
3. ✅ **CORS restrictions**: Whitelist Vercel URL + localhost only, no wildcard in production
4. ✅ **Prompt injection resistance**: System prompt treats docs as data, explicit instructions to answer from context only
5. ✅ **Error handling**: Generic error messages to frontend, detailed logs server-side only
6. ✅ **Audit logging**: All queries logged with timestamp, question, confidence, sources

**Planned but Not Implemented (◻️)**:

7. ◻️ **Rate limiting**: Simple IP-based throttling (acceptable risk for demo)
8. ◻️ **Authentication**: Admin endpoints unprotected (demo is public read-only)
9. ◻️ **Output length limits**: No hard cap on LLM response length (Groq has reasonable defaults)
10. ◻️ **Advanced prompt injection defense**: No adversarial testing (lightweight mitigation sufficient)

### Residual Risks (Acceptable for Capstone)

- No enterprise SSO/RBAC (demo is single-tenant/public)
- No encryption at rest (synthetic docs only, no sensitive data)
- No rate limiting (Groq free tier limits provide natural protection)

### Scope Boundaries (Intentionally Out of Scope)

- No multi-user authentication
- No scheduled/automated doc sync
- No production-grade monitoring/alerting
- No data retention policies
- Synthetic docs only (not production company data)

---

## 10. Deployment Readiness Checklist

**Pre-Deployment Configuration**:

- ✅ Environment variables documented in `.env.example`
- ✅ CORS origins configured for Vercel URL + localhost
- ✅ Health check endpoint implemented (`GET /health`)
- ✅ Database initialization on startup
- ✅ Vector DB auto-sync on startup
- ✅ API keys added to Render environment variables
- ✅ Frontend environment variables set in Vercel dashboard

**Post-Deployment Verification**:

- ✅ Frontend loads at https://engineering-onboarding-copilot.vercel.app
- ✅ Backend health check returns 200 with chunk count
- ✅ Database connection successful
- ✅ Vector DB indexed (275 chunks)
- ✅ Ask question flow works end-to-end
- ✅ Gap Radar dashboard displays data
- ✅ HTTPS certificates valid
- ✅ No CORS errors in browser console

**Deployment Status**: ✅ **Production-ready** (Deployed April 27-28, 2026)

---

## 11. Conclusion

The Engineering Onboarding Copilot successfully demonstrates a production-ready RAG system with novel confidence-based gap detection. The system achieves:

- **100% accuracy** on formal evaluation (10/10 test cases)
- **Zero infrastructure cost** ($0/month FREE stack)
- **Fast performance** (1.4s average response time)
- **Intelligent gap detection** (differentiator from standard RAG systems)
- **Comprehensive testing** (46+ automated tests + formal evaluation)
- **Production deployment** (live on Vercel + Render with auto-deploy)

The system is ready for capstone demonstration and evaluation, with all requirements satisfied.

**Key Achievements**:

- Novel architecture combining RAG with confidence-based routing
- Cost-conscious engineering decisions (FREE AI stack)
- Comprehensive testing strategy (unit, integration, edge case, E2E)
- Modern UI redesign (Berlin studio aesthetic with strategic mono fonts)
- Production deployment with CI/CD

**Future Enhancements** (post-capstone):

- Add authentication for admin endpoints
- Implement rate limiting
- Add frontend component tests (Jest/RTL)
- Expand to multi-repository support
- Add scheduled doc sync
- Implement persistent disk for production

---

**Document Status**: ✅ Final  
**Last Updated**: April 28, 2026
