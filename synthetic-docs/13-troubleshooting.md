# Troubleshooting Guide

## Common Issues and Solutions

This guide covers frequently encountered problems and their solutions. Check here first before asking for help!

## Application Won't Start

### Error: "Port already in use"

**Symptom**:

```
Error: listen EADDRINUSE: address already in use :::8000
```

**Solution**:

```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)

# Or use a different port
uvicorn app.main:app --port 8001
```

### Error: "Module not found"

**Symptom**:

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:

```bash
# Verify you're in virtual environment
which python  # Should show venv path

# If not, activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "Database connection failed"

**Symptom**:

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**:

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql  # macOS
systemctl status postgresql           # Linux

# Start PostgreSQL if stopped
brew services start postgresql@15

# Verify connection
psql -U appuser -d engineering_copilot_dev -h localhost

# Check DATABASE_URL in .env
cat backend/.env | grep DATABASE_URL
```

## API Errors

### 401 Unauthorized

**Cause**: Missing or invalid authentication token

**Solution**:

```python
# Verify JWT secret is set
echo $JWT_SECRET

# Check token expiration
# Tokens expire after 24 hours by default

# Generate new token by logging in again
```

### 422 Unprocessable Entity

**Cause**: Invalid request body or query parameters

**Common issues**:

- Missing required fields
- Wrong field types
- Field validation failed

**Solution**:

```bash
# Check API documentation for required fields
curl -X POST http://localhost:8000/docs

# Validate your JSON
echo '{"question": "test"}' | jq .

# Check FastAPI automatic docs
# Open http://localhost:8000/docs in browser
```

### 500 Internal Server Error

**Cause**: Server-side error

**Debugging steps**:

```bash
# Check server logs
tail -f backend/logs/app.log

# Or run with debug logging
LOG_LEVEL=debug uvicorn app.main:app

# Check for exceptions in terminal output
```

### 503 Service Unavailable

**Cause**: External dependency unavailable (database, Redis, Groq API)

**Check services**:

```bash
# Health check endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "checks": {
    "database": true,
    "vector_db": true,
    "llm_api": true
  }
}
```

## RAG Pipeline Issues

### Low Quality Answers

**Symptoms**:

- Answers don't match question
- Wrong information provided
- Irrelevant citations

**Debugging**:

```python
# Check retrieval results
GET /debug/retrieve?question=how+do+i+deploy

# Inspect similarity scores
# Should be > 0.7 for good matches

# Check if documents are indexed
GET /documents/stats
```

**Solutions**:

1. **Re-sync documents**: Embeddings may be stale
2. **Adjust chunk size**: Try 300-700 characters
3. **Improve question phrasing**: Be more specific
4. **Check document quality**: Is information actually in docs?

### "I cannot answer confidently" Responses

**Cause**: Low confidence score or insufficient documentation

**Check**:

```bash
# View confidence threshold
echo $CONFIDENCE_THRESHOLD  # Default: 0.7

# Check what was retrieved
# Look at similarity_scores in response

# If scores < 0.7, either:
# - Question is out of scope
# - Documentation gap exists
# - Embeddings need refresh
```

**Solutions**:

```bash
# Lower threshold temporarily (testing only)
export CONFIDENCE_THRESHOLD=0.6

# Or improve documentation coverage
# Add docs for that topic and re-sync
```

### Slow Response Times

**Symptoms**:

- Queries take > 5 seconds
- Timeout errors

**Diagnostics**:

```bash
# Check component latencies
curl http://localhost:8000/metrics

# Expected breakdown:
# - Embedding: < 100ms
# - Retrieval: < 200ms
# - LLM generation: 1-3s
# - Total: < 3.5s
```

**Solutions**:

1. **Check Groq API status**:

   ```bash
   curl https://status.groq.com
   ```

2. **Reduce chunk count**:

   ```bash
   export RETRIEVAL_TOP_K=3  # Default: 5
   ```

3. **Optimize database**:

   ```sql
   ANALYZE documents;
   REINDEX TABLE documents;
   ```

4. **Enable caching**:
   ```python
   # Check if Redis is running
   redis-cli ping  # Should return "PONG"
   ```

## Frontend Issues

### "Network Error" or "Failed to fetch"

**Cause**: Frontend can't reach backend API

**Check**:

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS configuration
# Frontend URL must be in ALLOWED_ORIGINS
grep ALLOWED_ORIGINS backend/.env

# Check frontend API URL
grep NEXT_PUBLIC_API_URL frontend/.env.local
```

**Solution**:

```bash
# backend/.env
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Page Won't Load / White Screen

**Check browser console**:

- Open DevTools (F12 or Cmd+Option+I)
- Look for JavaScript errors
- Check Network tab for failed requests

**Common fixes**:

```bash
# Clear Next.js cache
rm -rf frontend/.next

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

### CSS Not Loading / Styles Broken

**For Tailwind CSS**:

```bash
# Rebuild Tailwind
npm run build:css

# Check tailwind.config.js exists
ls frontend/tailwind.config.js

# Verify import in root layout/page
# Should have: import './globals.css'
```

## Database Issues

### Migration Errors

**Error**: "Target database is not up to date"

**Solution**:

```bash
# Check current version
alembic current

# Check pending migrations
alembic history

# Run migrations
alembic upgrade head

# If stuck, reset (development only!)
alembic downgrade base
alembic upgrade head
```

### Connection Pool Exhausted

**Symptom**:

```
TimeoutError: QueuePool limit of size 5 overflow 10 reached
```

**Solution**:

```bash
# Increase pool size in .env
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Or find connection leaks in code
# Always use async with for database sessions
```

### Slow Queries

**Diagnostic**:

```sql
-- Find slow queries
SELECT * FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**Solutions**:

```sql
-- Add missing indexes
CREATE INDEX idx_query_logs_timestamp ON query_logs(timestamp);

-- Update statistics
ANALYZE query_logs;

-- Check query plan
EXPLAIN ANALYZE SELECT * FROM documents WHERE file_path = '...';
```

## Docker / Deployment Issues

### Container Exits Immediately

**Check logs**:

```bash
docker logs <container-id>

# Or for docker-compose
docker-compose logs api
```

**Common causes**:

- Environment variables not set
- Database not ready when app starts
- Port binding conflict

### "Cannot connect to database" in Docker

**Solution** - Add healthcheck:

```yaml
# docker-compose.yml
services:
  api:
    depends_on:
      db:
        condition: service_healthy

  db:
    healthcheck:
      test: ["CMD-PGSQL", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### Out of Memory

**Symptom**:

```
MemoryError: Unable to allocate array
```

**Solutions**:

```bash
# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory

# Or limit model size
# Use smaller embedding model

# Reduce batch size
export EMBEDDING_BATCH_SIZE=10
```

## Git Issues

### Merge Conflicts

**When rebasing**:

```bash
# Fix conflicts in files
# Look for <<<<<<< markers

# After fixing
git add <resolved-files>
git rebase --continue

# Or abort and try different approach
git rebase --abort
```

### Accidentally Committed Secrets

**URGENT - If pushed to remote**:

```bash
# 1. Rotate the secret immediately
# Generate new API key

# 2. Remove from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (if allowed)
git push origin --force --all

# 4. Notify team to re-clone repo
```

## Groq API Issues

### Rate Limit Exceeded

**Error**: "429 Too Many Requests"

**Free tier limits**:

- 14,400 requests/day
- ~10 requests/minute average

**Solutions**:

```bash
# Implement caching
# Cache answers for repeated questions

# Add rate limiting on your API
# Prevent users from spamming

# Reduce LLM calls
# Only call LLM when confidence > threshold
```

### API Key Invalid

**Error**: "401 Invalid API key"

**Check**:

```bash
# Verify key is set
echo $GROQ_API_KEY

# Key should start with "gsk_"
# If not, regenerate at console.groq.com

# Verify no extra spaces
export GROQ_API_KEY=$(echo $GROQ_API_KEY | tr -d ' \n')
```

## Performance Debugging

### Find Bottlenecks

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        print(f"{func.__name__}: {duration:.2f}ms")
        return result
    return wrapper

@timer
async def retrieve_chunks(question):
    # ...
    pass

@timer
async def generate_answer(question, context):
    # ...
    pass
```

### Memory Leaks

```bash
# Monitor memory usage
pip install memory-profiler

# Profile function
python -m memory_profiler script.py

# Check for unclosed connections, file handles
lsof -p $(pgrep -f uvicorn)
```

## Getting Help

### Before Asking

1. ✅ Check this troubleshooting guide
2. ✅ Search GitHub issues
3. ✅ Check application logs
4. ✅ Try to isolate the problem
5. ✅ Create minimal reproduction

### What to Include

When asking for help, provide:

- **Error message** (full traceback)
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment** (OS, Python/Node version)
- **Relevant logs**
- **What you've tried**

### Where to Ask

- **Team Slack**: #engineering-help
- **GitHub Issues**: For bugs
- **Documentation**: Check wiki first
- **1:1 Pairing**: For complex debugging

## Useful Commands

```bash
# Check all services status
docker-compose ps

# View logs from all containers
docker-compose logs -f

# Restart specific service
docker-compose restart api

# Check disk space
df -h

# Check memory
free -h

# Check running processes
ps aux | grep python

# Network diagnostics
ping google.com
curl -v http://localhost:8000/health

# Database quick check
psql -U appuser -d engineering_copilot_dev -c "SELECT COUNT(*) FROM documents;"
```
