# Evaluation Plan & Demo Guide

This document covers the demo walkthrough, evaluation methodology, cost analysis, and success metrics.

---

## 🎬 Demo Scenario Walkthrough

### Quantic Presentation Compliance Checklist

**CRITICAL: Verify these BEFORE recording final demo**

- [ ] **Government-issued ID shown clearly** at beginning (name visible)
- [ ] **Face visible** throughout presentation (or at required intervals per rubric)
- [ ] **Audio quality tested** (clear, no background noise)
- [ ] **Screen text legible** (zoom in on small text, use high resolution)
- [ ] **Final duration**: 15-20 minutes (not shorter, not longer)
- [ ] **All required elements**: problem, solution, architecture, demo, Q&A
- [ ] **Screen recording software tested** (OBS, Zoom, or approved tool)
- [ ] **Backup recording** (record twice if possible)

**Failure to meet these requirements may require resubmission - check alignment carefully!**

---

### Demo-Safe Fallback Plan

**What if deployment is flaky on free tiers during recording?**

**Primary Demo Approach**:

- Live deployed demo (Vercel + Render URLs)
- Real-time interaction with production app

**Backup Plan** (if deployment issues occur):

- Local run demo (same codebase, `npm run dev` + `uvicorn`)
- Show deployed URLs separately (even if sleeping/slow)
- Pre-prepared sample questions with known good answers
- Screenshots/recordings of successful deploys as evidence

**Pre-Demo Checklist**:

- [ ] Test deployed app 24 hours before recording
- [ ] Wake up backend (hit `/health` endpoint if on free tier)
- [ ] Prepare 5-7 sample questions with expected answers
- [ ] Have local backup running during recording
- [ ] Record deployment evidence (URLs, health checks, timestamps)

**Deployment Strategy**: Primary plan is live deployed demo via public URLs. If free-tier instability occurs during recording, show the deployed URLs first, then complete the walkthrough locally using the same codebase to preserve demonstration continuity.

---

### Demo Script (15-20 minutes)

#### **1. Introduction (2 min)**

- Show government ID clearly (per Quantic requirement)
- Problem: New engineers ask same questions repeatedly, docs are fragmented
- Solution: AI onboarding assistant with evidence-based answering + gap detection
- Live demo walkthrough preview

#### **2. Show Synced Documentation (1 min)**

- Navigate to Sources/Sync page
- Show list of indexed documents
- Show last sync timestamp
- Explain: "Auto-synced from GitHub, no manual uploads"

#### **3. Ask Answerable Questions (5 min)**

**Question 1**: "How do I run the backend locally?"

- Show answer generated with step-by-step instructions
- Highlight source citations: `[docs/setup.md]`, `[README.md]`
- Click to view retrieved snippets
- Point out: "Answer grounded in actual documentation"

**Question 2**: "What's our testing strategy?"

- Show answer with testing framework details
- Multiple sources cited
- Demonstrate citation accuracy

**Question 3**: "Where is authentication implemented?"

- Show answer pointing to specific files/directories
- Code location references
- Architecture explanation from docs

#### **4. Trigger Documentation Gap (3 min)**

**Question 4**: "How do we rotate API keys in production?"

- Show response: "I cannot answer this confidently from the current documentation"
- Navigate to Documentation Gaps dashboard
- Show new gap logged with:
  - Question text
  - Timestamp
  - Confidence score
  - Suggested topic: "Security"
- Explain: "Team can prioritize filling this gap"

#### **5. Show Gap Dashboard (2 min)**

- Sort by frequency (show questions asked multiple times)
- Filter by status
- Explain workflow: new → reviewed → resolved
- Business value: "Improves documentation over time"

#### **6. Show Metrics/Observability (2 min)**

- Query log table or metrics panel
- Show:
  - Total questions asked
  - Average latency
  - Citation rate (% answers with sources)
  - Answerable vs. gap ratio (e.g., 80% answerable)
- Explain: "Production monitoring for quality"

#### **7. Technical Deep Dive (3 min)**

- Show architecture diagram
- Explain RAG pipeline:
  - GitHub sync → chunking → embeddings → vector DB
  - Semantic search → confidence check → answer or gap
- Highlight confidence-aware fallback
- Show CI/CD setup (GitHub Actions)

#### **8. Conclusion (2 min)**

- Recap differentiators:
  - Auto-ingestion (no uploads)
  - Evidence-based fallback (reduces bad answers)
  - Gap detection (feedback loop)
  - Production thinking (testing, CI/CD, observability)
  - AI safety (prompt injection resistance, input validation, audit logging)
- Future enhancements (CLI, scheduled sync, multi-source)
- Q&A

---

## 📊 Evaluation Plan

### Evaluation Question Set (20-30 Questions)

Create a **regression test set** of onboarding questions across categories:

#### **Answerable Questions (12-15)**:

- "How do I run the backend locally?"
- "What testing framework do we use?"
- "Where is authentication implemented?"
- "How do deployments work?"
- "What's our branching strategy?"
- "How do I add a new API endpoint?"
- "What database do we use?"
- "How do I run the test suite?"
- "Where are environment variables documented?"
- "What version of Node.js do we use?"
- "How is error logging handled?"
- "What's our code review process?"

#### **Ambiguous/Partial Coverage (4-6)**:

- "How do we handle secrets?" (partial docs exist)
- "What's the deployment rollback process?" (mentioned but not detailed)
- "How do I debug production issues?" (conceptual, not step-by-step)

