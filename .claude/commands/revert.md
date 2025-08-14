---
description: Git-based rollback system for reverting code changes and agent state to known good configurations
argument-hint: [--to-commit <hash>] [--list-points] [--dry-run] [--include-cache]
tools: [read, write, bash, task]
---

# Revert Command - Git-Based Rollback System

Comprehensive rollback system that reverts both code changes and agent cache state to known good configurations.

## Usage Options

- `/revert --list-points` - Show available rollback points with descriptions
- `/revert --to-commit abc123f` - Revert to specific commit hash
- `/revert --dry-run --to-commit abc123f` - Preview changes without executing
- `/revert --include-cache` - Also revert agent cache state to match commit
- `/revert` - Interactive mode to choose rollback point

## Revert Capabilities

### 1. Code Rollback with Git Integration

**Safe Git Rollback Process:**
```bash
# Check current Git status
git status --porcelain
git log --oneline -10

# For uncommitted changes - stash first
git stash push -m "Pre-revert stash $(date)"

# Revert to specific commit (creates new commit)
git revert <commit-hash> --no-edit

# Or reset to specific commit (destructive - requires confirmation)
git reset --hard <commit-hash>  # Only with explicit --force flag
```

**Rollback Safety Checks:**
- Verify target commit exists and is valid
- Check for uncommitted changes (require stash or explicit override)
- Confirm destructive operations with user
- Create safety stash before any destructive operations
- Validate working directory state after rollback

### 2. Agent Cache State Synchronization

**Cache State Rollback:**
When `--include-cache` is specified:
1. **Identify Target Cache State**: Find cached agent outputs for target commit
2. **Purge Incompatible Caches**: Remove cache entries newer than target commit
3. **Restore Historical Context**: Reinstate cache manifest for target commit
4. **Update Cache Tracking**: Update last-analysis-commit to match target

**Cache Rollback Process:**
```bash
# Find cache entries for target commit
find .claude/cache/agent-outputs/ -name "*-${TARGET_COMMIT}-*"

# Remove cache entries newer than target commit  
# (requires careful Git log analysis)

# Restore cache manifest state if backup exists
cp .claude/cache/backups/manifest-${TARGET_COMMIT}.json .claude/cache/cache-manifest.json

# Update cache tracking
echo "${TARGET_COMMIT}" > .claude/cache/last-analysis-commit
```

### 3. Interactive Rollback Point Selection

**Available Rollback Points:**
```
📚 Available Rollback Points:

Recent Commits:
   🎯 abc123f (2 hours ago) - "Complete authentication feature"
      Files: src/auth/*.py, tests/auth/*.py (✅ Tests passing)
      Cache: 15 agent entries, 89% hit rate
      
   🎯 def456a (4 hours ago) - "Add user registration endpoint"  
      Files: src/api/users.py, tests/api/test_users.py (✅ Tests passing)
      Cache: 12 agent entries, 76% hit rate
      
   🎯 ghi789b (1 day ago) - "Initial API structure"
      Files: src/api/*.py (⚠️ Some tests failing)
      Cache: 8 agent entries, 65% hit rate

Feature Milestones:
   📦 v1.2.0 (1 week ago) - "Authentication system complete"
      Status: ✅ Stable release
      Cache: Comprehensive coverage, high hit rates
      
   📦 v1.1.0 (2 weeks ago) - "Basic API functionality" 
      Status: ✅ Stable release  
      Cache: Basic coverage, moderate hit rates

Branch Points:
   🌿 main @ xyz987c - "Latest stable"
   🌿 feature/auth @ abc123f - "Current feature branch"
   🌿 develop @ mno456d - "Development branch"
```

### 4. Rollback Impact Analysis

