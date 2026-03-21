# API Authentication Guide

## Overview

Our API uses **JWT (JSON Web Token)** authentication for secure access. This guide covers authentication flows, token management, and best practices.

## Authentication Flow

### 1. User Registration

**Endpoint**: `POST /auth/register`

**Request**:

```json
{
  "email": "engineer@company.com",
  "username": "john_doe",
  "password": "SecureP@ssw0rd123",
  "full_name": "John Doe"
}
```

**Response**:

```json
{
  "id": 42,
  "email": "engineer@company.com",
  "username": "john_doe",
  "is_active": true,
  "created_at": "2026-03-21T10:30:00Z"
}
```

**Password Requirements**:

- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### 2. User Login

**Endpoint**: `POST /auth/login`

**Request**:

```json
{
  "username": "john_doe",
  "password": "SecureP@ssw0rd123"
}
```

**Response**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Token Properties**:

- **Type**: Bearer token
- **Algorithm**: HS256
- **Expiration**: 24 hours
- **Payload**: user_id, username, exp

### 3. Using Access Token

Include token in `Authorization` header:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:8000/ask
```

**Frontend (JavaScript)**:

```javascript
const response = await fetch("http://localhost:8000/ask", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ question: "How do I deploy?" }),
});
```

## Token Management

### Storing Tokens

**❌ Don't**: Store in localStorage (vulnerable to XSS)

```javascript
// DON'T DO THIS
localStorage.setItem("token", accessToken);
```

**✅ Do**: Store in httpOnly cookies

```javascript
// Server sets cookie
res.cookie("access_token", token, {
  httpOnly: true,
  secure: true, // HTTPS only
  sameSite: "strict",
  maxAge: 86400000, // 24 hours
});
```

**✅ Alternative**: Use secure session storage with proper XSS protection

### Token Refresh

**Endpoint**: `POST /auth/refresh`

**Request**:

```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response**:

```json
{
  "access_token": "new_access_token",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Implementation**:

```javascript
async function refreshToken() {
  const response = await fetch("/auth/refresh", {
    method: "POST",
    credentials: "include", // Send httpOnly cookie
  });

  if (!response.ok) {
    // Refresh failed, redirect to login
    window.location.href = "/login";
    return null;
  }

  return response.json();
}

// Auto-refresh before expiration
setInterval(refreshToken, 23 * 60 * 60 * 1000); // 23 hours
```

### Logout

**Endpoint**: `POST /auth/logout`

**Headers**:

```
Authorization: Bearer <access_token>
```

**Response**:

```json
{
  "message": "Successfully logged out"
}
```

**Client-side cleanup**:

```javascript
async function logout() {
  await fetch("/auth/logout", {
    method: "POST",
    credentials: "include",
  });

  // Clear client-side data
  sessionStorage.clear();

  // Redirect to login
  window.location.href = "/login";
}
```

## Protected Endpoints

### Authentication Required

All endpoints except these require authentication:

- `POST /auth/register`
- `POST /auth/login`
- `GET /health`
- `GET /docs` (Swagger UI)

### Authorization Levels

Different roles have different permissions:

| Endpoint             | Admin | Editor | Viewer |
| -------------------- | ----- | ------ | ------ |
| GET /ask             | ✅    | ✅     | ✅     |
| POST /documents/sync | ✅    | ✅     | ❌     |
| DELETE /documents    | ✅    | ❌     | ❌     |
| GET /gaps            | ✅    | ✅     | ✅     |
| PATCH /gaps/:id      | ✅    | ✅     | ❌     |
| GET /users           | ✅    | ❌     | ❌     |

### Implementing Protection

**Backend (FastAPI)**:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Extract and validate JWT token."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/ask")
async def ask_question(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user)
):
    """Protected endpoint - requires authentication."""
    # current_user is automatically injected
    return await process_question(request.question, current_user)
```

**Role-Based Protection**:

