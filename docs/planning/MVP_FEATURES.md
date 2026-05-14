# MVP Feature List & Scope Management

This document defines the **scope-frozen MVP features** for the Engineering Onboarding Copilot.

---

## 🚨 MVP Scope Freeze Statement

**Priority Sequencing:**

1. **First priority**: Core functionality (deployed app with documentation, agile workflow, design/testing docs, demo)
2. **Second priority**: Engineering rigor (CI/CD, comprehensive testing, stable production deployment)
3. **Third priority**: Differentiators (Gap Radar, evaluation metrics, AI safety controls)

**Any feature not listed in the MVP section below is deferred until all MVP acceptance criteria pass and the deployed app is demo-ready.**

This is strict scope protection to ensure project success.

---

## 🎯 MVP Feature List (Must Ship)

**Features 1-6 produce the core application experience and demo workflow. Features 7-9 demonstrate engineering rigor (CI/CD, testing/documentation quality, and production-safe design).**

- Features 1-6: Core application functionality (Q&A, citations, fallback, gaps, UI, metrics)
- Feature 7 (CI/CD): Automated deployment and quality checks
- Feature 8 (Testing & Docs): Comprehensive testing and technical documentation
- Feature 9 (Security): Production thinking and safety controls

---

### Core Features (Required)

#### **1. Documentation Indexing (Automatic on Startup)**

- Load markdown files from local `synthetic-docs/` directory
- Ingest all `.md` files using LangChain DirectoryLoader
- Parse, chunk (500 chars, 50 overlap), embed (Cohere 1024-dim), and index in ChromaDB
- Store source metadata (file path only)
- Automatic indexing on application startup (~10-15 seconds)

_Note: MVP uses local files for demonstration. Future enhancement could add GitHub repository sync._

#### **2. RAG Q&A with Citations**

- Web UI chat interface for questions
- Semantic search over indexed documentation
- Answer generation grounded in retrieved context
- Display source citations (file paths, snippets)
- Show retrieved chunks used for transparency

#### **3. Evidence-Based Confidence Gating** ⭐

- Detect low-evidence retrieval (low similarity scores, sparse context)
- Safe fallback response: "I cannot answer this confidently from the current documentation"
- Reduce unsupported answers via citation grounding
- Clear messaging when evidence is insufficient

#### **4. Documentation Gap Radar** ⭐ _Differentiator_

- Automatically log low-evidence queries
- Gap dashboard showing:
  - Question text
  - Timestamp
  - Confidence level (and optional numeric retrieval score for debugging)
  - Status (new / reviewed / resolved)
  - Frequency counter (increment for repeated questions)
- Prioritization by frequency

#### **5. Web Dashboard (Next.js)**

- **Ask Page**: Chat-style Q&A interface with source citations
- **Gap Radar Dashboard**: View and manage documentation gaps
- Simple, functional UI (Tailwind CSS)
- Responsive design for desktop and mobile

#### **6. Gap Management Features**

- View all logged documentation gaps
- See gap frequency (how many times asked)
- Update gap status (NEW → REVIEWED → RESOLVED)
- Delete resolved gaps
- Sort by frequency to prioritize improvements
- Display confidence scores for debugging

#### **7. Deployment**

- Automatic deployments via Vercel (frontend) and Render (backend) free tiers
- Production URLs: https://engineering-onboarding-copilot.vercel.app (frontend), https://engineering-onboarding-copilot.onrender.com (backend)
- Health check endpoint (`/health`)
- Public GitHub repository for portfolio
- Zero infrastructure cost ($0)

#### **8. Testing & Documentation**

- Unit tests (backend services with mocked LLM calls)
- Integration tests (RAG pipeline with test corpus)
- ~27 pytest functions + 2 manual test suites across 5 test files, 1,374 lines of test code
- Evaluation with 10 diverse questions (100% accuracy)
- `DESIGN_AND_TESTING.md` with comprehensive architecture documentation

#### **9. Basic Security & AI Safety Controls** ⭐

**MVP Minimum (Must Ship):**

- Secrets management via environment variables + `.env.example` provided
- Input validation (Pydantic schemas, max question length 500 chars)
- CORS allowlist (Vercel URL + localhost only)
- Production-safe error handling (no stack traces/secrets in UI responses)
- Prompt-injection-aware system prompt (treat retrieved docs as data, not instructions)
- Query audit logging with security-oriented retention (timestamp, question, sources, error outcomes)

_Note: Feature 6 (observability) and Feature 9 (audit logging) use the same query logging pipeline; Feature 6 focuses on operational metrics, Feature 9 focuses on audit/security retention._

**If Time Allows (Nice-to-Have):**

- Rate limiting (IP-based or reverse-proxy level)
- Ingestion blocklist patterns (`.env`, `secrets/`, `*.pem`)
- GitHub token scope validation documentation
- Output constraints (max response length enforcement)
- Data minimization allowlist for ingestion paths

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

**Rule**: Stretch features do NOT count toward capstone passing. Protect your MVP delivery.

