# Sprint 2 Backlog

**Sprint Goal**: "Capstone-ready RAG with confidence gating and Documentation Gap Radar differentiator"  
**Sprint Duration**: March 30 - April 26, 2026  
**Status**: Not Started

---

## 📋 Task List (Prioritized by Week)

### 🚨 WEEK 1-2: Confidence Scoring + Fallback (Mar 30 - Apr 12)

#### 1. ✅ DONE: Implement confidence detection

**Status**: DONE (Mar 28)  
**Priority**: CRITICAL  
**Estimate**: 4-6 hours  
**Actual**: 2 hours  
**Completion Notes**:

- Enhanced `_calculate_confidence()` with multi-factor calculation
- Added MIN_CONTEXT_WORDS = 50 (context sufficiency check)
- Added MIN_SOURCES = 2 (source diversity check)
- Added MIN_SIMILARITY_SCORE = 0.3 (minimum relevance threshold)
- Weighted scoring: 50% similarity + 25% source diversity + 25% context sufficiency
- Created test_confidence_enhanced.py for validation
- Test results show improved confidence scoring (0.68-0.79 range)
- Commit: 578d276

**Acceptance Criteria**: ✅

- ✅ Similarity score threshold implemented (< 0.7 = low confidence)
- ✅ Context sufficiency check (min words retrieved, min sources count)
- ✅ Source quality scoring (weighted by relevance)
- ✅ Confidence score returned in /ask API response
- ✅ Confidence calculation logged for debugging

---

#### 2. ✅ DONE: Safe fallback responses

**Status**: DONE (Mar 28)  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Actual**: 1.5 hours  
**Dependencies**: Task #1  
**Completion Notes**:

- Extracted FALLBACK_MESSAGE constant (DRY principle)
- Created `_create_fallback_response()` helper method
- Fixed type hint: `Optional[List[Document]]` for proper None handling
- Improved logging: "Returning fallback response to prevent hallucination"
- Reduced code duplication: eliminated 15 lines
- Test coverage: test_fallback_refactored.py with 5 test scenarios
- Commit: fc435bc

**Acceptance Criteria**: ✅

- ✅ When confidence < threshold, return fallback message
- ✅ Fallback message from FALLBACK_MESSAGE constant
- ✅ Fallback prevents unsupported LLM hallucinations (gating mechanism)
- ✅ Citation grounding enforced (no answer without sources)
- ✅ Tested with irrelevant questions ("What's the capital of France?")

---

#### 3. ✅ DONE: Improve prompt engineering

