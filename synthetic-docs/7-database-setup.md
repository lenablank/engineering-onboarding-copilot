# Database Setup Guide

## Overview

We use **PostgreSQL 15** as our primary database, with Redis for caching. This guide covers local setup, schema management, and common operations.

## Local Development Setup

### Installing PostgreSQL

**macOS** (using Homebrew):

```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian**:

```bash
sudo apt-get update
sudo apt-get install postgresql-15 postgresql-contrib
```

**Windows**:
Download installer from https://www.postgresql.org/download/windows/

### Creating the Development Database

```bash
# Create database user
createuser -P appuser
# Enter password when prompted

# Create database
createdb -O appuser engineering_copilot_dev

# Verify connection
psql -U appuser -d engineering_copilot_dev -h localhost
```

### Environment Configuration

Add to your `.env` file:

```bash
DATABASE_URL=postgresql://appuser:password@localhost:5432/engineering_copilot_dev
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

## Schema Management

### Running Migrations

We use **Alembic** for database migrations:

```bash
# Install Alembic
pip install alembic

# Run all pending migrations
alembic upgrade head

# Check current migration version
alembic current

# View migration history
alembic history
```

### Creating New Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add user preferences table"

# Create empty migration (for data migrations)
alembic revision -m "Backfill user data"

# Edit the generated file in alembic/versions/
```

## Core Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### Documents Table

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    file_path VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding_id VARCHAR(255),
    sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path)
);

CREATE INDEX idx_documents_path ON documents(file_path);
CREATE INDEX idx_documents_metadata ON documents USING GIN (metadata);
```

### Query Logs Table

```sql
CREATE TABLE query_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT,
    sources JSONB,
    confidence_score DECIMAL(3,2),
    latency_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_query_logs_user ON query_logs(user_id);
CREATE INDEX idx_query_logs_timestamp ON query_logs(timestamp);
```

## Redis Setup

### Installing Redis

**macOS**:

```bash
brew install redis
brew services start redis
```

**Ubuntu**:

```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### Redis Configuration

```bash
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600  # 1 hour
```

### Cache Keys Convention

```
cache:embeddings:{file_hash}
cache:query:{question_hash}
session:{user_id}
```

## Common Database Operations

### Backup and Restore

**Create backup**:

```bash
pg_dump -U appuser engineering_copilot_dev > backup.sql
```

**Restore from backup**:

```bash
psql -U appuser engineering_copilot_dev < backup.sql
```

### Database Reset (Development Only)

```bash
# WARNING: Destroys all data!
dropdb engineering_copilot_dev
createdb -O appuser engineering_copilot_dev
alembic upgrade head
```

### Useful SQL Queries

**Check table sizes**:

```sql
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;
```

**Check query performance**:

```sql
SELECT * FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

## Performance Optimization

### Connection Pooling

Use PgBouncer for connection pooling in production:

```bash
# Install PgBouncer
brew install pgbouncer

# Configure max connections
max_connections = 100
default_pool_size = 20
```

### Index Maintenance

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM documents WHERE file_path LIKE '%README%';

-- Rebuild indexes
REINDEX TABLE documents;

-- Update statistics
ANALYZE documents;
```

### Query Optimization Tips

1. Use `EXPLAIN ANALYZE` to debug slow queries
2. Add indexes for frequently filtered columns
3. Avoid `SELECT *` in production code
4. Use pagination for large result sets
5. Monitor connection pool usage

## Troubleshooting

### Connection Issues

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# View PostgreSQL logs
tail -f /usr/local/var/log/postgresql@15.log

# Test connection
psql -U appuser -d engineering_copilot_dev -h localhost
```

### Migration Conflicts

```bash
# Check for conflicts
alembic current

# Rollback one migration
alembic downgrade -1

# Force migration version
alembic stamp head
```

## Production Considerations

- Use managed services (AWS RDS, Google Cloud SQL)
- Enable automated backups (daily minimum)
- Set up replication for high availability
- Monitor query performance with pg_stat_statements
- Implement regular VACUUM operations
- Use connection pooling (PgBouncer)
