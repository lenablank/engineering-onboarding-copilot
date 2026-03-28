# Quantic Capstone Requirements & Rubric Alignment

This document outlines all Quantic capstone requirements and how this project meets them.

---

## 🎓 Required Submission Components (Non-Negotiable)

These 5 deliverables are explicitly required by the handbook:

| Required Deliverable              | Implementation                           | Evidence Location                          |
| --------------------------------- | ---------------------------------------- | ------------------------------------------ |
| **1. GitHub repository (shared)** | Monorepo with documented code            | Shared with `quantic-grader`               |
| **2. Deployed web application**   | Vercel (frontend) + Render (backend)     | Live URL in `CAPSTONE_SUBMISSION_LINKS.md` |
| **3. Agile task board**           | Trello with all sprints visible          | Link in `README.md` and submission doc     |
| **4. Design & testing document**  | Architecture, patterns, rationale, tests | `DESIGN_AND_TESTING.md`                    |
| **5. Demo video (15-20 min)**     | Walkthrough with ID shown, face visible  | Video link in submission doc               |

---

## 📊 Rubric-Critical Evidence (Needed for High Scores)

These elements are assessed via the rubric scoring (3-5 range):

| Rubric Criteria                       | Implementation                           | Evidence Location                        |
| ------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| **3+ sprints with agile methodology** | Sprint 1/2/3 with goals, reviews, retros | Sprint artifacts in `/docs/sprints/`     |
| **CI/CD tools & methodology**         | GitHub Actions (test, lint, build)       | `.github/workflows/ci.yml`               |
| **Well-designed code**                | Patterns, service layers, clean arch     | Code structure + `DESIGN_AND_TESTING.md` |
| **Well-tested code**                  | Unit, integration, E2E, regression set   | Test files + coverage reports            |
| **Appropriate documentation**         | Code comments, README, design doc        | All `.md` files, docstrings              |
| **Solo project camera presence**      | Only you visible and speaking            | Demo video (full 15-20 min)              |

---

## ⭐ Score-Boosting Initiative (Differentiators for 4-5 Range)

These go "above and beyond minimum requirements":

- ⭐ **Documentation Gap Radar** (unique differentiator, not just basic RAG)
- ⭐ **Evidence-based confidence gating** (production-grade fallback logic)
- ⭐ **Systematic evaluation methodology** (20-30 question regression set with metrics)
- ⭐ **Security & AI safety controls** (prompt injection resistance, audit logging)
- ⭐ **Observability** (query logs, latency tracking, citation rate monitoring)
- ⭐ **Cost optimization** ($3-5 total for entire capstone via free tiers)

---

## 🎯 Scoring Strategy

**Target: 8-10/10 Overall Score**

_Note: "8-10/10" is shorthand for the combined outcome of Quantic's two rubrics (Project score 0-5 + Presentation score 0-5 = Total 0-10). Target is 4-5 on Project + 4-5 on Presentation._

**Priority Sequencing:**

1. **First priority**: Deliver all 5 required submission components (repo, deployed app, Trello, design/testing doc, demo video)
2. **Second priority**: Rubric-critical evidence (3+ sprints with agile artifacts, stable deployed demo, CI/CD, comprehensive testing)
3. **Third priority**: Differentiators that show initiative (Gap Radar, evaluation metrics, AI safety controls)

**Formula**: Required components + Rubric-critical evidence + 2-3 strong differentiators = 8-10/10

---

## 🛡️ Minimum Passing Submission Mode (Fallback for 6-7/10)

**If behind schedule by end of Sprint 2**, freeze "nice-to-have" features and prioritize absolute minimum for passing:

### Core Must-Haves:

- ✅ Deployed app with Ask/Sources/Gaps pages functional
- ✅ RAG Q&A with citations working
- ✅ Evidence-based fallback behavior (gating low-confidence queries)
- ✅ Gap logging functional (dashboard shows logged gaps)
- ✅ 3 sprints evidenced with agile artifacts (goals, reviews, retros)
- ✅ Basic tests + CI/CD passing
- ✅ DESIGN_AND_TESTING.md complete (all required sections)
- ✅ Clean 15-20 min demo video (ID shown, face visible, all requirements)
- ✅ Repo shared with `quantic-grader`

### De-Prioritized (If Time Runs Out):

