# Engineering Onboarding Copilot

**RAG-powered internal knowledge assistant with Documentation Gap Radar**  
**Solo Capstone Project for Quantic MSSE**

[![Backend CI](https://github.com/lenablank/engineering-onboarding-copilot/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/lenablank/engineering-onboarding-copilot/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/lenablank/engineering-onboarding-copilot/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/lenablank/engineering-onboarding-copilot/actions/workflows/frontend-ci.yml)

> **Status:** Sprint 3 in progress (May 8, 2026). Core features complete, production deployed, evaluation complete (100% accuracy).

---

## 📍 Current Status

- **Phase**: Sprint 3 (Week 1 Complete - 5 days ahead of schedule)
- **Last Updated**: May 8, 2026
- **Current Focus**: Demo preparation and final polish
- **Cost**: $0 (using Cohere API embeddings + Groq free tier)
- **Timeline**: 12 weeks implementation (Mar 2 - May 24) + protected buffer week (May 25-31)
- **Deployment**: ✅ Live at https://engineering-onboarding-copilot.vercel.app

---

## 📋 Documentation

- **System Architecture**: [docs/technical/SYSTEM_ARCHITECTURE.md](docs/technical/SYSTEM_ARCHITECTURE.md) - Tech stack, data flows, RAG pipeline
- **Implementation Details**: [docs/technical/IMPLEMENTATION_DETAILS.md](docs/technical/IMPLEMENTATION_DETAILS.md) - Code patterns, API contracts, testing
- **Design & Testing**: [DESIGN_AND_TESTING.md](DESIGN_AND_TESTING.md) - Architecture, patterns, testing strategy (641 lines, all 11 required sections)
- **Sprint 0 Artifacts**: [docs/sprints/sprint-0/](docs/sprints/sprint-0/) - Sprint goal, backlog, review

---

## 🎯 One-Sentence Pitch

A web-based onboarding assistant that syncs engineering docs from a GitHub repository, answers new-engineer questions with cited evidence, and logs low-evidence queries as documentation gaps to improve documentation over time.

---

## 📖 Problem Statement

New engineers waste hours asking teammates basic onboarding questions ("How do I run tests?", "Where's auth implemented?", "What's our deployment process?"). Existing docs are fragmented, outdated, or undiscoverable. Teams don't know which documentation gaps exist until someone asks.

---

## ✨ Solution

An AI-powered onboarding assistant that:

- ✅ Auto-syncs engineering docs from GitHub (no manual uploads)
- ✅ Answers questions with source citations and evidence-based fallback behavior when documentation support is insufficient
- ✅ Detects and logs documentation gaps (improves knowledge base over time)
- ✅ Provides transparency (shows retrieved chunks, confidence levels)

---

## 🛠️ Technology Stack (Summary)

**Frontend**: Next.js 14 + TypeScript + Tailwind CSS  
**Backend**: FastAPI + Python 3.11+  
**AI/ML**: LangChain, Cohere API (embed-english-v3.0, 1024-dim embeddings, free tier), Groq (Llama-3.1-8b-instant, free tier)  
**Vector DB**: ChromaDB (persistent, embedded)  
**Database**: SQLite (gaps.db for Gap Radar)  
**Deployment**: Vercel (frontend) + Render (backend)  
**CI/CD**: GitHub Actions (backend + frontend workflows)

_For detailed tech stack rationale, see [docs/technical/SYSTEM_ARCHITECTURE.md](docs/technical/SYSTEM_ARCHITECTURE.md)_

---

## 💰 Budget

**Total Cost for 3.5-Month Capstone**: **$0** ✅

- **Embeddings**: Cohere API embed-english-v3.0 (1024-dim, free tier, 1000 req/min, $0)
- **LLM**: Groq API (14,400 requests/day free tier, $0)
- **Infrastructure**: $0 (Vercel, Render free tiers)

**Cost-Conscious Engineering Decision**: Chose FREE stack over paid alternatives (OpenAI) because this is an academic capstone project, not a commercial product. This demonstrates engineering maturity in selecting appropriate technologies based on project context and shows fiscal responsibility.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Groq API key (FREE, sign up at console.groq.com - optional for Sprint 0, needed for Sprint 1)
- Git + GitHub account

### Quick Setup

1. **Clone repo and install dependencies**

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

2. **Set up environment variables**

```bash
# Backend .env
GROQ_API_KEY=your_groq_key_here
COHERE_API_KEY=your_cohere_key_here
CORS_ORIGINS=http://localhost:3000

# Get API keys (both FREE):
# - Cohere: https://dashboard.cohere.com/api-keys
# - Groq: https://console.groq.com/keys

# Frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run locally (requires two terminals)**

```bash
# Terminal 1: Backend (from backend/)
uvicorn app.main:app --reload
# → Backend runs at http://localhost:8000

# Terminal 2: Frontend (from frontend/)
npm run dev
# → Frontend runs at http://localhost:3000
```

4. **Verify setup**

- Backend health: `http://localhost:8000/health`
- Frontend UI: `http://localhost:3000`

5. **Start building!**

Follow the week-by-week plan in [docs/planning/SPRINT_PLAN.md](docs/planning/SPRINT_PLAN.md)

---

## � Repository Structure

```
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # API endpoints
│   │   └── __init__.py
│   ├── prove_pipeline_simple.py  # Sprint 0 RAG proof script
│   ├── requirements.txt
│   ├── pyproject.toml         # Project config
│   └── README.md
├── synthetic-docs/            # Test documentation corpus
│   ├── 1-getting-started.md
│   ├── 2-architecture-overview.md
│   ├── 3-testing-guide.md
│   ├── 4-deployment.md
│   └── 5-api-reference.md
├── docs/
│   ├── technical/             # Architecture & implementation
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── IMPLEMENTATION_DETAILS.md
│   │   └── DESIGN_AND_TESTING_TEMPLATE.md
│   └── sprints/               # Agile artifacts
│       └── sprint-0/
│           ├── sprint-goal.md
│           ├── sprint-backlog.md
│           └── sprint-review.md
└── README.md
```

## 🔌 API Endpoints

**Backend REST API**:

- `POST /ask` - Submit question, get answer with citations
- `POST /sync` - Trigger documentation sync
- `GET /sources` - List indexed documents
- `GET /gaps` - List documentation gaps
- `PATCH /gaps/{id}` - Update gap status
- `GET /metrics` - Get observability metrics
- `GET /health` - Health check

_See [docs/technical/IMPLEMENTATION_DETAILS.md](docs/technical/IMPLEMENTATION_DETAILS.md) for complete API contracts and response schemas._

---

## 📦 Implementation Status

**Sprint 3 Week 1 Complete** (May 8, 2026) - **5 days ahead of schedule** 🚀

**Core Features (100% Complete)**:

- ✅ Full-stack RAG application (Next.js + FastAPI + ChromaDB + Cohere + Groq)
- ✅ Q&A with confidence scoring and fallback behavior
- ✅ Documentation Gap Radar (differentiator feature)
- ✅ Production deployment (Vercel + Render, both URLs live)
- ✅ Formal evaluation: **10/10 test cases passed (100% accuracy)**
- ✅ Comprehensive testing: 24 automated tests, multiple test levels
- ✅ Professional UI (Berlin studio aesthetic, responsive, animations)
- ✅ CI/CD pipelines (GitHub Actions: backend + frontend)
- ✅ Complete documentation (DESIGN_AND_TESTING.md: 641 lines)

**Remaining Work (Tasks 7-16)**:

- ⏳ Script demo video (Task 7, 2-3 hours)
- ⏳ Practice demo (Task 8, 2-3 hours)
- ⏳ **Record demo video** (Task 9, 4 hours) - **CRITICAL for submission**
- ⏳ Share repo with quantic-grader (Task 10, 5 min)
- ⏳ Sprint 3 retrospective (Task 13, 2-3 hours)
- ⏳ Final testing and polish (Task 14, 2-3 hours)
- ⏳ Submit by May 24, 2026 (personal deadline)

**System Metrics**:

- **Accuracy**: 100% (10/10 evaluation test cases)
- **Response Time**: 1.4s average (excluding cold start)
- **Cost**: $0 (free tier infrastructure)
- **Test Coverage**: 46+ test functions across 5 files (1,374 lines)
- **Documentation**: 275 chunks indexed from 15 markdown files

---
