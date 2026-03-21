# Monitoring and Observability

## Overview

Effective monitoring helps us detect issues before users notice them. This guide covers logging, metrics, tracing, and alerting strategies.

## Logging

### Structured Logging

Use structured logging for better parsing and querying:

```python
import structlog

logger = structlog.get_logger()

# Structured log entry
logger.info(
    "query_executed",
    user_id=user.id,
    question=question,
    latency_ms=latency,
    sources_count=len(sources),
    confidence=confidence_score
)
```

### Log Levels

Use appropriate log levels:

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General informational messages
- **WARNING**: Something unexpected but not critical
- **ERROR**: Error occurred but application continues
- **CRITICAL**: Serious error, application may crash

```python
logger.debug("Retrieving embeddings from vector database")
logger.info("User query processed successfully", user_id=123)
logger.warning("Low confidence in answer", confidence=0.4)
logger.error("Failed to connect to database", error=str(e))
logger.critical("Out of memory, shutting down", memory_used="98%")
```

### What to Log

**Always log**:

- API requests (method, path, status, latency)
- Database queries (query, duration)
- External API calls (service, endpoint, response time)
- Authentication events (login, logout, failures)
- Errors and exceptions

**Never log**:

- Passwords or API keys
- Credit card numbers
- Social security numbers
- Full user personal data

## Application Metrics

### Key Performance Indicators (KPIs)

Track these metrics for the RAG system:

**Query Metrics**:

- `query_count` - Total queries processed
- `query_latency_ms` - Time to answer (p50, p95, p99)
- `query_success_rate` - Percentage of successful responses
- `query_confidence_avg` - Average confidence score

**Retrieval Metrics**:

- `retrieval_latency_ms` - Time to retrieve relevant chunks
- `chunks_retrieved_avg` - Average number of chunks returned
- `similarity_score_avg` - Average similarity scores

**LLM Metrics**:

- `llm_call_count` - Number of LLM API calls
- `llm_latency_ms` - LLM response time
- `llm_token_usage` - Tokens consumed
- `llm_error_rate` - Failed LLM calls

**System Metrics**:

- `cpu_usage_percent` - CPU utilization
- `memory_usage_mb` - Memory consumption
- `disk_usage_gb` - Disk space used
- `api_requests_per_minute` - Request rate

### Implementing Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
query_counter = Counter('queries_total', 'Total queries processed')
query_duration = Histogram('query_duration_seconds', 'Query execution time')
confidence_gauge = Gauge('query_confidence', 'Latest query confidence score')

# Instrument code
@query_duration.time()
async def process_query(question: str) -> Answer:
    query_counter.inc()

    # Process query
    answer, confidence = await rag_pipeline(question)

    confidence_gauge.set(confidence)
    return answer
```

## Health Checks

### API Health Endpoint

```python
@app.get("/health")
async def health_check():
    """Check if all components are working."""
    checks = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": await check_database(),
            "vector_db": await check_chroma(),
            "llm_api": await check_groq(),
            "redis": await check_redis()
        }
    }

    # If any check fails, return 503
    if not all(checks["checks"].values()):
        checks["status"] = "unhealthy"
        return JSONResponse(status_code=503, content=checks)

    return checks
```

### Readiness vs Liveness

**Liveness Probe**: Is the application running?

```python
@app.get("/healthz")
async def liveness():
    return {"status": "alive"}
```

**Readiness Probe**: Is the application ready to serve traffic?

```python
@app.get("/readyz")
async def readiness():
    # Check if dependencies are connected
    if not await database.is_connected():
        return JSONResponse(status_code=503, content={"ready": False})
    return {"ready": True}
```

## Distributed Tracing

### OpenTelemetry Integration

Track requests across services:

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter

tracer = trace.get_tracer(__name__)

@app.post("/ask")
async def ask_question(question: str):
    with tracer.start_as_current_span("ask_question") as span:
        span.set_attribute("question.length", len(question))

        # Retrieval span
        with tracer.start_as_current_span("retrieve_chunks"):
            chunks = await retrieve(question)
            span.set_attribute("chunks.count", len(chunks))

        # LLM generation span
        with tracer.start_as_current_span("generate_answer"):
            answer = await llm_generate(question, chunks)

        return answer
```

### Correlation IDs

Track requests across logs:

```python
import uuid
from fastapi import Request

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id

    logger.info(
        "request_started",
        correlation_id=correlation_id,
        path=request.url.path
    )

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response
```

## Alerting

### Alert Configuration

Set up alerts for critical issues:

**High Priority Alerts**:

- API error rate > 5% for 5 minutes
- Database connection failures
- LLM API unavailable
- Disk usage > 90%

**Medium Priority**:

- Query latency p95 > 5 seconds
- Low confidence rate > 30%
- Memory usage > 80%

**Low Priority**:

- Dependency update available
- Documentation sync failed

### Alert Channels

- **Critical**: PagerDuty (ring engineer on-call)
- **High**: Slack #alerts channel
- **Medium**: Slack #monitoring channel
- **Low**: Email digest (daily)

## Dashboards

### Grafana Dashboard Layout

**Overview Panel**:

- Requests per minute (last 1 hour)
- Error rate percentage
- Average latency (p50, p95, p99)
- System health status

**RAG Performance Panel**:

- Questions answered per hour
- Average confidence score
- Retrieval accuracy
- LLM token usage

**Infrastructure Panel**:

- CPU usage by container
- Memory usage by container
- Database connection pool status
- Redis cache hit rate

## Error Tracking

### Sentry Integration

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://xxxxx@sentry.io/xxxxx",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,  # 10% of requests
    environment="production"
)

# Errors are automatically captured
# Manually capture context:
with sentry_sdk.configure_scope() as scope:
    scope.set_context("query", {"question": question, "user_id": user_id})
    sentry_sdk.capture_exception(e)
```

## Performance Monitoring

### Slow Query Detection

```python
import time
from functools import wraps

def monitor_performance(threshold_ms: int = 1000):
    """Decorator to log slow operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000

            if duration_ms > threshold_ms:
                logger.warning(
                    "slow_operation",
                    function=func.__name__,
                    duration_ms=duration_ms,
                    threshold_ms=threshold_ms
                )

            return result
        return wrapper
    return decorator

@monitor_performance(threshold_ms=2000)
async def process_query(question: str):
    # If this takes > 2 seconds, log warning
    pass
```

## Log Aggregation

We use **DataDog** for centralized logging:

**Log Query Examples**:

```
# Find all errors in last hour
status:error @timestamp:>now-1h

# Find slow queries
@latency_ms:>5000 service:api

# Find queries by specific user
@user_id:12345 service:api
```

## Best Practices

1. **Log contextual information** - Include user_id, correlation_id, timestamp
2. **Monitor what matters** - Focus on user-impacting metrics
3. **Set up alerts proactively** - Don't wait for users to report issues
4. **Use percentiles, not averages** - p95, p99 latency more meaningful
5. **Retain logs appropriately** - Balance cost vs compliance needs
6. **Test monitoring** - Verify alerts fire correctly
7. **Document runbooks** - What to do when alerts trigger

## Troubleshooting Guide

### High Latency

1. Check database query performance
2. Verify LLM API is responsive
3. Check if cache is working (Redis)
4. Review recent code deployments
5. Check infrastructure metrics (CPU, memory)

### High Error Rate

1. Check application logs for exceptions
2. Verify external services are available
3. Check database connection pool
4. Review recent configuration changes

### Low Confidence Scores

1. Check documentation freshness (last sync time)
2. Review retrieval quality (similarity scores)
3. Verify embedding model is working
4. Check if questions are out of scope
