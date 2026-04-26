# Sprint 2 Retrospective

**Sprint Duration**: March 30 - April 26, 2026  
**Sprint Goal**: "Capstone-ready RAG with confidence gating and Documentation Gap Radar differentiator"  
**Date**: April 26, 2026  
**Status**: **SPRINT 2 COMPLETE** 🎉

---

## 📊 Sprint Summary

### Completed Tasks: 9/12 (75%)

**Core Features (All Complete):**

1. ✅ Enhanced confidence detection (multi-factor scoring)
2. ✅ Safe fallback responses (prevent hallucination)
3. ✅ Improved prompt engineering (strict citation enforcement)
4. ✅ Edge case testing (19 tests, 78.9% pass rate)
5. ✅ Deployment options analysis (comprehensive documentation)
6. ✅ Database setup for Gap Radar (SQLite with SQLAlchemy 2.0)
7. ✅ Documentation gaps table schema (all fields + indexes)
8. ✅ Gap logging service (270 lines, 22/22 tests passing)
9. ✅ Gap Radar dashboard UI (React/TypeScript, full CRUD)

**Bonus Achievements:**

- ✅ CI/CD pipeline with GitHub Actions (backend + frontend)
- ✅ Modernized to SQLAlchemy 2.0 and langchain-chroma
- ✅ Zero TypeScript/ESLint errors across frontend
- ✅ Comprehensive test coverage (5 test files, 40+ tests)

**Cancelled/Deferred:**

- ❌ Sources page (implemented then removed - no user value)
- ❌ Manual sync button (dependent on Sources page)
- ⏸️ First evaluation run (deferred to Sprint 3)

---

## 🎯 What Went Well

### Technical Achievements

1. **Gap Radar Differentiator ⭐ (Sprint MVP)**
   - Complete end-to-end implementation: service → API → UI
   - Automatic gap detection when confidence < 0.7
   - SHA256-based deduplication with frequency tracking
   - Status workflow: NEW → REVIEWED → RESOLVED
   - Real-time statistics dashboard
   - 27 passing tests (17 unit + 5 integration + 5 edge cases)
   - **This is the capstone differentiator - goes beyond basic RAG**

2. **Confidence Gating (Production Safety)**
   - Multi-factor confidence calculation:
     - 50% similarity score (retrieval relevance)
     - 25% source diversity (multiple documents)
     - 25% context sufficiency (minimum 50 words)
   - Prevents hallucinations with strict fallback enforcement
   - Threshold tunable per environment (0.7 default)
   - Logged gap data for continuous improvement

3. **Code Quality Excellence**
   - SQLAlchemy 2.0 migration (Mapped[] types, zero deprecation warnings)
   - langchain-chroma upgrade (eliminated LangChain deprecations)
   - Type-safe throughout (Python type hints + TypeScript)
   - Zero Pylance/ESLint errors
   - Clean architecture: models, services, routes separation
   - Proper session management with context managers

4. **Testing Maturity**
   - Edge case testing: 19 tests across 6 categories
   - Gap service: 17 unit tests with in-memory SQLite
   - Integration tests: 5 tests for RAG + Gap service interaction
   - Database tests: Full CRUD verification
   - CI/CD automation: Tests run on every push
   - Deterministic tests (no flaky failures)

5. **Frontend Polish**
   - Gap Radar dashboard with intelligent filtering
   - Sort by frequency/date/confidence (asc/desc toggle)
   - Status filter (all/new/reviewed/resolved)
   - Real-time statistics (4 key metrics)
   - Color-coded status badges (red/yellow/green)
   - Empty states with helpful messaging
   - Responsive table layout with Tailwind CSS

### Process Wins

1. **On-Time Delivery**
   - 9/12 planned tasks completed (75%)
   - All critical path features done
   - Gap Radar differentiator fully implemented
   - Sprint goal achieved: "Capstone-ready RAG with confidence gating and Gap Radar"

2. **Smart Engineering Decisions**
   - SQLite over PostgreSQL (faster MVP, can migrate later)
   - Cancelled Sources page after UX review (no user value)
   - SHA256 hashing for O(1) duplicate detection
   - Moved to langchain-chroma for future compatibility
   - Added CI/CD early (caught issues immediately)

3. **Documentation Quality**
   - Sprint 2 backlog kept up-to-date throughout sprint
   - Edge case testing results documented
   - Comprehensive deployment options analysis
   - Clear acceptance criteria for all tasks
   - Git commits with detailed descriptions

