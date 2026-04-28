# Sprint 3 Backlog

**Sprint Goal**: "Deploy production-ready application and complete all Quantic graduation requirements"  
**Sprint Duration**: April 27 - May 24, 2026 (4 weeks)  
**Status**: In Progress (5/16 tasks complete, Week 1 done, ahead of schedule)

---

## 📋 Task List (Prioritized by Week)

### 🚀 WEEK 1: Deployment (Apr 27 - May 3)

#### 1. Deploy backend to Render ✅ DONE

**Status**: ✅ DONE (Completed April 27, 2026)  
**Priority**: CRITICAL  
**Estimate**: 4-6 hours  
**Actual**: 2 hours  
**Due**: May 1 (completed 3 days early)

**Acceptance Criteria**:

- [x] Create Render account (free tier)
- [x] Create new Web Service from GitHub repo
- [x] Configure build command: `cd backend && pip install -r requirements.txt`
- [x] Configure start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [x] Set environment variables:
  - [x] `GROQ_API_KEY`
  - [x] `COHERE_API_KEY` (switched to Cohere embeddings)
  - [x] `LLM_MODEL=llama-3.1-8b-instant`
  - [x] SQLite embedded (no DATABASE_URL needed)
  - [x] `CHROMA_PERSIST_DIRECTORY` configured
- [x] Deploy and verify backend health endpoint responds
- [x] Test `/api/ask` endpoint with sample question
- [x] Document backend URL in CAPSTONE_SUBMISSION_LINKS.md
- [x] ChromaDB auto-rebuilds on startup (ephemeral disk accepted)

**Implementation Notes**:

- Render free tier: 750 hours/month (sufficient for demo)
- Cold start expected (15-30 seconds first request)
- May need to switch to PostgreSQL if SQLite causes issues with ephemeral filesystem
- Consider pre-indexing documents in startup event

**Blockers Encountered & Resolutions**:

1. **Embedding dimension mismatch** (Local: 384-dim HuggingFace vs Production: 1024-dim Cohere)
   - **Resolution**: Switched to Cohere embeddings for both local and production
   - **Impact**: Better quality embeddings, consistent across environments

2. **ChromaDB ephemeral filesystem** (data lost on redeploy)
   - **Resolution**: Auto-rebuild from synthetic-docs/ on startup (~30s)
   - **Impact**: Acceptable for demo, cold start slightly longer

3. **Missing langchain-cohere dependency locally**
   - **Resolution**: Added to requirements.txt, installed in venv
   - **Impact**: No production impact, caught during local testing

**Deployment URL**: https://engineering-onboarding-copilot.onrender.com

---

#### 2. Deploy frontend to Vercel ✅ DONE

**Status**: ✅ DONE (Completed April 27-28, 2026)  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Actual**: 1 hour (+ 0.5 hours fixing build failure)  
**Due**: May 1 (completed 2 days early)  
**Dependencies**: Task #1

**Acceptance Criteria**:

- [x] Create Vercel account (free tier)
- [x] Import GitHub repository
- [x] Configure build settings:
  - [x] Framework: Next.js (auto-detected)
  - [x] Root directory: `frontend`
  - [x] Build command: `npm run build`
  - [x] Output directory: `.next`
- [x] Set environment variable: `NEXT_PUBLIC_API_URL=https://engineering-onboarding-copilot.onrender.com`
- [x] Deploy and verify frontend loads
- [x] Test Ask page with live backend
- [x] Test Gap Radar dashboard with live backend
- [x] Document frontend URL in CAPSTONE_SUBMISSION_LINKS.md
- [x] Verify CORS configuration allows Vercel domain

**Implementation Notes**:

- Vercel free tier: 100GB bandwidth/month
- Automatic deployments on git push
- Need to update backend CORS to allow Vercel domain

**Blockers Encountered & Resolutions**:

1. **Build failure: Unused useEffect import**
   - **Error**: ESLint error `@typescript-eslint/no-unused-vars`
   - **Resolution**: Removed unused import from ask/page.tsx
   - **Impact**: Fixed in commit 143b9ae, rebuild successful

2. **CORS configuration**
   - **Resolution**: Backend already configured with Vercel domain
   - **Impact**: No issues, worked on first try

**Deployment URL**: https://engineering-onboarding-copilot.vercel.app  
**Auto-deploy**: Enabled from main branch

---

#### 3. Verify end-to-end deployment ✅ DONE

