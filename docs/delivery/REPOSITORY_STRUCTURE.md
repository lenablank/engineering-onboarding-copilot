# Repository Structure & Key Documentation Files

This document outlines the GitHub repository structure and key files for the capstone project.

---

## 📁 GitHub Repository Structure

```
engineering-onboarding-copilot/
├── README.md                          # Project overview, setup instructions, deployment links
├── DESIGN_AND_TESTING.md              # ⭐ Quantic requirement: architecture + testing documentation
├── CAPSTONE_SUBMISSION_LINKS.md       # ⭐ Quick ref: deployed app, Trello, demo video, GitHub
├── .gitignore                         # Git ignore patterns
├── .github/
│   └── workflows/                     # GitHub Actions CI/CD pipelines (not yet implemented)
├── docs/                              # 📚 All project documentation
│   ├── INDEX.md                       # Documentation navigation guide
│   ├── planning/                      # Project planning documents
│   │   ├── PROJECT_OVERVIEW.md
│   │   ├── CAPSTONE_REQUIREMENTS.md
│   │   ├── MVP_FEATURES.md
│   │   └── SPRINT_PLAN.md
│   ├── technical/                     # Technical documentation
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── IMPLEMENTATION_DETAILS.md
│   │   └── DESIGN_AND_TESTING_TEMPLATE.md
│   ├── evaluation/                    # Testing and evaluation results
│   │   ├── sprint-2-edge-cases.md
│   │   └── sprint-3-formal-evaluation.md
│   ├── delivery/                      # Submission and career materials
│   │   ├── REPOSITORY_STRUCTURE.md   # This file
│   │   └── INTERVIEW_PREP.md
│   └── sprints/                       # Sprint artifacts (goals, backlogs, reviews)
│       ├── sprint-0/
│       ├── sprint-1/
│       └── sprint-2/
├── frontend/                          # Next.js application (deployed on Vercel)
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx              # Homepage with Ask interface
│   │       ├── layout.tsx            # Root layout
│   │       ├── globals.css           # Global styles
│   │       ├── ask/
│   │       │   └── page.tsx          # Ask question page
│   │       ├── gaps/
│   │       │   └── page.tsx          # Gap Radar dashboard
│   │       └── fonts/                # Custom fonts
│   ├── public/                        # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.mjs
│   ├── next.config.mjs
│   └── next-env.d.ts
├── backend/                           # FastAPI application (deployed on Render)
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── __init__.py
│   │   ├── routes/                   # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── gaps.py              # /api/gaps endpoints
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── rag_service.py       # RAG pipeline, confidence calculation
│   │   │   ├── gap_service.py       # Gap detection and management
│   │   │   └── vector_store.py      # ChromaDB vector store operations
│   │   ├── models/                   # Data models
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # SQLAlchemy database configuration
│   │   │   └── gap.py               # DocumentationGap model
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── logging.py           # Logging configuration
│   ├── tests/                         # Test files
│   │   ├── conftest.py
│   │   ├── test_rag_pipeline.py
│   │   ├── test_gap_service.py
│   │   ├── test_confidence_enhanced.py
│   │   └── test_fallback_refactored.py
│   ├── chroma_db/                     # ChromaDB vector database (persistent)
│   ├── requirements.txt               # Python dependencies
│   ├── pyproject.toml                # Python project metadata
│   ├── pyrightconfig.json            # Type checking configuration
│   ├── prove_pipeline_simple.py      # Development testing script
│   └── README.md                     # Backend setup instructions
├── synthetic-docs/                    # Sample documentation corpus
│   ├── 1-getting-started.md
│   ├── 2-architecture-overview.md
│   ├── 3-testing-guide.md
│   └── ... (15 total markdown files)
├── chroma_db/                         # Root-level ChromaDB data (legacy, can be removed)
├── render-build.sh                    # Render deployment build script
├── render-start.sh                    # Render deployment start script
└── test_production.sh                 # Production health check script
```

---

## ⭐ Key Files for Quantic Submission

### Required Deliverables (Top Level)

