# MVP Feature List & Scope Management

This document defines the **scope-frozen MVP features** required for capstone success.

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

**Features 1-6 produce the core application experience and demo workflow. Features 7-9 are necessary to demonstrate rubric-critical engineering evidence (CI/CD, testing/documentation quality, and production-safe design) for a strong capstone score.**

- Features 1-6: Core application functionality (Q&A, citations, fallback, gaps, UI, metrics)
- Feature 7 (CI/CD): Rubric-critical engineering methodology evidence
- Feature 8 (Testing & Docs): Required design/testing document + evaluation rigor
- Feature 9 (Security): Production thinking and above-minimum initiative

---

### Core Features (Required)

#### **1. GitHub Docs Sync (Manual Trigger for MVP)**

- Connect to local/mock GitHub repository
- Ingest markdown files: `README.md`, `/docs/**/*.md`
- Parse, chunk, embed, and index content
- Store source metadata (file path, chunk index, header hierarchy)
- Manual "Sync Now" button in UI

_Note: MVP does not include user-authenticated GitHub OAuth integration; ingestion targets a configured repository/path._

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

- **Ask Page**: Chat-style Q&A interface
- **Sources Page**: List of indexed docs + last sync timestamp
- **Gaps Page**: Documentation gaps dashboard
- Simple, functional UI (polish is secondary to functionality)

#### **6. Basic Observability**

- Query logging (question, answer, latency, sources, confidence level) for operational metrics
- Basic metrics calculated from query logs:
  - Average latency
  - Citation rate (% answers with sources)
  - Answerable vs. gap ratio
- Export to CSV or display in simple table (not fancy dashboard)

#### **7. CI/CD + Deployment**

- GitHub Actions: linting, tests, build checks
- Deployed to shareable URL (Vercel + Render free tiers)
- Health check endpoint (`/health`)
- Shared with `quantic-grader` GitHub account

#### **8. Testing & Documentation**

- Unit tests (backend services with mocked LLM calls)
- Integration tests (RAG pipeline with test corpus)
- Evaluation question set (20-30 questions)
- `DESIGN_AND_TESTING.md` with architecture rationale, deployment options analysis, and cost implications

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

### Feature 1: GitHub Docs Sync

- [ ] User can click "Sync Now" button
- [ ] System ingests all `.md` files from configured directory
- [ ] Chunking produces chunks < 2000 chars
- [ ] Embeddings stored in Chroma
- [ ] Sync status/timestamp updates in UI
- [ ] Sync completion logged to database

### Feature 2: RAG Q&A

- [ ] User can submit question from Ask page
- [ ] Response returns answer text + citations in `[file.md]` format
- [ ] Citations render as clickable file paths
- [ ] Retrieved chunks/snippets shown
- [ ] Loading/error states displayed
- [ ] Query logged to database

### Feature 3: Evidence-Based Confidence Gating

- [ ] Low similarity queries trigger fallback message
- [ ] Fallback message is clear and helpful
- [ ] Answerable responses include at least one citation; otherwise fallback is returned
- [ ] No unsupported factual claims in answerable responses (manual spot-check)
- [ ] Confidence level stored in query log

### Feature 4: Documentation Gap Radar

- [ ] Low-evidence queries appear in Gaps dashboard
- [ ] Gap entry shows question, timestamp, status, confidence level
- [ ] Gap entry displays confidence level (and optional numeric score if enabled for debugging)
- [ ] Repeated queries increment frequency counter
- [ ] User can update gap status (new → reviewed → resolved)
- [ ] Gaps sortable by frequency

### Feature 5: Web Dashboard

- [ ] Ask page renders without errors
- [ ] Sources page displays indexed files + metadata
- [ ] Gaps page displays all logged gaps
- [ ] Navigation between pages works
- [ ] Responsive design (mobile + desktop)

### Feature 6: Basic Observability

- [ ] All queries logged with latency, confidence level, sources
- [ ] Query logs are accessible for review (UI table and/or CSV export)
- [ ] Basic metrics calculated from query logs (avg latency, citation rate, gap ratio)
- [ ] Metrics viewable in UI or exported report

### Feature 7: CI/CD + Deployment

- [ ] GitHub Actions runs tests on PR
- [ ] Linting passes
- [ ] Build succeeds
- [ ] Frontend deployed to Vercel with live URL
- [ ] Backend deployed to Render with live URL
- [ ] App reachable via stable public URLs (free-tier cold starts acceptable and documented)
- [ ] Environment variables configured in Vercel/Render/Neon and documented in README
- [ ] `/health` endpoint returns 200
- [ ] Repo shared with `quantic-grader`

### Feature 8: Testing & Documentation

- [ ] Unit tests achieve > 70% backend coverage
- [ ] Integration tests pass for full RAG pipeline
- [ ] Evaluation set (20-30 questions) created
- [ ] DESIGN_AND_TESTING.md complete with all sections
- [ ] README has clear setup instructions + deliverable links
- [ ] Sprint artifacts saved in `/docs/sprints/`

### Feature 9: Basic Security & AI Safety Controls (MVP Minimum)

- [ ] API keys stored in environment variables only (`.env` in `.gitignore`)
- [ ] `.env.example` file included in repo
- [ ] Input validation enforced (max question length 500 chars, Pydantic schema)
- [ ] System prompt includes prompt-injection resistance instructions
- [ ] CORS configured for approved origins only (Vercel URL + localhost)
- [ ] Production error handling hides stack traces from UI responses
- [ ] Query audit logs stored with timestamps and sources

**If Time Allows:**

- [ ] Rate limiting implemented (IP-based or reverse-proxy level)
- [ ] Ingestion blocklist excludes sensitive patterns (`.env`, `secrets/`, `*.pem`)
- [ ] GitHub token scope documented as read-only
- [ ] Output constraints enforced (max response length, citation requirement)

---

## 🔗 Related Documentation

- [Project Overview](PROJECT_OVERVIEW.md) - Problem and solution
- [Capstone Requirements](CAPSTONE_REQUIREMENTS.md) - Quantic deliverables
- [System Architecture](SYSTEM_ARCHITECTURE.md) - Technical design
- [Implementation Details](IMPLEMENTATION_DETAILS.md) - How to build features
- [Sprint Plan](SPRINT_PLAN.md) - When to build features
