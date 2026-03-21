# Performance Optimization

## Overview

This guide covers performance optimization strategies for the RAG pipeline, database queries, API responses, and frontend rendering.

## RAG Pipeline Optimization

### Embedding Generation

**Problem**: Slow embedding generation for large documents

**Solutions**:

1. **Batch Processing**:

```python
# ❌ Slow: One at a time
for chunk in chunks:
    embedding = embed_model.encode(chunk.text)

# ✅ Fast: Batch processing
embeddings = embed_model.encode([c.text for c in chunks], batch_size=32)
```

2. **Caching**:

```python
import hashlib
from functools import lru_cache

def get_chunk_hash(text: str) -> str:
    """Generate hash for chunk text."""
    return hashlib.md5(text.encode()).hexdigest()

@lru_cache(maxsize=1000)
def get_cached_embedding(chunk_hash: str):
    """Cache embeddings to avoid recomputation."""
    # Check Redis cache first
    cached = redis.get(f"embedding:{chunk_hash}")
    if cached:
        return pickle.loads(cached)

    # Generate if not cached
    embedding = generate_embedding(text)
    redis.setex(f"embedding:{chunk_hash}", 86400, pickle.dumps(embedding))
    return embedding
```

3. **Model Selection**:

```python
# Trade-off between quality and speed

# Faster (384 dimensions, good quality)
model = SentenceTransformer('all-MiniLM-L6-v2')  # 120ms

# Slower (768 dimensions, better quality)
model = SentenceTransformer('all-mpnet-base-v2')  # 250ms
```

### Vector Search Optimization

**Problem**: Slow similarity search in large vector databases

**Solutions**:

1. **Limit Search Space**:

```python
# ❌ Search all documents
results = vectorstore.similarity_search(query, k=5)

# ✅ Filter by metadata first
results = vectorstore.similarity_search(
    query,
    k=5,
    filter={"category": "deployment"}  # Reduce search space
)
```

2. **Index Configuration**:

```python
# Chroma with optimized index
collection = client.create_collection(
    name="documents",
    metadata={
        "hnsw:space": "cosine",
        "hnsw:construction_ef": 200,  # Higher = better recall, slower build
        "hnsw:search_ef": 100,        # Higher = better recall, slower search
        "hnsw:M": 16                  # Connections per layer
    }
)
```

3. **Approximate Search**:

```python
# Trade accuracy for speed
results = vectorstore.similarity_search(
    query,
    k=5,
    search_type="similarity",  # Fast approximate search
    # vs "mmr" (maximal marginal relevance) - slower but better diversity
)
```

### LLM Response Time

**Problem**: Slow answer generation

**Solutions**:

1. **Reduce Context Size**:

```python
# ❌ Send all chunks
context = "\n\n".join([chunk.text for chunk in retrieved_chunks])

# ✅ Truncate to token limit
max_context_tokens = 2000
context = truncate_to_tokens(retrieved_chunks, max_context_tokens)
```

2. **Streaming Responses**:

```python
from fastapi.responses import StreamingResponse

@app.post("/ask/stream")
async def ask_streaming(question: str):
    """Stream LLM response as it generates."""
    async def generate():
        async for token in llm.astream(question):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")
```

3. **Prompt Optimization**:

```python
# ❌ Verbose prompt
prompt = f"""You are a helpful assistant. Here is the context: {context}.
Now please answer the following question very carefully and provide
detailed explanation with examples: {question}"""

# ✅ Concise prompt
prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
```

## Database Optimization

### Query Performance

**Problem**: Slow database queries

**Solutions**:

1. **Add Indexes**:

```sql
-- Index frequently queried columns
CREATE INDEX idx_documents_file_path ON documents(file_path);
CREATE INDEX idx_query_logs_timestamp ON query_logs(timestamp DESC);
CREATE INDEX idx_query_logs_user_id ON query_logs(user_id);

-- Composite index for common query patterns
CREATE INDEX idx_logs_user_timestamp ON query_logs(user_id, timestamp DESC);

-- Index for JSON queries
CREATE INDEX idx_documents_metadata ON documents USING GIN (metadata);
```

2. **Query Optimization**:

```python
# ❌ N+1 query problem
users = session.query(User).all()
for user in users:
    questions = user.questions  # Separate query for each user

# ✅ Eager loading
from sqlalchemy.orm import joinedload

users = session.query(User).options(joinedload(User.questions)).all()
```

3. **Pagination**:

```python
# ❌ Load all results
results = session.query(QueryLog).all()

# ✅ Paginate
from fastapi import Query

@app.get("/logs")
async def get_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100)
):
    offset = (page - 1) * page_size
    results = session.query(QueryLog).offset(offset).limit(page_size).all()
    return results
```

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Optimized connection pool
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Concurrent connections
    max_overflow=20,        # Additional connections under load
    pool_timeout=30,        # Wait time for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connections before use
    poolclass=QueuePool
)
```

### Database Caching

```python
from functools import lru_cache
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_or_query(key: str, query_fn, ttl: int = 3600):
    """Get from cache or execute query."""
    # Check cache
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    # Execute query
    result = query_fn()

    # Cache result
    redis_client.setex(key, ttl, json.dumps(result))
    return result