4. **Cost Efficiency**
   - $0 infrastructure (Vercel/Render/Neon free tiers)
   - $0 AI costs (HuggingFace + Groq free tier)
   - Demonstrates fiscal responsibility for academic project

---

## 🔧 What Could Be Improved

### Technical Challenges

1. **Test Coverage Gaps**
   - Edge cases: 4/19 tests failed (partial docs, ambiguous questions)
   - System is conservative (prefers fallback over hallucination)
   - Need better similarity scoring for partial matches
   - **Action**: Tune confidence thresholds in Sprint 3

2. **No Formal Evaluation Run**
   - Task #12 deferred (5-10 test questions)
   - No benchmark dataset for answer quality
   - No latency/cost metrics documented
   - **Action**: Complete evaluation in Sprint 3 before deployment

3. **Similarity Scoring Conservative**
   - Distance-to-similarity conversion may need tuning
   - MIN_SIMILARITY_SCORE = 0.3 may be too permissive
   - Weighted factors (50/25/25) not empirically validated
   - **Action**: A/B test different scoring formulas

4. **Session Management Bug**
   - Initial gap status update endpoint failed (500 errors)
   - Session not properly closed after update
   - Fixed with proper context manager pattern
   - **Learning**: Always use SQLAlchemy context managers

### Process Challenges

1. **Scope Creep Avoidance**
   - Sources page implemented then removed (3 hours wasted)
   - Should have validated user value before implementing
   - **Learning**: Prototype UI mockups first, validate with user stories

2. **Test-Driven Development**
   - Some features implemented before tests (gap service initially)
   - Refactored after realizing gaps in coverage
   - **Learning**: Write tests first for service layer logic

3. **Trello Board Hygiene**
   - Mixed Sprint 2 and Sprint 3 tasks on same list
   - **Action**: Use labels

---

## 📈 Sprint Metrics

| Metric          | Sprint 1     | Sprint 2     | Trend   |
| --------------- | ------------ | ------------ | ------- |
| Tasks Completed | 9/19 (47%)   | 9/12 (75%)   | ⬆️ +28% |
| Code Added      | ~1,500 lines | ~1,800 lines | ⬆️      |
| Test Coverage   | 3 test files | 5 test files | ⬆️      |
| Tests Passing   | ~15 tests    | 40+ tests    | ⬆️      |
| GitHub Actions  | 0 workflows  | 2 workflows  | ⬆️      |
| Type Errors     | ~5 warnings  | 0 errors     | ⬆️      |
| Cost            | $0           | $0           | ✅      |

---

## 🎓 Key Learnings

### Technical Learnings

1. **SQLAlchemy 2.0 is Strict (But Better)**
   - Mapped[] types catch errors at type-check time
   - Relationships require explicit configuration
   - Session management must use context managers
   - Migration effort: ~2 hours, worth it for type safety

2. **Confidence Scoring is Hard**
   - Multiple factors needed (similarity alone insufficient)
   - Thresholds need empirical tuning with real data
   - Conservative scoring prevents hallucinations (good tradeoff)
   - Logging confidence helps debug quality issues

3. **Gap Detection is Powerful**
   - Automatically surfaces documentation weaknesses
   - Frequency tracking identifies common pain points
   - Status workflow enables documentation improvement loop
   - **This is the differentiator that makes the project special**

4. **CI/CD Catches Issues Early**
   - Type errors caught before code review
   - Test failures visible immediately
   - Format checks enforce consistency
   - Worth the 3-hour setup investment

### Process Learnings

1. **Cancel Features Ruthlessly**
   - Sources page had no user value (removed after implementation)
   - Better to validate assumptions early with mockups
   - Don't be attached to sunk cost

2. **Test-Driven Development Saves Time**
   - Writing tests first clarifies requirements
   - Easier to refactor with test safety net
   - Integration tests catch session management bugs

3. **Documentation is Living**
   - Sprint backlog updated throughout sprint
   - Acceptance criteria helped define "done"
   - Git commits reference task numbers for traceability

---

## 🎯 Sprint Goal Assessment

**Sprint Goal**: "Capstone-ready RAG with confidence gating and Documentation Gap Radar differentiator"

**Status**: ✅ **ACHIEVED**

**Evidence:**

- ✅ Confidence gating prevents hallucinations (fallback responses)
- ✅ Gap Radar fully implemented (service + API + UI)
- ✅ Comprehensive testing (40+ tests passing)
- ✅ Production-quality code (zero type errors, CI/CD)
- ✅ $0 cost maintained (demonstrates fiscal responsibility)
- ✅ Differentiator complete (targets 4-5/5 rubric scores)