**Before executing rollback, analyze impact:**
```
🔍 Rollback Impact Analysis:

Target: Commit def456a "Add user registration endpoint"

Code Changes to Revert:
   📂 src/auth/
      ├── authentication.py (147 lines removed)
      ├── password_utils.py (89 lines removed)
      └── middleware.py (231 lines removed)
   
   📂 tests/auth/
      ├── test_authentication.py (removed)
      ├── test_password_utils.py (removed)
      └── test_middleware.py (removed)

Agent Cache Impact (with --include-cache):
   🗑️ Will Remove:
      - planner-abc123f-auth-feature.json (2.3KB)
      - tester-abc123f-auth-tests.json (4.1KB)
      - reviewer-abc123f-auth-review.json (1.8KB)
   
   💾 Will Restore:
      - Cache state as of def456a
      - 12 agent entries from earlier development
      - Cache hit rate: 76% → estimated post-rollback

Workflow State Impact:
   ⚠️ Current workflows in .claude/state/ will be marked as stale
   ⚠️ Any running workflows will be terminated
   🔄 Workflow state will be reset to match target commit

Risk Assessment:
   ⚠️ MEDIUM RISK: 2 hours of development work will be lost
   ⚠️ Cache efficiency may temporarily decrease
   ✅ Tests should pass after rollback (target commit was stable)
```

### 5. Rollback Execution Process

**Step 1: Pre-Rollback Safety**
```bash
# Create comprehensive backup
git stash push -m "Pre-revert-backup-$(date +%Y%m%d-%H%M%S)"

# Backup current cache state  
cp .claude/cache/cache-manifest.json .claude/cache/backups/manifest-backup-$(git rev-parse HEAD).json

# Stop any running workflows
# (Check .claude/state/workflows/ for active workflows)
```

**Step 2: Execute Git Rollback**
```bash
# Safe revert (creates new commit)
git revert <target-commit>..HEAD --no-edit

# Or hard reset (destructive - requires explicit confirmation)
git reset --hard <target-commit>
```

**Step 3: Synchronize Agent Cache (if --include-cache)**
```bash
# Remove incompatible cache entries
# Update cache manifest
# Reset cache tracking files
```

**Step 4: Validate Post-Rollback State**
```bash
# Run basic health checks
git status
git log --oneline -5

# Validate cache integrity
/cache-status

# Run smoke tests if available
pytest tests/ --maxfail=5 -q
```

### 6. Recovery Options

**If Rollback Goes Wrong:**
```bash
# Recover from pre-revert stash
git stash list
git stash apply stash@{0}  # Most recent pre-revert backup

# Or use Git reflog to find lost commits
git reflog
git reset --hard <previous-head>

# Restore cache state from backup
cp .claude/cache/backups/manifest-backup-<commit>.json .claude/cache/cache-manifest.json
```

### 7. Dry Run Preview

**Preview Mode (--dry-run):**
Shows exactly what would change without executing:
```
🔍 DRY RUN: Revert to def456a

Git Operations:
   ✓ Current HEAD: abc123f
   ✓ Target commit: def456a (exists, reachable)
   ✓ Files to revert: 15 files
   ✓ Commits to revert: 3 commits
   
   Command that would execute:
   git revert def456a..abc123f --no-edit

Cache Operations (--include-cache):
   ✓ Cache entries to remove: 7 entries (8.2KB)
   ✓ Historical cache entries to restore: 12 entries
   ✓ Cache manifest rollback: Available
   
   Commands that would execute:
   rm .claude/cache/agent-outputs/*-abc123f-*
   cp .claude/cache/backups/manifest-def456a.json .claude/cache/cache-manifest.json

Safety Measures:
   ✓ Pre-revert stash would be created
   ✓ Cache backup would be created  
   ✓ Recovery instructions would be provided
   
No changes made. Use without --dry-run to execute.
```

## Error Handling & Recovery

### Common Rollback Issues
- **Merge conflicts during revert**: Provide resolution guidance
- **Missing target commit**: Validate commit existence
- **Cache inconsistencies**: Rebuild cache if needed
- **Workflow conflicts**: Graceful workflow termination

### Emergency Recovery
- **Immediate undo**: Use Git reflog and stash recovery
- **Cache corruption**: Rebuild from existing cache entries
- **Partial rollback**: Manual recovery instructions
- **Branch protection**: Respect protected branch policies

This comprehensive revert system provides safe, predictable rollback capabilities that maintain both code and agent cache consistency.