1. **README.md** - Project overview with:
   - Problem statement and solution
   - Tech stack
   - Setup instructions
   - Deployment links
   - Links to all documentation

2. **DESIGN_AND_TESTING.md** - Formal design document with:
   - System architecture
   - Testing strategy
   - Design decisions and trade-offs

3. **CAPSTONE_SUBMISSION_LINKS.md** - Quick reference with:
   - Deployed frontend URL (Vercel)
   - Deployed backend URL (Render)
   - GitHub repository
   - Trello board
   - Demo video (YouTube)

### Core Documentation (docs/)

4. **docs/technical/SYSTEM_ARCHITECTURE.md** - Detailed architecture documentation

5. **docs/evaluation/sprint-3-formal-evaluation.md** - Final evaluation results

7. **docs/sprints/** - Sprint artifacts showing agile process

---

## 🚀 Deployment Configuration

### Frontend (Vercel)
- **Framework**: Next.js 14
- **Deployment**: Automatic on push to `main`
- **Environment Variables**: None required (API URL is production URL)

### Backend (Render)
- **Framework**: FastAPI + Uvicorn
- **Build Command**: `./render-build.sh`
- **Start Command**: `./render-start.sh`
- **Environment Variables**:
  - `COHERE_API_KEY` - Cohere embeddings API key
  - `GROQ_API_KEY` - Groq LLM API key
  - Database stored in SQLite (ephemeral on Render free tier)

---

## 📊 Testing Files

- **backend/tests/test_rag_pipeline.py** - RAG pipeline unit tests
- **backend/tests/test_gap_service.py** - Gap detection unit tests  
- **backend/tests/test_confidence_enhanced.py** - Confidence calculation tests
- **backend/tests/test_fallback_refactored.py** - Fallback behavior tests
- **docs/evaluation/sprint-3-formal-evaluation.md** - Integration test results

---

## 📝 Notes

- ChromaDB stores vector embeddings in `backend/chroma_db/` (gitignored)
- SQLite database for gaps at `backend/gaps.db` (gitignored)
- Synthetic documentation corpus in `synthetic-docs/` (15 markdown files)
- Total infrastructure cost: **$0** (all free tiers)
│   │   ├── test_ingestion.py
│   │   ├── test_rag.py
│   │   ├── test_gap_detection.py
│   │   ├── test_api_ask.py
│   │   ├── test_api_gaps.py
│   │   ├── test_metrics.py
│   │   └── conftest.py              # Pytest fixtures, mocks
│   ├── requirements.txt             # Runtime dependencies
│   ├── requirements-dev.txt         # Development dependencies (pytest, ruff, black, httpx)
│   └── .env.example
├── synthetic-docs/                    # Mock company engineering docs
│   ├── README.md
│   └── docs/
│       ├── setup.md
│       ├── architecture.md
│       ├── testing.md
│       ├── deployment.md
│       ├── api-guidelines.md
│       └── troubleshooting.md
├── scripts/
│   ├── seed_db.sql                   # Initial database schema
│   └── run_evaluation.py             # Execute evaluation question set
└── .gitignore
```

---

## 📄 Key Documentation Files

### CAPSTONE_SUBMISSION_LINKS.md - Quick reference for graders

```markdown
# Capstone Submission Links

**Student**: [Your Name]  
**Project**: Engineering Onboarding Copilot  
**Submission Date**: [Date]

## Required Links

- **Deployed Application**: https://your-app.vercel.app
- **GitHub Repository**: https://github.com/yourusername/engineering-onboarding-copilot
- **Trello Board**: https://trello.com/b/your-board-id
- **Demo Video**: https://youtu.be/your-video-id
- **Design & Testing Document**: [DESIGN_AND_TESTING.md](DESIGN_AND_TESTING.md)

## Quick Start

See [README.md](README.md) for full setup instructions.
```

---

### DESIGN_AND_TESTING.md - Rubric-critical document

```markdown
# Design and Testing Documentation

## 1. Project Objective and User Persona

[Problem statement, target user, use cases]

## 2. Architecture Overview

[System diagram, component descriptions, data flow]

## 3. Technology Choices and Rationale

[Why Next.js, FastAPI, Chroma, Postgres, HuggingFace (FREE), Groq (FREE), etc.]

## 4. Software and Architectural Patterns

[Patterns used and rationale - handbook explicitly requires this]

### Patterns Implemented:

- **Repository Pattern** (data access abstraction for Chroma/Postgres)
  - Reason: Decouples business logic from storage, enables easier testing with mocks
- **Service Layer Pattern** (RAG service, Gap service, Ingestion service)
  - Reason: Separates business logic from API controllers, promotes reusability
- **RAG Pattern** (Retrieval-Augmented Generation)
  - Reason: Core AI pattern for grounding LLM responses in documentation
- **API Gateway Pattern** (FastAPI as single entry point)
  - Reason: Centralized routing, CORS, error handling for frontend
- **Observer-style logging hooks** (cross-cutting query logging, gap detection)
  - Reason: Decoupled observability tracking without blocking main request flow

### Architectural Decisions:

- **Monorepo structure** (frontend + backend in one repo)
  - Reason: Simplifies deployment, single source of truth for capstone
- **REST over GraphQL**
  - Reason: Simpler for small API surface, better for demo/evaluation
- **Separate vector + relational DBs**
  - Reason: Chroma optimized for embeddings, Postgres for structured logs/gaps

## 5. RAG Pipeline Design

[Chunking strategy, retrieval approach, prompt design, citation format]

## 6. Evidence-Based Confidence Gating

[Heuristic design, threshold calibration, fallback behavior]

## 7. Deployment Options and Cost Implications

[Deployment options considered, selected option, cost tradeoffs]

### Options Considered:

- Local-only (lowest cost, poor accessibility for demo/grading)
- Vercel + Render + Neon (best for demo/public access, free tiers)
- Single-host container deployment (simpler ops, less frontend polish)
- Cloud-native (AWS/GCP/Azure - beyond student budget)

### Selected Option:

- **Vercel (frontend)** + **Render (backend)** + **Neon (database)**
- Rationale: Free tiers sufficient for capstone, auto-deploy from GitHub, production-quality URLs
- Cost: $0/month (within free tier limits)

### Tradeoffs Accepted:

- Backend cold starts on Render free tier (~30-60s wake-up after inactivity)
- Database connection limits on Neon free tier (acceptable for demo load)
- No horizontal scaling (not needed for capstone evaluation)
- **Chroma vector DB persistence**: Using on-demand rebuild from `synthetic-docs/` via Sync button (Render free tier may have ephemeral filesystem; rebuilding index on restart is acceptable for demo/capstone scope)

This deployment analysis addresses the handbook requirement for "deployment options recommended for the software (e.g. on-premises or cloud) including relative cost implications."

## 8. Testing Strategy and Rationale

[Unit, integration, smoke tests; mocking strategy; regression set - with reasons per Quantic requirement]

### Testing Approach and Rationale:

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

**6. Optional Live API Smoke Tests**

- **What**: Limited tests with real Groq API (not in CI)
- **Why**: Verify production deployment works with real services; validate response quality
- **When**: Manual pre-demo validation only (skipped in CI to preserve free tier quota)

### Why This Testing Strategy:

- **Mocking LLM calls**: Prevents rate limit issues and keeps CI fast
- **Regression set**: Demonstrates production thinking (metrics-driven quality)
- **Multiple test levels**: Catches different bug types (unit vs integration vs E2E)
- **CI-safe by default**: Fast, deterministic, no API dependencies in automated tests

## 9. Security and AI Safety Considerations

[Threat model, controls implemented, residual risks, future improvements]

### Lightweight Threat Model

- **Accidental API cost spikes** from abuse or runaway loops
- **Prompt injection** via malicious content in ingested docs
- **Information leakage** of sensitive data or internal errors
- **Unauthorized access** to admin endpoints (sync, gap resolution)
- **Data ingestion risks** (secrets/keys accidentally synced)

### Controls Implemented

1. **Secrets management**: API keys in environment variables only, `.env` in `.gitignore`, `.env.example` provided
2. **Input validation**: Max question length (500 chars), Pydantic schema validation, reject empty/malformed requests
3. **Output constraints**: Max response length enforced, citation requirement for answerable responses, fallback on low-evidence
4. **Prompt injection resistance**: System prompt explicitly treats docs as data, not instructions; answer only user question using retrieved content as evidence
5. **CORS restrictions**: Allow only frontend origin (Vercel URL + localhost for dev), no `*` in production
6. **Least-privilege access**: GitHub token read-only scope documented
7. **Data minimization**: Allowlist paths (`README.md`, `docs/**`), blocklist patterns (`.env`, `secrets/`, `*.pem`, `credentials`)
8. **Error handling**: No stack traces in production responses, generic error messages to UI, detailed logs server-side only
9. **Basic rate limiting**: Simple IP-based or token-bucket (or reverse-proxy level) to prevent cost spikes
10. **Audit logging**: Query logs track what was asked, when, sources used (observability + governance)

### Residual Risks (Acceptable for MVP)

- No enterprise SSO/RBAC (demo is single-tenant/public mode)
- No encryption at rest (acceptable for synthetic documentation)
- No advanced adversarial testing (prompt injection partially mitigated, not solved)
- Cold start latency on free tiers (deployment tradeoff)
- Vector DB persistence on free-tier ephemeral filesystem (mitigated by on-demand sync/rebuild)

### Future Improvements (Post-Capstone)

- Simple auth for admin endpoints (`/sync`, `/gaps/update`) with basic token
- Separate "demo mode" flag with reduced logging
- Request size limit on `/ask` endpoint
- GitHub token scope explicitly validated at ingestion time

**Signal to Interviewers**: Demonstrates security-aware AI engineering, zero-trust principles applied appropriately to scope.

## 10. Evaluation Methodology

[Question set design, metrics definitions, results table]

## 11. Known Limitations

[Threshold sensitivity, corpus specificity, cold start latency]

## 12. Future Improvements

[CLI, multi-source, scheduled sync, advanced metrics]
```

---

### EVALUATION.md - Shows production thinking

```markdown
# Evaluation Plan and Results

## Evaluation Question Set

[Table of 20-30 questions with expected behavior]

## Metrics Definitions

[Citation presence, relevance, latency, gap precision, etc.]

## Results

[Actual measurements from test run]

## Analysis

[What worked well, what needs tuning, threshold adjustments]
```

---

### AI_TOOLING_AND_ATTRIBUTION.md - Plagiarism compliance

```markdown
# AI Tooling and Attribution

## AI Coding Tools Used

- **GitHub Copilot / Cursor / Claude / ChatGPT** (specify which)
  - Used for: scaffolding boilerplate, code completion, test generation
  - Used for: debugging syntax errors, refactoring suggestions
  - NOT used for: core algorithm design without verification

## Manual Verification Process

- All AI-generated code manually reviewed and tested
- Algorithms understood conceptually before implementation
- Tests written to verify behavior, not just trust suggestions

## Code Attributions

### Framework/Library Code

- LangChain examples adapted from: [official docs link]
- FastAPI structure based on: [tutorial/example link]
- Next.js components adapted from: [shadcn/ui, official examples]

### Synthetic Documentation

- All engineering docs in `/synthetic-docs/` are original content
- Created specifically for this project, no external sources
- Intentionally includes gaps for gap detection demonstration

## Plagiarism Statement

All code is either:

1. Original work written/reviewed by me
2. AI-assisted with full understanding and verification
3. Framework/library code properly attributed above
4. Tutorial-based with modifications and attribution

No code copied from classmates, other capstone projects, or unattributed sources.
```

---

## 🔗 Related Documentation

- [Project Overview](../planning/PROJECT_OVERVIEW.md) - Problem and solution
- [Capstone Requirements](../planning/CAPSTONE_REQUIREMENTS.md) - Required deliverables
- [MVP Features](../planning/MVP_FEATURES.md) - Feature scope
- [System Architecture](../technical/SYSTEM_ARCHITECTURE.md) - Technical design
- [Implementation Details](../technical/IMPLEMENTATION_DETAILS.md) - How to build
