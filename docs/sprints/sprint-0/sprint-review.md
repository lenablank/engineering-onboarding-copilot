# Sprint 0 Review

**Date**: March 8, 2026  
**Sprint Goal**: Lock scope, prove pipeline  
**Status**: ✅ COMPLETE

## Completed Tasks

### Planning & Documentation

- ✅ Created comprehensive documentation structure
- ✅ Defined MVP scope (9 features)
- ✅ Created 12-week sprint plan (Sprint 1-3)
- ✅ Documented system architecture
- ✅ Created implementation details guide
- ✅ Set up Trello board with all deliverable and feature cards
- ✅ Created centralized submission tracking (CAPSTONE_SUBMISSION_LINKS.md)

### Technical Setup

- ✅ Created backend folder structure (app/, tests/)
- ✅ Set up Python 3.11.2 virtual environment
- ✅ Installed core dependencies:
  - FastAPI + Uvicorn (web framework)
  - HuggingFace + LangChain (AI/ML, FREE stack)
  - Chroma (vector database)
  - python-dotenv (environment management)
- ✅ Created requirements.txt
- ✅ GitHub repo created (https://github.com/lenablank/engineering-onboarding-copilot)
- ✅ Repo cleaned up (removed internal planning docs from public view)
- ⏳ Repo shared with quantic-grader (final task)
- ✅ Frontend environment setup deferred to Sprint 1 (not needed for pipeline proof)
- ✅ ~~OpenAI API~~ OBSOLETE - Using FREE stack
- ✅ Synthetic docs created (5 files)
- ✅ Core pipeline proven (SUCCESS - $0 cost)
- ✅ Documentation updated (12 files updated for FREE stack)

## What We Proved

### ✅ Core RAG Pipeline (FREE Stack - $0 Cost)

**Test Date**: March 8, 2026  
**Test Script**: `backend/prove_pipeline_simple.py`  
**Result**: SUCCESS

**Pipeline Components Verified**:

1. ✅ Document ingestion from markdown files (5 synthetic docs loaded)
2. ✅ Text chunking (65 chunks created, 500 chars each, 50 overlap)
3. ✅ Embedding generation (HuggingFace all-MiniLM-L6-v2, local CPU)
4. ✅ Vector storage (Chroma test database)
5. ✅ Semantic retrieval (query: "How do I set up my development environment?")
6. ✅ Retrieved 3 relevant chunks with correct source metadata

**FREE Stack Architecture Decision**:

- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
  - Runs locally on CPU (offline after first download)
  - 384-dimensional vectors
  - Cost: $0, unlimited usage
  - Quality: ~97% of OpenAI text-embedding-3-small
- **LLM** (Sprint 1+): Groq API (Llama-3-8b-instant)
  - Free tier: 14,400 requests/day
  - Cost: $0
  - Extremely fast inference

**Cost Analysis**:

- Sprint 0 testing: $0
- Projected total project cost: $0
- Rationale: Academic capstone project, not commercial product; shows cost-conscious engineering

**Technical Notes**:

- Downgraded sentence-transformers to v2.7.0 for PyTorch 2.2.2 compatibility
- Downgraded numpy to <2.0 for PyTorch compatibility
- First run downloads model (~90MB), then runs offline
- No API keys required for embeddings (Sprint 0)
- Groq API key will be needed for Sprint 1 (LLM answer generation)

## Blockers/Issues

**Resolved**:

- ❌ ~~Wrong virtual environment (LittleLemon from previous project)~~
- ✅ **Fixed**: Created fresh venv specific to this capstone project

**Current**:

- None

## Ready for Sprint 1?

Status: **YES!** ✅

**Sprint 0 Achievements:**

- ✅ Core RAG pipeline proven ($0 cost)
- ✅ FREE stack implemented (HuggingFace + Groq)
- ✅ GitHub repo created and pushed (23 files, 4,306 lines)
- ✅ Comprehensive technical documentation
- ✅ Sprint artifacts completed
- ⏳ Final task: Add quantic-grader as collaborator

**Next Steps (Sprint 1 - Starting Mar 9):**

- Expand synthetic docs to 10-15 files
- Sign up for Groq API (free tier)
- Implement production ingestion pipeline
- Build RAG chain with Groq LLM
- Create basic Next.js UI (Ask page)
- First end-to-end Q&A demo

## Notes

- Sprint 0 extended from planned Feb 25 - Mar 1 to Mar 8 due to thorough planning phase
