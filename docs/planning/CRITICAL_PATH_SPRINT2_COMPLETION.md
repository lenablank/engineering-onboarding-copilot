# Critical Path to Capstone Completion

**Analysis Date**: April 12, 2026  
**Days Remaining**: 14 days until April 26 deadline  
**Total Critical Work**: ~25 hours  
**Daily Average Needed**: 2 hours/day (manageable)

**Current Status**: 70% Complete - Higher Risk Than Expected

---

## ❌ CRITICAL BLOCKERS (Will Fail Capstone Without These)

### 1. DESIGN_AND_TESTING.md is 40% Placeholders ⚠️
**Current State**: Template text with `[Describe...]`, `[Insert...]`, `[To be completed...]`  
**Risk Level**: 🔴 **IMMEDIATE FAILURE** - This is graded deliverable #4  
**Time to Fix**: 6 hours

**What's Missing**:
- Section 1: Problem statement is placeholder: `[Describe the onboarding inefficiency problem...]`
- Section 2: Architecture diagrams: `[Insert High-Level Architecture diagram...]`
- Section 2: Data flow diagram: `[Insert Question Answering Flow diagram...]`
- Section 6: Confidence thresholds: `[Document actual thresholds tuned on evaluation set...]`
- Section 8: Test execution results: `[To be completed during implementation]`
- Section 10: Evaluation results: `[Insert table of 20-30 questions with expected behaviors...]`

**Impact**: Quantic graders expect completed documentation, not templates. Placeholders = incomplete work = low score.

---

### 2. No CI/CD Pipeline 🔴
**Current State**: `.github/workflows/*.yml` - **FILE DOES NOT EXIST**  
**Risk Level**: 🔴 **RUBRIC FAILURE** - "CI/CD tools & methodology" is explicit scoring criteria  
**Time to Fix**: 2-3 hours

**Why Critical**: 
- Quantic handbook explicitly requires: *"evidence of using CI/CD tools and following methodology"*
- This is TABLE STAKES for 2026 software engineering
- Without it, you're demonstrating outdated practices
- Easy to implement, unacceptable to skip

**What's Expected**:
- Automated tests on every push/PR
- Lint checks (black, flake8, eslint, prettier)
- Build verification (both frontend and backend)
- Success/fail badges in README (professional presentation)
- Status checks before merge (if using PRs)

**Files Needed**:
- `.github/workflows/ci.yml` (backend tests + linting)
- `.github/workflows/frontend.yml` (frontend build + type check)
- Update README.md with build status badges

---

### 3. No Deployment 🔴
**Current State**: CAPSTONE_SUBMISSION_LINKS.md says *"To be added in Sprint 3"*  
**Risk Level**: 🔴 **CANNOT SUBMIT** - Deliverable #2 requires live public URL  
**Time to Fix**: 3-4 hours scheduled, **6-8 hours realistic** (deployment always has surprises)

**Why This is Highest Risk**:
- External dependencies (Vercel, Render services)
- Environment variables (easy to misconfigure)
- CORS issues (common first-time deployment problem)
- Cold start troubleshooting on Render free tier
- DNS propagation delays
- Database initialization in production
- ChromaDB persistence strategy validation
- **Unknowns that can block for days**

**Timeline Concern**: 
- We're April 12, submission windows start soon
- If deployment blocks for 2-3 days, you're in serious trouble
- Need deployed URL for evaluation to be meaningful
- Need deployed URL for demo video recording

**What's Needed**:
1. Vercel account + project setup (frontend)
2. Render account + web service setup (backend)
3. Environment variables configured (Groq API key, CORS origins)
4. Health check endpoint verification (`/health` returns 200)
5. Frontend → Backend connectivity tested
6. ChromaDB re-indexing on startup verified
7. Gap logging to SQLite verified
8. All features working end-to-end on deployed URLs

