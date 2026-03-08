# Engineering Onboarding Copilot

**RAG-powered internal knowledge assistant with Documentation Gap Radar**  
**Solo Capstone Project for Quantic MSSE**

> **Status:** Planning and implementation roadmap. Features marked ✅ indicate intended MVP capabilities, not completed features.

---

## 📍 Current Status

- **Phase**: Sprint 0 Complete (Feb 25 - Mar 8, 2026)
- **Last Updated**: Mar 8, 2026
- **Current Focus**: Sprint 0 completed - FREE stack proven, ready for Sprint 1
- **Cost**: $0 (using HuggingFace local embeddings + Groq free tier)
- **Timeline**: 12 weeks implementation (Mar 2 - May 24) + protected buffer week (May 25-31)

---

## 📋 Quick Links

- **Trello Board**: [View Sprint Progress](https://trello.com/invite/b/69a427cee6ac597f2636cc22/ATTIc2511c7490ba36570a3a9b5a708ac4d17EFCD003/engineering-onboarding-copilot-msse-capstone) - Agile task tracking
- **Sprint Plan**: [docs/planning/SPRINT_PLAN.md](docs/planning/SPRINT_PLAN.md) - Week-by-week implementation guide
- **Project Overview**: [docs/planning/PROJECT_OVERVIEW.md](docs/planning/PROJECT_OVERVIEW.md) - Problem, solution, business case
- **MVP Features**: [docs/planning/MVP_FEATURES.md](docs/planning/MVP_FEATURES.md) - Detailed feature specs with acceptance criteria
- **System Architecture**: [docs/technical/SYSTEM_ARCHITECTURE.md](docs/technical/SYSTEM_ARCHITECTURE.md) - Tech stack, data flows, RAG pipeline
- **Implementation Details**: [docs/technical/IMPLEMENTATION_DETAILS.md](docs/technical/IMPLEMENTATION_DETAILS.md) - Code patterns, API contracts, testing
- **Design & Testing Template**: [docs/technical/DESIGN_AND_TESTING_TEMPLATE.md](docs/technical/DESIGN_AND_TESTING_TEMPLATE.md) - Required Quantic deliverable (will be completed with actual results during implementation and finalized as `DESIGN_AND_TESTING.md` before submission)
- **Evaluation & Demo**: [docs/evaluation/EVALUATION_AND_DEMO.md](docs/evaluation/EVALUATION_AND_DEMO.md) - Demo script, presentation requirements
- **Repository Structure**: [docs/delivery/REPOSITORY_STRUCTURE.md](docs/delivery/REPOSITORY_STRUCTURE.md) - Planned folder structure
- **Interview Prep**: [docs/delivery/INTERVIEW_PREP.md](docs/delivery/INTERVIEW_PREP.md) - Technical interview preparation

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

### Why This Is Strong

✅ **RAG at its core** (aligned with current AI engineering hiring expectations)  
✅ **Internal tool expertise** (what employers want to see)  
✅ **Clear differentiator** (Gap Radar is unique)  
✅ **Production-conscious thinking** (evidence-based gating, evaluation, citation grounding)  
✅ **Solo-friendly scope** (MVP realistic for 3.5 months)  
✅ **Impressive demos** (live Q&A with citations, gap detection in action)

---

## 🎓 Quantic Capstone Deliverables & Rubric Alignment

### Required Submission Components (Non-Negotiable)

These 5 deliverables are explicitly required by the handbook:

| Required Deliverable              | Implementation                           | Evidence Location                          |
| --------------------------------- | ---------------------------------------- | ------------------------------------------ |
| **1. GitHub repository (shared)** | Monorepo with documented code            | Shared with `quantic-grader`               |
| **2. Deployed web application**   | Vercel (frontend) + Render (backend)     | Live URL in `CAPSTONE_SUBMISSION_LINKS.md` |
| **3. Agile task board**           | Trello with all sprints visible          | Link in `README.md` and submission doc     |
| **4. Design & testing document**  | Architecture, patterns, rationale, tests | `DESIGN_AND_TESTING.md`                    |
| **5. Demo video (15-20 min)**     | Walkthrough with ID shown, face visible  | Video link in submission doc               |

### Rubric-Critical Evidence (Needed for High Scores)

These elements are assessed via the rubric scoring (3-5 range):

| Rubric Criteria                       | Implementation                           | Evidence Location                        |
| ------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| **3+ sprints with agile methodology** | Sprint 1/2/3 with goals, reviews, retros | Sprint artifacts in `/docs/sprints/`     |
| **CI/CD tools & methodology**         | GitHub Actions (test, lint, build)       | `.github/workflows/ci.yml`               |
| **Well-designed code**                | Patterns, service layers, clean arch     | Code structure + `DESIGN_AND_TESTING.md` |
| **Well-tested code**                  | Unit, integration, E2E, regression set   | Test files + coverage reports            |
| **Appropriate documentation**         | Code comments, README, design doc        | All `.md` files, docstrings              |
| **Solo project camera presence**      | Only you visible and speaking            | Demo video (full 15-20 min)              |

### Score-Boosting Initiative (Differentiators for 4-5 Range)

These go "above and beyond minimum requirements":

- ⭐ **Documentation Gap Radar** (unique differentiator, not just basic RAG)
- ⭐ **Evidence-based confidence gating** (production-grade fallback logic)
- ⭐ **Systematic evaluation methodology** (20-30 question regression set with metrics)
- ⭐ **Cost-conscious engineering** (FREE stack: $0 for entire project, shows engineering maturity)
- ⭐ **Security & AI safety controls** (prompt injection resistance, audit logging)
- ⭐ **Observability** (query logs, latency tracking, citation rate monitoring)
- ⭐ **Cost optimization** ($3-5 total for entire capstone via free tiers)

**Scoring Strategy**: Deliver all 5 required components + rubric-critical evidence + 2-3 strong differentiators = target 8-10/10.

---

## 🚨 MVP Scope Freeze Statement

**Priority Sequencing for High Scores:**

1. **First priority**: Deliver all 5 required submission components (repo, deployed app, Trello, design/testing doc, demo video)
2. **Second priority**: Rubric-critical evidence (3+ sprints with agile artifacts, stable deployed demo, CI/CD, comprehensive testing)
3. **Third priority**: Differentiators that show initiative (Gap Radar, evaluation metrics, AI safety controls)

**Any feature not listed in the MVP section below is deferred until all MVP acceptance criteria pass and the deployed app is demo-ready.**

This is non-negotiable scope protection to ensure capstone success.

---

## 🎯 MVP Feature List (Must Ship for Capstone Success)

**These 9 features enable the 5 required deliverables + rubric-critical evidence:**

- Features 1-6 power the deployed web app and demo
- Feature 7 (CI/CD) provides rubric-critical evidence of engineering methodology
- Feature 8 (Testing & Docs) produces the required design/testing document
- Feature 9 (Security) demonstrates production-safe design and initiative

**Timeline**: Sprint 0 planning (Feb 25 - Mar 1) followed by 12 weeks of implementation (Mar 2 - May 24), with a protected buffer week (May 25-31) before the May 31 official deadline.

### Core Features (Required)

**1. GitHub Docs Sync (Manual Trigger for MVP)**

- Connect to configured GitHub repository or local docs path
- Ingest markdown files: `README.md`, `/docs/**/*.md`
- Parse, chunk, embed, and index content
- Store source metadata (file path, chunk index, header hierarchy)
- Manual "Sync Now" button in UI
- _MVP uses configured repo/path with manual sync trigger — no end-user GitHub OAuth integration_

**2. RAG Q&A with Citations**

- Web UI chat interface for questions
- Semantic search over indexed documentation
- Answer generation grounded in retrieved context
- Display source citations (file paths, snippets)
- Show retrieved chunks used for transparency

**3. Evidence-Based Confidence Gating** ⭐

- Detect low-evidence retrieval (low similarity scores, sparse context)
- Safe fallback response: "I cannot answer this confidently from the current documentation"
- Reduce unsupported answers via citation grounding
- Clear messaging when evidence is insufficient

**4. Documentation Gap Radar** ⭐ _Differentiator_

- Automatically log low-evidence queries
- Gap dashboard showing:
  - Question text
  - Timestamp
  - Status (new/reviewed/resolved)
  - Frequency counter (increment for repeated questions)
  - Confidence level (optional in UI, always logged for debugging)
- Prioritization by frequency

**5. Web Dashboard (Next.js)**

- **Ask Page**: Chat-style Q&A interface
- **Sources Page**: List of indexed docs + last sync timestamp
- **Gaps Page**: Documentation gaps dashboard
- Simple, functional UI (polish is secondary to functionality)

**6. Basic Observability**

- Query logging (question, answer, latency, sources, confidence level)
- Basic metrics:
  - Average latency
  - Citation presence rate
  - Answerable vs. gap ratio
- Export to CSV or display in simple table (not fancy dashboard)

**7. CI/CD + Deployment**

- GitHub Actions: linting, tests, build checks
- Deployed to shareable URL (Vercel + Render free tiers)
- Health check endpoint (`/health`)
- Shared with `quantic-grader` GitHub account

**8. Testing & Documentation**

- Unit tests (backend services with mocked LLM calls)
- Integration tests (RAG pipeline with test corpus)
- Evaluation question set (20-30 questions)
- `DESIGN_AND_TESTING.md` with architecture rationale, deployment options analysis, and cost implications

**9. Security & AI Safety Controls** ⭐

**Must Ship (MVP Minimum)**:

- Secrets management via environment variables (no credentials in source control)
- Input validation (schema validation, max question length)
- Prompt-injection-aware prompting (treat retrieved docs as data, not instructions)
- CORS restrictions for approved frontend origins
- Production-safe error handling (no stack traces/secrets exposed)
- Query audit logging (observability + governance)

**Nice to Have (If Time Allows After Core MVP)**:

- Output constraints (max response length enforcement)
- Least-privilege GitHub tokens (read-only scope)
- Data minimization in ingestion (allowlist docs paths, exclude sensitive patterns)
- Request rate limiting

---

## 🚀 Stretch Goals (Only If Ahead of Schedule)

**Do NOT attempt these until MVP is complete and tested**

- **CLI client** calling the same API (`ask "How do I run tests?"`)
- **Second ingestion source** (static docs export, NOT live scraping)
- **Scheduled auto-sync** (cron job, daily/weekly)
- **Retrieval debugging panel** (show top-k chunks + similarity scores)
- **Advanced metrics dashboard** (interactive charts, time-series)
- **Topic auto-tagging** (LLM-based categorization of gaps)
- **Onboarding checklist UI** with progress tracking

---

## 🛠️ Technology Stack (Summary)

**Frontend**: Next.js 14 + TypeScript + Tailwind CSS  
**Backend**: FastAPI + Python 3.11+  
**AI/ML**: LangChain, HuggingFace (all-MiniLM-L6-v2 embeddings, local, FREE), Groq (Llama-3-8b-instant, free tier)  
**Vector DB**: Chroma (local-first)  
**Database**: PostgreSQL (Neon free tier)  
**Deployment**: Vercel (frontend) + Render (backend)  
**CI/CD**: GitHub Actions

_For detailed tech stack rationale, see [docs/technical/SYSTEM_ARCHITECTURE.md](docs/technical/SYSTEM_ARCHITECTURE.md)_

---

## 💰 Budget

**Total Cost for 3.5-Month Capstone**: **$0** ✅

- **Embeddings**: HuggingFace (local, unlimited, FREE)
- **LLM**: Groq API (14,400 requests/day free tier, $0)
- **Infrastructure**: $0 (Vercel, Render, Neon free tiers)

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
cp .env.example .env
# Add your OpenAI API key, database URL

# Frontend .env.local
# Create frontend/.env.local and add:
# NEXT_PUBLIC_API_URL=http://localhost:8000
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

## 📚 Documentation Structure

```
docs/
├── INDEX.md                              # Documentation navigation
├── planning/
│   ├── PROJECT_OVERVIEW.md               # Problem, solution, business case
│   ├── CAPSTONE_REQUIREMENTS.md          # Quantic handbook requirements mapping
│   ├── MVP_FEATURES.md                   # Detailed feature specs
│   └── SPRINT_PLAN.md                    # Week-by-week implementation plan
├── technical/
│   ├── SYSTEM_ARCHITECTURE.md            # System design, tech stack, RAG pipeline
│   ├── IMPLEMENTATION_DETAILS.md         # Code patterns, API contracts, testing
│   └── DESIGN_AND_TESTING_TEMPLATE.md    # Template for required deliverable
├── evaluation/
│   └── EVALUATION_AND_DEMO.md            # Demo script, presentation requirements
├── delivery/
│   ├── REPOSITORY_STRUCTURE.md           # Planned folder structure
│   └── INTERVIEW_PREP.md                 # Technical interview preparation
└── reference/
    ├── CAPSTONE_HANDBOOK.md              # Quantic official handbook
    ├── AI_AUGMENTED_PRODUCTIVITY.md      # Course notes
    ├── AI_FOR_BUSINESS_NOTES.md          # Course notes
    └── AI_LEADERSHIP_MANAGEMENT.md       # Course notes
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

## 🎉 Critical Success Factors

1. **Protect your MVP scope** - Do not attempt stretch goals early
2. **Test and evaluate early** - Week 3 first eval run to validate approach
3. **Document as you go** - Don't save all docs for end
4. **Weekly reviews** - Stay on track, adjust if needed
5. **Quantic compliance** - Double-check demo requirements before final recording

---
