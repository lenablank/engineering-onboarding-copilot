# Git Workflow

## Overview

We use a trunk-based development workflow with short-lived feature branches. This guide covers branching strategy, commit conventions, and common Git operations.

## Branching Strategy

### Main Branches

**`main`**:

- Production-ready code only
- Protected branch (requires PR + reviews)
- Automatically deploys to production
- Never commit directly

**`develop`**:

- Integration branch for features
- Deploys to staging environment
- Merged to `main` for releases

### Feature Branches

Create feature branches from `develop`:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-confidence-scoring
```

**Branch Naming Convention**:

- Feature: `feature/short-description`
- Bug fix: `fix/issue-description`
- Hotfix: `hotfix/critical-bug`
- Refactor: `refactor/component-name`
- Documentation: `docs/update-readme`

**Examples**:

```
feature/groq-llm-integration
fix/database-connection-leak
hotfix/security-vulnerability-cve-2024-1234
refactor/extract-rag-service
docs/add-deployment-guide
```

## Commit Message Convention

We follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Simple commit
git commit -m "feat(api): add /ask endpoint for questions"

# With body
git commit -m "fix(database): resolve connection pool exhaustion

Connection pool was not releasing connections properly,
leading to exhaustion under high load. Added proper
cleanup in finally block.

Fixes #123"

# Breaking change
git commit -m "feat(auth): migrate to JWT authentication

BREAKING CHANGE: API now requires JWT tokens instead of
API keys. All clients must update authentication method."
```

### Good Commit Messages

✅ **Good**:

```
feat(rag): implement confidence scoring for answers
fix(embeddings): handle empty documents gracefully
docs(api): update authentication section
refactor(retrieval): extract similarity calculation
test(api): add integration tests for /ask endpoint
```

❌ **Bad**:

```
update stuff
fixes
WIP
changes
asdf
```

## Common Git Operations

### Starting New Work

```bash
# Ensure you're on develop
git checkout develop

# Get latest changes
git pull origin develop

# Create feature branch
git checkout -b feature/my-feature

# Make changes, then stage them
git add <files>

# Commit with message
git commit -m "feat: add new feature"

# Push to remote
git push -u origin feature/my-feature
```

### Keeping Branch Up to Date

```bash
# Fetch latest changes
git fetch origin

# Rebase your branch on develop
git rebase origin/develop

# If conflicts, resolve them and:
git add <resolved-files>
git rebase --continue

# Force push (since history changed)
git push --force-with-lease
```

### Amending Last Commit

```bash
# Make additional changes
git add <files>

# Amend without changing message
git commit --amend --no-edit

# Or amend with new message
git commit --amend -m "feat: updated feature


"

# Force push
git push --force-with-lease
```

### Interactive Rebase (Clean Up History)

```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# In the editor:
# pick → keep commit
# reword → change commit message
# squash → merge into previous commit
# drop → delete commit
```

### Stashing Changes

```bash
# Save work in progress
git stash save "WIP: working on confidence logic"

# List stashes
git stash list

# Apply stash
git stash apply stash@{0}

# Apply and remove from stash list
git stash pop
```

### Cherry-Picking Commits

```bash
# Apply specific commit from another branch
git cherry-pick <commit-hash>

# Cherry-pick without committing (review first)
git cherry-pick -n <commit-hash>
```

## Pull Request Workflow

### 1. Create PR

```bash
# Push your branch
git push origin feature/my-feature

# Go to GitHub and create PR
# Or use GitHub CLI:
gh pr create --title "Add confidence scoring" --body "Implementation details..."
```

### 2. Address Review Feedback

```bash
# Make requested changes
git add <files>
git commit -m "fix: address review feedback"
git push origin feature/my-feature
```

### 3. Merge After Approval

GitHub will handle the merge. After merge:

```bash
# Switch back to develop
git checkout develop

# Pull latest (includes your merged changes)
git pull origin develop

# Delete feature branch locally
git branch -d feature/my-feature

# Delete on remote
git push origin --delete feature/my-feature
```

## Resolving Merge Conflicts

```bash
# When rebasing causes conflicts
git status  # See conflicting files

# Edit files to resolve conflicts
# Look for markers:
<<<<<<< HEAD
current changes
=======
incoming changes
>>>>>>> branch-name

# After resolving
git add <resolved-files>
git rebase --continue

# If you want to abort
git rebase --abort
```

## Git Best Practices

### Do's ✅

- **Commit frequently** - Small, logical commits
- **Pull before push** - Stay up to date
- **Use descriptive commit messages** - Future you will thank you
- **Review your changes** - Use `git diff` before committing
- **Test before pushing** - Don't break the build
- **Keep commits atomic** - One logical change per commit

### Don'ts ❌

- **Don't commit secrets** - API keys, passwords, etc.
- **Don't commit generated files** - Build outputs, node_modules
- **Don't force push to shared branches** - Only to your feature branches
- **Don't commit directly to main** - Always use PRs
- **Don't commit commented-out code** - Delete it (it's in history)
- **Don't commit "WIP" to main branches** - Use git stash

## Useful Git Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --oneline --all
    amend = commit --amend --no-edit
    pushf = push --force-with-lease
    history = log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
```

Usage:

```bash
git st              # git status
git co main         # git checkout main
git history         # pretty commit history
git pushf           # safe force push
```

## Troubleshooting

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

### Undo Last Commit (Discard Changes)

```bash
git reset --hard HEAD~1
```

### Recover Deleted Branch

```bash
# Find commit hash
git reflog

# Recreate branch
git checkout -b recovered-branch <commit-hash>
```

### Remove File from Git (Keep Locally)

```bash
git rm --cached <file>
echo "<file>" >> .gitignore
git commit -m "chore: remove file from tracking"
```

### Fix Pushed Commit with Wrong Message

```bash
git commit --amend -m "fix: correct message"
git push --force-with-lease
```

## Git Hooks

We use pre-commit hooks for quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks from .pre-commit-config.yaml
pre-commit install

# Hooks run automatically on commit
# Or run manually:
pre-commit run --all-files
```

Our hooks check:

- Code formatting (Black, Prettier)
- Linting (ESLint, flake8)
- Type checking
- No secrets committed
- No merge conflict markers

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Documentation](https://git-scm.com/doc)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Oh Shit, Git!?!](https://ohshitgit.com/) - Fixing common mistakes
