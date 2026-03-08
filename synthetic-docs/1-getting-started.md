# Getting Started

Welcome to the engineering team! This guide will help you set up your development environment and understand our workflow.

## Prerequisites

Before you begin, ensure you have the following installed:

- **macOS or Linux** (Windows WSL2 also supported)
- **Python 3.11+** for backend development
- **Node.js 18+** for frontend development
- **Git** for version control
- **Docker Desktop** (optional, for local database testing)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/company/engineering-platform.git
cd engineering-platform
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Environment Configuration

Copy the example environment files and fill in your local values:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

Ask your team lead for the development API keys and database credentials.

### 5. Run the Application

**Start Backend** (in backend/ directory):

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

**Start Frontend** (in frontend/ directory):

```bash
npm run dev
```

The web app will be available at `http://localhost:3000`

## Verify Your Setup

1. Open `http://localhost:3000` in your browser
2. You should see the dashboard homepage
3. Try creating a test user account
4. Check that API requests are working in the browser console

## Next Steps

- Read the [Architecture Overview](./2-architecture-overview.md)
- Review our [Testing Guide](./3-testing-guide.md)
- Understand the [Deployment Process](./4-deployment.md)
- Browse the [API Reference](./5-api-reference.md)

## Getting Help

- **Slack**: #engineering-help channel
- **Team Lead**: Sarah Johnson (@sarah.johnson)
- **Documentation Issues**: File a ticket in Jira under "DOCS" project
