---
description: Run comprehensive code review
argument-hint: [--static|--security|--style|--ai|--all]
tools: [bash, task]
---

Running comprehensive code review for recent changes...

## Review Pipeline

Based on arguments: $ARGUMENT (default: all checks)

### 1. Static Analysis
Running static analysis tools:

```bash
# Python projects
if command -v ruff >/dev/null 2>&1; then
    echo "Running ruff (Python linter)..."
    ruff check .
fi

if command -v mypy >/dev/null 2>&1; then
    echo "Running mypy (type checking)..."
    mypy .
fi

# JavaScript/TypeScript projects  
if command -v eslint >/dev/null 2>&1; then
    echo "Running ESLint..."
    eslint .
fi

# General
if command -v grep >/dev/null 2>&1; then
    echo "Checking for common issues..."
    grep -r "TODO\|FIXME\|XXX" --include="*.py" --include="*.js" --include="*.ts" .
fi
```

### 2. Security Analysis
Checking for security issues:

```bash
# Python security
if command -v bandit >/dev/null 2>&1; then
    echo "Running bandit (security scanner)..."
    bandit -r .
fi

# General security patterns
grep -r "password\|secret\|key\|token" --include="*.py" --include="*.js" --include="*.ts" . | grep -v test
```

### 3. Code Style Check
Checking code formatting:

```bash
# Auto-format if tools available
if command -v black >/dev/null 2>&1; then
    echo "Running black (Python formatter)..."
    black --check .
fi

if command -v prettier >/dev/null 2>&1; then
    echo "Running prettier (JS/TS formatter)..."
    prettier --check .
fi
```

### 4. AI Code Review
Now invoking the reviewer agent for semantic analysis...

The review process will analyze:
- Recent changes via git diff
- Code correctness and logic
- Security considerations
- Performance implications
- Maintainability and style
- Test coverage for new code

Results will be prioritized as:
- **Critical**: Must fix before proceeding
- **Important**: Should address soon  
- **Suggestions**: Consider for improvement