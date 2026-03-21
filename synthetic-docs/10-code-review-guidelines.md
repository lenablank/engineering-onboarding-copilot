# Code Review Guidelines

## Overview

Code reviews are essential for maintaining code quality, sharing knowledge, and catching bugs early. Every pull request requires approval from at least one team member before merging.

## Pull Request Best Practices

### Creating a PR

**Good PR Title**:

```
✅ Add confidence scoring to RAG pipeline
✅ Fix: Database connection pool exhaustion
✅ Refactor: Extract embedding logic to separate service
```

**Bad PR Title**:

```
❌ Updates
❌ Fix stuff
❌ WIP changes
```

### PR Description Template

```markdown
## What does this PR do?

Brief description of the changes

## Why are we making this change?

Context and motivation

## How was this tested?

- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manually tested in development environment

## Screenshots (if applicable)

Attach before/after screenshots for UI changes

## Related Issues

Fixes #123
Relates to #456
```

### PR Size Guidelines

- **Small** (preferred): < 200 lines changed
- **Medium**: 200-500 lines changed
- **Large** (avoid): > 500 lines changed

Break large changes into smaller, reviewable PRs.

## Reviewing Code

### What to Look For

**Functionality**:

- Does the code do what it's supposed to do?
- Are edge cases handled?
- Are there potential bugs?

**Code Quality**:

- Is the code readable and maintainable?
- Are variable/function names descriptive?
- Is there unnecessary complexity?
- Is code duplicated?

**Testing**:

- Are there adequate unit tests?
- Do tests cover edge cases?
- Are integration tests needed?

**Security**:

- Are inputs validated?
- Are secrets properly managed?
- Could this introduce vulnerabilities?

**Performance**:

- Are there obvious performance issues?
- Is caching used appropriately?
- Are database queries optimized?

### Review Comments

Use constructive, respectful language:

**✅ Good Comments**:

```
"Consider extracting this into a separate function for reusability."

"This looks good! One suggestion: we could add error handling
for the network request to improve resilience."

"Nice refactoring! This is much more readable."

"Question: What happens if `user` is None here?"
```

**❌ Avoid**:

```
"This is wrong."
"Why would you do it this way?"
"This makes no sense."
```

### Comment Tags

Use tags to indicate the nature of comments:

- **[BLOCKING]**: Must be addressed before merge
- **[SUGGESTION]**: Optional improvement
- **[QUESTION]**: Seeking clarification
- **[NITPICK]**: Minor style/formatting issue
- **[PRAISE]**: Well done!

Example:

```
[BLOCKING] This will cause a database deadlock if two users
access this simultaneously. Need to add transaction locking.

[SUGGESTION] Consider using a list comprehension here for
better readability.

[QUESTION] Why are we using a while loop instead of a for loop?

[NITPICK] Missing trailing comma in this list.

[PRAISE] Great job adding comprehensive tests for this feature!
```

## Reviewer Responsibilities

### Response Time

- Review PRs within **24 hours** during work week
- Mark yourself unavailable if on vacation
- Assign backup reviewers for urgent PRs

### Approval Criteria

Only approve if:

- ✅ Code functions correctly
- ✅ Tests are adequate and passing
- ✅ No obvious security issues
- ✅ Follows code style guidelines
- ✅ Documentation updated if needed

### When to Request Changes

Request changes for:

- Bugs or broken functionality
- Missing critical tests
- Security vulnerabilities
- Violations of architectural principles
- Significant style/quality issues

## Author Responsibilities

### Responding to Feedback

- Address all blocking comments
- Respond to questions and suggestions
- Mark conversations as resolved after addressing
- Thank reviewers (positive team culture!)

### Handling Disagreements

If you disagree with feedback:

1. **Explain your reasoning** - Help reviewer understand your approach
2. **Ask for clarification** - Maybe you misunderstood the comment
3. **Propose alternatives** - Suggest a different solution
4. **Escalate if needed** - Involve tech lead for architectural decisions

**Don't**:

- Ignore feedback
- Get defensive
- Dismiss suggestions without discussion

## Self-Review Checklist

Before requesting review:

- [ ] Code compiles and runs locally
- [ ] All tests passing
- [ ] No debug code or commented-out code
- [ ] No hardcoded secrets or credentials
- [ ] Linter warnings addressed
- [ ] Self-reviewed the diff on GitHub
- [ ] Updated relevant documentation
- [ ] Added/updated tests for new functionality
- [ ] Confirmed branch is up to date with main

## Common Code Smells

### 1. Long Functions

```python
# ❌ Too long (150+ lines)
def process_user_data(user):
    # ... 150 lines of logic ...
    pass

# ✅ Extracted into smaller functions
def process_user_data(user):
    validated_user = validate_user(user)
    enriched_user = enrich_user_data(validated_user)
    return save_user(enriched_user)
```

### 2. Magic Numbers

```python
# ❌ What does 3600 mean?
cache.set(key, value, 3600)

# ✅ Use named constants
CACHE_TTL_SECONDS = 3600  # 1 hour
cache.set(key, value, CACHE_TTL_SECONDS)
```

### 3. Nested Conditionals

```python
# ❌ Hard to follow
if user:
    if user.is_active:
        if user.has_permission:
            if not user.is_suspended:
                # do something
                pass

# ✅ Guard clauses
if not user:
    return
if not user.is_active:
    return
if not user.has_permission:
    return
if user.is_suspended:
    return

# do something
```

### 4. Missing Error Handling

```python
# ❌ No error handling
def fetch_user(user_id):
    response = requests.get(f"/api/users/{user_id}")
    return response.json()

# ✅ Proper error handling
def fetch_user(user_id):
    try:
        response = requests.get(f"/api/users/{user_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error(f"Timeout fetching user {user_id}")
        raise
    except requests.HTTPError as e:
        logger.error(f"HTTP error fetching user {user_id}: {e}")
        raise
```

## Code Style

### Python (Backend)

- Follow **PEP 8** style guide
- Use **Black** formatter
- Maximum line length: 100 characters
- Type hints for function signatures
- Docstrings for public functions

```python
def calculate_confidence(similarity_scores: list[float]) -> float:
    """
    Calculate confidence score based on retrieval similarity.

    Args:
        similarity_scores: List of similarity scores from vector search

    Returns:
        Confidence score between 0 and 1
    """
    if not similarity_scores:
        return 0.0
    return sum(similarity_scores) / len(similarity_scores)
```

### TypeScript (Frontend)

- Use **TypeScript** strict mode
- Use **Prettier** formatter
- Use **ESLint** for linting
- Functional components with hooks

```typescript
interface Question {
  text: string;
  timestamp: Date;
}

const AskQuestion: React.FC = () => {
  const [question, setQuestion] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Implementation
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* JSX */}
    </form>
  );
};
```

## Automated Checks

Every PR runs automated checks:

- ✅ **Linting** (ESLint, Black, Prettier)
- ✅ **Type checking** (TypeScript, Pyright)
- ✅ **Unit tests** (Jest, pytest)
- ✅ **Code coverage** (must maintain >80%)
- ✅ **Security scanning** (npm audit, pip-audit)

Fix all automated check failures before requesting review.

## Merge Strategy

### Squash Merging (Preferred)

For feature branches:

- Squash all commits into one
- Clean up commit message
- Easier to revert if needed

### Merge Commits

For release branches:

- Preserve commit history
- Track exactly what was released

### Rebase

For keeping feature branch up to date:

```bash
git fetch origin
git rebase origin/main
```

## After Merge

Post-merge responsibilities:

- [ ] Delete feature branch
- [ ] Monitor CI/CD deployment
- [ ] Watch for errors in monitoring
- [ ] Close related issues
- [ ] Update project board

## Resources

- [Google Engineering Practices - Code Review](https://google.github.io/eng-practices/review/)
- Internal Code Style Guide (wiki)
- Team Architecture Decision Records (ADRs)
