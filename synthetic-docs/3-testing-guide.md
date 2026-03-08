# Testing Guide

Quality is our top priority. This guide covers our testing practices, tools, and best practices.

## Testing Philosophy

- **Test before you ship**: All new features must have tests
- **Coverage goal**: Minimum 80% code coverage for backend, 60% for frontend
- **Test pyramid**: More unit tests, fewer integration tests, minimal E2E tests
- **CI enforcement**: All tests must pass before merging to main

## Types of Tests

### 1. Unit Tests

Test individual functions and methods in isolation.

**Backend (Python - pytest)**:

```python
# tests/test_user_service.py
def test_create_user_with_valid_data():
    user = create_user(email="test@example.com", name="Test User")
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.id is not None
```

**Frontend (TypeScript - Jest)**:

```typescript
// tests/utils.test.ts
import { formatDate } from "@/utils/date";

test("formatDate formats ISO date correctly", () => {
  const result = formatDate("2026-03-08");
  expect(result).toBe("March 8, 2026");
});
```

### 2. Integration Tests

Test how multiple components work together.

**Backend API Tests**:

```python
# tests/integration/test_api.py
def test_user_registration_flow(client):
    # Register user
    response = client.post("/api/auth/register", json={
        "email": "newuser@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 201

    # Verify user can login
    response = client.post("/api/auth/login", json={
        "email": "newuser@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### 3. End-to-End (E2E) Tests

Test complete user flows in a browser environment.

**Using Playwright**:

```typescript
// e2e/user-journey.spec.ts
import { test, expect } from "@playwright/test";

test("user can sign up and create first project", async ({ page }) => {
  await page.goto("http://localhost:3000");
  await page.click("text=Sign Up");
  await page.fill("[name=email]", "e2e@test.com");
  await page.fill("[name=password]", "TestPass123!");
  await page.click('button:has-text("Create Account")');

  await expect(page).toHaveURL("/dashboard");
  await page.click("text=New Project");
  await page.fill("[name=projectName]", "My First Project");
  await page.click('button:has-text("Create")');

  await expect(page.locator("text=My First Project")).toBeVisible();
});
```

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_user_service.py

# Run tests matching pattern
pytest -k "test_user"
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test -- UserProfile.test.tsx
```

### E2E Tests

```bash
# Run all E2E tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific test
npx playwright test user-journey.spec.ts
```

## Writing Good Tests

### Best Practices

1. **Descriptive test names**: Use clear, behavior-focused names

   ```python
   # Good
   def test_user_cannot_register_with_duplicate_email():

   # Bad
   def test_register():
   ```

2. **Arrange-Act-Assert pattern**:

   ```python
   def test_update_user_profile():
       # Arrange
       user = create_test_user()
       new_name = "Updated Name"

       # Act
       updated_user = update_user_profile(user.id, name=new_name)

       # Assert
       assert updated_user.name == new_name
   ```

3. **Test one thing**: Each test should verify a single behavior

4. **Use fixtures for setup**: Avoid repetitive setup code

   ```python
   @pytest.fixture
   def authenticated_client(client):
       token = get_test_token()
       client.headers = {"Authorization": f"Bearer {token}"}
       return client
   ```

5. **Mock external dependencies**:

   ```python
   from unittest.mock import patch

   @patch('app.services.email.send_email')
   def test_user_registration_sends_email(mock_send_email):
       register_user(email="test@example.com")
       mock_send_email.assert_called_once()
   ```

## Continuous Integration

All tests run automatically on GitHub Actions when you:

- Create a pull request
- Push commits to a pull request
- Merge to main branch

**Required checks**:

- ✅ Backend unit tests pass
- ✅ Backend coverage ≥ 80%
- ✅ Frontend tests pass
- ✅ Linting passes (flake8, ESLint)
- ✅ Type checking passes (mypy, TypeScript)

## Test Database

We use a separate test database to avoid affecting development data:

```python
# conftest.py
@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    engine = create_engine("postgresql://localhost/test_db")
    Base.metadata.create_all(engine)

    session = Session(engine)
    yield session

    session.close()
    Base.metadata.drop_all(engine)
```

## Debugging Failed Tests

```bash
# Run with verbose output
pytest -v

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Jest documentation](https://jestjs.io/)
- [Playwright documentation](https://playwright.dev/)
- Internal: Testing best practices wiki
