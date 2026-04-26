# Sprint 3 Backlog

**Sprint Goal**: "Deploy production-ready application and complete all Quantic graduation requirements"  
**Sprint Duration**: April 27 - May 24, 2026 (4 weeks)  
**Status**: In Progress

---

## 📋 Task List (Prioritized by Week)

### 🚀 WEEK 1: Deployment (Apr 27 - May 3)

#### 1. Deploy backend to Render

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 4-6 hours  
**Due**: May 1

**Acceptance Criteria**:

- [ ] Create Render account (free tier)
- [ ] Create new Web Service from GitHub repo
- [ ] Configure build command: `cd backend && pip install -r requirements.txt`
- [ ] Configure start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Set environment variables:
  - [ ] `GROQ_API_KEY` (from .env)
  - [ ] `LLM_MODEL=llama-3.1-8b-instant`
  - [ ] `DATABASE_URL` (SQLite path or upgrade to Postgres)
  - [ ] `CHROMA_PERSIST_DIRECTORY=/opt/render/project/chroma_db`
- [ ] Deploy and verify backend health endpoint responds
- [ ] Test `/api/ask` endpoint with sample question
- [ ] Document backend URL in CAPSTONE_SUBMISSION_LINKS.md
- [ ] Verify ChromaDB persistence works across deploys

**Implementation Notes**:

- Render free tier: 750 hours/month (sufficient for demo)
- Cold start expected (15-30 seconds first request)
- May need to switch to PostgreSQL if SQLite causes issues with ephemeral filesystem
- Consider pre-indexing documents in startup event

**Potential Blockers**:

- ChromaDB persistence on ephemeral filesystem (may need volume or Postgres backend)
- Groq API rate limits (14,400 req/day should be sufficient)

---

#### 2. Deploy frontend to Vercel

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Due**: May 1  
**Dependencies**: Task #1

**Acceptance Criteria**:

- [ ] Create Vercel account (free tier)
- [ ] Import GitHub repository
- [ ] Configure build settings:
  - [ ] Framework: Next.js
  - [ ] Root directory: `frontend`
  - [ ] Build command: `npm run build`
  - [ ] Output directory: `.next`
- [ ] Set environment variable: `NEXT_PUBLIC_API_URL=<render-backend-url>`
- [ ] Deploy and verify frontend loads
- [ ] Test Ask page with live backend
- [ ] Test Gap Radar dashboard with live backend
- [ ] Document frontend URL in CAPSTONE_SUBMISSION_LINKS.md
- [ ] Verify CORS configuration allows Vercel domain

**Implementation Notes**:

- Vercel free tier: 100GB bandwidth/month
- Automatic deployments on git push
- Need to update backend CORS to allow Vercel domain

**Potential Blockers**:

- CORS configuration (need to add Vercel domain to allow_origins)
- Environment variable propagation

---

#### 3. Verify end-to-end deployment

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 1-2 hours  
**Due**: May 2  
**Dependencies**: Task #1, #2

**Acceptance Criteria**:

- [ ] Test user flow: Homepage → Ask Question → Get Answer with Citations
- [ ] Test Gap Radar: Ask low-confidence question → Verify logged in /gaps
- [ ] Test Gap Radar: Filter, sort, view statistics
- [ ] Test on mobile device (responsive design)
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Verify no console errors in browser DevTools
- [ ] Verify no 500 errors in Render logs
- [ ] Test cold start behavior (acceptable latency)
- [ ] Document any deployment-specific issues

**Implementation Notes**:

- Create test plan checklist for systematic verification
- Take screenshots for documentation

---

#### 4. Run formal evaluation (5-10 test questions)

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Due**: May 3

**Acceptance Criteria**:

- [ ] Create 10 test questions covering all scenarios:
  - [ ] 3 well-documented questions (should get confident answers)
  - [ ] 2 partially-documented questions (medium confidence)
  - [ ] 2 undocumented questions (should trigger fallback + gap logging)
  - [ ] 2 edge cases (empty, very long, special characters)
  - [ ] 1 irrelevant question (sports/weather, should fallback)
