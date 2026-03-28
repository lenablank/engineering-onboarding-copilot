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

#### 2. Safe fallback responses

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Dependencies**: Task #1  
**Due**: Apr 7

**Acceptance Criteria**:

- [ ] When confidence < threshold, return fallback message
- [ ] Fallback message: "I cannot answer this confidently from the current documentation. This question has been logged as a documentation gap."
- [ ] Fallback prevents unsupported LLM hallucinations
- [ ] Citation grounding enforced (no answer without sources)
- [ ] Test with irrelevant questions (e.g., "What's the weather?")

---

#### 3. Improve prompt engineering

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Due**: Apr 8

**Acceptance Criteria**:

- [ ] Update system prompt with strict citation enforcement
- [ ] Add instruction: "Answer ONLY from provided context. DO NOT use external knowledge."
- [ ] Add few-shot examples showing good citation format
- [ ] Test prompt prevents hallucinations
- [ ] Document prompt template in code comments

**Implementation Notes**:

- Update RAGService prompt template
- Consider adding negative examples (what NOT to do)
- Test with ambiguous questions

---

#### 4. Test edge cases

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Dependencies**: Task #1, #2, #3  
**Due**: Apr 10

**Acceptance Criteria**:

- [ ] Test irrelevant questions (sports, weather, math)
- [ ] Test ambiguous questions (multiple interpretations)
- [ ] Test questions with partial documentation coverage
- [ ] Test empty/very short questions
- [ ] Document test results in `/docs/evaluation/sprint-2-edge-cases.md`

---

#### 5. Document deployment options

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 2-3 hours  
**Due**: Apr 12

**Acceptance Criteria**:

- [ ] Add deployment analysis to DESIGN_AND_TESTING.md
- [ ] Compare: Local-only vs. Vercel+Render vs. cloud-native
- [ ] Document cost implications for each option
- [ ] Document selected option with rationale
- [ ] Include scaling considerations

---

### ⭐ WEEK 3: Documentation Gap Radar (DIFFERENTIATOR) (Apr 13-19)

#### 6. Set up Postgres database

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Due**: Apr 14

**Acceptance Criteria**:

- [ ] Install PostgreSQL locally (or use Supabase free tier)
- [ ] Create database: `engineering_onboarding_db`
- [ ] Configure connection in backend/.env (DATABASE_URL)
- [ ] Add psycopg2 to requirements.txt
- [ ] Test connection from FastAPI startup

**Implementation Notes**:

- Use Supabase free tier for easy deployment later
- Alternative: SQLite for MVP if Postgres setup is blocked
- Store DATABASE_URL in .env (keep credentials secure)

---

#### 7. Create documentation_gaps table

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 1-2 hours  
**Dependencies**: Task #6  
**Due**: Apr 15

**Acceptance Criteria**:

- [ ] Schema created:
  - `id` (UUID, primary key)
  - `question` (text, NOT NULL)
  - `confidence_score` (float)
  - `retrieval_context` (JSONB, stores retrieved chunks)
  - `frequency` (integer, default 1)
  - `status` (enum: new, reviewed, resolved)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- [ ] Migration script in `backend/migrations/`
- [ ] Add indexes on `created_at`, `frequency`, `status`

**Implementation Notes**:

- Consider using Alembic for migrations
- Store retrieval_context for debugging (optional)

---

#### 8. Build gap logging service

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 4-5 hours  
**Dependencies**: Task #7  
**Due**: Apr 17

**Acceptance Criteria**:

- [ ] Create `app/services/gap_service.py`
- [ ] Function: `log_gap(question, confidence, chunks)` 
- [ ] Check if question already exists → increment frequency
- [ ] New questions get status='new', frequency=1
- [ ] Integrate with RAGService.ask() - auto-log when confidence < threshold
- [ ] Test: Ask same low-confidence question 3x → frequency=3

**Implementation Notes**:

- Use fuzzy matching to detect duplicate questions (optional: 90% similarity)
- Store question hash for faster lookups

---

#### 9. Create /gaps dashboard page

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 5-6 hours  
**Dependencies**: Task #8  
**Due**: Apr 19

**Acceptance Criteria**:

- [ ] New frontend route: `frontend/src/app/gaps/page.tsx`
- [ ] Backend API: `GET /gaps` returns all gaps with pagination
- [ ] Display: question, confidence, frequency, status, timestamp
- [ ] Sort options: frequency (desc), recency (desc), status
- [ ] Filter by status: new, reviewed, resolved
- [ ] (Optional if time) Status update UI (mark as reviewed/resolved)
- [ ] Empty state message when no gaps exist
- [ ] Responsive design with Tailwind

**Implementation Notes**:

- Use simple table layout (no need for fancy charts)
- Color-code by status: red (new), yellow (reviewed), green (resolved)

---

### 📄 WEEK 4: Sources Page + Review (Apr 20-26)

#### 10. Create /sources page

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 4-5 hours  
**Due**: Apr 22

**Acceptance Criteria**:

- [ ] New frontend route: `frontend/src/app/sources/page.tsx`
- [ ] Backend API: `GET /sources` returns indexed docs metadata
- [ ] Display: file path, chunk count, last indexed timestamp
- [ ] Show total docs count, total chunks count
- [ ] List all source files in indexed collection
- [ ] Simple table layout with search/filter (optional)

**Implementation Notes**:

- Query ChromaDB collection metadata
- Store last_indexed_at in collection metadata (add in Task #11)

---

#### 11. Manual sync button

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Dependencies**: Task #10  
**Due**: Apr 24

**Acceptance Criteria**:

- [ ] "Sync Now" button on /sources page
- [ ] Backend API: `POST /sync` triggers re-indexing
- [ ] Clear existing Chroma collection (use delete_collection)
- [ ] Re-load all markdown files from synthetic-docs/
- [ ] Re-chunk and re-embed
- [ ] Return sync status: success/failed, docs indexed, chunks created
- [ ] Sync status indicator: "Syncing...", "Last synced 2 min ago"

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
**Done**: 1 (✅ Task #1)  
**In Progress**: 0  
**Not Started**: 16

**Sprint 2 Status**: In Progress (Week 1/4)

**Completed**:
- ✅ Task #1: Enhanced confidence detection (Mar 28)

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