**Scope Guardrail**: A stretch feature may only be started if all MVP acceptance criteria remain green after the previous sprint review.

---

## ✅ MVP Feature-Level Acceptance Criteria

### Feature 1: Documentation Indexing (Automatic on Startup)

- [x] System automatically ingests all `.md` files from `synthetic-docs/` directory on startup
- [x] Chunking produces chunks (500 chars, 50 overlap)
- [x] Embeddings generated using Cohere API (1024-dim)
- [x] Embeddings stored in ChromaDB
- [x] Health endpoint reports indexing status (chunk count)
- [x] Indexing completes in ~10-15 seconds

### Feature 2: RAG Q&A

- [x] User can submit question from Ask page
- [x] Response returns answer text + citations in `[file.md]` format
- [x] Citations render as links to source files
- [x] Retrieved chunks/snippets shown in UI
- [x] Loading/error states displayed
- [x] Queries processed with Groq LLM (Llama-3.1-8b-instant)

### Feature 3: Evidence-Based Confidence Gating

- [x] Low similarity queries (confidence <0.70) trigger fallback message
- [x] Fallback message is clear and helpful
- [x] Answerable responses include citations from retrieved context
- [x] No unsupported factual claims in answerable responses (manual spot-check via evaluation)
- [x] Spam filtering implemented (confidence ≤0.11 rejected, not logged)

### Feature 4: Documentation Gap Radar

- [x] Low-evidence queries (0.11 < confidence < 0.70) appear in Gaps dashboard
- [x] Gap entry shows question, timestamp, status, confidence level, frequency
- [x] Gap entry displays confidence percentage
- [x] Repeated queries increment frequency counter
- [x] User can update gap status (NEW → REVIEWED → RESOLVED)
- [x] User can delete gaps (false positives, resolved items)
- [x] Gaps sortable by frequency, date, or confidence

### Feature 5: Web Dashboard

- [x] Ask page renders without errors
- [x] Gap Radar page displays all logged gaps with management controls
- [x] Home page with feature overview and navigation
- [x] Navigation between pages works
- [x] Responsive design (mobile + desktop)
- [x] Modern UI with Tailwind CSS and Framer Motion animations

### Feature 6: Gap Management & Observability

- [x] Low-confidence queries logged to SQLite database
- [x] Gap entries tracked with frequency, status, confidence, timestamps
- [x] Gap statistics available via API (total gaps, by status, most frequent)
- [x] Full gap lifecycle management (view, update status, delete)
- [x] Gaps serve as operational metrics for documentation quality

### Feature 7: CI/CD + Deployment

- [x] Frontend deployed to Vercel with live URL (https://engineering-onboarding-copilot.vercel.app)
- [x] Backend deployed to Render with live URL (https://engineering-onboarding-copilot.onrender.com)
- [x] App reachable via stable public URLs (free-tier cold starts <60s, documented)
- [x] Environment variables configured in Vercel/Render and documented in README
- [x] `/health` endpoint returns 200 with chunk count
- [x] Repo shared with `quantic-grader`
- [x] Auto-deploy from GitHub main branch (Vercel + Render)
- [x] Zero infrastructure cost ($0/month)

### Feature 8: Testing & Documentation

- [x] Unit tests (~27 pytest functions across 5 files, 1,374 lines of test code)
- [x] Integration tests with real databases (SQLite, ChromaDB)
- [x] Manual test suites for edge cases and RAG pipeline (2 files)
- [x] Formal evaluation with 10 test cases (100% accuracy)
- [x] DESIGN_AND_TESTING.md complete with all 11 sections (681 lines)
- [x] README has clear setup instructions + deliverable links
- [x] Sprint artifacts saved in `/docs/sprints/sprint-{0,1,2,3}/`

### Feature 9: Basic Security & AI Safety Controls (MVP Minimum)

- [x] API keys stored in environment variables only (`.env` in `.gitignore`)
- [x] `.env.example` file included in repo
- [x] Input validation enforced (max question length 500 chars, Pydantic schema)
- [x] System prompt includes prompt-injection resistance instructions
- [x] CORS configured for approved origins only (Vercel URL + localhost)
- [x] Production error handling hides stack traces from UI responses
- [x] Gap logs stored with timestamps, questions, confidence, sources (SQLite)

**Deferred (Not Implemented):**

- Rate limiting (acceptable for demo; Groq free tier provides natural limits)
- Ingestion blocklist (not needed for local synthetic docs)
- GitHub token scope (GitHub sync deferred)
- Output length constraints (Groq has reasonable defaults)

---

## 🔗 Related Documentation

- [Project Overview](PROJECT_OVERVIEW.md) - Problem and solution
- [Capstone Requirements](CAPSTONE_REQUIREMENTS.md) - Quantic deliverables
- [System Architecture](SYSTEM_ARCHITECTURE.md) - Technical design
- [Implementation Details](IMPLEMENTATION_DETAILS.md) - How to build features
- [Sprint Plan](SPRINT_PLAN.md) - When to build features
