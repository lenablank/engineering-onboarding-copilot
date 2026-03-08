# Sprint 0 Backlog

## Planning & Setup

- [x] Create comprehensive planning documentation
- [x] Create Trello board with all cards
- [x] Add Trello link to README
- [x] Create CAPSTONE_SUBMISSION_LINKS.md
- [x] Create Sprint 0 artifacts folder (sprint-goal.md, sprint-backlog.md, sprint-review.md)
- [x] Set up Python backend environment (Python 3.11.2 venv)
- [x] Install backend dependencies (FastAPI, OpenAI, LangChain, Chroma)
- [x] Create environment configuration files (.env, .env.example, .gitignore)
- [x] Create 5 synthetic engineering docs (getting-started, architecture, testing, deployment, API reference)
- [x] Create proof-of-concept pipeline script (main.py with /prove-pipeline endpoint)
- [x] ~~Configure OpenAI API key~~ OBSOLETE - Migrated to FREE stack (HuggingFace local + Groq)
- [x] ~~Set OpenAI spending limit~~ OBSOLETE - Total cost $0 with FREE stack
- [x] Test prove_pipeline_simple.py to verify RAG pipeline works (SUCCESS - $0 cost)
- [x] Migrate to FREE stack (HuggingFace all-MiniLM-L6-v2 + Groq Llama-3-8b)
- [x] Update backend code for FREE embeddings (main.py, prove_pipeline_simple.py)
- [x] Update documentation files for FREE stack (12 files updated)
- [x] Create GitHub repository (https://github.com/lenablank/engineering-onboarding-copilot)
- [x] Clean up README for public repo (removed internal planning references)
- [ ] Share repo with quantic-grader
- [x] Update Sprint 0 review with results (test results, FREE stack details documented)
- [ ] ~~Set up Next.js frontend~~ DEFERRED to Sprint 1 Week 3 (not needed for pipeline proof)

## Notes

- Extended Sprint 0 from Feb 25 - Mar 1 to Mar 8 due to thorough planning phase
- Better to have solid planning than rush into coding
- Backend environment successfully created (Python 3.11.2 venv)
- **Major decision**: Migrated to FREE stack (HuggingFace + Groq) for $0 cost
  - Rationale: Academic capstone, not commercial product
  - Shows cost-conscious engineering (positive for rubric)
  - Quantic handbook doesn't require OpenAI specifically
  - Groq free tier (14,400/day) >> project needs (~10-20/day)
