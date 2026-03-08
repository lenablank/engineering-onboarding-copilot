# Deployment Guide

This guide covers how we deploy our application to different environments.

## Environments

We maintain three environments:

| Environment     | URL                 | Purpose                | Auto-Deploy                 |
| --------------- | ------------------- | ---------------------- | --------------------------- |
| **Development** | localhost:3000      | Local development      | No                          |
| **Staging**     | staging.company.com | Pre-production testing | Yes (on merge to `develop`) |
| **Production**  | app.company.com     | Live application       | Manual promotion            |

## Deployment Pipeline

### 1. Development → Staging (Automatic)

When you merge a pull request to the `develop` branch:

1. **GitHub Actions workflow triggers**
2. **Tests run** (unit, integration, E2E)
3. **Docker images built** (backend, frontend)
4. **Images pushed** to AWS ECR
5. **Kubernetes deployment updated** (staging cluster)
6. **Health checks performed**
7. **Notification sent** to #deployments Slack channel

**Typical duration**: 8-12 minutes

### 2. Staging → Production (Manual)

Production deployments require manual approval:

1. **Verify staging** is working correctly
2. **Create release PR** from `develop` to `main`
3. **Get approval** from at least 2 team members
4. **Merge to main** (does not auto-deploy)
5. **Run deployment workflow**:
   ```bash
   # In repository settings → Actions → Run workflow
   # Select: "Deploy to Production"
   # Branch: main
   ```
6. **Monitor deployment** in DataDog
7. **Smoke test** production endpoints
8. **Announce** in #general Slack channel

**Typical duration**: 10-15 minutes (including smoke tests)

## CI/CD Pipeline (GitHub Actions)

### Workflow: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest --cov=app
      - name: Run frontend tests
        run: |
          cd frontend
          npm install
          npm test

  build-and-deploy:
    needs: test
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: |
          docker build -t backend:${{ github.sha }} ./backend
          docker build -t frontend:${{ github.sha }} ./frontend

      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login ...
          docker push backend:${{ github.sha }}
          docker push frontend:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/backend backend=backend:${{ github.sha }}
          kubectl set image deployment/frontend frontend=frontend:${{ github.sha }}
```

## Infrastructure

### AWS Resources

- **EKS Cluster**: Kubernetes cluster (3 nodes)
- **RDS**: PostgreSQL database (Multi-AZ)
- **ElastiCache**: Redis cache
- **S3**: Static asset storage
- **CloudFront**: CDN for frontend
- **Route53**: DNS management
- **ECR**: Docker image registry

### Kubernetes Resources

**Backend Deployment**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
```

## Database Migrations

We use Alembic for database schema migrations.

### Creating a Migration

```bash
cd backend
alembic revision --autogenerate -m "Add user preferences table"
```

### Applying Migrations

**Development**:

```bash
alembic upgrade head
```

**Staging/Production** (automatic during deployment):

- Migrations run as Kubernetes init container
- Deployment waits for migrations to complete
- If migration fails, deployment is rolled back

### Migration Best Practices

1. **Always test locally first**
2. **Make migrations backwards compatible** when possible
3. **Avoid long-running migrations** in production
4. **Have a rollback plan** for complex changes

## Rollback Procedures

If something goes wrong in production:

### Quick Rollback (< 5 minutes)

```bash
# Rollback to previous Kubernetes deployment
kubectl rollout undo deployment/backend
kubectl rollout undo deployment/frontend

# Verify rollback
kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend
```

### Database Rollback (if needed)

```bash
# Find migration to rollback to
alembic history

# Rollback one migration
alembic downgrade -1

# Or rollback to specific revision
alembic downgrade abc123
```

## Monitoring Post-Deployment

After deploying, monitor for 30 minutes:

1. **Error rates** in DataDog
2. **Response times** (should be < 200ms p95)
3. **Database query performance**
4. **User-reported issues** in #support channel
5. **Log aggregation** in CloudWatch

### Health Check Endpoints

- Backend: `GET /health`
- Frontend: `GET /api/health`

Both should return `200 OK` with:

```json
{
  "status": "healthy",
  "version": "1.2.3",
  "timestamp": "2026-03-08T10:30:00Z"
}
```

## Hotfix Process

For critical bugs in production:

1. **Create hotfix branch** from `main`:

   ```bash
   git checkout main
   git pull
   git checkout -b hotfix/critical-bug-fix
   ```

2. **Make minimal fix** (only the critical issue)

3. **Test thoroughly** locally

4. **Create PR** with "HOTFIX" label

5. **Get expedited review** (1 approver minimum)

6. **Deploy immediately** to production

7. **Backport fix** to `develop` branch

## Secrets Management

Never commit secrets to the repository!

**Development**: Use `.env` files (gitignored)

**Staging/Production**: Use AWS Secrets Manager

```bash
# Store secret
aws secretsmanager create-secret --name prod/database/password --secret-string "..."

# Kubernetes retrieves via External Secrets Operator
```

## Deployment Checklist

Before deploying to production:

- [ ] All tests passing on `develop`
- [ ] Staging environment tested by QA
- [ ] Database migrations tested
- [ ] No known critical bugs
- [ ] Monitoring alerts configured
- [ ] Rollback plan documented
- [ ] Team notified in Slack
- [ ] Off-hours deployment (if high-risk)

## Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)
- Internal: Deployment runbook (Confluence)