**Evidence Required**:
- Update CAPSTONE_SUBMISSION_LINKS.md with live URLs
- Screenshots of deployed app (backup if free tier flaky)
- Health check response showing 275 chunks indexed

---

### 4. No Evaluation Run (Task #12) 🟡
**Current State**: No regression test set, no metrics measurement  
**Risk Level**: 🟡 **Missing Differentiator** - Systematic evaluation shows initiative  
**Time to Fix**: 3-4 hours  
**Impact**: Difference between 6/10 and 9/10 score

**What Makes This Important**:
- Demonstrates systematic engineering methodology
- Proves quality beyond "it works on my machine"
- Shows production thinking (metrics-driven decisions)
- Provides concrete data for DESIGN_AND_TESTING.md Section 10
- Highlights Gap Radar differentiator with real metrics

**What's Needed**:
1. Create 15-20 test questions covering:
   - **Answerable** (5-7 questions): Questions with good doc coverage
   - **Partial** (3-4 questions): Questions with some but incomplete docs
   - **Gaps** (4-5 questions): Questions with no relevant docs (should trigger gap logging)
   - **Edge cases** (2-3 questions): Ambiguous, multi-part, or complex queries

2. Run against deployed system (or local if deployment delayed)

3. Measure metrics:
   - **Answer accuracy** (manual review: correct/incorrect/partial)
   - **Citation rate** (% of answers with proper source citations)
   - **Confidence scoring** (distribution of confidence scores)
   - **Latency** (p50, p95, p99 response times)
   - **Gap detection rate** (% of actual gaps correctly identified)
   - **False positive rate** (% of answerable questions incorrectly marked as gaps)

4. Document results in:
   - `docs/evaluation/sprint-2-eval-results.md` (detailed results)
   - DESIGN_AND_TESTING_TEMPLATE.md Section 10 (summary table)

**Example Test Questions**:
```
Answerable:
- "How do I run tests locally?"
- "What's our CI/CD pipeline configuration?"
- "How do I set up the database?"

Gaps:
- "How do we rotate API keys in production?"
- "What's the incident response process?"
- "How do we handle GDPR data deletion requests?"
```

---

### 5. No Demo Video 🔴
**Current State**: Not recorded  
**Risk Level**: 🔴 **CANNOT SUBMIT** - Deliverable #5 is mandatory  
**Time to Fix**: 4-6 hours (script 1h, practice 1h, record 2-3h, editing 1h)  
**Reality**: Plan for 2-3 takes (first recording always has mistakes)

**Quantic Requirements** (Non-Negotiable):
- ✅ Duration: 15-20 minutes (not shorter, not longer)
- ✅ Government-issued ID shown clearly at beginning (name visible)
- ✅ Face visible throughout presentation (or at required intervals per rubric)
- ✅ Audio quality clear (no background noise, test microphone)
- ✅ Screen text legible (zoom in on small text, high resolution recording)
- ✅ All required elements covered: problem, solution, architecture, demo, results

**Content Structure**:
1. **Introduction** (2 min): ID shown, problem statement, solution overview
2. **Architecture** (3 min): System diagram, tech stack, design decisions
3. **Live Demo** (8-10 min): Ask questions, show citations, trigger gap, show Gap Radar
4. **Evaluation Results** (2 min): Metrics, what worked, what didn't
5. **Agile Process** (2 min): Sprint artifacts, Trello board, retrospectives
6. **Conclusion** (1 min): Lessons learned, future improvements

**Recording Tips**:
- Use OBS Studio or Zoom (test beforehand)
- Record in quiet environment (no interruptions)
- Close unnecessary browser tabs (clean demo environment)
- Pre-seed database with 3-5 gap examples
- Prepare 5-7 sample questions with known good answers
- Have backup recording (record twice if possible)
- Export in MP4 format (widely compatible)