**Status**: ✅ DONE (Completed April 27, 2026)  
**Priority**: CRITICAL  
**Estimate**: 1-2 hours  
**Actual**: 0.5 hours  
**Due**: May 2 (completed 4 days early)  
**Dependencies**: Task #1, #2

**Acceptance Criteria**:

- [x] Test user flow: Homepage → Ask Question → Get Answer with Citations
- [x] Test Gap Radar: Ask low-confidence question → Verify logged in /gaps
- [x] Test Gap Radar: Filter, sort, view statistics
- [x] Test on mobile device (responsive design working)
- [x] Test on different browsers (Chrome, Safari tested)
- [x] Verify no console errors in browser DevTools
- [x] Verify no 500 errors in Render logs
- [x] Test cold start behavior (~60s acceptable for free tier)
- [x] Document any deployment-specific issues

**Verification Results**:

- ✅ All user flows working end-to-end
- ✅ Q&A with citations functioning correctly
- ✅ Gap detection and logging working
- ✅ Responsive design validated
- ✅ Cold starts acceptable (~60s first request, then fast)
- ✅ No blocking issues found

**Known Limitations** (acceptable for demo):

- Cold start latency on Render free tier (expected behavior)
- Ephemeral filesystem (ChromaDB rebuilds on deploy)

**Implementation Notes**:

- Create test plan checklist for systematic verification
- Take screenshots for documentation

---

#### 4. Run formal evaluation (10 test questions) ✅ DONE

**Status**: ✅ DONE (Completed April 27, 2026)  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Actual**: 4 hours  
**Due**: May 3 (completed 5 days early)

**Acceptance Criteria**:

- [x] Create 10 test questions covering all scenarios:
  - [x] 3 well-documented questions (confident answers)
  - [x] 2 partially-documented questions (medium confidence)
  - [x] 2 undocumented questions (fallback + gap logging)
  - [x] 2 edge cases (empty, very long)
  - [x] 1 irrelevant question (weather, fallback)
- [x] Run each question through deployed production system
- [x] Measure and record:
  - [x] Response time (average 1.4s)
  - [x] Confidence score (all within expected ranges)
  - [x] Answer quality (10/10 correct)
  - [x] Citation accuracy (all citations relevant)
  - [x] Gap logging (verified in dashboard)
- [x] Calculate metrics:
  - [x] Accuracy rate: **100%** (10/10 correct)
  - [x] Fallback rate: 30% (3/10 expected fallbacks)
  - [x] Average latency: 1.4 seconds (excluding cold start)
  - [x] Average confidence for correct answers: 76%
- [x] Document results in `/docs/evaluation/sprint-3-formal-evaluation.md`
- [x] No quality issues found, system production-ready

**Evaluation Results**:

- ✅ **100% accuracy** across all test cases
- ✅ Confidence calibration validated (high confidence = correct)
- ✅ Fallback behavior working as designed
- ✅ Gap detection logging correctly
- ✅ Fast performance (1.4s average)
- ✅ System ready for capstone demo

**Document**: `docs/evaluation/sprint-3-formal-evaluation.md` (committed b8009e0)

**Implementation Notes**:

- Use deployed environment (not local) for realistic metrics
- Take screenshots of Gap Radar showing logged questions
- Compare results to Sprint 2 edge case testing

---

### 🎨 UNPLANNED WORK: UI Redesign (Studio Aesthetic)

**Completed**: April 27-28, 2026  
**Total Time**: ~6 hours (not in original estimates)

#### UI Redesign (Studio Aesthetic)

**Status**: ✅ DONE  
**Priority**: HIGH (user-initiated improvement)  
**Actual Time**: ~6 hours

**What Was Done**:

1. Created design proposal
2. Implemented design system in globals.css (1 hour)
   - CSS variables for colors
   - Grid pattern background
   - Custom animations
   - Brutalist styling tokens
3. Redesigned home page (1.5 hours)
   - Massive 72px hero heading
   - Brutalist buttons with shadows
   - Feature cards with inline icons
   - Strategic mono font usage
4. Redesigned ask page (2 hours)
   - Chat-style interface
   - Confidence badges with icons
   - Fixed bottom input bar
   - Removed redundant navigation
5. Redesigned gap radar page (1 hour)
   - Data table with brutalist styling
   - Stats cards with mono fonts
   - Consistent design system
6. Main navigation update (0.5 hours)
   - Unified nav bar across all pages
   - Mono font for branding

**Strategic Mono Font Usage**:

- ✅ Main headings (ENGINEERING ONBOARDING COPILOT)
- ✅ Navigation links (Ask Question, Gap Radar)
- ✅ UI labels (YOU, COPILOT)
- ✅ Stats and metrics (confidence percentages, gap counts)
- ✅ Character counter
- ❌ Body text (kept readable sans-serif)

**Dependencies Installed**:

- framer-motion@11.0.0 (animations)
- lucide-react@0.344.0 (modern icons)

**Files Modified**:

- `frontend/src/app/globals.css` (complete redesign)
- `frontend/src/app/page.tsx` (home page redesign)
- `frontend/src/app/ask/page.tsx` (chat interface rewrite)
- `frontend/src/app/gaps/page.tsx` (dashboard redesign)
- `frontend/src/app/layout.tsx` (main navigation)
- `frontend/package.json` (new dependencies)

**Commits**:

- 0359244: "Redesign UI: studio aesthetic with strategic mono font usage"
- 143b9ae: "Fix build: remove unused useEffect import"
- 05021e0: "Remove internal design doc"

**Rationale**:
This unplanned work significantly improves the professional presentation of the capstone demo while maintaining all functionality. The aesthetic aligns with the technical nature of the product (engineering onboarding) and creates a memorable visual identity.

**Impact on Sprint**:

- ➕ Improved demo quality and professional appearance
- ➕ Differentiates from typical academic projects
- ➕ No functionality lost, all features working
- ➖ 6 hours of unplanned work (offset by being ahead of schedule)
- ➖ Added 2 npm dependencies (minimal bundle size impact)

---

### 📝 WEEK 2: Documentation + Demo Prep (May 4 - May 10)

#### 5. Complete DESIGN_AND_TESTING.md (testing section) ✅ DONE

**Status**: ✅ DONE (Completed April 28, 2026)  
**Priority**: CRITICAL  
**Estimate**: 3-4 hours  
**Actual**: 4 hours  
**Due**: May 7 (completed 9 days early)

**Acceptance Criteria**:

- [x] All 11 required sections completed
- [x] Section 8: Testing Strategy (comprehensive)
  - [x] Unit testing approach (pytest with mocks)
  - [x] Integration testing (RAG + Gap + Vector store)
  - [x] Edge case testing methodology (463 lines)
  - [x] Testing rationale documented
  - [x] Test coverage: 5 files, 1,374 lines, 46+ test functions
- [x] Section 9: Security and AI Safety
  - [x] Threat model documented
  - [x] Controls implemented (6/10)
  - [x] Residual risks accepted
- [x] Section 7: Deployment with actual URLs
  - [x] Production URLs documented
  - [x] Environment variables listed
  - [x] $0/month cost analysis
  - [x] Tradeoffs documented
- [x] All sections match Quantic rubric requirements
- [x] Committed to GitHub (cc426f6)

**Document Highlights**:

- ✅ 641 lines covering all required sections
- ✅ Comprehensive testing section with actual execution data
- ✅ 100% evaluation accuracy documented
- ✅ Architecture diagrams included
- ✅ Evidence-based with file references
- ✅ Production deployment details

**Commit**: cc426f6 - "Complete DESIGN_AND_TESTING.md with comprehensive testing section"

**Implementation Notes**:

- Reference test files as evidence
- Include evaluation results as quality metrics
- Keep technical but accessible for non-engineers

---

#### 6. Write Sprint 3 backlog updates ✅ DONE

**Status**: ✅ DONE (Completed April 28, 2026)  
**Priority**: MEDIUM  
**Estimate**: 1 hour  
**Actual**: 1 hour  
**Due**: May 7 (completed 9 days early)

**Acceptance Criteria**:

- [x] Update this file with completion notes for Tasks #1-5
- [x] Mark completed tasks with ✅ DONE
- [x] Add actual hours vs. estimates
- [x] Note all blockers encountered and resolutions
- [x] Document unplanned work (UI redesign)
- [x] Update sprint status

**Sprint Status Update**:

- **Before**: "In Progress" (0/16 tasks)
- **Now**: "In Progress" (5/16 tasks complete, 31% done)
- **Timeline**: Week 1 complete in 2 days (5 days ahead of schedule)

---

#### 7. Script demo video content

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Due**: May 8

**Acceptance Criteria**:

