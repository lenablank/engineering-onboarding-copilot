# Engineering Onboarding Copilot - Project Overview

**RAG-powered internal knowledge assistant with Documentation Gap Radar**  
**Solo Capstone Project**

---

## 📋 One-Sentence Pitch

A web-based onboarding assistant that syncs engineering docs from a GitHub repository, answers new-engineer questions with cited evidence, and logs low-evidence queries as documentation gaps to improve documentation over time.

---

## ❌ Problem Statement

New engineers waste hours asking teammates basic onboarding questions ("How do I run tests?", "Where's auth implemented?", "What's our deployment process?"). Existing docs are fragmented, outdated, or undiscoverable. Teams don't know which documentation gaps exist until someone asks.

---

## ✅ Solution

An AI-powered onboarding assistant that:

- Syncs engineering docs from a GitHub repository (manual trigger in MVP, no manual file uploads)
- Answers questions with source citations and evidence-based fallback behavior when documentation support is insufficient
- Detects and logs documentation gaps (improves knowledge base over time)
- Provides transparency (shows retrieved chunks, confidence levels)

**MVP Scope Note**: The capstone MVP targets a configured repository/path with manual sync trigger (no GitHub OAuth or scheduled sync).

---

## 💡 Why This Is Strong

✅ **RAG at its core** (strong Berlin AI market alignment)  
✅ **Internal tool expertise** (what employers want to see)  
✅ **Clear differentiator** (Gap Radar is unique)  
✅ **Production-conscious thinking** (evidence-based gating, evaluation, citation grounding)  
✅ **Solo-friendly scope** (MVP realistic for 12 weeks implementation + Sprint 0 planning)  
✅ **Impressive demos** (live Q&A with citations, gap detection in action)

---

## 🎯 Project Goals

### Technical Goals

- Implement production-conscious RAG pipeline with confidence gating
- Build evidence-based fallback system to reduce unsupported answers
- Create automated documentation gap detection and tracking
- Deploy fully functional web application with CI/CD

### Learning Goals

- Master RAG implementation patterns (chunking, embedding, retrieval, generation)
- Gain experience with vector databases and semantic search
- Understand LLM orchestration and prompt engineering
- Learn production AI system evaluation and metrics

### Career Goals

- Build portfolio project aligned with Berlin AI job market
- Demonstrate internal tools engineering expertise
- Show production thinking and systematic evaluation approach
- Create compelling demo for interviews

---

## 📚 Related Documentation

- [Capstone Requirements & Rubric](CAPSTONE_REQUIREMENTS.md) - Quantic deliverables and scoring
- [MVP Features](MVP_FEATURES.md) - Feature list, scope, and acceptance criteria
- [System Architecture](SYSTEM_ARCHITECTURE.md) - Technical architecture and design
- [Implementation Details](IMPLEMENTATION_DETAILS.md) - RAG pipeline, testing, deployment
- [Evaluation & Demo](EVALUATION_AND_DEMO.md) - Demo plan, evaluation metrics
- [Sprint Plan](SPRINT_PLAN.md) - Sprint breakdown and timeline
- [Repository Structure](REPOSITORY_STRUCTURE.md) - Project organization
- [Interview Prep](INTERVIEW_PREP.md) - Talking points and learning outcomes