**Common Mistakes to Avoid**:
- ❌ Not showing ID clearly (automatic resubmission)
- ❌ Face not visible (violates rubric requirements)
- ❌ Going over 20 minutes (shows poor planning)
- ❌ Under 15 minutes (seems rushed, incomplete)
- ❌ No audio testing (poor quality audio)
- ❌ Tiny text unreadable (zoom in!)
- ❌ Rambling without structure (write script first)

---

## ⚠️ HIGH-PRIORITY GAPS (Impact Score 7/10→9/10)

### 6. Test Coverage Unknown
**Current State**: 7 test files exist (`test_*.py`), but no coverage measurement  
**Issue**: Cannot claim "well-tested code" without evidence  
**Time to Fix**: 30 minutes  

**Fix**:
```bash
cd backend
source venv/bin/activate
pytest --cov=app --cov-report=html --cov-report=term
open htmlcov/index.html
```

**Document in**: DESIGN_AND_TESTING_TEMPLATE.md Section 8  
**Target**: >70% backend coverage (focus on business logic, not boilerplate)

---

### 7. Architecture Diagrams Missing
**Current State**: Placeholders in Section 2: `[Insert High-Level Architecture diagram...]`  
**Issue**: Graders expect visual documentation, text-only is weak  
**Time to Fix**: 1-2 hours

**Required Diagrams**:
1. **System Architecture** (components + data flow):
   ```
   [Frontend (Next.js)] → [Backend API (FastAPI)] → [Vector DB (Chroma)]
                                                  ↘ [SQLite (Gaps)]
                                                  ↘ [LLM (Groq)]
   ```

2. **Question Answering Flow** (request/response):
   ```
   User Question → Embedding → Vector Search → Context Retrieval 
   → Prompt + Context → LLM → Answer + Citations → User
        ↓ (if low confidence)
   Gap Detection → Log to DB → Gap Radar
   ```

**Tools**: 
- Mermaid (markdown-native, renders in GitHub)
- draw.io (easy, export as PNG)
- ASCII art (acceptable if clear)
- Excalidraw (simple, clean)

**Insert in**: DESIGN_AND_TESTING_TEMPLATE.md Section 2

---

### 8. Sprint 3 Not Started
**Current State**: Sprint 2 ending April 12, Sprint 3 artifacts don't exist  
**Issue**: Rubric requires "3+ sprints with agile artifacts"  
**Time to Fix**: 1 hour

**Required Sprint 3 Artifacts**:
- `docs/sprints/sprint-3/sprint-goal.md` - Deployment + evaluation + demo
- `docs/sprints/sprint-3/sprint-backlog.md` - Task list with estimates
- `docs/sprints/sprint-3/sprint-review.md` - What was delivered (write at end)
- `docs/sprints/sprint-3/sprint-retrospective.md` - Lessons learned (write at end)

**Sprint 3 Focus** (April 13-26, 14 days):
- CI/CD setup
- Deployment (Vercel + Render)
- Evaluation run
- Documentation completion
- Demo video recording
- Final polish

---

## ✅ WHAT'S WORKING WELL (Don't Touch, Already Strong)

- ✅ **Gap Radar** fully functional (differentiator implemented, 22/22 tests passing)
- ✅ **Confidence gating** working with comprehensive tests
- ✅ **Code quality** excellent (typed, tested, clean separation of concerns)
- ✅ **Deployment analysis** comprehensive (Section 7 complete, $0 strategy documented)
- ✅ **Git commits** meaningful, well-documented (professional commit messages)
- ✅ **Trello board** active with sprints 1-2 visible
- ✅ **Cost optimization** $0 strategy documented with detailed rationale
- ✅ **Backend tests** 7 test files covering confidence, fallback, gaps, edge cases
- ✅ **Frontend** clean React components with TypeScript, zero errors

---

## 📊 EFFORT vs IMPACT MATRIX