```python
def require_role(allowed_roles: List[str]):
    """Decorator to enforce role-based access control."""
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

@app.post("/documents/sync")
async def sync_documents(
    current_user: User = Depends(require_role(["admin", "editor"]))
):
    """Only admins and editors can sync documents."""
    pass
```

## API Keys (Alternative Authentication)

For service-to-service communication or CLI tools:

### Generating API Keys

**Endpoint**: `POST /auth/api-keys`

**Request**:

```json
{
  "name": "CLI Tool",
  "expires_days": 90
}
```

**Response**:

```json
{
  "api_key": "eak_1a2b3c4d5e6f7g8h9i0j",
  "name": "CLI Tool",
  "expires_at": "2026-06-19T10:30:00Z"
}
```

⚠️ **Important**: Save the API key immediately. It cannot be retrieved later.

### Using API Keys

```bash
# In header
curl -H "X-API-Key: eak_1a2b3c4d5e6f7g8h9i0j" \
  http://localhost:8000/ask

# Or as query parameter (less secure)
curl "http://localhost:8000/ask?api_key=eak_1a2b3c4d5e6f7g8h9i0j"
```

### Revoking API Keys

**Endpoint**: `DELETE /auth/api-keys/{key_id}`

## Security Best Practices

### Token Security

1. **Use HTTPS in production** - Never send tokens over HTTP
2. **Short expiration times** - 24 hours maximum
3. **Rotate secrets regularly** - Change JWT_SECRET periodically
4. **Strong secret keys** - Use cryptographically secure random strings

```python
# Generate strong JWT secret
import secrets
JWT_SECRET = secrets.token_urlsafe(32)
```

### Password Security

1. **Never store plaintext passwords**
2. **Use bcrypt for hashing** (never MD5 or SHA1)
3. **Implement account lockout** after failed attempts
4. **Enforce strong password policy**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed_password = pwd_context.hash(plain_password)

# Verify password
is_valid = pwd_context.verify(plain_password, hashed_password)
```

### Rate Limiting

Prevent brute force attacks:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(credentials: LoginRequest):
    pass
```

### Audit Logging

Log authentication events:

```python
logger.info(
    "login_attempt",
    username=username,
    ip_address=request.client.host,
    success=True,
    timestamp=datetime.utcnow()
)

logger.warning(
    "login_failed",
    username=username,
    ip_address=request.client.host,
    reason="invalid_password",
    timestamp=datetime.utcnow()
)
```

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Invalid authentication credentials",
  "error_code": "INVALID_TOKEN"
}
```

**Reasons**:

- Token missing
- Token expired
- Token invalid
- Invalid signature

### 403 Forbidden

```json
{
  "detail": "Insufficient permissions",
  "error_code": "FORBIDDEN"
}
```

**Reason**: User authenticated but lacks required role/permission

### 429 Too Many Requests

```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds.",
  "retry_after": 60
}
```

## Testing Authentication

### Getting a Test Token

```bash
# Register test user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestP@ssw0rd123"
  }'

# Login to get token
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestP@ssw0rd123"
  }' | jq -r '.access_token')

# Use token
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I deploy?"}'
```

### Unit Testing

```python
import pytest
from fastapi.testclient import TestClient

def test_protected_endpoint_without_auth(client: TestClient):
    """Test that protected endpoints require authentication."""
    response = client.post("/ask", json={"question": "test"})
    assert response.status_code == 401

def test_protected_endpoint_with_auth(client: TestClient, test_token):
    """Test protected endpoint with valid token."""
    response = client.post(
        "/ask",
        json={"question": "test"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
```

## Migration from API Keys to JWT

If switching from API key to JWT authentication:

1. **Support both temporarily** (transition period)
2. **Deprecate old method** (announce sunset date)
3. **Update client code** (migrate to JWT)
4. **Remove API key support** (after transition)

## Resources

- [JWT.io](https://jwt.io/) - Debug and validate JWTs
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
