---
description: Summarize current project context
argument-hint: [file-glob-pattern] (optional)
tools: [read, glob, bash]
---

Analyzing project context for: ${ARGUMENT:-"entire project"}

## Project Context Summary

### 1. Project Structure Analysis
Examining directory structure and main components...

```bash
echo "=== Project Structure ==="
find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" | head -20
echo ""
echo "=== Main Directories ==="
find . -maxdepth 2 -type d | grep -v "\.git\|node_modules\|__pycache__" | sort
```

### 2. Recent Development Activity
Checking recent changes and development patterns...

```bash
echo "=== Recent Commits ==="
git log --oneline -10 2>/dev/null || echo "No git history available"
echo ""
echo "=== Current Branch Status ==="
git status --porcelain 2>/dev/null || echo "Not a git repository"
```

### 3. Dependencies and Configuration
Analyzing project dependencies...

```bash
echo "=== Dependencies ==="
if [ -f "package.json" ]; then
    echo "Node.js project detected"
    cat package.json | grep -A 20 '"dependencies"'
elif [ -f "requirements.txt" ]; then
    echo "Python project detected"
    head -20 requirements.txt
elif [ -f "Cargo.toml" ]; then
    echo "Rust project detected"
    cat Cargo.toml | grep -A 10 '\[dependencies\]'
else
    echo "No standard dependency file found"
fi
```

### 4. Test Coverage and Quality
Examining test structure and coverage...

```bash
echo "=== Test Files ==="
find . -name "*test*" -o -name "*spec*" | head -10
echo ""
echo "=== TODO Items ==="
grep -r "TODO\|FIXME\|XXX" --include="*.py" --include="*.js" --include="*.ts" --include="*.md" . 2>/dev/null | head -10
```

### 5. Key Components Analysis
Reading and summarizing key files...

This analysis will examine:
- Main application entry points
- Configuration files
- Key modules and their responsibilities
- API endpoints or main interfaces
- Documentation structure

Based on the file patterns: ${ARGUMENT:-"src/**, docs/**, *.md, package.json, requirements.txt"}

## Context Digest
After analysis, I'll provide a structured summary including:

### Core Components
- **Main modules**: [Purpose and functionality]
- **Entry points**: [How the application starts]
- **Configuration**: [Key settings and environment]

### Development State  
- **Active features**: [Current development focus]
- **Test coverage**: [Testing approach and coverage]
- **Technical debt**: [Known issues or improvements needed]

### Quick Start Guide
- **Setup**: [How to get started]
- **Key commands**: [Essential development commands]
- **Architecture notes**: [Important design decisions]