| Task | Effort | Impact | Priority | Blockers | When |
|------|--------|--------|----------|----------|------|
| **Create CI/CD pipeline** | 3h | 🔴 BLOCKER | **P0** | None | **TODAY** |
| **Deploy to Vercel+Render** | 4-8h | 🔴 BLOCKER | **P0** | CI/CD done (confidence) | **Tomorrow** |
| **Run evaluation (Task #12)** | 4h | 🟡 HIGH | **P1** | Deployment (needs live URL) | Day 3-4 |
| **Complete DESIGN_AND_TESTING.md** | 6h | 🔴 BLOCKER | **P0** | Evaluation (needs data) | Day 4-5 |
| **Architecture diagrams** | 2h | 🟡 MEDIUM | **P2** | None (can parallelize) | Day 5-6 |
| **Test coverage report** | 0.5h | 🟡 MEDIUM | **P2** | None | Day 6 |
| **Sprint 3 setup** | 1h | 🟡 MEDIUM | **P2** | None | Day 6 |
| **Record demo video** | 5h | 🔴 BLOCKER | **P0** | All above done | Day 10-12 |

**Total Critical Path**: ~25 hours across 14 days = **2 hours/day average** (manageable)

**Dependency Chain**:
```
CI/CD (3h) → Deploy (4-8h) → Evaluate (4h) → Complete docs (6h) → Demo (5h)
                ↓
         Diagrams (2h, parallel)
         Coverage (0.5h, parallel)
         Sprint 3 (1h, parallel)
```

---

## 🎯 RECOMMENDED ACTION PLAN (Sequenced by Dependencies)

### **WEEK 1: Technical Foundation (Apr 12-18)**

#### **Day 1 (TODAY - Apr 12): CI/CD Pipeline** ⏰ 3 hours
**Why first**: 
- No external dependencies (just YAML files)
- Predictable work (2-3 hours, no surprises)
- Gives confidence before deployment
- Protects all future commits

**Tasks**:
1. Create `.github/workflows/backend-ci.yml`:
   - Run pytest on push/PR
   - Run black (code formatting check)
   - Run flake8 or ruff (linting)
   - Python 3.11 matrix
   - Cache pip dependencies for speed

2. Create `.github/workflows/frontend-ci.yml`:
   - Run `npm run build` (TypeScript compilation)
   - Run `npm run lint` (ESLint)
   - Node 20.x
   - Cache node_modules for speed

3. Update README.md:
   - Add build status badges
   - Link to CI workflows

4. Test locally:
   - Commit and push
   - Verify workflows run successfully
   - Fix any failing tests

**Acceptance Criteria**:
- ✅ Green checkmarks on GitHub commits
- ✅ All tests passing in CI
- ✅ Build status badges showing "passing"

---

#### **Day 2-3 (Apr 13-14): Deployment** ⏰ 6-8 hours (scheduled 4h, reality check)
**Why second**: 
- Highest-risk unknown (external services, debugging)
- Starting early gives buffer for troubleshooting
- Needed for evaluation to be meaningful

**Tasks**:

**Frontend (Vercel)**: ~2 hours
1. Create Vercel account (free tier)
2. Connect GitHub repository
3. Configure project:
   - Root directory: `frontend`
   - Framework preset: Next.js
   - Build command: `npm run build`
   - Environment variables: `NEXT_PUBLIC_API_URL=https://<your-backend>.onrender.com`
4. Deploy and test
5. Save URL: `https://<project>.vercel.app`

**Backend (Render)**: ~4-6 hours (troubleshooting buffer)
1. Create Render account (free tier)
2. Create Web Service:
   - Connect GitHub repo
   - Root directory: `backend`
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Environment variables:
   - `GROQ_API_KEY=<your-key>`
   - `ALLOWED_ORIGINS=https://<frontend>.vercel.app,http://localhost:3000`
   - `DATABASE_URL=sqlite:///./gaps.db` (or Neon if using)
4. Wait for build (10-15 min first time)
5. Test health endpoint: `https://<backend>.onrender.com/health`
6. Troubleshoot:
   - Check logs for errors
   - Verify ChromaDB indexes on startup (275 chunks)
   - Test CORS (frontend → backend request)
   - Verify cold start behavior (15 min idle → 30-60s wake)

**Integration Testing**: ~1 hour
1. Frontend loads at Vercel URL
2. Ask question end-to-end (frontend → backend → LLM → response)
3. Gap Radar shows logged gaps
4. Citations display correctly
5. No CORS errors in browser console

**Documentation**:
1. Update `CAPSTONE_SUBMISSION_LINKS.md`:
   - Frontend URL: `https://<project>.vercel.app`
   - Backend URL: `https://<backend>.onrender.com`
2. Take screenshots (backup if free tier flaky during demo)

**Acceptance Criteria**:
- ✅ Frontend accessible at public Vercel URL
- ✅ Backend health check returns 200 with 275 chunks
- ✅ Ask question works end-to-end on deployed URLs
- ✅ Gap Radar displays on deployed frontend
- ✅ HTTPS certificates valid (auto-managed)
- ✅ No CORS errors

---

#### **Day 4 (Apr 15): Evaluation Run (Task #12)** ⏰ 4 hours
**Why after deployment**: Need live deployed system for realistic metrics

**Tasks**:

1. **Create test question set** (1 hour):
   - Write 15-20 questions in `docs/evaluation/test-questions.md`
   - Categories: Answerable (7), Partial (4), Gaps (5), Edge (3)
   - Example:
     ```markdown
     ## Answerable Questions (Should Return Good Answers)
     1. "How do I run tests locally?"
     2. "What's our CI/CD pipeline configuration?"
     ...

     ## Gap Questions (Should Trigger Fallback + Gap Logging)
     1. "How do we rotate API keys in production?"
     2. "What's the incident response process?"
     ...
     ```

2. **Run evaluation** (2 hours):
   - Submit each question via deployed frontend (or API)
   - Record results in spreadsheet:
     - Question text
     - Expected behavior (answerable/gap/partial)
     - Actual behavior (match/mismatch)
     - Confidence score
     - Citation count
     - Response time (seconds)
     - Gap logged? (yes/no)
   - Calculate metrics:
     - Answer accuracy: X% correct responses
     - Citation rate: Y% answers with citations
     - Confidence distribution: Z% high, Q% medium, R% low
     - Latency: p50, p95, p99
     - Gap detection: precision & recall

3. **Document results** (1 hour):
   - Create `docs/evaluation/sprint-2-eval-results.md` with detailed findings
   - Update DESIGN_AND_TESTING_TEMPLATE.md Section 10 with summary table
   - Include screenshots of Gap Radar with logged gaps

**Acceptance Criteria**:
- ✅ 15-20 questions tested
- ✅ Metrics calculated (accuracy, citation rate, latency, gap detection)
- ✅ Results documented in evaluation file
- ✅ Section 10 of DESIGN_AND_TESTING.md complete with data

---

#### **Day 5-6 (Apr 16-17): Complete DESIGN_AND_TESTING.md** ⏰ 6 hours
**Why after evaluation**: Need metrics data to fill placeholders

**Tasks**:

1. **Section 1: Problem Statement** (30 min):
   - Replace `[Describe the onboarding inefficiency problem...]` with actual description
   - Use persona: new engineer, first 30 days
   - Pain points: scattered docs, blocking teammates, missing documentation

2. **Section 2: Architecture Diagrams** (2 hours):
   - Create system architecture diagram (Mermaid or draw.io)
   - Create data flow diagram (question → answer flow)
   - Insert into Section 2

3. **Section 6: Confidence Thresholds** (1 hour):
   - Replace `[Document actual thresholds tuned on evaluation set...]` with actual values
   - Document: MAX_SIMILARITY_THRESHOLD, MIN_CONTEXT_WORDS, MIN_SOURCES
   - Explain calibration process (tested on evaluation set)

4. **Section 8: Test Execution Results** (1 hour):
   - Run `pytest --cov=app --cov-report=term` in backend
   - Document actual test results:
     - Test suites: pytest (backend), jest (frontend if added)
     - Environment: macOS local, GitHub Actions Ubuntu
     - Results: "X passed, Y skipped, 0 failed"
     - Coverage: "Z% backend coverage"
   - Replace `[To be completed during implementation]` with actual data

5. **Section 10: Evaluation Results** (1 hour):
   - Copy summary table from evaluation results file
   - Add key findings (what worked, what didn't)
   - Include Gap Radar effectiveness metrics

6. **Final polish** (30 min):
   - Search for any remaining `[...]` placeholders
   - Spell check
   - Formatting consistency
   - Verify all sections complete

**Acceptance Criteria**:
- ✅ Zero placeholder text remaining
- ✅ All diagrams inserted
- ✅ All metrics documented with evidence
- ✅ Professional presentation quality
- ✅ Ready for grader review

---

#### **Day 6-7 (Apr 17-18): Parallel Tasks** ⏰ 3.5 hours total

**Test Coverage Report** (30 min):
```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term
open htmlcov/index.html
# Document coverage % in Section 8
```

**Architecture Diagrams** (if not done in Day 5-6):
- System architecture
- Data flow diagram

**Sprint 3 Setup** (1 hour):
- Create `docs/sprints/sprint-3/` folder
- `sprint-goal.md`: "Deploy, evaluate, document, and demo capstone project"
- `sprint-backlog.md`: List remaining tasks (CI/CD, deploy, eval, docs, demo)
- Leave review/retro empty (fill at end of sprint)

**Acceptance Criteria**:
- ✅ Test coverage measured and documented
- ✅ Diagrams created and inserted
- ✅ Sprint 3 artifacts created (goal + backlog)

---

### **WEEK 2: Documentation & Demo (Apr 19-25)**

#### **Day 8-9 (Apr 19-20): Demo Preparation** ⏰ 3 hours

**Script Writing** (2 hours):
1. Write detailed demo script (15-20 minutes verbatim)
2. Structure:
   - 0:00-2:00: Intro (ID shown, problem, solution)
   - 2:00-5:00: Architecture (diagrams, tech stack, design decisions)
   - 5:00-13:00: Live demo (ask questions, show citations, trigger gap, Gap Radar)
   - 13:00-15:00: Evaluation metrics (accuracy, latency, gap detection)
   - 15:00-17:00: Agile process (Trello, sprints, retrospectives)
   - 17:00-19:00: Conclusion (lessons learned, future work)
3. Time each section (practice with stopwatch)

**Environment Preparation** (1 hour):
1. Pre-seed database with 3-5 gap examples (for demo)
2. Prepare 5-7 sample questions with known good answers
3. Clean browser (close tabs, clear cache, no embarrassing bookmarks visible)
4. Test recording software (OBS Studio or Zoom)
5. Test microphone and audio levels
6. Choose quiet recording location

**Acceptance Criteria**:
- ✅ Script written and timed (fits 15-20 min)
- ✅ Demo environment clean and ready
- ✅ Recording software tested

---

#### **Day 10-11 (Apr 21-22): Demo Recording** ⏰ 5 hours (plan for 2-3 takes)

**Recording Setup** (30 min):
1. Close all unnecessary apps
2. Set "Do Not Disturb" mode
3. Open deployed frontend URL
4. Open Trello board in separate tab
5. Have script visible on second monitor or paper
6. Test audio one final time

**Recording Take 1** (2 hours):
1. Show ID clearly (government-issued, name visible)
2. Follow script
3. Keep face visible throughout (or at required intervals)
4. Demo all features live
5. Watch for time (15-20 min target)

**Review + Retake if Needed** (2.5 hours):
1. Watch recording fully
2. Check audio quality (clear, no background noise)
3. Check video quality (text legible, no glitches)
4. Check timing (15-20 min, not too short or long)
5. Re-record if major issues (common on first take)

**Acceptance Criteria**:
- ✅ Recording 15-20 minutes duration
- ✅ ID shown clearly at beginning
- ✅ Face visible throughout
- ✅ Audio clear and professional
- ✅ All features demonstrated
- ✅ Exported as MP4 file

---

#### **Day 12-13 (Apr 23-24): Final Polish** ⏰ 3 hours

**Sprint 2 Retrospective (Task #13)** (2 hours):
1. Create `docs/sprints/sprint-2/sprint-retrospective.md`
2. Sections:
   - What went well (Gap Radar, confidence gating, clean code)
   - What didn't go well (Sources page cancellation, underestimated deployment)
   - Lessons learned (question requirements early, deployment takes longer than planned)
   - Action items for next time
3. Update sprint backlog final status

**Sprint 3 Completion** (30 min):
1. Update `sprint-backlog.md` with actual completion dates
2. Write `sprint-review.md` (what was delivered: CI/CD, deployment, evaluation, docs, demo)
3. Write `sprint-retrospective.md` (reflections on capstone project overall)

**Final Testing** (30 min):
1. Smoke test deployed app one final time
2. Verify all URLs in CAPSTONE_SUBMISSION_LINKS.md work
3. Check GitHub repo is shared with `quantic-grader`
4. Verify Trello board is public/shareable
5. Confirm all 5 deliverables ready

**Acceptance Criteria**:
- ✅ All sprint artifacts complete
- ✅ All 5 deliverables verified ready
- ✅ Submission links document updated

---

#### **Day 14 (Apr 25): Buffer Day** 🛡️
- Reserve for any unexpected issues
- Re-recording demo if needed
- Fixing deployment issues if free tier flaky
- Final documentation polish

---

## 🚨 SENIOR ENGINEER RECOMMENDATIONS

### **Start with CI/CD TODAY (Not Deployment)**

**Rationale**:
1. ✅ **CI/CD is predictable**: 2-3 hours, no external dependencies, known patterns
2. ✅ **Gives you confidence**: Automated tests passing before you deploy
3. ✅ **Low risk**: If it breaks, you just fix the YAML file (no external services)
4. ✅ **Protects future work**: Every commit validated automatically
5. ⚠️ **Deployment is HIGH RISK**: External services, CORS, env vars, debugging can eat 2-3 DAYS
6. ⚠️ **Start deployment early**: Gives buffer time for unknowns

**Order of Operations**:
```
TODAY:    CI/CD (3h) - Predictable, foundational
TOMORROW: Deploy (4-8h) - High-risk, start early for buffer time
DAY 3-4:  Evaluate (4h) - Needs deployed URL
DAY 4-5:  Complete docs (6h) - Needs evaluation data
DAY 10+:  Demo (5h) - Needs everything above done
```

### **Why Deployment is Riskiest**

From 15 years of experience, deployment ALWAYS takes longer than planned:

**Common Issues** (budget extra time):
- Environment variables misconfigured (2 hour debug session)
- CORS origins wrong (1 hour)
- Cold start behavior not as documented (2 hours testing)
- ChromaDB doesn't re-index properly (3 hours debugging)
- Database migrations fail (2 hours)
- Dependency conflicts in production vs local (4 hours)
- Free tier rate limits hit during testing (1 day wait)
- DNS propagation delays (2-24 hours)

**Reality Check**: 
- Scheduled: 4 hours
- Realistic: 6-8 hours  
- Worst case: 2-3 days if major issues

**Starting deployment Day 2** gives you:
- 12 days buffer before demo recording
- Time to troubleshoot without panic
- Ability to evaluate against live system
- Real production data for documentation

### **Critical Path Dependencies**

You CANNOT do these out of order:
1. CI/CD → Gives confidence before deploying
2. Deploy → Unlocks evaluation (needs live URLs)
3. Evaluate → Generates data to complete documentation
4. Complete docs → Needed before demo recording
5. Demo → Final deliverable, requires everything above

**Parallelizable** (can do anytime):
- Architecture diagrams (no dependencies)
- Test coverage report (no dependencies)
- Sprint 3 setup (no dependencies)

### **What Could Go Wrong** (Risk Mitigation)

**Scenario 1: Deployment blocks for 3 days**
- Mitigation: Started Day 2, discovered issue Day 3, fixed by Day 5
- Still have 9 days for evaluation, docs, demo
- ✅ Recoverable

**Scenario 2: Deployment blocks for 3 days BUT started Day 8**
- Discovered issue Day 9, fixed by Day 12
- Only 2 days for evaluation, docs, demo
- ❌ Major risk, likely rushed/incomplete

**Scenario 3: Demo re-recording needed**
- Built in 2-3 takes expectation (Day 10-11)
- Buffer day (Day 14) available
- ✅ Recoverable

### **Success Indicators** (How You'll Know You're On Track)

**End of Day 1 (Today)**: 
- ✅ Green checkmarks on GitHub (CI/CD passing)
- ✅ README has build status badges

**End of Day 3**:
- ✅ Deployed frontend URL accessible
- ✅ Deployed backend health check returns 200
- ✅ Ask question works end-to-end on deployed URLs

**End of Day 5**:
- ✅ Evaluation complete with metrics
- ✅ DESIGN_AND_TESTING.md has zero placeholders

**End of Day 11**:
- ✅ Demo video recorded and reviewed
- ✅ All 5 deliverables ready for submission

---

## 📋 IMMEDIATE NEXT STEPS (TODAY - Apr 12)

### **Option A: CI/CD Pipeline First** ⭐ **RECOMMENDED**
**Time**: 3 hours TODAY  
**Why**: Low risk, predictable, foundational, gives confidence  
**Output**: Green checks on GitHub, automated testing

### Option B: Deployment First
**Time**: 6-8 hours tomorrow + TODAY  
**Why**: Highest risk, start early for buffer  
**Concern**: Rushing into unknowns without safety net

### Option C: Documentation First
**Time**: 6 hours  
**Why**: It's a blocker deliverable  
**Issue**: Can't complete without evaluation data (which needs deployment)

---

## 🎯 FINAL RECOMMENDATION

**Do this TODAY (Apr 12):**

1. **CI/CD Pipeline** (3 hours) - Makes everything else safer
2. **Commit plan** (5 min) - Git commit this file for tracking

**Do TOMORROW (Apr 13):**

3. **Deploy to Vercel + Render** (6-8 hours) - Start early, expect issues

**This sequence**:
- Gives you confidence (CI/CD passing before deploy)
- Starts highest-risk work early (12 day buffer)
- Follows dependencies (can't evaluate without deployment)
- Protects against unknowns (time to troubleshoot)

---

## 💡 LESSONS FROM SENIOR ENGINEERING

**Things I've Learned the Hard Way**:

1. ✅ **"It works on my machine" ≠ "It works in production"**
   - CI/CD catches this before deployment

2. ⚠️ **Deployment ALWAYS takes 2-3x longer than estimated**
   - Start early, give yourself buffer time

3. ✅ **Documentation requires real data, not placeholders**
   - Run evaluation first, then complete docs

4. ⚠️ **Demo videos take 2-3 takes minimum**
   - First recording always has mistakes, budget re-record time

5. ✅ **Automated testing is insurance**
   - Catches regressions, enables confident changes

6. ⚠️ **External dependencies are unpredictable**
   - Vercel/Render free tiers can be flaky, have backup plan

7. ✅ **Question requirements early**
   - Sources page cancellation shows maturity (you did this well!)

**You're doing great work. The code quality is excellent. Now we need to wrap it in professional delivery (CI/CD, deployment, documentation, demo) to match that quality.**

Let's start with CI/CD today. Ready?
