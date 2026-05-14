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
│   │   ├── IMPLEMENTATION_DETAILS.md
│   │   └── DESIGN_AND_TESTING_TEMPLATE.md
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

## 🔗 Related Documentation

- [Project Overview](../planning/PROJECT_OVERVIEW.md) - Problem and solution
- [Capstone Requirements](../planning/CAPSTONE_REQUIREMENTS.md) - Required deliverables
- [MVP Features](../planning/MVP_FEATURES.md) - Feature scope
- [System Architecture](../technical/SYSTEM_ARCHITECTURE.md) - Technical design
- [Implementation Details](../technical/IMPLEMENTATION_DETAILS.md) - How to build
