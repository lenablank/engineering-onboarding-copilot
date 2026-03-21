# Sprint Implementation Plan

**Sprint 0 (Planning) + 3 Implementation Sprints over 12 Weeks**  
**Protected Buffer Week Before May 31 Deadline**  
**Solo Capstone Project - Structured for Quantic Requirements**

---

## 📅 Timeline Overview

- **Sprint 0 (Planning + Setup)**: Feb 25 - Mar 1 (5 days)
- **Sprint 1 (Foundation + Basic RAG)**: Mar 2 - Mar 29 (4 weeks)
- **Sprint 2 (Gap Radar + Confidence + UI)**: Mar 30 - Apr 26 (4 weeks)
- **Sprint 3 (Testing + Deploy + Docs)**: Apr 27 - May 24 (4 weeks)
- **Protected Buffer**: May 25 - May 31 (7 days - emergency fixes only, ideally zero work)

**Personal Deadline**: May 24, 2026  
**Official Deadline**: May 31, 2026

---

## 🎯 Agile Process Note (Solo Project)

Even as a solo developer, maintain formal Scrum structure to align with Quantic rubric requirements:

### Roles (All You)

- **Product Owner**: Define requirements, prioritize backlog, accept user stories
- **Scrum Master**: Facilitate process, remove blockers, track progress
- **Developer**: Implement features, write tests, deploy

### Sprint Artifacts (Create for Each Sprint)

Store in `/docs/sprints/sprint-{N}/`:

- `sprint-goal.md` - One-sentence objective
- `sprint-backlog.md` - User stories with acceptance criteria (or Trello export)
- `sprint-review.md` - Demo notes, acceptance decisions
- `sprint-retro.md` - What went well, what to improve

---

## 📅 Sprint 0: Planning + Setup (Feb 25 - Mar 1, 2026)

**Sprint Goal**: "Lock scope, create Trello board, set up repo skeleton, and prove core pipeline before heavy coding"

### Tasks (5 days)

**Day 1-2 (Feb 25-26): Trello + Scope Lock**

- [ ] Create Trello board with lists:
  - Backlog, Sprint 0, Sprint 1, Sprint 2, Sprint 3, In Progress, Blocked, Review/Verify, Done
- [ ] Add 5 required Quantic deliverable cards:
  - Share repo with `quantic-grader`
  - Deploy web application (live URL)
  - Trello board with sprint evidence
  - `DESIGN_AND_TESTING.md` document
  - Demo video (15-20 min, ID shown)
- [ ] Add MVP Features 1-9 as cards
- [ ] Populate Sprint 1 backlog (15-20 tasks)
- [ ] Create `/docs/sprints/sprint-0/` folder with:
  - `sprint-goal.md`
  - `sprint-backlog.md`

**Day 2-3 (Feb 26-27): Repo + Environment**

- [ ] Initialize GitHub repo (monorepo recommended)
- [ ] Share repo with `quantic-grader` (initial access)
- [ ] Set up Next.js project (`npx create-next-app@latest`)
- [x] Set up FastAPI project (create venv, install dependencies)
- [ ] Configure linting/formatting (ESLint, Prettier, Black)
- [x] ~~Set OpenAI API key~~ OBSOLETE - Using FREE stack (no API key for embeddings)
- [x] Create repo skeleton:
  - `backend/app/` (main.py, services/, models/, tests/)
  - `frontend/` (defer to Sprint 1)
  - `docs/sprints/`
  - `README.md`, `.gitignore`, `.env.example`

**Day 4-5 (Feb 28 - Mar 1, extended to Mar 8): Synthetic Docs + Prove Pipeline**

- [x] **Create 5 synthetic docs** (mock company engineering docs):
  - `synthetic-docs/1-getting-started.md`
  - `synthetic-docs/2-architecture-overview.md`
  - `synthetic-docs/3-testing-guide.md`
  - `synthetic-docs/4-deployment.md`
  - `synthetic-docs/5-api-reference.md`
  - (Intentionally leave gaps for gap detection demo)
- [x] Implement markdown file reading (Python)
- [x] Implement basic chunking (LangChain RecursiveCharacterTextSplitter)
- [x] HuggingFace embedding integration (FREE, local, all-MiniLM-L6-v2)
- [x] Store first embeddings in Chroma (prove vector DB works)
- [x] Verify vector search works (test query: "How do I set up development environment?")
- [x] Migrate to FREE stack (cost-conscious engineering decision)
- [ ] Update all documentation for FREE stack
- [ ] Create GitHub repo and share with quantic-grader
- [x] **Sprint 0 Review**: Pipeline proven ($0 cost), ready for Sprint 1

**Deliverables**:

- Trello board populated with all sprints
- Repo skeleton initialized
- Python environment configured (venv, dependencies)
- FREE stack proven (HuggingFace + Groq for Sprint 1)
- Synthetic docs created (5 files minimum)
- Core pipeline proven (markdown → chunks → embeddings → retrieval)
- Sprint 0 artifacts (`sprint-goal.md`, `sprint-review.md`)
- **Total cost: $0**
- Core pipeline proven (markdown → chunks → embeddings → retrieval)
- Sprint 0 artifacts (`sprint-goal.md`, `sprint-review.md`)

**De-Risk Rationale**: Prove ingestion → chunking → embedding → retrieval EARLY with minimal docs before expanding. Creating all docs first risks burning time before knowing if the pipeline works.

---

## 📅 Sprint 1: Foundation + Basic RAG (Mar 2 - Mar 29, 2026)

**Sprint Goal**: "Deliver working Q&A system with GitHub sync and basic RAG pipeline"

### Week 1-2 (Mar 2-15): Expand Synthetic Docs + Ingestion Pipeline

**Tasks**:

- [ ] **Expand synthetic docs to 10-15 files** (now that pipeline proven in Sprint 0)
- [ ] Implement full GitHub file ingestion (local path first)
- [ ] Markdown parsing improvements (handle code blocks, tables)
- [ ] Semantic chunking by headers (LangChain MarkdownHeaderTextSplitter)
- [ ] Chunk metadata preservation (file path, header hierarchy, chunk index)

**Deliverables**:

- Synthetic docs corpus (~10-15 files)
- Full markdown ingestion pipeline
- Proper semantic chunking working

---

### Week 3-4 (Mar 16-29): RAG Pipeline + Basic UI

**Tasks**:

- [ ] Sign up for Groq API (free tier, 14,400 requests/day)
- [ ] Add GROQ_API_KEY to backend/.env
- [ ] Test Groq LLM connectivity with simple prompt
- [ ] Create LangChain RAG chain:
  - Prompt template with citations
  - Answer generation with Groq Llama-3-8b-instant (FREE, fast)
  - Source extraction
- [ ] Test with sample questions
- [ ] **First evaluation run** (prove pipeline works early)

- [ ] Create Ask page (simple chat interface)
- [ ] Display answer + source citations
- [ ] Show retrieved chunks/snippets for transparency
- [ ] Basic error handling (loading states, API errors)
- [ ] **Sprint 1 Review** (Mar 29): Working Q&A demo

**Deliverables**:

- Groq API configured (free tier)
- Chroma vector DB with indexed docs (using HuggingFace embeddings from Sprint 0)
- Basic RAG Q&A functionality with Groq LLM
- Functional web UI (Ask page)
- User can submit question and get cited answer
- Initial test results
- Sprint 1 review notes (`sprint-review.md`)
- Sprint 1 retrospective (`sprint-retro.md`)

---

## 📅 Sprint 2: Confidence + Gap Detection (Mar 30 - Apr 26, 2026)

**Sprint Goal**: "Capstone-ready RAG with confidence gating and Documentation Gap Radar differentiator"

**Feature Freeze**: No new user-facing features after Sprint 2 review unless required to fix a blocker for MVP acceptance criteria.

### Week 1-2 (Mar 30 - Apr 12): Confidence Scoring + Fallback

**Tasks**:

- [ ] Implement confidence detection:
  - Similarity score threshold (e.g., < 0.7 = low confidence)
  - Context sufficiency check (min words, min sources)
  - Source quality scoring
- [ ] Safe fallback responses ("I cannot answer this confidently...")
- [ ] Prevent unsupported answers via citation grounding
- [ ] Improve prompt engineering:
  - Strict citation enforcement
  - "Answer only from provided context"
  - Better few-shot examples
- [ ] Test edge cases (irrelevant questions, ambiguous queries)
- [ ] Document deployment options analysis in DESIGN_AND_TESTING.md:
  - Local-only vs. Vercel+Render vs. cloud-native
  - Cost implications documented
  - Selected option with rationale

**Deliverables**:

- Confidence gating functional
- Evidence-based fallback behavior
- Deployment analysis documented

---

### Week 3 (Apr 13-19): Documentation Gap Radar ⭐ (Differentiator)

**Tasks**:

- [ ] Create Postgres `documentation_gaps` table
- [ ] Implement gap logging service:
  - Auto-log low-confidence questions
  - Track frequency (increment for repeated questions)
  - (Optional if time allows: Topic tagging - rule-based or LLM-extracted)
- [ ] Gap dashboard UI:
  - List all gaps (question, timestamp, status)
  - Sort by frequency/recency
  - Status management (new → reviewed → resolved)
  - (Optional if time allows: Add notes field)

**Deliverables**:

- Documentation Gap Radar fully functional
- Gap dashboard accessible in web UI
- Frequency tracking working

---

### Week 4 (Apr 20-26): Sources & Sync Management UI + Sprint Review

**Tasks**:

- [ ] Sources page:
  - List indexed documents
  - Show last sync timestamp
  - File count, chunk count
- [ ] Manual "Sync Now" button
- [ ] Sync status indicator (in progress/success/failed)
- [ ] Re-sync capability (clear old index, re-ingest)

**Deliverables**:

- Sources page functional
- Sync management working
- User can trigger manual sync

---

**Tasks (continued)**:

- [ ] Test with diverse questions (onboarding scenarios)
- [ ] **Sprint 2 Review** (Apr 26): Gap detection demo
- [ ] Sprint 2 retrospective

**Deliverables**:

- Sources page functional
- Sync management working
- User can trigger manual sync
- Sprint 2 review notes
- Sprint 2 retrospective

**Note**: Testing moved to Sprint 3 for better sequencing

---

## 📅 Sprint 3: Testing + Deploy + Demo (Apr 27 - May 24, 2026)

**Sprint Goal**: "Fully tested, deployed, demo-ready system with all submission artifacts complete by May 24"

**Focus**: Observability, deployment, tests, docs, demo, and bug fixes only (no new features)

### Week 1 (Apr 27 - May 3): Testing + Metrics

**Tasks (Prioritized)**:

- [ ] **Unit tests (backend services with mocked LLM calls)** - Priority 1
- [ ] **Integration tests (full RAG pipeline with test corpus)** - Priority 1
- [ ] Minimal frontend component tests for core components (Ask, Gaps, Sources) - Priority 2
- [ ] Implement query logging (all questions → Postgres)
- [ ] Metrics calculation:
  - Average latency per query
  - Citation presence rate
  - Answerable vs. gap ratio
  - (Optional: Most common topics)
- [ ] Metrics dashboard or export (CSV/JSON)
- [ ] Performance optimization:
  - Batch embedding generation
  - Query time optimization (aim for <4s p50)

**Deliverables**:

- Test suite >70% backend coverage
- Integration tests passing
- Query logging functional
- Basic observability metrics
- Metrics viewable/exportable

---

### Week 2 (May 4-10): CI/CD + Deployment

**Tasks**:

- [ ] GitHub Actions workflow:
  - Linting (ESLint, ruff/black)
  - Tests (pytest, frontend tests)
  - Build checks
- [ ] Deploy backend to Render (or Railway free tier)
- [ ] Deploy frontend to Vercel
- [ ] Set up Neon Postgres (production DB)
- [ ] Environment variable management (secrets)
- [ ] Health check endpoint (`/health`)
- [ ] **Verify `quantic-grader` repo access still active + final repo readiness**

**Deliverables**:

- CI/CD pipeline functional
- Deployed application (live URLs)
- Production database configured
- Repo shared with grader

---

### Week 3 (May 11-17): Documentation + Demo Prep

**Tasks**:

- [ ] Create demo script (15-20 min presentation structure)
- [ ] Prepare demo questions showcasing:
  - Successful Q&A with citations
  - Gap detection in action
  - Sources transparency
  - Metrics overview
- [ ] **Record draft demo video** (rehearsal - allows re-recording if needed)
- [ ] Verify README.md has:
  - Project overview
  - Setup instructions
  - Architecture diagram
  - Demo walkthrough
- [ ] Complete DESIGN_AND_TESTING.md:
  - Architecture + patterns + rationale
  - Testing strategy + results
  - Deployment options + cost analysis

**Deliverables**:

- Draft demo video recorded (15-20 min)
- README.md complete
- DESIGN_AND_TESTING.md complete
- Sprint artifacts for all sprints (0, 1, 2, 3)

---

### Week 4 (May 18-24): Final Polish + Submission

**Tasks**:

- [ ] UI polish (consistent styling, loading states, error messages)
- [ ] Final testing (end-to-end user flows)
- [ ] Performance check (latency < 4s p50)
- [ ] Security review:
  - API key protection (.env not committed)
  - Input validation working
  - CORS configured
  - No stack traces in production
- [ ] **Record final demo video** (or use draft from Week 3 if sufficient):
  - Government-issued ID shown clearly
  - Face visible throughout
  - Professional presentation
- [ ] **ALL WORK COMPLETE BY MAY 24** (personal deadline)
- [ ] **Capstone submission ready**:
  - CAPSTONE_SUBMISSION_LINKS.md populated
  - All links verified working
  - Trello board public/shared
  - Demo video uploaded

**Deliverables (by May 24)**:

- Production-ready application
- All required deliverables submitted
- Sprint 3 review + retrospective
- Capstone complete! 🎉