- [ ] Run each question through deployed system
- [ ] Measure and record:
  - [ ] Response time (latency)
  - [ ] Confidence score
  - [ ] Answer quality (correct/incorrect/fallback)
  - [ ] Citation accuracy (sources match answer content)
  - [ ] Gap logging (low-confidence questions appear in dashboard)
- [ ] Calculate metrics:
  - [ ] Accuracy rate (correct answers / total questions)
  - [ ] Fallback rate (fallback responses / total questions)
  - [ ] Average latency
  - [ ] Average confidence for correct answers
- [ ] Document results in `/docs/evaluation/sprint-3-formal-evaluation.md`
- [ ] Identify any quality issues requiring fixes

**Implementation Notes**:

- Use deployed environment (not local) for realistic metrics
- Take screenshots of Gap Radar showing logged questions
- Compare results to Sprint 2 edge case testing

---

### 📝 WEEK 2: Documentation + Demo Prep (May 4 - May 10)

#### 5. Complete DESIGN_AND_TESTING.md (testing section)

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 3-4 hours  
**Due**: May 7

**Acceptance Criteria**:

- [ ] Section 4: Testing Strategy
  - [ ] Unit testing approach (pytest, in-memory DB)
  - [ ] Integration testing (RAG + Gap service)
  - [ ] Edge case testing methodology
  - [ ] CI/CD testing automation (GitHub Actions)
  - [ ] Test coverage summary (40+ tests)
- [ ] Section 6: Quality Assurance
  - [ ] Type checking (Pyright, TypeScript)
  - [ ] Code formatting (Black, ESLint)
  - [ ] Linting rules
- [ ] Update Section 7: Deployment with actual URLs
  - [ ] Production URLs (Vercel + Render)
  - [ ] Environment variables list
  - [ ] Deployment verification steps
- [ ] Review entire document for completeness
- [ ] Verify all sections match Quantic rubric requirements
- [ ] Commit to GitHub

**Implementation Notes**:

- Reference test files as evidence
- Include evaluation results as quality metrics
- Keep technical but accessible for non-engineers

---

#### 6. Write Sprint 3 backlog updates

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 1 hour  
**Due**: May 7

**Acceptance Criteria**:

- [ ] Update this file with completion notes for Tasks #1-4
- [ ] Mark completed tasks with ✅ DONE
- [ ] Add actual hours vs. estimates
- [ ] Note any blockers encountered and resolutions
- [ ] Update status to "In Progress" → "Nearly Complete"

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

**Total Tasks**: 16  
**Critical Path**: 10 tasks (Tasks #1-5, #9-10, #13-14, #16)  
**Nice-to-Have**: 6 tasks (Tasks #6, #8, #11-12, #15)

**Estimated Hours**: 35-50 hours over 4 weeks (~10-12 hours/week)

**Key Milestones**:

- Week 1 (May 3): Deployment complete, evaluation done
- Week 2 (May 10): Documentation complete, demo scripted
- Week 3 (May 17): Demo recorded, repo shared, submission ready
- Week 4 (May 24): Final testing, retrospective, **PERSONAL DEADLINE**

---

## 🚨 Risk Register

| Risk                           | Probability | Impact | Mitigation                                    |
| ------------------------------ | ----------- | ------ | --------------------------------------------- |
| Render deployment issues       | Medium      | High   | Start early (Week 1), read docs carefully     |
| Vercel deployment issues       | Low         | Medium | Well-documented, common framework             |
| ChromaDB persistence issues    | Medium      | Medium | Test early, migrate to Postgres if needed    |
| Demo recording technical issue | Medium      | High   | Practice multiple times, have backup plan    |
| Evaluation reveals bugs        | Low         | Medium | Run in Week 1, fix before demo                |
| Time overrun                   | Low         | High   | Conservative estimates, buffer week built in  |
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

*Sprint 3 backlog created: April 26, 2026*  
*Sprint starts: April 27, 2026*  
*Personal deadline: May 24, 2026*  
*Official deadline: May 31, 2026*