- [ ] Create demo script (15-20 minutes) with sections:
  - [ ] Introduction (30s): Name, project title, Quantic MSSE
  - [ ] Problem statement (1 min): Why this exists
  - [ ] Architecture overview (2 min): Tech stack, FREE cost analysis
  - [ ] Feature demo: Ask Question (3 min)
    - Show well-documented question → confident answer with citations
    - Show undocumented question → fallback response
  - [ ] Feature demo: Gap Radar ⭐ (5 min)
    - Navigate to /gaps dashboard
    - Show logged gaps with frequency counts
    - Explain differentiator value
    - Show status workflow
    - Show statistics
  - [ ] Code walkthrough (4 min): Show key implementation files
    - `rag_service.py` - confidence calculation
    - `gap_service.py` - gap logging
    - `gaps/page.tsx` - dashboard UI
  - [ ] Testing & CI/CD (2 min): Show test files and GitHub Actions
  - [ ] Deployment (1 min): Show live URLs, explain infrastructure
  - [ ] Conclusion (1 min): Summary, learnings, future work
- [ ] Prepare ID for verification (show at beginning or end)
- [ ] List technical setup needed (screen recording, mic, browser tabs)
- [ ] Identify demo data to prepare (questions to ask, gaps to show)

**Implementation Notes**:

- Practice timing each section to stay under 20 minutes
- Prepare fallback plan if live demo fails (screenshots/pre-recorded clips)
- Ensure Gap Radar is prominently featured (differentiator)

---

#### 8. Practice demo walkthrough

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Due**: May 10  
**Dependencies**: Task #7

**Acceptance Criteria**:

- [ ] Do full dry run following script (time it)
- [ ] Verify deployed system is stable for demo
- [ ] Prepare browser tabs in advance:
  - [ ] Frontend homepage
  - [ ] Ask page
  - [ ] Gap Radar dashboard
  - [ ] GitHub repo (code walkthrough)
  - [ ] GitHub Actions (CI/CD)
  - [ ] Render dashboard (deployment)
- [ ] Test screen recording software (OBS, Loom, Zoom, etc.)
- [ ] Test audio quality (clear, no background noise)
- [ ] Practice speaking clearly and at good pace
- [ ] Adjust script based on timing
- [ ] Create backup plan if something breaks during recording

**Implementation Notes**:

- Record practice run to review pacing and clarity
- Ensure confident delivery (you built this!)

---

### 🎥 WEEK 3: Demo Video + Final Docs (May 11 - May 17)

#### 9. Record demo video (15-20 min)

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 3-5 hours (including retakes)  
**Due**: May 15  
**Dependencies**: Task #7, #8

**Acceptance Criteria**:

- [ ] Set up recording environment (quiet, good lighting)
- [ ] Show ID verification (government-issued ID visible for ~5 seconds)
- [ ] Record full demo following script
- [ ] Ensure audio is clear (no background noise, echo)
- [ ] Ensure video quality is good (readable text, smooth playback)
- [ ] Demo shows:
  - [ ] Live application working (all features)
  - [ ] Gap Radar differentiator prominently featured
  - [ ] Code walkthrough of key files
  - [ ] Test suite and CI/CD
  - [ ] Deployment infrastructure
- [ ] Video length: 15-20 minutes (not shorter, not longer)
- [ ] Export as MP4 with good compression (< 500MB if possible)
- [ ] Upload to YouTube as unlisted video
- [ ] Add video URL to CAPSTONE_SUBMISSION_LINKS.md
- [ ] Verify video plays correctly (no corruption)

**Implementation Notes**:

- Expect 2-3 takes to get it right
- Budget full afternoon for recording
- Have backup recording method ready
- Test upload before committing to final version

**Potential Blockers**:

- Live demo fails during recording (have screenshots ready)
- Audio issues (test equipment beforehand)
- Time management (practice timing)

---

#### 10. Share repo with quantic-grader

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 30 minutes  
**Due**: May 15

**Acceptance Criteria**:

- [ ] Add `quantic-grader` as collaborator to GitHub repo
- [ ] Verify they have "Read" access (sufficient for grading)
- [ ] Ensure all required files are committed and pushed:
  - [ ] `DESIGN_AND_TESTING.md` (complete)
  - [ ] `CAPSTONE_SUBMISSION_LINKS.md` (all URLs filled)
  - [ ] Sprint 0, 1, 2, 3 artifacts in `/docs/sprints/`
  - [ ] All code (backend + frontend)
  - [ ] Test files
  - [ ] CI/CD workflows
- [ ] Verify repo is public or collaborator has access
- [ ] Send confirmation email if required by Quantic
- [ ] Document completion in CAPSTONE_SUBMISSION_LINKS.md

**Implementation Notes**:

- Double-check GitHub username spelling: `quantic-grader`
- Verify access by logging out and checking repo visibility

