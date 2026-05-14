# Engineering Onboarding Copilot

**AI-powered documentation assistant with automated gap detection**

> A production RAG system that answers engineering questions with cited sources and identifies documentation gaps to improve knowledge bases over time.

🎥 **[Demo Video](https://drive.google.com/file/d/1ZO7LkoiAJLp1WnlxHjQv3U27Jh8xDndc/view?usp=sharing)** | 🔗 **[Live App](https://engineering-onboarding-copilot.vercel.app)** | 📋 **[Trello Board](https://trello.com/invite/b/69a427cee6ac597f2636cc22/ATTIc2511c7490ba36570a3a9b5a708ac4d17EFCD003/engineering-onboarding-copilot-msse-capstone)** | 📚 **[Documentation](docs/INDEX.md)**

---

## 🎯 What It Does

An intelligent documentation assistant that:

- **Answers questions** with source citations from your documentation
- **Confidence scoring** - shows when answers are reliable vs. uncertain
- **Gap detection** - automatically logs questions it can't answer confidently
- **Gap Radar dashboard** - prioritizes documentation improvements by frequency
- **Smart filtering** - distinguishes legitimate questions from spam/gibberish

Perfect for engineering teams onboarding new developers or maintaining internal wikis.

---

## ✨ Key Features

### Core Functionality
- ✅ **RAG-powered Q&A** - Semantic search over markdown documentation
- ✅ **Source citations** - Every answer links back to original docs
- ✅ **Confidence gating** - Clear fallback when evidence is insufficient
- ✅ **Gap Radar** - Track unanswered questions by frequency and confidence

### Engineering Quality
- ✅ **Production deployment** - Live on Vercel (frontend) + Render (backend)
- ✅ **Comprehensive testing** - 46 test functions, 1,374 lines of test code
- ✅ **Zero infrastructure cost** - Built entirely on free tiers
- ✅ **Type-safe** - TypeScript frontend, Python type hints in backend

---

## 🛠️ Technology Stack

| Layer | Technology | Why |
|-------|------------|-----|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS | Modern React framework, type safety, rapid styling |
| **Backend** | FastAPI, Python 3.11+ | Async performance, automatic OpenAPI docs |
| **Embeddings** | Cohere embed-english-v3.0 (1024-dim) | Free tier, high-quality semantic understanding |
| **LLM** | Groq Llama 3.1 8B | Free tier, extremely fast inference |
| **Vector DB** | ChromaDB | Persistent local storage, Python-native |
| **Database** | SQLite | Embedded, zero-config gap tracking |
| **Deployment** | Vercel + Render | Free tiers, automatic deployments |

**Total infrastructure cost:** $0

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Cohere API key](https://dashboard.cohere.com/api-keys) (free)
- [Groq API key](https://console.groq.com/keys) (free)

### Installation

1. **Clone and setup backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
# backend/.env
COHERE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

3. **Setup frontend**
```bash
cd ../frontend
npm install
```

4. **Run locally** (two terminals)
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
# → http://localhost:8000

# Terminal 2: Frontend  
cd frontend
npm run dev
# → http://localhost:3000
```

---

## 📖 How It Works

### RAG Pipeline

1. **Indexing**: Markdown files are chunked, embedded (Cohere 1024-dim), and stored in ChromaDB
2. **Retrieval**: User question is embedded and matched against docs using cosine similarity
3. **Confidence calculation**: Weighted score based on similarity, source diversity, and context sufficiency
4. **Generation**: If confidence ≥ 70%, Groq LLM generates answer with citations
5. **Fallback**: If confidence < 70%, returns clear message and logs to Gap Radar

### Gap Detection

Questions with confidence between 11-70% are analyzed:
- **Engineering-related** → Logged as documentation gap
- **Spam/gibberish** → Filtered out with different response

Gap Radar dashboard shows:
- Question text and confidence score
- Frequency (how many times asked)
- Status (NEW / REVIEWED / RESOLVED)
- Sortable by frequency to prioritize fixes

---

## 🏗️ Project Structure

```
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── main.py        # API entry point
│   │   ├── services/      # RAG pipeline, gap detection
│   │   ├── models/        # Database models
│   │   ├── routes/        # API endpoints
│   │   └── utils/         # Logging, helpers
│   └── tests/             # Pytest suite (46 test functions)
│
├── frontend/              # Next.js application
│   └── src/app/
│       ├── page.tsx       # Homepage with Ask interface
│       └── gaps/          # Gap Radar dashboard
│           └── page.tsx
│
├── synthetic-docs/        # Sample documentation corpus (15 MD files)
├── docs/                  # Project documentation
│   ├── technical/         # Architecture, implementation details
│   ├── planning/          # Project overview, features
│   ├── evaluation/        # Test results and evaluation
│   └── sprints/           # Development artifacts
│
└── DESIGN_AND_TESTING.md  # Comprehensive design document
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Submit question, get answer with citations |
| `/api/gaps/` | GET | List documentation gaps |
| `/api/gaps/{id}/status` | PATCH | Update gap status |
| `/api/gaps/{id}` | DELETE | Delete gap |
| `/api/gaps/stats` | GET | Gap statistics |
| `/health` | GET | Health check |

See [Implementation Details](docs/technical/IMPLEMENTATION_DETAILS.md) for complete API contracts.

---

## 📊 Evaluation Results

**Test Set:** 10 diverse questions (well-documented, edge cases, spam)  
**Accuracy:** 100% (10/10 correct behaviors)  
**Avg Response Time:** 1.4 seconds  
**Test Coverage:** 46 test functions across 5 test files

Full evaluation: [docs/evaluation/sprint-3-formal-evaluation.md](docs/evaluation/sprint-3-formal-evaluation.md)

---

## 📚 Documentation

- **[System Architecture](docs/technical/SYSTEM_ARCHITECTURE.md)** - Tech stack, data flows, design decisions
- **[Implementation Details](docs/technical/IMPLEMENTATION_DETAILS.md)** - Code patterns, API contracts, testing strategy
- **[Design & Testing](DESIGN_AND_TESTING.md)** - Comprehensive architecture and test documentation
- **[Repository Structure](docs/delivery/REPOSITORY_STRUCTURE.md)** - File organization guide

---

## 🎓 What I Learned

Building this project taught me:

1. **Confidence scoring is essential** - RAG systems need to know when they don't know
2. **Gap detection creates feedback loops** - Every "I don't know" becomes actionable data
3. **Free tiers are viable** - $0 infrastructure for a production-quality AI system
4. **Type safety matters** - TypeScript + Python type hints caught bugs early
5. **Testing RAG is hard** - Mocking LLM responses, evaluating semantic quality

---

## � Author

**Elena Blank**  
[GitHub](https://github.com/lenablank) | [LinkedIn](https://www.linkedin.com/in/elena-blank/)

---

**Built with ❤️ using free-tier AI services to demonstrate that production-quality RAG systems don't require expensive infrastructure.**
