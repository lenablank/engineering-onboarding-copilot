# Trello Board Setup Guide

**Complete step-by-step instructions for setting up your Capstone Trello board**  
**Time required: 60-90 minutes**

---

## Step 1: Create Board (5 minutes)

1. Go to [trello.com](https://trello.com)
2. Click **"Create new board"**
3. **Board name**: `Engineering Onboarding Copilot - MSSE Capstone`
4. **Visibility**: Set to **Workspace** or **Public** (must be shareable with quantic-grader)
5. **Background**: Choose any color/image you like
6. Click **"Create"**

---

## Step 2: Create Lists (5 minutes)

Create these lists **in this exact order** (left to right):

1. **Backlog**
2. **Sprint 0 (Planning)**
3. **Sprint 1**
4. **Sprint 2**
5. **Sprint 3**
6. **In Progress**
7. **Blocked**
8. **Review / Verify**
9. **Done**

**How to create a list:**

- Click **"Add a list"** on the right
- Type the list name
- Click **"Add list"**
- Repeat for all 9 lists

---

## Step 3: Create Labels (5 minutes)

Click **"Show Menu"** (top right) → **"Labels"** → Create these labels:

| Label Name       | Color  | Purpose                            |
| ---------------- | ------ | ---------------------------------- |
| **Required**     | Red    | Quantic deliverables (must submit) |
| **MVP**          | Orange | Core features (must build)         |
| **Initiative**   | Purple | Above and beyond features          |
| **Evidence**     | Yellow | Provides rubric scoring evidence   |
| **Feature**      | Green  | Feature implementation             |
| **Deliverable**  | Blue   | Submission items                   |
| **Bug**          | Red    | Issues to fix                      |
| **Nice-to-Have** | Gray   | Post-MVP improvements              |
| **Sprint Demo**  | Pink   | Sprint demo recordings             |

---

## Step 4: Add Required Deliverable Cards to Backlog (15 minutes)

### Card 1: [DELIVERABLE] Share repo with quantic-grader

**Add to list:** Backlog  
**Labels:** Required, Deliverable, Evidence

**Description:**

```
Share GitHub repository with the quantic-grader account for evaluation.
Required by Quantic handbook.
```

**Checklist:**

- [ ] Create GitHub repository
- [ ] Add quantic-grader as collaborator (Settings → Collaborators)
- [ ] Verify access granted
- [ ] Document in Sprint 0 review (initial access)
- [ ] Re-verify access in Sprint 3 Week 2 (May 4-10)
- [ ] Add confirmation to CAPSTONE_SUBMISSION_LINKS.md

---

### Card 2: [DELIVERABLE] Deploy web application (live URL)

**Add to list:** Backlog  
**Labels:** Required, Deliverable, Evidence

**Description:**

```
Deploy frontend, backend, and database to free-tier hosting.
Provide live URL for grader testing.
```

**Checklist:**

- [ ] Deploy frontend to Vercel (free tier)
- [ ] Deploy backend to Render (free tier)
- [ ] Set up Neon Postgres database (free tier)
- [ ] Configure environment variables (all platforms)
- [ ] Verify app accessible via public URL
- [ ] Test all features work in production
- [ ] Add live URL to README.md
- [ ] Add live URL to CAPSTONE_SUBMISSION_LINKS.md

---

### Card 3: [DELIVERABLE] Trello board with sprint evidence

**Add to list:** Backlog  
**Labels:** Required, Deliverable, Evidence

**Description:**

```
Maintain Trello board documenting all tasks and sprints.
Must show completion of user stories and tasks.
```

**Checklist:**

- [ ] Create Trello board (this!)
- [ ] Add all lists and cards
- [ ] Complete Sprint 0 tasks
- [ ] Complete Sprint 1 tasks
- [ ] Complete Sprint 2 tasks
- [ ] Complete Sprint 3 tasks
- [ ] All 3 implementation sprints visible with artifacts
- [ ] Make board public/shareable
- [ ] Add Trello URL to README.md Quick Links section
- [ ] Add Trello URL to CAPSTONE_SUBMISSION_LINKS.md

---

### Card 4: [DELIVERABLE] DESIGN_AND_TESTING.md document

**Add to list:** Backlog  
**Labels:** Required, Deliverable, Evidence

**Description:**

```
Complete design and testing document in repository.
Must include patterns, rationale, and testing details.
```

**Checklist:**

- [ ] Start from DESIGN_AND_TESTING_TEMPLATE.md
- [ ] Document architecture decisions (Sprint 1-2)
- [ ] Document design patterns used (Service Layer, Repository, RAG)
- [ ] Document rationale for technology choices
- [ ] Document deployment options analysis + cost implications
- [ ] Document all testing done (unit, integration, evaluation)
- [ ] Document testing methods and coverage
- [ ] Add actual test results and metrics
- [ ] Complete traceability matrix
- [ ] Finalize by Sprint 3 Week 3 (May 11-17)
- [ ] Rename to DESIGN_AND_TESTING.md (remove TEMPLATE)

---

### Card 5: [DELIVERABLE] Demo video (15-20 min, ID shown, voice over)

**Add to list:** Backlog  
**Labels:** Required, Deliverable, Evidence

**Description:**

```
Record final capstone demonstration video.
Must show ID, face visible, voice over throughout.
```

**Checklist:**

- [ ] Prepare demo script (Sprint 3 Week 3)
- [ ] Test demo flow (ensure no errors)
- [ ] Record draft demo video (Sprint 3 Week 3: May 11-17)
- [ ] Review draft for issues
- [ ] Record final demo video (Sprint 3 Week 4: May 18-24)
- [ ] **Voice over included (speak throughout - required)**
- [ ] Government-issued ID shown clearly at start
- [ ] Face visible throughout presentation
- [ ] Demonstrate all core features (Ask, Citations, Gaps, Sources, Metrics)
- [ ] Show deployed app (not localhost)
- [ ] 15-20 minutes total length
- [ ] Upload to YouTube (unlisted), Google Drive, or Loom
- [ ] Add video link to CAPSTONE_SUBMISSION_LINKS.md

---

## Step 5: Add MVP Feature Cards to Backlog (20 minutes)

### Card 6: [FEATURE 1] GitHub Docs Sync (Manual Trigger)

**Add to list:** Backlog  
**Labels:** MVP, Feature

**Description:**

```
Ingest markdown files from configured GitHub repository or local path.
Manual sync trigger (no OAuth in MVP).
```

**Checklist:**

- [ ] Configure docs source path (local or GitHub)
- [ ] Implement markdown file discovery (.md files)
- [ ] Implement file reading (Python)
- [ ] Parse markdown content
- [ ] Semantic chunking by headers (LangChain)
- [ ] Preserve chunk metadata (file path, header hierarchy, chunk index)
- [ ] Generate embeddings (HuggingFace all-MiniLM-L6-v2, local, FREE)
- [ ] Store in Chroma vector DB
- [ ] Create /sync API endpoint
- [ ] Add "Sync Now" button in UI
- [ ] Display sync status (in progress / success / failed)
- [ ] Show sync metadata (file count, chunk count, timestamp)

---

### Card 7: [FEATURE 2] RAG Q&A with Citations

**Add to list:** Backlog  
**Labels:** MVP, Feature

**Description:**

```
Semantic search + answer generation with source citations.
Core RAG functionality.
```

**Checklist:**

- [ ] Implement question embedding (HuggingFace all-MiniLM-L6-v2, local, FREE)
- [ ] Implement semantic search (Chroma query)
- [ ] Retrieve top-k relevant chunks (k=5-10)
- [ ] Build LangChain RAG chain
- [ ] Create system prompt (citation enforcement)
- [ ] Integrate LLM (Groq Llama-3-8b-instant, free tier)
- [ ] Extract source citations from answer
- [ ] Create /ask API endpoint
- [ ] Return answer + sources + confidence + chunks
- [ ] Create Ask page UI
- [ ] Display answer text
- [ ] Display source citations (file paths, snippets)
- [ ] Show retrieved chunks for transparency

---

### Card 8: [FEATURE 3] Evidence-Based Confidence Gating

**Add to list:** Backlog  
**Labels:** MVP, Feature, Initiative

**Description:**

```
Detect low-evidence queries and provide safe fallback.
Prevents unsupported answers.
```

**Checklist:**

- [ ] Implement confidence detection function
- [ ] Check max similarity score (threshold ~0.7)
- [ ] Check context sufficiency (min chars, min sources)
- [ ] Return confidence level (high/medium/low/gap)
- [ ] Implement safe fallback response
- [ ] "I cannot answer this confidently from current documentation"
- [ ] Route low-evidence queries to gap logging
- [ ] Display confidence indicator in UI
- [ ] Test with edge cases (irrelevant questions, ambiguous queries)

---

### Card 9: [FEATURE 4] Documentation Gap Radar

**Add to list:** Backlog  
**Labels:** MVP, Feature, Initiative

**Description:**

```
Auto-log low-evidence queries and create gap dashboard.
Unique differentiator feature.
```

**Checklist:**

- [ ] Create Postgres documentation_gaps table
- [ ] Implement gap logging service
- [ ] Auto-log questions when confidence < threshold
- [ ] Track frequency (increment for repeated questions)
- [ ] Normalize questions for deduplication
- [ ] Store status (new/reviewed/resolved)
- [ ] Create /gaps API endpoint
- [ ] Create Gaps dashboard UI
- [ ] Display all gaps (question, timestamp, status, frequency)
- [ ] Sort by frequency/recency
- [ ] Add status management (mark reviewed/resolved)
- [ ] Optional: Add notes field
- [ ] Optional: Topic auto-tagging

---

### Card 10: [FEATURE 5] Web Dashboard (Ask/Sources/Gaps)

**Add to list:** Backlog  
**Labels:** MVP, Feature

**Description:**

```
Next.js frontend with 3 core pages.
Functional UI (polish secondary to functionality).
```

**Checklist:**

- [ ] Set up Next.js 14 project (App Router)
- [ ] Configure TypeScript + Tailwind CSS
- [ ] Create Ask page (chat-style interface)
- [ ] Create Sources page (list indexed docs + sync button)
- [ ] Create Gaps page (gap dashboard)
- [ ] Add navigation (header/sidebar)
- [ ] Add loading states
- [ ] Add error handling
- [ ] Connect to backend API
- [ ] Basic responsive design
- [ ] Deploy to Vercel

---

### Card 11: [FEATURE 6] Basic Observability

**Add to list:** Backlog  
**Labels:** MVP, Feature

**Description:**

```
Query logging and basic metrics.
CSV export or simple table display.
```

**Checklist:**

- [ ] Create Postgres query_logs table
- [ ] Log all queries (question, answer, latency, confidence, sources)
- [ ] Use UTC timestamps
- [ ] Calculate metrics:
  - Average latency
  - Citation presence rate
  - Answerable vs gap ratio
- [ ] Create /metrics API endpoint
- [ ] Display metrics in UI or export to CSV
- [ ] Optional: Add metrics page with simple charts

---

### Card 12: [FEATURE 7] CI/CD + Deployment

**Add to list:** Backlog  
**Labels:** MVP, Feature, Evidence

**Description:**

```
GitHub Actions CI/CD pipeline + deployed app.
Required rubric evidence.
```

**Checklist:**

- [ ] Create .github/workflows/ci.yml
- [ ] Add backend linting (ruff or flake8)
- [ ] Add backend unit tests (pytest)
- [ ] Add frontend linting (ESLint)
- [ ] Add frontend build check
- [ ] Configure CI to run on push to main
- [ ] Add build status badge to README
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render
- [ ] Configure production environment variables
- [ ] Add /health endpoint
- [ ] Verify CI/CD pipeline works end-to-end

---

### Card 13: [FEATURE 8] Testing & Documentation

**Add to list:** Backlog  
**Labels:** MVP, Feature, Evidence

**Description:**

```
Unit tests, integration tests, evaluation set.
Complete DESIGN_AND_TESTING.md document.
```

**Checklist:**

- [ ] Write unit tests for backend services (mocked LLM)
- [ ] Write integration tests for RAG pipeline
- [ ] Write minimal frontend component tests
- [ ] Target >70% backend coverage
- [ ] Create evaluation question set (20-30 questions)
- [ ] Run evaluation and collect metrics
- [ ] Document all tests in DESIGN_AND_TESTING.md
- [ ] Add docstrings to Python code
- [ ] Add JSDoc comments to TypeScript code
- [ ] Complete design rationale
- [ ] Complete testing methodology

---

### Card 14: [FEATURE 9] Security & AI Safety Controls

**Add to list:** Backlog  
**Labels:** MVP, Feature

**Description:**

```
Security controls split into must-ship and nice-to-have.
```

**Checklist - Must Ship (MVP Minimum):**

- [ ] Secrets management via .env (no credentials in source)
- [ ] Input validation (schema validation, max question length)
- [ ] Prompt-injection-aware prompting (treat docs as data)
- [ ] CORS restrictions (approved frontend origins)
- [ ] Production-safe error handling (no stack traces exposed)
- [ ] Query audit logging

**Checklist - Nice to Have (If Time Allows):**

- [ ] Output constraints (max response length)
- [ ] Least-privilege GitHub tokens (read-only)
- [ ] Data minimization (allowlist paths, exclude sensitive)
- [ ] Request rate limiting

---

## Step 6: Add Sprint Demo Cards (10 minutes)

### Card 15: [SPRINT DEMO] Record Sprint 1 Demo Video

**Add to list:** Sprint 1  
**Labels:** Required, Evidence, Sprint Demo  
**Due Date:** March 29, 2026

**Description:**

```
Record 5-10 minute demo of Sprint 1 deliverables.
Required by Quantic handbook for sprint review.
```

**Checklist:**

- [ ] Prepare demo script (show working Q&A system)
- [ ] Screen capture of Ask page
- [ ] Voice over explaining what was built
- [ ] Demonstrate question → answer with citations
- [ ] Show retrieved chunks/snippets
- [ ] Show basic RAG pipeline working
- [ ] Record video (5-10 minutes)
- [ ] Upload to YouTube (unlisted), Google Drive, or Loom
- [ ] Add link to /docs/sprints/sprint-1/sprint-review.md
- [ ] Reference video in sprint review notes

---

### Card 16: [SPRINT DEMO] Record Sprint 2 Demo Video

**Add to list:** Sprint 2  
**Labels:** Required, Evidence, Sprint Demo  
**Due Date:** April 26, 2026

**Description:**

```
Record 5-10 minute demo of Sprint 2 deliverables.
Show confidence gating and Gap Radar working.
```

**Checklist:**

- [ ] Prepare demo script (focus on new features)
- [ ] Screen capture of confidence gating
- [ ] Voice over explaining fallback behavior
- [ ] Demonstrate low-evidence question → gap logged
- [ ] Show Gaps dashboard with frequency tracking
- [ ] Show Sources page + manual sync
- [ ] Demonstrate status management (new → reviewed → resolved)
- [ ] Record video (5-10 minutes)
- [ ] Upload video
- [ ] Add link to /docs/sprints/sprint-2/sprint-review.md

---

### Card 17: [SPRINT DEMO] Record Sprint 3 Demo Video

**Add to list:** Sprint 3  
**Labels:** Required, Evidence, Sprint Demo  
**Due Date:** May 24, 2026

**Description:**

```
Record 5-10 minute demo of Sprint 3 deliverables.
Show testing, CI/CD, metrics, deployed app.
```

**Checklist:**

- [ ] Prepare demo script (testing + deployment focus)
- [ ] Screen capture of deployed app (not localhost)
- [ ] Voice over explaining testing approach
- [ ] Show CI/CD pipeline (GitHub Actions)
- [ ] Demonstrate metrics/observability
- [ ] Show test coverage report
- [ ] Demonstrate full end-to-end flow
- [ ] Record video (5-10 minutes)
- [ ] Upload video
- [ ] Add link to /docs/sprints/sprint-3/sprint-review.md

---

## Step 7: Add Sprint 0 Cards (10 minutes)

Move these cards to **Sprint 0 (Planning)** list (most should already be done today!):

### Card 18: Create Trello board

**Labels:** Required, Evidence  
**Status:** ✅ You're doing this right now!

---

### Card 19: Add required deliverable cards

**Labels:** Required  
**Checklist:**

- [ ] Card 1: Share repo
- [ ] Card 2: Deploy app
- [ ] Card 3: Trello board
- [ ] Card 4: Design/testing doc
- [ ] Card 5: Demo video

---

### Card 20: Add MVP feature cards

**Labels:** MVP  
**Checklist:**

- [ ] Card 6: GitHub sync
- [ ] Card 7: RAG Q&A
- [ ] Card 8: Confidence gating
- [ ] Card 9: Gap Radar
- [ ] Card 10: Web dashboard
- [ ] Card 11: Observability
- [ ] Card 12: CI/CD
- [ ] Card 13: Testing
- [ ] Card 14: Security

---

### Card 21: Add Sprint Demo cards

**Labels:** Required, Sprint Demo  
**Checklist:**

- [ ] Sprint 1 demo card
- [ ] Sprint 2 demo card
- [ ] Sprint 3 demo card

---

### Card 22: Create Sprint 0 artifacts folder

**Labels:** Required

**Checklist:**

- [ ] Create /docs/sprints/sprint-0/ folder
- [ ] Create sprint-goal.md (one-sentence objective)
- [ ] Create sprint-backlog.md (list of tasks)
- [ ] Create sprint-review.md (what was completed)

---

### Card 23: Initialize GitHub repo

**Labels:** Required, Evidence

**Checklist:**

- [ ] Create GitHub repo
- [ ] Add .gitignore (Python, Node, .env)
- [ ] Add README.md skeleton
- [ ] Create folder structure (backend/, frontend/, docs/)
- [ ] Initial commit
- [ ] Share with quantic-grader

---

### Card 24: Set up Next.js frontend

**Labels:** MVP

**Checklist:**

- [ ] Run npx create-next-app@latest
- [ ] Configure TypeScript
- [ ] Configure Tailwind CSS
- [ ] Create basic folder structure (components/, pages/, styles/)
- [ ] Test dev server runs

---

### Card 25: Set up FastAPI backend

**Labels:** MVP

**Checklist:**

- [ ] Create backend/ folder
- [ ] Create Python venv
- [ ] Install FastAPI, uvicorn, python-dotenv
- [ ] Create app/main.py with Hello World endpoint
- [ ] Create .env.example
- [ ] Test server runs (uvicorn app.main:app --reload)

---

### Card 26: ~~Configure OpenAI API~~ Sign up for Groq API (FREE)

**Labels:** Required, MVP

**Checklist:**

- [x] ~~Get OpenAI API key~~ OBSOLETE
- [x] ~~Set spending limit~~ OBSOLETE - Using FREE stack ($0 cost)
- [ ] Sign up for Groq API (console.groq.com, free tier: 14,400/day)
- [ ] Add GROQ_API_KEY to backend/.env (for Sprint 1 LLM)
- [ ] Test Groq connection (simple prompt)

**Note**: Embeddings use HuggingFace (local, no API key needed)

---

### Card 27: Create 5 synthetic docs

**Labels:** MVP

**Checklist:**

- [ ] Create synthetic-docs/ folder
- [ ] Create README.md (company overview)
- [ ] Create docs/setup.md (local environment)
- [ ] Create docs/architecture.md (system design)
- [ ] Create docs/testing.md (testing practices)
- [ ] Create docs/deployment.md (deploy instructions)
- [ ] Intentionally leave gaps for gap detection demo

---

### Card 28: Implement markdown ingestion

**Labels:** MVP

**Checklist:**

- [ ] Create backend/app/services/ingestion.py
- [ ] Implement file discovery (find .md files)
- [ ] Implement file reading
- [ ] Test with synthetic docs

---

### Card 29: Implement chunking

**Labels:** MVP

**Checklist:**

- [ ] Install langchain, langchain-text-splitters
- [ ] Implement MarkdownHeaderTextSplitter
- [ ] Implement RecursiveCharacterTextSplitter (chunk_size=2000)
- [ ] Preserve metadata (file path, headers, chunk index)
- [ ] Test chunking output

---

### Card 30: ~~Integrate OpenAI~~ Set up HuggingFace embeddings (FREE)

**Labels:** MVP

**Checklist:**

- [x] Install sentence-transformers
- [x] Create backend/app/services/embeddings.py (or integrate in main.py)
- [x] Implement HuggingFace embedding generation (all-MiniLM-L6-v2)
- [x] Test local embedding generation (first run downloads model ~90MB)
- [x] Verify embeddings work ($0 cost, unlimited usage)

**Note**: Already completed in Sprint 0 with prove_pipeline_simple.py

---

### Card 31: Set up Chroma vector DB

**Labels:** MVP

**Checklist:**

- [ ] Install chromadb
- [ ] Create backend/app/services/vector_store.py
- [ ] Initialize Chroma client (persistent)
- [ ] Store embeddings + metadata
- [ ] Test storage works

---

### Card 32: Prove retrieval works

**Labels:** MVP

**Checklist:**

- [ ] Implement query function
- [ ] Test: query → retrieve similar chunks
- [ ] Print top 5 results
- [ ] Verify relevance scores
- [ ] Verify metadata preserved

---

### Card 33: Sprint 0 Review

**Labels:** Required

**Checklist:**

- [ ] Document what was completed
- [ ] Write /docs/sprints/sprint-0/sprint-review.md
- [ ] Take screenshots of Trello board
- [ ] Note what worked well
- [ ] Note what to improve
- [ ] Confirm ready for Sprint 1 (starts Mar 2)

---

## Step 8: Populate Sprint 1 Tasks (10 minutes)

Add these granular task cards to **Sprint 1** list:

1. Expand synthetic docs to 10-15 files
2. Implement full GitHub file ingestion
3. Add markdown parsing for code blocks/tables
4. Implement semantic chunking (MarkdownHeaderTextSplitter)
5. Preserve chunk metadata (file path, headers)
6. ~~Integrate OpenAI~~ Already done: HuggingFace embeddings (Sprint 0, FREE)
7. Sign up for Groq API (FREE tier, for LLM)
8. Set up Chroma vector DB (persistent)
9. Build RAG chain with LangChain + Groq
10. Create /ask API endpoint (FastAPI)
11. Create Ask page UI (Next.js)
12. Display citations + source snippets
13. Add error handling (loading states, API errors)
14. Write unit tests for chunking
15. Write unit tests for embeddings (mocked)
16. Set up basic CI/CD pipeline (GitHub Actions)
17. First evaluation run (5-10 test questions)
18. Sprint 1 retrospective
19. [SPRINT DEMO] Record Sprint 1 demo video

---

## Step 9: Final Checklist (5 minutes)

Before you start working, verify:

- [ ] ✅ Board created and named correctly
- [ ] ✅ All 9 lists created in correct order
- [ ] ✅ All 9 labels created with correct colors
- [ ] ✅ 5 required deliverable cards in Backlog
- [ ] ✅ 9 MVP feature cards in Backlog
- [ ] ✅ 3 Sprint Demo cards (one in each Sprint list)
- [ ] ✅ 16 Sprint 0 task cards created
- [ ] ✅ 18 Sprint 1 task cards created
- [ ] ✅ Board visibility set to Public/Workspace
- [ ] ✅ You're ready to start working!

---

## Step 10: Update Documentation

Once your Trello board is created:

1. **Add Trello URL to README.md:**

```markdown
## 📋 Quick Links

- **Trello Board**: [View Sprint Progress](YOUR_TRELLO_URL_HERE) - Agile task tracking
- **Sprint Plan**: [docs/planning/SPRINT_PLAN.md](docs/planning/SPRINT_PLAN.md) - Week-by-week guide
```

2. **Create CAPSTONE_SUBMISSION_LINKS.md:**

```markdown
# Capstone Submission Links

**Student Name**: Your Name  
**Submission Date**: May 24, 2026

## Required Deliverables

1. **GitHub Repository**: https://github.com/YOUR_USERNAME/YOUR_REPO
2. **Deployed Application**: [To be added in Sprint 3]
3. **Trello Board**: YOUR_TRELLO_URL_HERE
4. **Design & Testing Document**: [DESIGN_AND_TESTING.md](DESIGN_AND_TESTING.md)
5. **Demo Video**: [To be added in Sprint 3 Week 4]

## Sprint Demo Videos

- **Sprint 1 Demo**: [To be added Mar 29]
- **Sprint 2 Demo**: [To be added Apr 26]
- **Sprint 3 Demo**: [To be added May 24]
```

---

## 🎉 You're Done!

Your Trello board is now:

- ✅ Fully set up with all required cards
- ✅ Aligned with Quantic handbook requirements
- ✅ Ready for Sprint 0 work (starting today)
- ✅ Organized to track all 3 implementation sprints

**Next step:** Start moving Sprint 0 cards to "In Progress" and get to work!

---

## 💡 Tips for Using Your Board

### Daily Workflow:

1. Pick a card from current sprint list
2. Move to "In Progress"
3. Work on it
4. Move to "Review / Verify" when done
5. Test/verify it works
6. Move to "Done"

### Weekly Workflow:

- Friday: Review what you completed
- Check off checklist items
- Update sprint artifacts
- Plan next week's priorities

### Sprint Workflow:

- End of sprint: Record demo video
- Write sprint review
- Write sprint retrospective
- Move all unfinished cards back to Backlog
- Populate next sprint list

**Good luck with your capstone! 🚀**