# Usage
def get_document_stats():
    return get_cached_or_query(
        "stats:documents",
        lambda: session.query(Document).count(),
        ttl=300  # 5 minutes
    )
```

## API Performance

### Response Caching

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")

@app.get("/documents")
@cache(expire=300)  # Cache for 5 minutes
async def list_documents():
    return {"documents": get_all_documents()}
```

### Async Processing

```python
import asyncio

# ❌ Sequential (slow)
def process_documents(docs):
    for doc in docs:
        embed = generate_embedding(doc.text)
        store_in_db(embed)

# ✅ Concurrent (fast)
async def process_documents(docs):
    tasks = [process_single_doc(doc) for doc in docs]
    await asyncio.gather(*tasks)

async def process_single_doc(doc):
    embed = await generate_embedding_async(doc.text)
    await store_in_db_async(embed)
```

### Response Compression

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress > 1KB
```

## Frontend Optimization

### Code Splitting

```javascript
// ❌ Load everything upfront
import { AskPage } from "./components/AskPage";
import { GapsPage } from "./components/GapsPage";
import { SourcesPage } from "./components/SourcesPage";

// ✅ Lazy load components
const AskPage = lazy(() => import("./components/AskPage"));
const GapsPage = lazy(() => import("./components/GapsPage"));
const SourcesPage = lazy(() => import("./components/SourcesPage"));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/ask" element={<AskPage />} />
        <Route path="/gaps" element={<GapsPage />} />
        <Route path="/sources" element={<SourcesPage />} />
      </Routes>
    </Suspense>
  );
}
```

### API Client Optimization

```javascript
// Implement request deduplication
const requestCache = new Map();

async function cachedFetch(url, options = {}) {
  const key = `${url}-${JSON.stringify(options)}`;

  // Return in-flight request if exists
  if (requestCache.has(key)) {
    return requestCache.get(key);
  }

  // Make request
  const promise = fetch(url, options).finally(() => {
    // Clear after completion
    setTimeout(() => requestCache.delete(key), 1000);
  });

  requestCache.set(key, promise);
  return promise;
}
```

### Debouncing User Input

```javascript
import { useState, useEffect } from "react";

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage in search/question input
function AskQuestion() {
  const [input, setInput] = useState("");
  const debouncedInput = useDebounce(input, 500); // Wait 500ms

  useEffect(() => {
    if (debouncedInput) {
      fetchSuggestions(debouncedInput);
    }
  }, [debouncedInput]);
}
```

### Virtual Scrolling for Large Lists

```javascript
import { FixedSizeList } from "react-window";

function GapsList({ gaps }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={gaps.length}
      itemSize={100}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <GapItem gap={gaps[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}
```

## Monitoring Performance

### Backend Metrics

```python
from prometheus_client import Histogram
import time

# Track request duration
REQUEST_DURATION = Histogram(
    'request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

@app.middleware("http")
async def track_timing(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response
```

### Frontend Performance

```javascript
// Measure component render time
import { Profiler } from "react";

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime,
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);

  // Log to analytics
  analytics.track("component_render", {
    component: id,
    duration: actualDuration,
  });
}

<Profiler id="AskPage" onRender={onRenderCallback}>
  <AskPage />
</Profiler>;
```

## Performance Testing

### Load Testing

```bash
# Install Apache Bench
brew install apache-bench

# Test API endpoint
ab -n 1000 -c 10 -p question.json -T application/json \
  http://localhost:8000/ask

# Results show:
# - Requests per second
# - Mean response time
# - Percentiles (p50, p95, p99)
```

### Database Query Analysis

```sql
-- Enable query timing
\timing on

-- Analyze slow queries
EXPLAIN ANALYZE
SELECT * FROM documents
WHERE file_path LIKE '%README%';

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

## Performance Checklist

### Backend

- [ ] Database queries use appropriate indexes
- [ ] Connection pooling configured
- [ ] Expensive operations cached (Redis)
- [ ] Async/await used for I/O operations
- [ ] Batch processing for embeddings
- [ ] API responses cached where appropriate
- [ ] Rate limiting implemented
- [ ] Response compression enabled

### Frontend

- [ ] Code splitting implemented
- [ ] Images optimized and lazy loaded
- [ ] API calls debounced/throttled
- [ ] Virtual scrolling for long lists
- [ ] Bundle size optimized (<200KB gzipped)
- [ ] Unused dependencies removed

### RAG Pipeline

- [ ] Embedding caching implemented
- [ ] Vector database indexed properly
- [ ] Context size optimized
- [ ] Retrieval filtered by metadata
- [ ] Prompt templates concise

## Resources

- [FastAPI Performance Tips](https://fastapi.tiangolo.com/deployment/concepts/)
- [PostgreSQL Performance](https://www.postgresql.org/docs/current/performance-tips.html)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [Web.dev Performance](https://web.dev/performance/)