**Status**: DONE (Mar 28 - completed with Task #2)  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Actual**: 30 minutes (part of Task #2)  
**Completion Notes**:

- Updated SYSTEM_PROMPT with stricter instructions
- Added "respond EXACTLY:" to emphasize fallback wording
- Added rule 6: "Do NOT answer questions outside the provided context"
- Added reminder: "When in doubt, use the fallback response"
- Better emphasis on preventing hallucinations
- Commit: fc435bc (same as Task #2)

**Acceptance Criteria**: ✅

- ✅ Update system prompt with strict citation enforcement
- ✅ Add instruction: "Answer ONLY from provided context. DO NOT use external knowledge."
- ✅ Prompt emphasizes exact fallback response wording
- ✅ Test prompt prevents hallucinations (verified in test_fallback_refactored.py)
- ✅ Prompt template documented in code with clear rules

---

#### 4. ✅ DONE: Test edge cases

**Status**: DONE (Apr 9)  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Actual**: 3 hours  
**Dependencies**: Task #1, #2, #3  
**Completion Notes**:

- Created comprehensive test suite: `test_edge_cases.py`
- Executed 19 tests across 6 categories
- Test results: 15/19 passed (78.9%)
- Generated detailed report in `docs/evaluation/sprint-2-edge-cases.md`
- Key findings:
  - Irrelevant questions: 100% fallback rate (perfect)
  - Well-documented questions: 0% fallback rate, avg 0.79 confidence
  - System demonstrates conservative behavior (avoids hallucinations)
  - Input validation working correctly
  - Typo tolerance confirmed via embeddings

**Acceptance Criteria**: ✅

- ✅ Test irrelevant questions (sports, weather, math) - 5/5 passed
- ✅ Test ambiguous questions (multiple interpretations) - 2/3 passed
- ✅ Test questions with partial documentation coverage - 1/3 passed (conservative behavior)
- ✅ Test empty/very short questions - 3/3 passed
- ✅ Document test results in `/docs/evaluation/sprint-2-edge-cases.md`

---

#### 5. ✅ DONE: Document deployment options

**Status**: DONE (Apr 12)  
**Priority**: MEDIUM  
**Estimate**: 2-3 hours  
**Actual**: 2 hours  
**Due**: Apr 12  
**Completion Notes**:

- Enhanced DESIGN_AND_TESTING_TEMPLATE.md Section 7 with comprehensive deployment analysis
- Compared 4 options: Local-only ($0), Vercel+Render ($0, SELECTED), VPS ($5/month), Cloud-native ($20-50/month)
- Documented detailed cost breakdown: $0/month infrastructure + $0 AI = $0 total
- Added free tier limits table (Vercel 100GB, Render 750hrs, Groq 14,400 req/day)
- Documented tradeoffs accepted (cold starts, ephemeral filesystem, no scaling)
- Added deployment readiness checklist and post-deployment verification steps
- Explained cost-conscious engineering: chose free stack (HuggingFace + Groq) over commercial (OpenAI)
- Documented scaling path for future growth
- Addressed Quantic handbook requirement: "deployment options recommended for the software including relative cost implications"

**Acceptance Criteria**: ✅

- ✅ Add deployment analysis to DESIGN_AND_TESTING.md
- ✅ Compare: Local-only vs. Vercel+Render vs. cloud-native
- ✅ Document cost implications for each option
- ✅ Document selected option with rationale
- ✅ Include scaling considerations

---

### ⭐ WEEK 3: Documentation Gap Radar (DIFFERENTIATOR) (Apr 13-19)

#### 6. Set up Postgres database

**Status**: Not Started  
**Priority**: CRITICAL

#### 6. ✅ DONE: Set up database for Gap Radar

**Status**: DONE (Apr 9)  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Actual**: 2 hours  
**Completion Notes**:

- Chose SQLite for MVP implementation (faster setup, zero config)
- Created database models using SQLAlchemy 2.0
- Implemented `DocumentationGap` model with all required fields
- Added DATABASE_URL to .env configuration
- Created comprehensive test suite (`test_database_setup.py`)
- All CRUD operations verified and working
- Database initialized on FastAPI startup
- 4 indexes created (question, frequency, status, created_at)
- Ready for gap logging service integration

**Acceptance Criteria**: ✅

- ✅ Database configured (SQLite - can migrate to Postgres later)
- ✅ Connection configured in backend/.env (DATABASE_URL)
- ✅ SQLAlchemy already in requirements.txt (no changes needed)
- ✅ Connection tested successfully from FastAPI startup
- ✅ Database file created: `gaps.db`

**Technical Implementation**:

- Files created:
  - `app/models/database.py` - Database setup & session management
  - `app/models/gap.py` - DocumentationGap model
  - `app/models/__init__.py` - Package exports
  - `test_database_setup.py` - Comprehensive test suite
- Integration: Added `init_db()` to FastAPI startup event
- Migration path: SQLite → Postgres when needed (schema compatible)

---

#### 7. ✅ DONE: Create documentation_gaps table

**Status**: DONE (Apr 9 - completed with Task #6)  
**Priority**: CRITICAL  
**Estimate**: 1-2 hours  
**Actual**: Included in Task #6  
**Dependencies**: Task #6  
**Completion Notes**:

- Schema created with SQLAlchemy models
- All required fields implemented
- Automatic timestamp management (created_at, updated_at)
- UUIDv4 primary keys
- JSON field for retrieval context
- Enum for status (NEW, REVIEWED, RESOLVED)
- All tests passing (insert, update, query, delete)

**Acceptance Criteria**: ✅

- ✅ Schema created with all required fields:
  - ✅ `id` (UUID, primary key)
  - ✅ `question` (text, NOT NULL)
  - ✅ `confidence_score` (float)
  - ✅ `retrieval_context` (JSON, stores retrieved chunks)
  - ✅ `frequency` (integer, default 1)
  - ✅ `status` (enum: new, reviewed, resolved)
  - ✅ `created_at` (timestamp)
  - ✅ `updated_at` (timestamp)
- ✅ Schema managed by SQLAlchemy ORM (no manual migrations needed for SQLite)
- ✅ Indexes created on `created_at`, `frequency`, `status`, `question`

---

#### 8. ✅ DONE: Build gap logging service

**Status**: DONE (Apr 9)  
**Priority**: CRITICAL  
**Estimate**: 4-5 hours  
**Actual**: 4.5 hours  
**Dependencies**: Task #7  
**Completion Notes**:

- Created comprehensive `GapService` class (270 lines)
- Implemented SHA256 hash-based deduplication (detects identical questions)
- Auto-increment frequency counter for duplicate questions
- Full CRUD operations: create, get_all, get_by_id, update_status, get_stats
- REST API with 4 endpoints: GET /api/gaps, GET /api/gaps/stats, GET /api/gaps/{id}, PATCH /api/gaps/{id}/status
- Integrated with RAGService.ask() - auto-logs when confidence < CONFIDENCE_THRESHOLD
- Status workflow: NEW → REVIEWED → RESOLVED
- Comprehensive test coverage: 22/22 tests passing (17 unit + 5 integration)
- All tests verify: creation, deduplication, frequency tracking, status updates, statistics
- Modernized to SQLAlchemy 2.0 Mapped[] types (zero type errors)
- Committed (15ebf65) and pushed to GitHub

**Acceptance Criteria**: ✅

- ✅ Created `app/services/gap_service.py` (270 lines)
- ✅ Function: `log_gap(question, confidence_score, retrieval_context, status)`
- ✅ Duplicate detection via SHA256 question hash → increments frequency
- ✅ New questions get status='NEW', frequency=1
- ✅ Integrated with RAGService.ask() - auto-logs when confidence < 0.7
- ✅ Tested: Same low-confidence question 3x → frequency=3 ✓

**Technical Implementation**:

- Files created:
  - `app/services/gap_service.py` - Main service class with CRUD operations
  - `app/routes/gaps.py` - REST API endpoints
  - `tests/test_gap_service.py` - 17 unit tests
  - `tests/test_gap_integration.py` - 5 integration tests
- SHA256 hashing for O(1) duplicate detection
- SQLAlchemy session management with proper cleanup
- Type-safe with Mapped[] types (zero Pylance errors)

---

#### 9. ✅ DONE: Create /gaps dashboard page

**Status**: DONE (Apr 12)  
**Priority**: CRITICAL  
**Estimate**: 5-6 hours  
**Actual**: 4 hours  
**Dependencies**: Task #8  
**Completion Notes**:

- Created clean, senior-level React component with TypeScript
- Implemented real-time data fetching from backend API
- Built responsive table UI with Tailwind CSS
- Added sort functionality (frequency, date, confidence) with toggle
- Implemented status filter (all, new, reviewed, resolved)
- Statistics dashboard with 4 key metrics
- Color-coded status badges (red=new, yellow=reviewed, green=resolved)
- Empty state messaging
- Navigation bar added to app layout
- Gap Radar feature card added to homepage
- Fixed backend session management issue in status update
- All 5 integration tests passing
- Zero TypeScript/ESLint errors

**Acceptance Criteria**: ✅

- ✅ New frontend route: `frontend/src/app/gaps/page.tsx` (340 lines)
- ✅ Backend API: `GET /api/gaps/` returns all gaps with pagination support
- ✅ Display: question, confidence, frequency, status, timestamp
- ✅ Sort options: frequency, recency, confidence (asc/desc toggle)
- ✅ Filter by status: all, new, reviewed, resolved
- ✅ Empty state message when no gaps exist
- ✅ Responsive design with Tailwind CSS

**Technical Implementation**:

- Files created:
  - `frontend/src/app/gaps/page.tsx` - Main dashboard component (340 lines)
  - Updated `frontend/src/app/layout.tsx` - Added navigation bar with Gap Radar link
  - Updated `frontend/src/app/page.tsx` - Added Gap Radar feature card
- Features:
  - Real-time statistics: total gaps, occurrences, status breakdown
  - Client-side sorting with asc/desc toggle
  - Server-side filtering by status
  - Responsive table layout with hover states
  - Click-to-sort column headers
  - Refresh button for manual data reload
- Bug fix: Fixed backend session management in `update_gap_status()` (was causing 500 errors)
- Clean code: Proper TypeScript types, reusable formatters, no prop drilling

**Implementation Notes**:

- Simple table layout (no complex charts - keeping it maintainable)
- Color-coding: red (NEW), yellow (REVIEWED), green (RESOLVED)

---

### 📄 WEEK 4: Sources Page + Review (Apr 20-26)

#### 10. ❌ CANCELLED: Create /sources page

**Status**: CANCELLED (Apr 12)  
**Priority**: WAS: HIGH  
**Estimate**: 4-5 hours  
**Actual**: 3 hours (then removed)  
**Decision Date**: Apr 12  
**Reason for Cancellation**:

Upon implementation and UX review, determined the Sources page provides no real user value:
- Users don't need to see which files are indexed (they need answers to questions)
- Nothing actionable or clickable (read-only list of file names)
- Admins wouldn't use a UI for this (would use code, terminal, or logs)
- Better to keep UI focused on core user journeys: Ask Question → Get Answer → Gap Radar

Engineering decision: Remove to maintain clean, purposeful UX. Sync functionality (Task #11) will be moved to a more appropriate location if needed.

**Code removed**:
- Frontend: `/sources` page and navigation link
- Backend: `/api/sources/` endpoint, routes/sources.py, get_sources() method
- All changes reverted cleanly

**Lesson learned**: Question feature requirements early. "Admin page" features should solve real admin workflows, not just display debug data in a UI.

---

#### 11. Manual sync button

**Status**: Not Started  
**Priority**: MEDIUM (was HIGH)  
**Estimate**: 2-3 hours (reduced from 3-4)  
**Dependencies**: None (Task #10 removed)  
**Due**: Apr 24

**Re-scoped Approach**:
Since Sources page removed, sync functionality will be implemented differently:
- Option A: Add sync button to homepage with status indicator
- Option B: CLI script: `python sync_docs.py` (simpler, more appropriate for admin task)
- Decision to be made when implementing

**Acceptance Criteria**:

- [ ] Manual sync capability exists (UI or CLI)
- [ ] Backend API: `POST /sync` triggers re-indexing
- [ ] Clear existing Chroma collection (use delete_collection)
- [ ] Re-load all markdown files from synthetic-docs/
- [ ] Re-chunk and re-embed
- [ ] Return sync status: success/failed, docs indexed, chunks created

**Implementation Notes**:

- Add locking to prevent concurrent syncs
- Show progress indicator during sync (loading spinner)

---

#### 12. First evaluation run (5-10 test questions)

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Dependencies**: Tasks #1-9  
**Due**: Apr 25

**Acceptance Criteria**:

- [ ] Create 10 test questions covering:
  - Answerable questions (should get cited answers)
  - Partially documented questions (medium confidence)
  - Undocumented questions (should trigger gap logging)
  - Edge cases (irrelevant, ambiguous)
- [ ] Document expected answers
- [ ] Run through system, record actual responses
- [ ] Measure: accuracy, citation rate, confidence scores, latency
- [ ] Document results in `/docs/evaluation/sprint-2-eval-results.md`
- [ ] Identify gaps for Sprint 3 improvements

---

#### 13. Sprint 2 review & retrospective

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 1-2 hours  
**Due**: Apr 26

**Acceptance Criteria**:

- [ ] Create `sprint-retrospective.md` covering:
  - Sprint 2 summary (features completed)
  - What went well
  - Challenges encountered
  - Learnings captured
  - Action items for Sprint 3
  - Metrics: tasks completed, code additions, performance
- [ ] Review Gap Radar functionality (demo to yourself as PO)
- [ ] Verify all critical features working end-to-end

---

### 🔄 OPTIONAL (Only if time allows after critical tasks)

#### 14. Error handling improvements (from Sprint 1)

**Status**: Not Started  
**Priority**: LOW  
**Estimate**: 2 hours  
**Acceptance Criteria**:

- [ ] Add retry button on API failures
- [ ] Toast notifications for errors
- [ ] Better loading states
- [ ] Network error detection

---

#### 15. Preserve chunk metadata (headers)

**Status**: Not Started  
**Priority**: LOW  
**Estimate**: 2 hours  
**Acceptance Criteria**:

- [ ] Store header hierarchy in chunk metadata
- [ ] Format: "## Setup > ### Local Development"
- [ ] Display in retrieved chunks section

---

#### 16. Markdown parsing for code blocks

**Status**: Not Started  
**Priority**: LOW  
**Estimate**: 2-3 hours  
**Acceptance Criteria**:

- [ ] Preserve code blocks during chunking
- [ ] Handle markdown tables
- [ ] Preserve formatting in snippets

---

#### 17. Semantic chunking (MarkdownHeaderTextSplitter)

**Status**: Not Started  
**Priority**: LOW  
**Estimate**: 3 hours  
**Acceptance Criteria**:

- [ ] Use MarkdownHeaderTextSplitter instead of RecursiveCharacterTextSplitter
- [ ] Test with synthetic docs
- [ ] Compare chunk quality vs. current approach

---

## 📊 Progress Tracking

**Total Tasks**: 17 (13 critical + 4 optional)  
**Done**: 6 (✅ Tasks #1, #2, #3, #4, #6, #7)  
**In Progress**: 0  
**Not Started**: 11

**Sprint 2 Status**: In Progress (Week 2/4)

**Completed**:

- ✅ Task #1: Enhanced confidence detection (Mar 28)
- ✅ Task #2: Safe fallback responses (Mar 28)
- ✅ Task #3: Improved prompt engineering (Mar 28)
- ✅ Task #4: Edge case testing (Apr 9)
- ✅ Task #6: Database setup for Gap Radar (Apr 9)
- ✅ Task #7: Documentation gaps table (Apr 9)

---

## 🎯 Weekly Breakdown

### Week 1 (Mar 30 - Apr 5)

**Focus**: Confidence scoring foundation

- Task #1: Confidence detection
- Task #2: Fallback responses

### Week 2 (Apr 6 - Apr 12)

**Focus**: Prompt improvements + edge case testing

- Task #3: Prompt engineering
- Task #4: Edge case testing
- Task #5: Deployment docs

### Week 3 (Apr 13 - Apr 19) ⭐ CRITICAL WEEK

**Focus**: Gap Radar implementation

- Task #6: Postgres setup
- Task #7: Table schema
- Task #8: Gap logging service
- Task #9: /gaps dashboard

### Week 4 (Apr 20 - Apr 26)

**Focus**: Sources page + evaluation

- Task #10: /sources page
- Task #11: Manual sync
- Task #12: Evaluation run
- Task #13: Sprint review & retro

---

## 🚨 Risk Management

**Risk**: Postgres setup delays Gap Radar implementation  
**Mitigation**: Use SQLite as fallback for MVP, migrate to Postgres in Sprint 3

**Risk**: Gap detection produces too many false positives  
**Mitigation**: Tune confidence threshold based on evaluation results (Task #12)

**Risk**: Scope creep from optional tasks  
**Mitigation**: Feature freeze - only do optional tasks if all critical tasks complete by Apr 22

---

## Definition of Done (Per Task)

- [ ] Code written and tested locally
- [ ] Committed to git with descriptive message
- [ ] API endpoints tested with Postman/curl (if backend task)
- [ ] UI tested in browser (if frontend task)
- [ ] No console errors
- [ ] Trello card moved to Done

## Definition of Done (Sprint 2)

- [ ] All 13 critical tasks complete
- [ ] Gap Radar working end-to-end (ask low-confidence question → logged → visible in dashboard)
- [ ] Evaluation run completed with results documented
- [ ] Sprint retrospective written
- [ ] Trello board updated (all done cards moved)
- [ ] Main branch CI/CD passing (when implemented in Sprint 3)
- [ ] Demo-ready for confidence gating + Gap Radar features
