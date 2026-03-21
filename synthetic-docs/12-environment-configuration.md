# Environment Configuration

## Overview

Proper environment configuration is critical for development, testing, and production deployments. This guide covers environment variables, configuration management, and environment-specific settings.

## Environment Files

### Development (.env)

Create `backend/.env` for local development:

```bash
# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=debug

# API Keys (FREE tier)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Database
DATABASE_URL=postgresql://appuser:password@localhost:5432/engineering_copilot_dev
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# Vector Database
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=documents

# Security
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60  # seconds

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
RETRIEVAL_TOP_K=5
CONFIDENCE_THRESHOLD=0.7

# LLM Configuration
LLM_MODEL=llama-3-8b-instant
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=500
```

### Frontend (.env.local)

Create `frontend/.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# Application
NEXT_PUBLIC_APP_NAME=Engineering Onboarding Copilot
NEXT_PUBLIC_APP_VERSION=1.0.0

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_GAP_RADAR=true

# Development
NEXT_PUBLIC_DEBUG=true
```

### Template Files (.env.example)

**CRITICAL**: Never commit `.env` to Git!

Instead, provide `.env.example` (without real values):

```bash
# Application
APP_ENV=development
DEBUG=true

# API Keys (sign up at console.groq.com)
GROQ_API_KEY=your_groq_api_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security (generate with: openssl rand -hex 32)
JWT_SECRET=your_jwt_secret_here
```

## Environment-Specific Configuration

### Development

- **Purpose**: Local development on your machine
- **Database**: Local PostgreSQL
- **Debug mode**: Enabled
- **Hot reload**: Enabled
- **CORS**: Allow localhost
- **Rate limiting**: Relaxed

### Staging

- **Purpose**: Pre-production testing
- **Database**: Staging database (separate from production)
- **Debug mode**: Disabled
- **HTTPS**: Required
- **CORS**: Only staging domain
- **Rate limiting**: Production-like

### Production

- **Purpose**: Live user-facing application
- **Database**: Production database with backups
- **Debug mode**: Disabled
- **HTTPS**: Required (enforced)
- **CORS**: Only production domain
- **Rate limiting**: Strict
- **Monitoring**: All metrics enabled
- **Secrets**: Managed by cloud provider

## Loading Environment Variables

### Python (FastAPI)

```python
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_env: str = "development"
    debug: bool = False
    log_level: str = "info"

    # API Keys
    groq_api_key: str

    # Database
    database_url: str
    db_pool_size: int = 5

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl: int = 3600

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    # RAG
    chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_top_k: int = 5
    confidence_threshold: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Usage
settings = get_settings()
print(f"Running in {settings.app_env} mode")
```

### Next.js (TypeScript)

```typescript
// lib/config.ts
interface Config {
  apiUrl: string;
  apiTimeout: number;
  appName: string;
  enableAnalytics: boolean;
}

export const config: Config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  apiTimeout: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || "30000"),
  appName: process.env.NEXT_PUBLIC_APP_NAME || "Engineering Copilot",
  enableAnalytics: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === "true",
};

// Validate required env vars at build time
if (!process.env.NEXT_PUBLIC_API_URL && process.env.NODE_ENV === "production") {
  throw new Error("NEXT_PUBLIC_API_URL must be set in production");
}
```

## Secrets Management

### Development

Store secrets in `.env` file (gitignored):

```bash
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

### Production

Use cloud provider secret managers:

**AWS Secrets Manager**:

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secrets = get_secret('prod/engineering-copilot/app')
groq_api_key = secrets['GROQ_API_KEY']
```

**Google Cloud Secret Manager**:

```python
from google.cloud import secretmanager

def get_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')
```

**Environment Variables (Docker/Kubernetes)**:

```yaml
# kubernetes-deployment.yaml
env:
  - name: GROQ_API_KEY
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: groq-api-key
```

## Configuration Validation

### Startup Checks

Validate configuration on application startup:

```python
from typing import List

def validate_config(settings: Settings) -> List[str]:
    """Validate configuration and return list of errors."""
    errors = []

    # Check required secrets
    if not settings.groq_api_key:
        errors.append("GROQ_API_KEY is required")

    if not settings.jwt_secret or len(settings.jwt_secret) < 32:
        errors.append("JWT_SECRET must be at least 32 characters")

    # Validate URLs
    if not settings.database_url.startswith(('postgresql://', 'postgres://')):
        errors.append("DATABASE_URL must be a PostgreSQL connection string")

    # Validate numeric ranges
    if settings.chunk_size < 100 or settings.chunk_size > 2000:
        errors.append("CHUNK_SIZE must be between 100 and 2000")

    if not 0 <= settings.confidence_threshold <= 1:
        errors.append("CONFIDENCE_THRESHOLD must be between 0 and 1")

    # Environment-specific checks
    if settings.app_env == "production":
        if settings.debug:
            errors.append("DEBUG must be False in production")
        if "localhost" in settings.database_url:
            errors.append("Cannot use localhost database in production")

    return errors

# On startup
errors = validate_config(settings)
if errors:
    for error in errors:
        logger.error(f"Configuration error: {error}")
    raise ValueError("Invalid configuration")
```

## Docker Configuration

### Multi-Stage Build with Env

```dockerfile
# Dockerfile
FROM python:3.11-slim as base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment defaults (override with -e or docker-compose)
ENV APP_ENV=production
ENV DEBUG=false
ENV LOG_LEVEL=info

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=development
      - DEBUG=true
      - DATABASE_URL=postgresql://postgres:password@db:5432/engineering_copilot
      - REDIS_URL=redis://redis:6379/0
      - GROQ_API_KEY=${GROQ_API_KEY}
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=engineering_copilot
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## Environment Detection

```python
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"

def get_environment() -> Environment:
    """Detect current environment."""
    env = os.getenv("APP_ENV", "development").lower()
    try:
        return Environment(env)
    except ValueError:
        logger.warning(f"Unknown environment '{env}', defaulting to development")
        return Environment.DEVELOPMENT

def is_production() -> bool:
    """Check if running in production."""
    return get_environment() == Environment.PRODUCTION

def is_development() -> bool:
    """Check if running in development."""
    return get_environment() == Environment.DEVELOPMENT

# Usage
if is_production():
    # Enable strict security settings
    app.add_middleware(HTTPSRedirectMiddleware)
    ALLOWED_HOSTS = ["yourdomain.com"]
else:
    # Development settings
    ALLOWED_HOSTS = ["*"]
```

## Configuration Best Practices

### Security

1. **Never commit secrets** - Use .gitignore for .env files
2. **Use strong secrets** - Generate with `openssl rand -hex 32`
3. **Rotate secrets regularly** - Especially after team member departure
4. **Use different secrets per environment** - Never reuse prod secrets in dev
5. **Limit access** - Only give secrets to who needs them

### Organization

1. **Group related vars** - Database, Security, RAG, etc.
2. **Use prefixes** - `DB_`, `REDIS_`, `LLM_` for clarity
3. **Document in .env.example** - Explain what each var does
4. **Validate on startup** - Fail fast with clear error messages
5. **Use defaults wisely** - Good defaults for dev, require explicit prod config

### Naming Conventions

```bash
# ✅ Good
DATABASE_URL
JWT_SECRET
GROQ_API_KEY
CHUNK_SIZE

# ❌ Bad
db
secret
key
size
```

## Troubleshooting

### Environment Variable Not Loading

```bash
# Check if file exists
ls -la .env

# Check file permissions
chmod 600 .env

# Verify loading in code
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GROQ_API_KEY'))"
```

### Docker Not Picking Up Changes

```bash
# Rebuild without cache
docker-compose build --no-cache

# Or
docker build --no-cache -t myapp .
```

### Wrong Environment Loaded

```python
# Debug which .env file is loaded
from dotenv import load_dotenv, find_dotenv

env_file = find_dotenv()
print(f"Loading environment from: {env_file}")
load_dotenv(env_file, verbose=True)
```

## Resources

- [12-Factor App: Config](https://12factor.net/config)
- [Python dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
