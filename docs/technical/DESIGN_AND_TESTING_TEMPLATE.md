# Design and Testing Documentation

**Required Quantic Deliverable**

**Status**: Draft (to be completed during implementation with measured results and updated to Final before submission)

---

## 1. Project Objective and User Persona

### Problem Statement

[Describe the onboarding inefficiency problem: new engineers waste hours asking teammates questions, docs are fragmented/outdated/undiscoverable, teams don't know what's missing]

### Target User

**Persona**: New engineer joining a software company

**Attributes**:

- Tenure: First 30 days at company
- Role: Backend or full-stack engineer
- Goal: Self-serve setup/architecture/workflow answers without blocking teammates
- Pain point: Cannot find answers in scattered/outdated documentation

### Use Cases

1. **Question Answering**: "How do I run tests locally?"
2. **Source Discovery**: "Where is authentication implemented?"
3. **Gap Identification**: Detecting missing/incomplete documentation

---

## 2. Architecture Overview

### System Diagram

[Insert High-Level Architecture diagram from SYSTEM_ARCHITECTURE.md - create during implementation]

### Component Descriptions

- **Frontend**: Next.js web app (Ask/Sources/Gaps pages)
- **Backend**: FastAPI REST API (ingestion, RAG, gap detection services)
- **Vector DB**: Chroma for semantic search over documentation chunks
- **Relational DB**: Postgres for query logs, gaps, sync history
- **AI Stack**: HuggingFace (local embeddings) + Groq (LLM, free tier)

### Data Flow

[Insert Question Answering Flow diagram from SYSTEM_ARCHITECTURE.md - create during implementation]

**Request/Response Boundaries**:

- Frontend (stateless) → Backend API (stateless) → Vector DB (stateful) + Relational DB (stateful)
- Chroma and Postgres maintain state; API and frontend are stateless services

---

## 3. Technology Choices and Rationale

| Technology         | Reason                                                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Next.js 14**     | Modern React framework, SSR, excellent Vercel integration                                                                   |
| **TypeScript**     | Type safety, catches bugs at compile time                                                                                   |
| **FastAPI**        | Async-capable, automatic API docs, Python AI ecosystem                                                                      |
| **LangChain**      | RAG chains, prompt templates, proven patterns                                                                               |
| **Chroma**         | Local-first vector DB, persistent storage, Python-native, free                                                              |
| **Neon Postgres**  | Serverless Postgres free tier, structured data (logs, gaps)                                                                 |
| **HuggingFace**    | FREE local embeddings (all-MiniLM-L6-v2), runs on CPU, no API costs, unlimited usage, 97% quality of OpenAI at $0 cost      |
| **Groq API**       | FREE LLM (Llama-3-8b-instant), 14,400 requests/day free tier, extremely fast inference, cost-conscious engineering decision |
| **Vercel**         | Free tier frontend hosting, auto-deploy from GitHub                                                                         |
| **Render**         | Free tier backend hosting, Python support                                                                                   |
| **GitHub Actions** | Native CI/CD integration, free for public repos                                                                             |

---

## 4. Software and Architectural Patterns

**This section explicitly required by Quantic handbook**

### Patterns Implemented

- **Repository Pattern** (data access abstraction for Chroma/Postgres)
  - **Reason**: Decouples business logic from storage, enables easier testing with mocks
- **Service Layer Pattern** (RAG service, Gap service, Ingestion service)
  - **Reason**: Separates business logic from API controllers, promotes reusability
- **RAG Pattern** (Retrieval-Augmented Generation)
  - **Reason**: Core AI pattern for grounding LLM responses in documentation
- **API Gateway Pattern** (FastAPI as single entry point)
  - **Reason**: Centralized routing, CORS handling, error handling for frontend
- **Observer-style logging hooks** (cross-cutting query logging, gap detection)
  - **Reason**: Decoupled observability tracking without blocking main request flow; implemented as function calls in request pipeline rather than full event dispatch system

### Architectural Decisions

- **Monorepo structure** (frontend + backend in one repo)
  - **Reason**: Simplifies deployment, single source of truth for capstone submission
- **REST over GraphQL**
  - **Reason**: Simpler for small API surface, better for demo/evaluation, less overhead
