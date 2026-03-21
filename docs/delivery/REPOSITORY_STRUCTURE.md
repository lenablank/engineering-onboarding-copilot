# Repository Structure & Key Documentation Files

This document outlines the GitHub repository structure and key documentation files for the capstone.

---

## 📁 GitHub Repository Structure

```
engineering-onboarding-copilot/
├── README.md                          # Project overview, setup, LINKS TO ALL DELIVERABLES
├── DESIGN_AND_TESTING.md              # ⭐ Quantic requirement: architecture + testing
├── EVALUATION.md                      # Evaluation plan, question set, results
├── CAPSTONE_SUBMISSION_LINKS.md       # ⭐ Quick ref: deployed app, Trello, demo video
├── AI_TOOLING_AND_ATTRIBUTION.md      # AI usage, code sources, plagiarism compliance
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions (test, lint, build)
├── docs/
│   ├── sprints/                       # Sprint artifacts (goals, reviews, retros, backlogs)
│   │   ├── sprint-1/
│   │   │   ├── sprint-goal.md
│   │   │   ├── sprint-backlog.md
│   │   │   ├── sprint-review.md
│   │   │   └── sprint-retro.md
│   │   ├── sprint-2/
│   │   └── sprint-3/
│   ├── demo/                          # Demo preparation artifacts
│   │   ├── demo-script.md
│   │   ├── demo-checklist.md
│   │   ├── sample-questions.md
│   │   └── backup-plan.md
│   ├── api/                           # API contract documentation
│   │   └── endpoints.md               # API endpoint specs
│   └── architecture-diagram.png       # System architecture visual
├── frontend/                          # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx              # Home/Ask page
│   │   │   ├── sources/page.tsx      # Sources page
│   │   │   ├── gaps/page.tsx         # Documentation Gaps dashboard
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── AskInterface.tsx
│   │   │   ├── AnswerDisplay.tsx
│   │   │   ├── SourcesList.tsx
│   │   │   ├── GapsDashboard.tsx
│   │   │   └── SyncButton.tsx
│   │   └── lib/
│   │       └── api.ts                # API client
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── .env.example                  # Frontend env vars (NEXT_PUBLIC_API_URL)
├── backend/                           # FastAPI application
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── ask.py           # /ask endpoint
│   │   │   │   ├── sync.py          # /sync endpoint
│   │   │   │   ├── sources.py       # /sources endpoint
│   │   │   │   ├── gaps.py          # /gaps endpoint
│   │   │   │   └── health.py        # /health endpoint
│   │   ├── services/
│   │   │   ├── ingestion.py         # GitHub sync, chunking, embedding
│   │   │   ├── rag.py               # RAG pipeline, semantic search
│   │   │   ├── gap_detection.py     # Confidence gating, gap logging
│   │   │   └── metrics.py           # Query logging, analytics
│   │   ├── models/
│   │   │   ├── database.py          # SQLAlchemy models
│   │   │   └── schemas.py           # Pydantic schemas
│   │   ├── db/
│   │   │   └── connection.py        # Postgres connection
│   │   └── config.py                # Environment config
│   ├── tests/
│   │   ├── fixtures/
│   │   │   ├── test-docs/           # Mock documentation
│   │   │   └── evaluation_questions.json
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