**Gaps:**

- ⚠️ Evaluation run not completed (deferred to Sprint 3)
- ⚠️ Application not yet deployed (Sprint 3)

---

## 🚀 Looking Ahead to Sprint 3

### Critical Path (Must-Haves)

1. **Deploy Application**
   - Vercel (frontend) + Render (backend)
   - Environment variables configured
   - Health checks verified
   - **Deliverable**: Live URL for Quantic submission

2. **Complete DESIGN_AND_TESTING.md**
   - Architecture section complete (done)
   - Testing strategy section needs expansion
   - Deployment section complete (done)
   - **Deliverable**: Required for graduation

3. **Run Formal Evaluation**
   - 5-10 test questions covering all scenarios
   - Measure: accuracy, latency, confidence scores
   - Document in /docs/evaluation/
   - Identify any quality gaps before demo

4. **Record Demo Video**
   - 15-20 minutes showing all features
   - Show Gap Radar differentiator prominently
   - Include ID verification
   - **Deliverable**: Required for graduation

5. **Share Repo with quantic-grader**
   - Add as collaborator
   - Ensure all artifacts visible
   - **Deliverable**: Required for graduation

### Nice-to-Haves (If Time)

- GitHub file ingestion (currently using synthetic docs)
- Improved error handling (loading states, retries)
- Markdown code block parsing for better formatting
- Performance optimization (caching, query optimization)

### Risks & Mitigations

| Risk                                | Probability | Impact | Mitigation                       |
| ----------------------------------- | ----------- | ------ | -------------------------------- |
| Deployment complexity               | Medium      | High   | Start early, use free tier docs  |
| Evaluation reveals quality issues   | Low         | Medium | Fix before deployment            |
| Demo recording takes multiple takes | Medium      | Low    | Script demo, practice beforehand |
| Last-minute requirements changes    | Low         | High   | Feature freeze after Sprint 2    |

---

## 🎉 Celebrations

### Team (Solo) Wins

1. **Gap Radar Differentiator Complete** ⭐
   - This is the feature that sets this project apart
   - Full implementation: backend + frontend + tests
   - Production-ready code quality

2. **Code Quality Excellence**
   - Zero type errors across entire codebase
   - Comprehensive test coverage (40+ tests)
   - CI/CD automation working

3. **On-Time Delivery**
   - 75% task completion (vs 47% Sprint 1)
   - All critical features done
   - Sprint goal achieved

4. **Cost Discipline**
   - Maintained $0 cost throughout project
   - Proves FREE stack is viable for production

---

## 📝 Action Items for Sprint 3

### Week 1 (Apr 27 - May 3)

- [ ] Deploy backend to Render
- [ ] Deploy frontend to Vercel
- [ ] Verify end-to-end deployment
- [ ] Run formal evaluation (5-10 test questions)

### Week 2 (May 4 - May 10)

- [ ] Complete DESIGN_AND_TESTING.md (testing section)
- [ ] Write Sprint 3 backlog
- [ ] Script demo video content
- [ ] Practice demo walkthrough

### Week 3 (May 11 - May 17)

- [ ] Record demo video (15-20 min)
- [ ] Share repo with quantic-grader
- [ ] Final code cleanup and documentation review
- [ ] Create submission checklist

### Week 4 (May 18 - May 24)

- [ ] Sprint 3 retrospective
- [ ] Final testing on deployed environment
- [ ] Buffer for last-minute fixes
- [ ] **PERSONAL DEADLINE: May 24**

### Protected Buffer (May 25 - May 31)

- Emergency fixes only
- Ideally zero work needed
- **OFFICIAL DEADLINE: May 31**

---

## 🙏 Acknowledgments

**This sprint was successful because:**

- Clear sprint goal provided focus
- Ruthless prioritization (cancelled Sources page)
- Test-driven development caught bugs early
- Modern tooling (SQLAlchemy 2.0, TypeScript, CI/CD)
- Feature freeze discipline (no scope creep)

**Personal growth:**

- Learned SQLAlchemy 2.0 best practices
- Improved confidence scoring algorithms
- Better at validating feature value before implementation
- More comfortable with CI/CD setup

---

## ✅ Sprint 2 Status: COMPLETE

**Next**: Sprint 3 (Deployment + Documentation + Demo)  
**Timeline**: 28 days remaining until personal deadline  
**Confidence**: HIGH (on track for May 24 completion)

---

_Retrospective completed: April 26, 2026_  
_Sprint 2 officially closed_  
_Ready to begin Sprint 3_
