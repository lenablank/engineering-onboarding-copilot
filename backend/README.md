# Backend - Engineering Onboarding Copilot

FastAPI backend for RAG-powered documentation assistant.

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Required environment variables:

```env
# Cohere API (for embeddings - FREE 1M calls/month)
COHERE_API_KEY=your_cohere_key_here

# Groq API (for LLM - FREE 14,400 requests/day)
GROQ_API_KEY=your_groq_key_here
```

Get API keys:
- Cohere: https://dashboard.cohere.com/api-keys (free tier)
- Groq: https://console.groq.com/keys (free tier)

### 4. Verify Setup (Sprint 0)

```bash
python prove_pipeline_simple.py
```

Expected output: `🎉 SUCCESS! Core RAG pipeline is functional!`

### 5. Run Development Server

```bash
uvicorn app.main:app --reload
```

API available at: http://localhost:8000

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── tests/                # Unit tests (Sprint 1+)
├── .env                  # Environment variables (gitignored)
├── .env.example          # Environment template
├── .gitignore
├── pyproject.toml        # Python project config
├── requirements.txt      # Dependencies
└── prove_pipeline_simple.py  # Sprint 0 proof script
```

## API Endpoints

### GET /

Returns API information

### GET /health

Health check endpoint

### POST /prove-pipeline

Sprint 0: Proves RAG pipeline is functional

- Loads synthetic docs
- Generates embeddings
- Tests retrieval

## Development

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy app/
```

### Testing (Sprint 1+)

```bash
pytest
```

## Sprint 0 Goals

- ✅ Backend environment setup
- ✅ Synthetic documentation (5 files)
- ✅ Proof-of-concept RAG pipeline
- ✅ FastAPI hello world endpoints

## Next: Sprint 1

- Full ingestion pipeline
- Q&A functionality
- Unit tests
- Frontend integration
