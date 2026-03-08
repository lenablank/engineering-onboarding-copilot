# API Reference

This document provides a comprehensive reference for all API endpoints in our platform.

## Base URLs

- **Development**: `http://localhost:8000`
- **Staging**: `https://api-staging.company.com`
- **Production**: `https://api.company.com`

## Authentication

All API requests (except public endpoints) require a Bearer token in the Authorization header.

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Obtaining a Token

**POST** `/api/auth/login`

```json
// Request
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

// Response (200 OK)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Core Endpoints

### Health Check

**GET** `/health`

Returns the API health status. No authentication required.

**Response** (200 OK):

```json
{
  "status": "healthy",
  "version": "1.2.3",
  "timestamp": "2026-03-08T10:30:00Z"
}
```

---

### User Management

#### Get Current User

**GET** `/api/users/me`

Returns the authenticated user's profile.

**Response** (200 OK):

```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar_url": "https://cdn.company.com/avatars/usr_abc123.jpg",
  "created_at": "2026-01-15T09:20:00Z",
  "role": "developer"
}
```

#### Update User Profile

**PATCH** `/api/users/me`

Updates the authenticated user's profile.

**Request**:

```json
{
  "name": "Jane Doe",
  "avatar_url": "https://cdn.company.com/avatars/new.jpg"
}
```

**Response** (200 OK):

```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "Jane Doe",
  "avatar_url": "https://cdn.company.com/avatars/new.jpg",
  "updated_at": "2026-03-08T10:30:00Z"
}
```

#### List Users

**GET** `/api/users`

Returns a paginated list of users. Requires `admin` role.

**Query Parameters**:

- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20, max: 100)
- `role` (string): Filter by role ("admin", "developer", "viewer")

**Response** (200 OK):

```json
{
  "items": [
    {
      "id": "usr_abc123",
      "email": "user1@example.com",
      "name": "User One",
      "role": "developer"
    },
    {
      "id": "usr_def456",
      "email": "user2@example.com",
      "name": "User Two",
      "role": "admin"
    }
  ],
  "total": 42,
  "page": 1,
  "per_page": 20,
  "pages": 3
}
```

---

### Project Management

#### Create Project

**POST** `/api/projects`

Creates a new project.

**Request**:

```json
{
  "name": "My New Project",
  "description": "A project for building awesome features",
  "visibility": "private"
}
```

**Response** (201 Created):

```json
{
  "id": "proj_xyz789",
  "name": "My New Project",
  "description": "A project for building awesome features",
  "visibility": "private",
  "owner_id": "usr_abc123",
  "created_at": "2026-03-08T10:30:00Z"
}
```

#### Get Project

**GET** `/api/projects/{project_id}`

Returns details for a specific project.

**Response** (200 OK):

```json
{
  "id": "proj_xyz789",
  "name": "My New Project",
  "description": "A project for building awesome features",
  "visibility": "private",
  "owner": {
    "id": "usr_abc123",
    "name": "John Doe"
  },
  "members_count": 5,
  "created_at": "2026-01-15T09:20:00Z",
  "updated_at": "2026-03-08T10:30:00Z"
}
```

#### Update Project

**PATCH** `/api/projects/{project_id}`

Updates a project. Must be project owner or admin.

**Request**:

```json
{
  "name": "Updated Project Name",
  "description": "New description"
}
```

**Response** (200 OK): Same as Get Project

#### Delete Project

**DELETE** `/api/projects/{project_id}`

Deletes a project. Must be project owner or admin.

**Response** (204 No Content)

---

### Task Management

#### List Tasks

**GET** `/api/projects/{project_id}/tasks`

Returns all tasks for a project.

**Query Parameters**:

- `status` (string): Filter by status ("todo", "in_progress", "done")
- `assigned_to` (string): Filter by user ID

**Response** (200 OK):

```json
{
  "items": [
    {
      "id": "task_123",
      "title": "Implement user authentication",
      "description": "Add JWT-based authentication",
      "status": "in_progress",
      "priority": "high",
      "assigned_to": {
        "id": "usr_abc123",
        "name": "John Doe"
      },
      "due_date": "2026-03-15",
      "created_at": "2026-03-01T10:00:00Z"
    }
  ],
  "total": 15
}
```

#### Create Task

**POST** `/api/projects/{project_id}/tasks`

Creates a new task in a project.

**Request**:

```json
{
  "title": "Fix bug in login flow",
  "description": "Users can't login with email",
  "priority": "high",
  "assigned_to": "usr_abc123",
  "due_date": "2026-03-10"
}
```

**Response** (201 Created):

```json
{
  "id": "task_456",
  "title": "Fix bug in login flow",
  "status": "todo",
  "priority": "high",
  "created_at": "2026-03-08T10:30:00Z"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "received": "not-an-email"
    }
  }
}
```

### Common Error Codes

| Status Code | Error Code            | Description                       |
| ----------- | --------------------- | --------------------------------- |
| 400         | `VALIDATION_ERROR`    | Request validation failed         |
| 401         | `UNAUTHORIZED`        | Missing or invalid authentication |
| 403         | `FORBIDDEN`           | Insufficient permissions          |
| 404         | `NOT_FOUND`           | Resource not found                |
| 409         | `CONFLICT`            | Resource already exists           |
| 429         | `RATE_LIMIT_EXCEEDED` | Too many requests                 |
| 500         | `INTERNAL_ERROR`      | Server error                      |

## Rate Limiting

API requests are rate-limited per user:

- **Free tier**: 100 requests per hour
- **Pro tier**: 1000 requests per hour
- **Enterprise**: 10,000 requests per hour

Rate limit info is included in response headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1678276800
```

## Pagination

List endpoints support pagination via query parameters:

- `page`: Page number (starts at 1)
- `per_page`: Items per page (max 100)

Response includes pagination metadata:

```json
{
  "items": [...],
  "total": 256,
  "page": 2,
  "per_page": 20,
  "pages": 13
}
```

## Filtering and Sorting

Most list endpoints support filtering and sorting:

```http
GET /api/projects?status=active&sort=created_at:desc&per_page=50
```

## Webhooks

Configure webhooks to receive real-time notifications:

**POST** `/api/webhooks`

```json
{
  "url": "https://your-app.com/webhook",
  "events": ["project.created", "task.updated"],
  "secret": "whsec_..."
}
```

Webhook payloads include a signature in headers:

```http
X-Webhook-Signature: sha256=...
X-Webhook-Event: project.created
```

## SDK Examples

### Python

```python
import requests

API_URL = "https://api.company.com"
TOKEN = "your_token_here"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Get current user
response = requests.get(f"{API_URL}/api/users/me", headers=headers)
user = response.json()
print(f"Hello, {user['name']}!")
```

### TypeScript

```typescript
const API_URL = "https://api.company.com";
const TOKEN = "your_token_here";

async function getCurrentUser() {
  const response = await fetch(`${API_URL}/api/users/me`, {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
    },
  });

  const user = await response.json();
  console.log(`Hello, ${user.name}!`);
}
```

## Postman Collection

Download our Postman collection: [Download Link]

Import it to Postman and set your API token in the collection variables.

## Questions?

- API Issues: #api-support on Slack
- Feature Requests: File a Jira ticket
- Documentation: Contribute via GitHub