---

#### 11. Final code cleanup and documentation review

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 2-3 hours  
**Due**: May 16

**Acceptance Criteria**:

- [ ] Run code formatters:
  - [ ] Backend: `black app/`
  - [ ] Frontend: `npm run lint -- --fix`
- [ ] Remove unused imports, commented code
- [ ] Ensure all `.env.example` files are up-to-date
- [ ] Update README.md with final deployment URLs
- [ ] Verify all links in documentation work
- [ ] Fix any typos in documentation
- [ ] Ensure consistent formatting across markdown files
- [ ] Remove any TODO comments or placeholder text
- [ ] Commit and push all changes

**Implementation Notes**:

- This is polish, not major changes
- Goal: professional presentation for graders

---

#### 12. Create submission checklist

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 1 hour  
**Due**: May 17

**Acceptance Criteria**:

- [ ] Create `/docs/delivery/SUBMISSION_CHECKLIST.md` with:
  - [ ] ✅ GitHub repo shared with quantic-grader
  - [ ] ✅ Live frontend URL (Vercel)
  - [ ] ✅ Live backend URL (Render)
  - [ ] ✅ Trello board link (public)
  - [ ] ✅ DESIGN_AND_TESTING.md complete
  - [ ] ✅ Demo video URL (YouTube unlisted)
  - [ ] ✅ All sprint artifacts (0, 1, 2, 3) committed
  - [ ] ✅ README.md updated with deployment info
  - [ ] ✅ Code formatted and cleaned
  - [ ] ✅ Tests passing (CI/CD green)
  - [ ] ✅ No sensitive data in repo (.env files gitignored)
- [ ] Verify each item on checklist
- [ ] Document submission date and confirmation

**Implementation Notes**:

- This is final verification before submission
- Use this checklist on May 24 (personal deadline)

---

### ✅ WEEK 4: Final Sprint + Buffer (May 18 - May 24)

#### 13. Sprint 3 retrospective

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Due**: May 22

**Acceptance Criteria**:

- [ ] Create `/docs/sprints/sprint-3/sprint-retrospective.md`
- [ ] Follow same format as Sprint 1 & 2 retrospectives
- [ ] Document:
  - [ ] Sprint summary (tasks completed)
  - [ ] What went well (deployment, demo, documentation)
  - [ ] What could be improved (challenges encountered)
  - [ ] Sprint metrics (compare to Sprint 1 & 2)
  - [ ] Key learnings (technical and process)
  - [ ] Sprint goal assessment (achieved/not achieved)
  - [ ] Final project status (ready for submission)
- [ ] Reflect on entire capstone journey (3 sprints)
- [ ] Commit and push to GitHub

**Implementation Notes**:

- This is the final retrospective
- Should include reflection on full project lifecycle
- Celebrate completion!

---

#### 14. Final testing on deployed environment

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Due**: May 23

**Acceptance Criteria**:

- [ ] Re-run full end-to-end test suite on deployed environment
- [ ] Verify no regressions since initial deployment
- [ ] Test all user flows:
  - [ ] Ask question → Get answer → View sources
  - [ ] Ask low-confidence question → View gap in dashboard
  - [ ] Filter and sort gaps
  - [ ] View gap statistics
- [ ] Check error logs in Render (no 500 errors)
- [ ] Verify application handles cold starts gracefully
- [ ] Test on mobile devices (responsive)
- [ ] Verify demo video still accurately represents current state
- [ ] Document any issues found and fix immediately

**Implementation Notes**:

- Final quality check before submission
- Fix critical issues only (feature freeze in effect)

---

#### 15. Buffer for last-minute fixes

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 4-6 hours reserved  
**Due**: May 24

**Acceptance Criteria**:

- [ ] Available time for unexpected issues
- [ ] Fix any critical bugs found in final testing
- [ ] Address any grader feedback (if early submission)
- [ ] Re-record demo video if necessary (only if critical issue)
- [ ] Final commit and push of any fixes

**Implementation Notes**:

- Ideally no work needed (everything done early)
- Do not introduce new features
- Critical fixes only

---

#### 16. ✅ PERSONAL DEADLINE: May 24

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: N/A  
**Due**: May 24

**Acceptance Criteria**:

- [ ] All tasks #1-15 complete
- [ ] Submission checklist verified (all items ✅)
- [ ] Project ready for grading
- [ ] Submit to Quantic portal (if required)
- [ ] Backup project files locally
- [ ] Celebrate completion! 🎉

**Implementation Notes**:

- Official deadline is May 31 (7-day buffer)
- Personal deadline May 24 provides safety margin
- After this, only emergency fixes

---

### 🛡️ PROTECTED BUFFER: May 25 - May 31

**Purpose**: Emergency fixes only  
**Goal**: Zero work needed (everything complete by May 24)

**Allowed Activities**:

- Critical bug fixes (if grader finds showstopper)
- Re-upload demo video (only if corrupted/lost)
- Update submission links (only if changed)

**Not Allowed**:

- New features
- Non-critical improvements
- Code refactoring
- Documentation rewriting

---

## 📊 Sprint 3 Summary

**Total Tasks**: 16 planned + 1 unplanned (UI redesign)  
**Completed**: 6 tasks (5 planned + 1 unplanned) = 31% of planned tasks  
**In Progress**: Tasks #7-16  
**Status**: Significantly ahead of schedule (Week 1 complete in 2 days)

**Time Tracking**:

- **Estimated Hours**: 35-50 hours total over 4 weeks
- **Actual Hours (Week 1)**: ~18.5 hours
  - Task 1 (Deploy backend): 2 hours (est: 4-6)
  - Task 2 (Deploy frontend): 1.5 hours (est: 2-3)
  - Task 3 (Verify deployment): 0.5 hours (est: 1-2)
  - Task 4 (Formal evaluation): 4 hours (est: 3-4)
  - Task 5 (DESIGN_AND_TESTING.md): 4 hours (est: 3-4)
  - Task 6 (Backlog update): 1 hour (est: 1)
  - **Unplanned UI Redesign**: 6 hours
- **Efficiency**: Completed Week 1 tasks in 2 days vs planned 7 days

**Key Milestones** (Updated):

- ✅ **Week 1 (May 3)**: Deployment complete, evaluation done, DESIGN_AND_TESTING.md complete
  - **Actual**: Completed April 27-28 (5 days ahead)
  - **Status**: 100% complete + unplanned UI redesign
- ⏳ **Week 2 (May 10)**: Documentation updates, demo scripted, practice
  - **Status**: Not started (9 days ahead of schedule)
- ⏳ **Week 3 (May 17)**: Demo recorded, repo shared, submission ready
- ⏳ **Week 4 (May 24)**: Final testing, retrospective, **PERSONAL DEADLINE**

**Achievements**:

- ✅ 100% evaluation accuracy (10/10 test cases)
- ✅ Zero infrastructure cost ($0/month)
- ✅ Production deployment live and stable
- ✅ Comprehensive documentation complete
- ✅ Modern UI redesign (Berlin studio aesthetic)
- ✅ 5 days ahead of original schedule

---

## 🚨 Risk Register

| Risk                           | Probability | Impact | Mitigation                                   |
| ------------------------------ | ----------- | ------ | -------------------------------------------- |
| Render deployment issues       | Medium      | High   | Start early (Week 1), read docs carefully    |
| Vercel deployment issues       | Low         | Medium | Well-documented, common framework            |
| ChromaDB persistence issues    | Medium      | Medium | Test early, migrate to Postgres if needed    |
| Demo recording technical issue | Medium      | High   | Practice multiple times, have backup plan    |
| Evaluation reveals bugs        | Low         | Medium | Run in Week 1, fix before demo               |
| Time overrun                   | Low         | High   | Conservative estimates, buffer week built in |
| Grader finds critical issue    | Low         | High   | Protected buffer week for emergency fixes    |

---

## 🎯 Definition of Done

Sprint 3 is complete when:

- ✅ All 5 Quantic required deliverables submitted
- ✅ Application deployed and accessible via public URLs
- ✅ Demo video recorded and uploaded
- ✅ DESIGN_AND_TESTING.md complete
- ✅ Repo shared with quantic-grader
- ✅ Sprint 3 retrospective written
- ✅ Submission checklist 100% verified
- ✅ Personal deadline met (May 24, 2026)

---

## 🚫 Out of Scope

**NOT doing in Sprint 3** (feature freeze):

- GitHub file ingestion (beyond MVP scope)
- Markdown code block parsing (nice-to-have)
- Performance optimization (unless breaks demo)
- Additional UI features (Gap Radar is complete)
- Database migration to Postgres (unless SQLite fails)
- New Gap Radar features
- Additional test coverage (40+ tests sufficient)

---

_Sprint 3 backlog created: April 26, 2026_  
_Sprint starts: April 27, 2026_  
_Personal deadline: May 24, 2026_  
_Official deadline: May 31, 2026_