- **Separate vector + relational DBs**
  - **Reason**: Chroma optimized for embeddings/semantic search, Postgres for structured logs/gaps

**Evidence (Implementation)**:

- Backend services: `backend/app/services/rag.py`, `gap_detection.py`, `ingestion.py`
- API routes: `backend/app/api/routes/ask.py`, `sync.py`, `gaps.py`
- Data models: `backend/app/models/database.py`, `schemas.py`

---

## 5. RAG Pipeline Design

### Chunking Strategy

**Approach**: Semantic chunking by markdown headers (better than fixed-size):

- Split by headers (preserves context)
- Max chunk size: ~500 tokens (~2000 chars)
- Overlap: 50-100 tokens for continuity
- Metadata: file path, header hierarchy, chunk index

**Implementation**: LangChain MarkdownHeaderTextSplitter + RecursiveCharacterTextSplitter

**Code Block Handling**: Preserve code fences where useful; avoid splitting inside short code snippets to maintain context for setup/deployment questions

### Retrieval Approach

1. Convert question to embedding (HuggingFace all-MiniLM-L6-v2, local, FREE)
2. Semantic search in Chroma (top-k=10 chunks)
3. Filter by similarity threshold
4. Return chunks with metadata

### Prompt Design

**System Prompt**:

- Role: Engineering onboarding assistant
- Constraints: Answer only from provided docs, cite sources, no invention
- Format: Answer with citations in [file.md] format

**User Prompt**:

- Includes question + retrieved chunks
- Enforces citation requirement

### Citation Format

`[docs/setup.md]` - inline citations linking to source files

**Evidence (Implementation)**:

- Chunking logic: `backend/app/services/ingestion.py`
- Retrieval logic: `backend/app/services/rag.py`
- Prompt templates: `backend/app/services/rag.py` (system/user prompts)
- Tests: `backend/tests/test_ingestion.py`, `test_rag.py`

---

## 6. Evidence-Based Confidence Gating

### Heuristic Design

Confidence detection based on:

1. **Max similarity score** (higher = better match)
2. **Context sufficiency** (min words, min sources)
3. **Source diversity** (multiple files = stronger evidence)

### Threshold Calibration

[Document actual thresholds tuned on evaluation set during implementation]

**Important**: Confidence score is an evidence sufficiency heuristic for routing behavior, **not a factual correctness guarantee**. High confidence means "sufficient documentation retrieved," not "answer is correct."

**Metric Type**: Thresholds were calibrated against the actual retrieval score type returned by the Chroma query configuration (distance vs similarity; cosine vs euclidean), and normalized where necessary before applying gating heuristics.

Example thresholds (to be tuned):

- High confidence: max_score > 0.85, context > 200 chars, ≥1 source
- Medium: max_score > 0.7, context > 100 chars
- Low: max_score > 0.6
- Gap: max_score ≤ 0.6 or insufficient context

### Fallback Behavior

Low-confidence queries:

- Return safe message: "I cannot answer this confidently from the current documentation"
- Log to documentation_gaps table
- Increment frequency if similar question exists
- Suggest manual answer

**Evidence (Implementation)**:

- Confidence detection: `backend/app/services/gap_detection.py`
- Gap logging: `backend/app/models/database.py` (DocumentationGap model)
- Tests: `backend/tests/test_gap_detection.py`

---

## 7. Deployment Options and Cost Implications

**This section explicitly required by Quantic handbook**

### Options Considered

1. **Local-only**
   - Cost: $0
   - Pros: Free, full control
   - Cons: Poor accessibility for demo/grading, no public URL

2. **Vercel + Render + Neon** ⭐ **(Selected)**
   - Cost: $0/month (free tiers)
   - Pros: Production-quality URLs, auto-deploy from GitHub, good demo experience
   - Cons: Cold starts, connection limits

3. **Single-host container** (e.g., DigitalOcean)
   - Cost: ~$5/month
   - Pros: Simpler ops, no cold starts
   - Cons: Less frontend polish, manual deployment

4. **Cloud-native** (AWS/GCP/Azure)
   - Cost: $20-50/month minimum
   - Pros: Enterprise-grade infrastructure
   - Cons: Beyond student budget, overkill for capstone

### Selected Option

**Vercel (frontend) + Render (backend) + Neon (database)**

**Rationale**:

- Free tiers sufficient for capstone demonstration
- Auto-deploy from GitHub (CI/CD integration)
- Production-quality URLs for grading
- No cost ($0/month)

**Estimated infrastructure cost at implementation time**: $0/month using free tiers (subject to provider limits and policy changes) + $0 AI costs (HuggingFace local + Groq free tier) = **$0 total for capstone**

**Cost-conscious engineering decision**: Chose FREE stack (HuggingFace + Groq) over paid alternatives (OpenAI) because this is an academic capstone project, not a commercial product. Shows engineering maturity in making appropriate technology choices based on project context.

### Tradeoffs Accepted

- **Backend cold starts** on Render free tier (~30-60s wake-up after inactivity)
  - Mitigation: Mention in demo, acceptable for capstone evaluation
- **Database connection limits** on Neon free tier
  - Mitigation: Sufficient for demo load, no high-concurrency needs
- **No horizontal scaling**
  - Mitigation: Not needed for capstone evaluation
- **Chroma vector DB persistence** on Render free tier
  - Strategy: MVP deployment uses local persistent storage if supported by Render; otherwise re-sync on startup or manual sync for demo (ephemeral filesystem acceptable for capstone scope)
  - Mitigation: On-demand rebuild from `synthetic-docs/` repository via Sync button

This deployment analysis addresses the handbook requirement for "deployment options recommended for the software (e.g. on-premises or cloud) including relative cost implications."

**Evidence (Implementation)**:

- Frontend deployment config: `vercel.json` or Vercel dashboard settings
- Backend deployment config: `render.yaml` or Render dashboard settings
- CI/CD workflow: `.github/workflows/ci.yml`
- Health check endpoint: `backend/app/api/routes/health.py`

---

## 8. Testing Strategy and Rationale

**This section explicitly required by Quantic handbook - must include "all testing done and testing methods used and reasons why"**

### Testing Approach and Rationale

**1. Unit Tests with Mocked LLM/Embedding APIs**

- **What**: Test chunking, validation, business logic in isolation
- **Why**: Avoid flaky/expensive API calls in CI; fast feedback; deterministic results
- **Tool**: pytest with unittest.mock
- **Coverage Target**: >70% backend coverage (focus on business logic, not boilerplate)
- **Example**: Test markdown parsing without calling external APIs

**2. Integration Tests with Real Vector DB**

- **What**: Test RAG pipeline end-to-end with local Chroma
- **Why**: Validate retrieval logic works correctly; catch integration bugs between components
- **Tool**: pytest with test fixtures
- **Example**: Test full sync → chunk → embed → search flow with test corpus

**3. Frontend Component Tests**

- **What**: React component rendering, user interactions
- **Why**: Ensure UI components work in isolation before integration
- **Tool**: Jest + React Testing Library
- **Example**: Test Ask page form submission and answer display

**4. End-to-End Smoke Tests**

- **What**: Full user flow testing (Ask → Answer → Gap logging)
- **Why**: Validate complete system integration; catch deployment issues
- **Tool**: Playwright or manual testing
- **Example**: Submit question in browser, verify answer appears with citations

**5. Regression Test Set (20-30 Questions)**

- **What**: Predefined questions with expected behaviors (answerable/gap/citation required)
- **Why**: Measure quality metrics (citation rate, latency); detect regressions between sprints; demonstrate systematic evaluation
- **Tool**: Custom evaluation script with automated assertions
- **Example**: "How do I run tests?" should cite `docs/testing.md`

**6. Optional Live API Smoke Tests**

- **What**: Limited tests with real Groq API (not in CI to avoid rate limits)
- **Why**: Verify production deployment works with real services; validate cost estimates
- **When**: Manual pre-demo validation only (skipped in CI due to cost)
- **Example**: Run 5-10 real queries against deployed app before final demo

### Why This Testing Strategy

- **Mocking LLM calls**: Prevents $50+ CI costs from 100s of test runs per PR
- **Regression set**: Demonstrates production thinking (metrics-driven quality assurance)
- **Multiple test levels**: Catches different bug types (unit bugs vs integration issues vs E2E deployment problems)
- **CI-safe by default**: Fast, deterministic, cost-free automated tests enable frequent commits

### Test Execution Environments

**Tests Run in CI** (automated on every PR):