---

## 📅 Protected Buffer Week (May 25-31, 2026)

**Goal**: Rest + emergency fixes only (ideally ZERO project work)

**Allowed Activities**:

- Fix critical deployment bugs only (if app goes down)
- Re-upload demo video only if file corrupted
- Update submission links only if broken

**NOT Allowed**:

- New features
- Major refactoring
- Scope expansion
- "Just one more thing" syndrome

**If May 24 deadline was met, this week should be completely free.**

**Official submission deadline: May 31, 2026**

---

## 🚀 Immediate Next Steps (Sprint 0 Kickoff - Feb 25-Mar 1)

See Sprint 0 section above for detailed breakdown. Key focus:

1. **Day 1-2**: Create Trello board, add all cards, Sprint 0 artifacts
2. **Day 2-3**: Repo setup, environment config, skeleton folders
3. **Day 4-5**: Create 5 synthetic docs, prove core pipeline

**Sprint 0 Goal**: Lock scope, prove pipeline, ready for Sprint 1 coding on Mar 2.

---

## ✅ Definition of Done

### Per User Story

- [ ] Code written and committed
- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] No linting errors
- [ ] Documented in code comments/docstrings
- [ ] Manually tested in browser/API
- [ ] Reviewed (self-review checklist completed)
- [ ] Merged to main branch
- [ ] Trello card moved to Done

### Per Sprint

- [ ] Sprint goal demo recorded (video or screenshots + notes)
- [ ] Sprint review notes written (`/docs/sprints/sprint-N/sprint-review.md`)
- [ ] Sprint retrospective notes written (`/docs/sprints/sprint-N/sprint-retro.md`)
- [ ] Trello board updated (all done cards moved, next sprint populated)
- [ ] Main branch CI/CD passing (all tests green)
- [ ] Documentation updated for completed features (README, DESIGN_AND_TESTING.md)
- [ ] Evaluation run completed (if Sprint 2 or later)
- [ ] No incomplete user stories marked as "Done" (be honest)

---

## 📆 Weekly Cadence

**Monday**: Sprint planning (if starting new sprint), review backlog  
**Wednesday**: Mid-sprint check-in, adjust if blocked  
**Friday**: Weekly review, update Trello, plan next week  
**End of Sprint**: Sprint review (demo to self as PO), retrospective (write notes)

---

## 🚨 Risk Register

| Risk                                | Impact   | Mitigation                                                          |
| ----------------------------------- | -------- | ------------------------------------------------------------------- |
| **Scope creep**                     | High     | MVP scope frozen, stretch goals explicitly deferred                 |
| **~~OpenAI costs~~** OBSOLETE       | None     | Using FREE stack (HuggingFace + Groq) = $0 cost                     |
| **Groq rate limits**                | Very Low | 14,400/day free tier >> project needs (~10-20/day), <1% utilization |
| **Free-tier deployment unreliable** | Low      | Accept cold start latency, document in limitations                  |
| **Evaluation shows low quality**    | Medium   | Test early (Week 3), iterate on prompts and thresholds              |
| **Solo burnout**                    | Medium   | Weekly reviews, realistic sprint sizing, skip stretch if needed     |
| **Chroma/vector DB issues**         | Low      | Well-tested library, local-first, fall back to in-memory if needed  |

---

## 🎯 Success Criteria (Prioritized)

### Priority 1 - Required Deliverables

- [ ] GitHub repository shared with quantic-grader
- [ ] Deployed web application with live URL
- [ ] Trello board with 3+ sprints visible
- [ ] DESIGN_AND_TESTING.md complete
- [ ] 15-20 min demo video (ID shown, face visible)

### Priority 2 - Rubric-Critical Evidence

- [ ] Stable deployed demo (works throughout presentation)
- [ ] 3 sprints with agile artifacts (goals, reviews, retros)
- [ ] CI/CD pipeline functional (GitHub Actions)
- [ ] Well-designed code (patterns, service layers)
- [ ] Well-tested code (>70% coverage, regression set)

### Priority 3 - Score-Boosting Differentiators

- [ ] Documentation Gap Radar (unique, shows initiative)
- [ ] Systematic evaluation methodology (metrics, regression testing)
- [ ] Security & AI safety controls (production thinking)
- [ ] Evidence-based gating (goes beyond basic RAG)

---

**This sprint plan is your roadmap to a successful capstone. Follow it systematically, maintain agile discipline, and you'll deliver an impressive project.** 🚀

**See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for full project context, [SYSTEM_ARCHITECTURE.md](../technical/SYSTEM_ARCHITECTURE.md) for technical architecture, and [IMPLEMENTATION_DETAILS.md](../technical/IMPLEMENTATION_DETAILS.md) for implementation guidance.**