#### **Intentionally Missing (4-6)** - _Gap Detection Triggers_:

- "How do we rotate API keys in production?" (not documented)
- "What's the disaster recovery plan?" (not documented)
- "How do I set up local SSL certificates?" (not documented)
- "What are our SLA commitments?" (not documented)

---

### Evaluation Metrics

| Metric                      | Definition                                               | Target (MVP)       |
| --------------------------- | -------------------------------------------------------- | ------------------ |
| **Citation Presence Rate**  | % of answerable responses with `[source]` citations      | > 95%              |
| **Citation Relevance**      | Manual spot-check: citation actually supports claim      | > 90% (10 samples) |
| **Answerability Coverage**  | % of answerable questions that get answer (not fallback) | > 80%              |
| **Gap Detection Precision** | % of gap-flagged questions that truly lack docs          | > 75%              |
| **Latency p50**             | Median query latency (including LLM call)                | < 4s               |
| **Latency p95**             | 95th percentile latency (free-tier variability accepted) | < 8s               |
| **False Positives**         | Answerable questions incorrectly flagged as gaps         | < 10%              |

---

### Evaluation Execution

1. **Setup**: Sync synthetic docs corpus (~10-15 markdown files with intentional gaps)
2. **Run**: Execute all 20-30 questions via API
3. **Measure**: Collect latency, confidence levels, citations, gap logs
4. **Manual Review**: Spot-check 10 answers for citation relevance
5. **Document**: Results table in `DESIGN_AND_TESTING.md`

**Deliverable**: Include evaluation results in testing document to demonstrate production thinking.

---

## 🎯 Success Metrics (Realistic Targets)

### Technical Targets (Measurable in Tests)

✅ **Latency**: p50 < 4s, p95 < 8s on free-tier hosting  
✅ **Citation Presence**: > 95% of answerable responses include `[source]` format  
✅ **Citation Relevance**: > 90% accuracy in manual spot-check (10 samples)  
✅ **Fallback Behavior**: Triggered on most out-of-scope/missing-topic queries  
✅ **No Uncited Claims**: Manual review finds zero unsupported factual claims in eval set  
✅ **Sync Reliability**: Ingestion completes successfully on demo corpus  
✅ **Gap Detection**: Repeated queries increment frequency counter correctly

### Product Targets (Demo-Verifiable)

✅ User can complete 3 onboarding questions with cited answers  
✅ Missing-topic query appears in Gap Radar within 1 request cycle  
✅ Gap frequency increments when same question asked twice  
✅ Sources page displays indexed files with metadata  
✅ Sync button updates timestamp and chunk count

### Capstone Rubric Targets

✅ **Project Score**: 4-5/5 (functional, polished, innovative)  
✅ **Presentation Score**: 4-5/5 (clear, confident, comprehensive)  
✅ **Overall**: 8-10/10 passing score

**Anti-Goal**: Do NOT claim "zero hallucinations" or "perfect accuracy" - these are unmeasurable guarantees.  
**Better Claim**: "Reduces unsupported answers via citation grounding, fallback gating, and evaluation-driven tuning."

---

## 💰 Cost Analysis

### Development Phase (3.5 months)

#### **AI Costs (FREE Stack)**:

**Embeddings** (HuggingFace all-MiniLM-L6-v2):

- Cost: $0 (runs locally on CPU)
- First-time model download: ~90MB (one-time, then offline)
- Unlimited usage: No API calls, no rate limits
- Quality: ~97% of OpenAI text-embedding-3-small

**LLM Calls** (Groq Llama-3-8b-instant):

- Cost: $0 (free tier: 14,400 requests/day)
- Development testing: ~10-20 queries/day
- Usage: <1% of free tier limit
- Speed: Extremely fast inference (great for demos)

**Total AI costs for 3.5 months**: $0

**Rationale**: Academic capstone project, not commercial product. Shows cost-conscious engineering decision-making (positive for rubric evaluation).

#### **Infrastructure**:

- **Vercel** (frontend): Free tier (no cost)
- **Render** (backend): Free tier (sleeps after inactivity, acceptable for demo)
- **Neon Postgres**: Free tier (1 database, 0.5 GB storage)
- **Chroma**: Local file-based (no cost)

**Total Monthly Cost**: **$0.60-1.00**  
**Total Capstone Cost**: **$2-4**

---

### Production Simulation Costs

If you want to simulate moderate usage for demo:

- 100 queries for demo prep: ~$0.12
- 10 re-syncs: negligible
- Total extra: ~$0.15

**Grand Total**: **$0 for entire capstone** ✅

**Cost-Conscious Engineering**: Chose FREE stack (HuggingFace + Groq) over paid alternatives because this is an academic project, not a commercial product. This decision demonstrates engineering maturity in selecting appropriate technologies based on project context.

---

### Cost Protection Strategies

1. **No API costs**: Local embeddings + Groq free tier = $0
2. **Groq rate limits**: 14,400/day free tier >> project needs (~10-20/day)
3. **Unlimited embeddings**: Local CPU processing, no API calls
4. **Zero risk**: Cannot exceed budget that doesn't exist

---

## 🔗 Related Documentation

- [Project Overview](../planning/PROJECT_OVERVIEW.md) - Problem and solution
- [MVP Features](../planning/MVP_FEATURES.md) - What to build and test
- [Implementation Details](../technical/IMPLEMENTATION_DETAILS.md) - How to implement and test
- [Interview Prep](../delivery/INTERVIEW_PREP.md) - How to talk about the project