- Unit tests (mocked LLM/embeddings)
- Integration tests (local Chroma)
- Frontend component tests
- Linting and build checks

**Tests Run Locally/Manually Only**:

- Live API smoke tests (with real Groq API if needed, or use mocks)
- End-to-end Playwright tests (optional)
- Full evaluation regression set (pre-demo)

### Testing Actually Executed (Final Version Only)

[To be completed during implementation]

**Test Execution Summary**:

- Test suites executed: [pytest, jest, evaluation script]
- Date(s): [Sprint 2/3 dates]
- Environment: [Ubuntu CI runner, local macOS]
- Results: [e.g., "142 passed, 3 skipped, 0 failed"]
- Coverage: [X% backend, Y% frontend]
- Known skipped tests: [list with reasons]

**Evidence (Implementation)**:

- Unit tests: `backend/tests/test_*.py`
- Integration tests: `backend/tests/test_rag.py`, `test_gap_detection.py`
- Frontend tests: `frontend/src/**/*.test.tsx`
- CI workflow: `.github/workflows/ci.yml`
- Evaluation script: `scripts/run_evaluation.py`
- Coverage reports: Generated by pytest-cov, uploaded to CI artifacts

---

## 9. Security and AI Safety Considerations

### Lightweight Threat Model

1. **Accidental API cost spikes** from abuse or runaway loops
2. **Prompt injection** via malicious content in ingested docs
3. **Information leakage** of sensitive data or internal errors
4. **Unauthorized access** to admin endpoints (sync, gap resolution)
5. **Data ingestion risks** (secrets/keys accidentally synced)

### Controls Planned for MVP (Implementation Status Updated in Final Version)

**MVP Must-Have Controls**:

1. **Secrets management**: API keys in environment variables only, `.env` in `.gitignore`, `.env.example` provided
2. **Input validation**: Max question length (500 chars), Pydantic schema validation, reject empty/malformed requests
3. **CORS restrictions**: Allow only frontend origin (Vercel URL + localhost for dev), no `*` in production
4. **Prompt injection resistance**: System prompt explicitly treats docs as data, not instructions; answer only user question using retrieved content as evidence
5. **Error handling**: No stack traces in production responses, generic error messages to UI, detailed logs server-side only
6. **Audit logging**: Query logs track what was asked, when, sources used (observability + governance)

**Additional Controls (Implemented If Time Allowed)**:

7. **Output constraints**: Max response length enforced, citation requirement validation
8. **Least-privilege access**: GitHub token read-only scope explicitly documented
9. **Data minimization**: Allowlist paths (`README.md`, `docs/**`), blocklist patterns (`.env`, `secrets/`, `*.pem`, `credentials`)
10. **Basic rate limiting**: Simple IP-based or token-bucket (or reverse-proxy level) to prevent cost spikes

**Final Version Status Indicators**:

- ✅ Implemented and verified
- ◻️ Planned but not implemented (documented as future work)
- ⏳ Partially implemented (specify what's missing)

### Residual Risks (Acceptable for MVP)

- No enterprise SSO/RBAC (demo is single-tenant/public mode)
- No encryption at rest (acceptable for synthetic documentation)
- No advanced adversarial testing (prompt injection partially mitigated, not solved)
- Cold start latency on free tiers (deployment tradeoff)

### Scope Boundaries (Intentionally Out of Scope for MVP)

- No SSO or multi-user authentication
- No multi-tenant auth
- No GitHub OAuth integration
- No scheduled/automated sync (manual trigger only)
- Single repository only (no multi-repo aggregation)
- Synthetic docs only for demo (not production company data)

### Future Improvements (Post-Capstone)

- Simple auth for admin endpoints (`/sync`, `/gaps/update`) with basic token
- Separate "demo mode" flag with reduced logging
- Request size limit on `/ask` endpoint
- GitHub token scope explicitly validated at ingestion time

**Signal to Interviewers**: Demonstrates security-aware AI engineering, zero-trust principles applied appropriately to scope.

**Evidence (Implementation)**:

- Environment config: `backend/app/config.py`, `.env.example`
- Input validation: `backend/app/models/schemas.py` (Pydantic models)
- CORS config: `backend/app/main.py`
- Error handling: `backend/app/api/routes/*` (exception handlers)
- Audit logs: `backend/app/models/database.py` (QueryLog model)

---

## 10. Evaluation Methodology

[Fill in with actual evaluation results during implementation]

### Evaluation Question Set

[Insert table of 20-30 questions with expected behaviors and actual results - sample format below]

| Question                              | Expected Behavior  | Actual Result | Citations Present    | Latency (s) | Pass/Fail |
| ------------------------------------- | ------------------ | ------------- | -------------------- | ----------- | --------- |
| "How do I run tests locally?"         | Answerable         | [Answer text] | ✅ `docs/testing.md` | [X.X]       | Pass      |
| "What's our API key rotation policy?" | Gap (missing docs) | [Fallback]    | N/A                  | [X.X]       | Pass      |
| ...                                   | ...                | ...           | ...                  | ...         | ...       |

### Metrics Measured

1. **Citation Presence Rate**: [X%] (Target: >95%)
2. **Citation Relevance**: [Manual spot-check results - see rubric below]
3. **Latency**: p50 [X]s, p95 [X]s (Target: p50 <4s)
4. **Gap Detection Precision**: [X%] true gaps / total gaps logged
5. **Answerability Rate**: [X%] questions answered vs. gapped

### Citation Relevance Rubric (Manual Review)

**Sample**: 10 randomly selected answerable responses

**Scored Pass/Fail on**:

- Citation exists ✅/❌
- Citation supports claim ✅/❌
- No uncited factual claims ✅/❌

**Results**: [X/10 passed all criteria]

### Results Analysis

[What worked well, what needed tuning, threshold adjustments made]

**Evidence (Implementation)**:

- Evaluation questions: `backend/tests/fixtures/evaluation_questions.json`
- Evaluation script: `scripts/run_evaluation.py`
- Results table: `EVALUATION.md` (separate results document)

---

## 11. Known Limitations

- **Threshold sensitivity**: Confidence thresholds calibrated for specific corpus; may need re-tuning for different documentation styles
- **Corpus specificity**: Works best with technical engineering docs; general knowledge questions may be gapped inappropriately
- **Cold start latency**: Render free tier has ~30-60s wake-up time after inactivity (acceptable for demo)
- **Single repository**: MVP limited to one documentation source; multi-repo requires stretch implementation
- **No real-time sync**: Manual sync only; scheduled ingestion is stretch goal
- **LLM dependencies**: Relies on Groq API availability (14,400/day free tier, very high limit for project needs)

---

## 12. Future Improvements (Post-Capstone)

- **CLI client** for command-line Q&A
- **Second ingestion source** (Confluence, Notion, static exports)
- **Scheduled auto-sync** (daily/weekly cron job)
- **Retrieval debugging UI** (show top-k chunks + similarity scores)
- **Advanced metrics dashboard** (interactive charts, time-series)
- **Topic auto-tagging** (LLM-based categorization of gaps)
- **Semantic chunking improvements** (better code block handling)
- **Multi-tenant support** (per-team documentation spaces)

---

## 13. Traceability Matrix

Mapping of Quantic handbook requirements to evidence in this capstone:

| Requirement                                   | Evidence Location                                                    |
| --------------------------------------------- | -------------------------------------------------------------------- |
| **Design decisions & architectural patterns** | Section 4 above; `backend/app/services/*`                            |
| **Technology choices with rationale**         | Section 3 above                                                      |
| **Testing methods used and reasons why**      | Section 8 above; `backend/tests/*`, `frontend/**/*.test.tsx`         |
| **Deployment options + cost implications**    | Section 7 above; deployment configs                                  |
| **Working software evidence**                 | README.md, deployed URLs in CAPSTONE_SUBMISSION_LINKS.md, demo video |
| **Agile methodology evidence**                | `/docs/sprints/sprint-{1,2,3}/`, Trello board                        |
| **CI/CD tools and methodology**               | `.github/workflows/ci.yml`, Section 7                                |
| **Well-designed code**                        | Repository structure, service layer pattern, Section 4               |
| **Well-tested code**                          | Test suites (Section 8), coverage reports                            |
| **Appropriate documentation**                 | This file, README.md, code comments, API docs                        |

---

**This document serves as the required "Design and Testing Document" for Quantic capstone submission.**
