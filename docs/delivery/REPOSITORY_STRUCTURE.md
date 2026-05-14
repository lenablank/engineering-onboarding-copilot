# Repository Structure & Key Documentation Files

This document outlines the GitHub repository structure and key files for the project.

---

## 📁 GitHub Repository Structure

```
engineering-onboarding-copilot/
├── README.md                          # Project overview, setup instructions, deployment links
├── DESIGN_AND_TESTING.md              # Architecture + testing documentation
├── CAPSTONE_SUBMISSION_LINKS.md       # Quick ref: deployed app, Trello, demo video, GitHub
├── .gitignore                         # Git ignore patterns
├── docs/                              # 📚 All project documentation
│   ├── INDEX.md                       # Documentation navigation guide
│   ├── planning/                      # Project planning documents
│   │   ├── PROJECT_OVERVIEW.md
│   │   ├── MVP_FEATURES.md
│   │   ├── SPRINT_PLAN.md
│   │   └── CRITICAL_PATH_SPRINT2_COMPLETION.md
│   ├── technical/                     # Technical documentation
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   └── IMPLEMENTATION_DETAILS.md
│   ├── evaluation/                    # Testing and evaluation results
│   │   ├── sprint-2-edge-cases.md
│   │   └── sprint-3-formal-evaluation.md
│   ├── delivery/                      # Delivery documentation
│   │   └── REPOSITORY_STRUCTURE.md   # This file
│   └── sprints/                       # Sprint artifacts (goals, backlogs, reviews)
│       ├── sprint-0/
│       ├── sprint-1/
│       ├── sprint-2/
│       └── sprint-3/
├── frontend/                          # Next.js application (deployed on Vercel)
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx              # Homepage with Ask interface
│   │       ├── layout.tsx            # Root layout
│   │       ├── globals.css           # Global styles
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
│   ├── conftest.py                    # Pytest fixtures and configuration
│   ├── test_rag_pipeline.py           # Manual RAG pipeline testing (not pytest)
│   ├── test_gap_service.py            # Gap service pytest tests (18 tests)
│   ├── test_gap_integration.py        # Gap integration pytest tests (7 tests)
│   ├── test_database_setup.py         # Database setup pytest test (1 test)
│   ├── test_edge_cases.py             # Manual edge case testing (not pytest)
│   ├── manual_verify_confidence.py    # Manual confidence verification script
│   ├── manual_verify_fallback.py      # Manual fallback verification script
│   ├── prove_pipeline_simple.py       # Simple pipeline verification script
│   ├── tests/                         # Empty directory (tests in backend/ root)
│   ├── chroma_db/                     # ChromaDB vector database (persistent)
│   ├── gaps.db                        # SQLite database for documentation gaps
│   ├── requirements.txt               # Python dependencies (production)
│   ├── requirements-deploy.txt        # Render deployment dependencies
│   ├── runtime.txt                    # Python version for Render
│   ├── pyproject.toml                 # Python project metadata
│   ├── pyrightconfig.json             # Type checking configuration
│   ├── .env.example                   # Environment variables template
│   └── README.md                      # Backend setup instructions
├── synthetic-docs/                    # Sample documentation corpus (15 markdown files)
│   ├── 1-getting-started.md
│   ├── 2-architecture-overview.md
│   ├── 3-testing-guide.md
│   ├── 4-deployment.md
│   ├── 5-api-reference.md
│   ├── 6-ci-cd-pipeline.md
│   ├── 7-database-setup.md
│   ├── 8-security-practices.md
│   ├── 9-monitoring-observability.md
│   ├── 10-code-review-guidelines.md
│   ├── 11-git-workflow.md
│   ├── 12-environment-configuration.md
│   ├── 13-troubleshooting.md
│   ├── 14-api-authentication.md
│   └── 15-performance-optimization.md
├── chroma_db/                         # Root-level ChromaDB data (legacy, can be removed)
├── render-build.sh                    # Render deployment build script
├── render-start.sh                    # Render deployment start script
└── test_production.sh                 # Production health check script
```

---

## ⭐ Key Documentation Files

### Project Overview (Top Level)

1. **README.md** - Project overview with:
   - Problem statement and solution
   - Tech stack and technology choices
   - Setup and installation instructions
   - Deployment links
   - Links to comprehensive documentation

2. **DESIGN_AND_TESTING.md** - Comprehensive design document with:
   - System architecture and diagrams
   - Testing strategy and coverage
   - Design decisions and trade-offs
   - Deployment options analysis

3. **CAPSTONE_SUBMISSION_LINKS.md** - Quick reference with:
   - Live frontend URL (Vercel)
   - Live backend URL (Render)
   - GitHub repository link
   - Trello board
   - Demo video (YouTube)

### Core Documentation (docs/)

4. **docs/technical/SYSTEM_ARCHITECTURE.md** - Detailed technical architecture

5. **docs/technical/IMPLEMENTATION_DETAILS.md** - Implementation patterns and API contracts

6. **docs/planning/PROJECT_OVERVIEW.md** - Problem statement and solution overview

7. **docs/evaluation/sprint-3-formal-evaluation.md** - Final evaluation results (10 test questions, 100% accuracy)

8. **docs/sprints/** - Sprint artifacts showing development process

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

**Pytest Test Suite** (~27 automated test functions, 5 files, 1,374 lines):
- `backend/test_gap_service.py` - Gap service unit tests (18 tests)
- `backend/test_gap_integration.py` - Gap integration tests (7 tests)
- `backend/test_database_setup.py` - Database setup test (1 test)
- `backend/conftest.py` - Pytest fixtures and configuration

**Manual Test Suites** (2 scripts for manual verification):
- `backend/test_rag_pipeline.py` - Manual RAG pipeline testing
- `backend/test_edge_cases.py` - Manual edge case testing

**Verification Scripts**:
- `backend/manual_verify_confidence.py` - Confidence threshold verification
- `backend/manual_verify_fallback.py` - Fallback behavior verification
- `backend/prove_pipeline_simple.py` - Simple pipeline proof

**Evaluation Results**:
- `docs/evaluation/sprint-2-edge-cases.md` - Edge case testing results
- `docs/evaluation/sprint-3-formal-evaluation.md` - Final evaluation (10 test cases, 100% accuracy)

---

## 📝 Notes

- ChromaDB stores vector embeddings in `backend/chroma_db/` (gitignored, re-indexed on startup)
- SQLite database for gaps at `backend/gaps.db` (gitignored, persistent on Render)
- Synthetic documentation corpus in `synthetic-docs/` (15 markdown files)
- Test files located in `backend/` root directory (not `backend/tests/` subdirectory)
- Total infrastructure cost: **$0** (all free tiers: Vercel, Render, Cohere, Groq)
```

---

## 🔗 Related Documentation

- [Project Overview](../planning/PROJECT_OVERVIEW.md) - Problem and solution
- [MVP Features](../planning/MVP_FEATURES.md) - Feature scope and acceptance criteria
- [Sprint Plan](../planning/SPRINT_PLAN.md) - Historical sprint planning (with disclaimer)
- [System Architecture](../technical/SYSTEM_ARCHITECTURE.md) - Technical design and data flow
- [Implementation Details](../technical/IMPLEMENTATION_DETAILS.md) - RAG pipeline and deployment
- [Design & Testing](../../DESIGN_AND_TESTING.md) - Comprehensive design document (681 lines)
- [Documentation Index](../INDEX.md) - Complete documentation navigation