- ⚠️ Advanced metrics dashboard (CSV export acceptable)
- ⚠️ Rate limiting (document as future improvement)
- ⚠️ Ingestion blocklist patterns (document security controls implemented)
- ⚠️ UI polish beyond functional (focus on working > beautiful)

**This fallback ensures passing even if timeline slips. It does NOT weaken your ambition—it makes your plan robust.**

---

## 🚨 MVP Escape Hatch (Sprint 2 Checkpoint)

**End of Sprint 2 Status Check:**

If any of these are NOT complete:

- Working Q&A with citations
- Confidence gating + fallback
- Gap Radar dashboard functional
- Sources page working
- 70%+ test coverage
- Deployment URLs live

**Then**: Immediately freeze Feature 6 (advanced observability) and Feature 9 (nice-to-have security controls) and focus only on core demo readiness + documentation completion.

**Goal**: Ensure stable deployed demo > attempting all differentiators.

---

## ✅ Capstone Submission Checklist

### Code & Repository

- [ ] GitHub repo shared with `quantic-grader`
- [ ] Clean README with setup instructions
- [ ] DESIGN_AND_TESTING.md includes architecture + testing + rationale + deployment options
- [ ] All code committed and pushed
- [ ] `.gitignore` properly configured (no API keys)
- [ ] AI_TOOLING_AND_ATTRIBUTION.md documents AI usage and attributions

### Deployment

- [ ] Frontend deployed to Vercel (live URL)
- [ ] Backend deployed to Render (live URL)
- [ ] App reachable via stable public URLs; free-tier cold starts and temporary sleep are acceptable and documented
- [ ] Database on Neon (connected)
- [ ] All environment variables configured
- [ ] Health check endpoint working

### Documentation

- [ ] Design/testing document created
- [ ] Architecture diagrams included
- [ ] API documentation (endpoints, schemas)
- [ ] Test coverage report
- [ ] Demo script prepared

### Demo Video (15-20 min)

- [ ] You visible on camera throughout (per rubric requirement)
- [ ] _Solo project note: "All members visible and speaking" requirement is satisfied by single presenter being visible and speaking throughout_
- [ ] Government-issued ID shown clearly at beginning
- [ ] Live application walkthrough
- [ ] Successful Q&A demonstration
- [ ] Gap detection demonstration
- [ ] Technical architecture explanation
- [ ] Business value articulation
- [ ] Q&A time included
- [ ] Video uploaded and link shared

### Trello Board

- [ ] All user stories created
- [ ] Sprint 1/2/3 clearly organized
- [ ] Acceptance criteria visible
- [ ] Progress tracked and updated
- [ ] Link shared in README.md

### Agile Artifacts

- [ ] Sprint goals documented for each sprint
- [ ] Sprint reviews completed (written acceptance notes, no video needed for solo)
- [ ] Sprint retrospectives documented
- [ ] Artifacts stored in `/docs/sprints/sprint-{N}/`

---

## 📋 Agile Process Note (Solo Project)

Even as a solo developer, maintain formal Scrum structure to align with Quantic requirements:

**Roles** (all you):

- **Product Owner**: Define requirements, prioritize backlog, accept user stories
- **Scrum Master**: Facilitate process, remove blockers, track progress
- **Developer**: Implement features, write tests, deploy

**Sprint Artifacts** (create for each sprint):

- Sprint Goal (one-sentence objective)
- Sprint Backlog (user stories with acceptance criteria)
- Sprint Review notes (written acceptance decisions, no video recording needed)
- Sprint Retrospective notes (what went well, what to improve)

**Note**: Only ONE demo video is required - the final 15-20 minute capstone presentation at project completion. Sprint reviews for solo projects are just written documentation.

**Deliverables Location**: Store in `/docs/sprints/sprint-{N}/` with:

- `sprint-goal.md`
- `sprint-backlog.md` (or Trello export)
- `sprint-review.md`
- `sprint-retro.md`

---

## 🔗 Related Documentation

- [Project Overview](PROJECT_OVERVIEW.md) - Problem, solution, why this project
- [MVP Features](MVP_FEATURES.md) - Feature list and acceptance criteria
- [Sprint Plan](SPRINT_PLAN.md) - Detailed sprint breakdown
- [Repository Structure](REPOSITORY_STRUCTURE.md) - File organization
