# CI/CD Pipeline

## Overview

Our CI/CD pipeline automates testing, building, and deployment processes using GitHub Actions. This ensures code quality and enables rapid, reliable releases.

## Pipeline Architecture

```
Push to Branch → Lint → Test → Build → Deploy (if main)
```

## GitHub Actions Workflow

### Linting & Code Quality

Every pull request triggers automated checks:

- **ESLint** for JavaScript/TypeScript
- **Black** for Python formatting
- **Prettier** for consistent code style
- **Type checking** with TypeScript and Pyright

### Testing Pipeline

Tests run in parallel to reduce feedback time:

```yaml
- Unit tests (Jest for frontend, pytest for backend)
- Integration tests (API endpoint testing)
- E2E tests (Playwright - runs nightly only)
```

**Test Requirements**:

- Minimum 80% code coverage
- All tests must pass before merge
- No skipped tests in main branch

### Build Process

**Frontend Build**:

```bash
npm run build
# Creates optimized production bundle
# Output: .next/ directory
```

**Backend Build**:

```bash
docker build -t api:latest .
# Creates containerized API image
```

### Deployment

#### Staging Deployment

Automatic deployment on merge to `develop` branch:

1. Build Docker images
2. Push to container registry
3. Deploy to staging environment
4. Run smoke tests
5. Notify team in Slack

#### Production Deployment

Triggered by creating a release tag:

```bash
git tag v1.2.3
git push origin v1.2.3
```

**Production Checklist**:

- [ ] Staging tests passing for 24+ hours
- [ ] Database migrations reviewed
- [ ] Feature flags configured
- [ ] Rollback plan documented

## Branch Protection Rules

### Main Branch

- Requires pull request reviews (2 approvers)
- Status checks must pass
- Branch must be up to date
- Linear history (squash merges only)

### Develop Branch

- Requires 1 approver
- All checks must pass
- Fast-forward merges allowed

## Environment Variables

Environment-specific variables are managed through GitHub Secrets:

- `PRODUCTION_DATABASE_URL`
- `API_KEY_SERVICE_A`
- `JWT_SECRET`
- `SENTRY_DSN`

**Never commit secrets to the repository.**

## Monitoring Deployments

Track deployment status:

```bash
# Check latest deployment
gh run list --workflow=deploy.yml

# View deployment logs
gh run view <run-id> --log
```

## Common Issues

### Failed Builds

1. Check build logs in GitHub Actions tab
2. Verify environment variables are set
3. Confirm all dependencies are installed
4. Check for merge conflicts

### Test Failures

- Review test output in CI logs
- Run tests locally: `npm test` or `pytest`
- Check for flaky tests (re-run if suspected)

### Deployment Rollback

If production deployment fails:

```bash
# Quick rollback to previous version
kubectl rollout undo deployment/api
```

## Performance Optimizations

- Caching dependencies (`actions/cache`)
- Running tests in parallel
- Docker layer caching
- Conditional job execution

## Best Practices

1. **Keep pipelines fast** (target < 10 minutes)
2. **Fail fast** (run quick checks first)
3. **Make failures obvious** (clear error messages)
4. **Cache aggressively** (dependencies, Docker layers)
5. **Monitor pipeline health** (track success rates)

## Future Improvements

- Automated security scanning with Snyk
- Performance regression testing
- Automated changelog generation
- Blue-green deployment strategy
