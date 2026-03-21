# Sprint 1 Backlog

**Sprint Goal**: Deliver working Q&A system with GitHub sync and basic RAG pipeline  
**Sprint Duration**: March 2 - March 29, 2026  
**Status**: In Progress (Week 3/4)

---

## 📋 Task List (Prioritized)

### 🚨 CRITICAL PATH (Must Complete)

#### 1. ✅ DONE: Set up HuggingFace embeddings

**Status**: DONE (Sprint 0)  
**Notes**: Using all-MiniLM-L6-v2, FREE stack, working

---

#### 2. ⏳ IN PROGRESS: Expand synthetic docs to 10-15 files

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 3-4 hours  
**Acceptance Criteria**:

- Create 5-10 additional markdown files
- Cover realistic engineering topics: CI/CD, database setup, API design, security, monitoring
- Intentionally leave some gaps for Sprint 2 gap detection
- Each file 500-1500 words

---

#### 3. 🚨 BLOCKER: Sign up for Groq API + configure

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 15 minutes  
**Acceptance Criteria**:

- Sign up at console.groq.com
- Get API key (free tier: 14,400 requests/day)
- Add GROQ_API_KEY to backend/.env
- Add to .env.example (without actual key)

---

#### 4. 🚨 BLOCKER: Integrate Groq LLM for answer generation

**Status**: Not Started  
**Priority**: CRITICAL  
**Estimate**: 2-3 hours  
**Dependencies**: Task #3  
**Acceptance Criteria**:

- Install langchain-groq package
- Test Groq connectivity with simple prompt
- Verify Llama-3-8b-instant model works
- Log first successful LLM response

---

#### 5. Build RAG chain with LangChain

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 4-6 hours  
**Dependencies**: Task #4  
**Acceptance Criteria**:

- Create prompt template with citation instructions
- Build retrieval chain (Chroma → retrieve top-k)
- Build generation chain (Groq → answer with sources)
- Combine into single RAG chain
- Test with 3-5 sample questions
- Verify citations appear in answers

---

#### 6. Create /ask API endpoint (FastAPI)

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Dependencies**: Task #5  
**Acceptance Criteria**:

- POST /ask endpoint accepts question
- Calls RAG chain
- Returns answer + sources + retrieved chunks
- Handles errors gracefully
- Request/response models with Pydantic

---

#### 7. Set up Next.js frontend

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 2-3 hours  
**Acceptance Criteria**:

- Run `npx create-next-app@latest frontend`
- TypeScript + Tailwind CSS configured
- ESLint + Prettier configured
- Basic layout component
- Environment variables setup (.env.local)
- Dev server runs on localhost:3000

---

#### 8. Create Ask page UI (Next.js)

**Status**: Not Started  
**Priority**: HIGH  
**Estimate**: 4-6 hours  
**Dependencies**: Task #7  
**Acceptance Criteria**:

- Chat-style interface (question input + submit)
- Display answer with formatting
- Show source citations (file paths + snippets)
- Show retrieved chunks for transparency
- Loading states while waiting for API
- Error handling (API down, network errors)

---

#### 9. Display citations + source snippets

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 2 hours  
**Dependencies**: Task #8  
**Acceptance Criteria**:

- Citations shown below answer
- Each citation shows: file path, relevant snippet
- Retrieved chunks expandable/collapsible
- Basic styling for readability

---

#### 10. Add error handling (loading states, API errors)

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 2 hours  
**Dependencies**: Task #8  
**Acceptance Criteria**:

- Loading spinner during API call
- Error messages for failed requests
- Retry button on errors
- Toast notifications for success/error

---

### 📦 BACKEND IMPROVEMENTS (Nice to Have)

#### 11. Implement full GitHub file ingestion

**Status**: Partially Done (Sprint 0 has basic loading)  
**Priority**: MEDIUM  
**Estimate**: 2-3 hours  
**Acceptance Criteria**:

- Load from configurable directory path
- Support nested folders
- Filter by file extension (.md only)
- Skip common ignore patterns (.git, node_modules)

---

#### 12. Add markdown parsing for code blocks/tables

**Status**: Not Started  
**Priority**: LOW  
**Estimate**: 2-3 hours  
**Acceptance Criteria**:

- Preserve code blocks in chunks
- Handle markdown tables
- Preserve formatting in retrieved snippets

---

#### 13. Implement semantic chunking (MarkdownHeaderTextSplitter)

**Status**: Not Started (using basic RecursiveCharacterTextSplitter)  
**Priority**: MEDIUM  
**Estimate**: 2-3 hours  
**Acceptance Criteria**:

- Split by markdown headers (##, ###)
- Preserve header hierarchy in metadata
- Better chunk boundaries than character-based splitting
- Test with synthetic docs

---

#### 14. Preserve chunk metadata (file path, headers)

**Status**: Partially Done (basic metadata exists)  
**Priority**: MEDIUM  
**Estimate**: 1-2 hours  
**Acceptance Criteria**:

- Store file path in metadata
- Store header hierarchy (e.g., "## Setup > ### Local Development")
- Store chunk index
- Return metadata with retrieved chunks

---

### 🧪 TESTING & QUALITY

#### 15. Write unit tests for chunking

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 2 hours  
**Acceptance Criteria**:

- Test chunking with sample markdown
- Verify chunk sizes
- Verify metadata preservation
- Test edge cases (empty files, huge files)

---

#### 16. Write unit tests for embeddings (mocked)

**Status**: Not Started  
**Priority**: LOW  
**Estimate**: 2 hours  
**Acceptance Criteria**:

- Mock HuggingFace API calls
- Test embedding generation flow
- Verify vector dimensions

---

#### 17. Set up basic CI/CD pipeline (GitHub Actions)

**Status**: Not Started  
**Priority**: LOW (can defer to Sprint 3)  
**Estimate**: 2-3 hours  
**Acceptance Criteria**:

- Run linting (Black, ESLint)
- Run tests on push
- Basic build check

---

#### 18. First evaluation run (5-10 test questions)

**Status**: Not Started  
**Priority**: MEDIUM  
**Estimate**: 2-3 hours  
**Dependencies**: Task #6, #8  
**Acceptance Criteria**:

- Create 5-10 test questions
- Expected answers documented
- Run through system
- Document results (accuracy, citation quality)
- Identify gaps for Sprint 2

---

#### 19. Sprint 1 retrospective

**Status**: Not Started  
**Priority**: HIGH (Required for rubric)  
**Estimate**: 1 hour  
**Due**: March 29  
**Acceptance Criteria**:

- Create sprint-retrospective.md
- What went well
- What to improve
- Action items for Sprint 2

---

## 📊 Progress Tracking

**Total Tasks**: 19  
**Done**: 1 (✅ HuggingFace embeddings)  
**In Progress**: 0  
**Not Started**: 18  
**Blocked**: 2 (Groq setup blocking RAG chain)

---

## 🎯 This Week Focus (Mar 21-24)

**MUST COMPLETE** (in order):

1. Expand synthetic docs (Task #2)
2. Groq API signup (Task #3)
3. Groq integration (Task #4)
4. RAG chain (Task #5)

**STRETCH**: 5. /ask endpoint (Task #6)

---

## 🎯 Next Week Focus (Mar 25-29)

**MUST COMPLETE**:

1. Next.js setup (Task #7)
2. Ask page UI (Task #8)
3. End-to-end testing
4. Sprint retrospective (Task #19)

**NICE TO HAVE**:

- Error handling (Task #10)
- First evaluation run (Task #18)
- Semantic chunking (Task #13)
