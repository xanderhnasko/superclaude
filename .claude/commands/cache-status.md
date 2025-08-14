---
description: Display comprehensive cache status, hit rates, and token efficiency metrics
argument-hint: [--detailed] [--agent <agent-name>] [--cleanup]
tools: [read, bash, task]
---

# Cache Status Report

Display comprehensive caching performance metrics and token efficiency statistics.

## Usage
- `/cache-status` - Overview of cache performance
- `/cache-status --detailed` - Detailed breakdown by agent
- `/cache-status --agent planner` - Status for specific agent
- `/cache-status --cleanup` - Show cleanup recommendations

## Cache Performance Analysis

### 1. Overall Statistics
Read cache manifest and display:
- **Total Cache Entries**: Number of cached agent outputs
- **Overall Hit Rate**: Percentage of agent requests served from cache
- **Token Savings**: Total tokens saved through caching
- **Storage Usage**: Cache directory size and cleanup status

### 2. Per-Agent Breakdown
For each agent, show:
- **Cache Hit Rate**: Percentage of requests served from cache
- **Token Savings**: Tokens saved vs. fresh execution
- **Average Cache Age**: How long cache entries remain valid
- **Most Effective Scopes**: Which file patterns cache best

### 3. Git Integration Status
- **Last Analysis Commit**: Last commit with valid cache entries
- **Current Branch**: Active Git branch
- **Pending Changes**: Files changed since last cache update
- **Cache Invalidation**: Which caches need updating

### 4. Performance Recommendations
Based on analysis, suggest:
- **Cache Strategy Improvements**: Scope adjustments, TTL changes
- **Storage Optimizations**: Cleanup opportunities, compression
- **Workflow Optimizations**: Agent scheduling improvements
- **Token Efficiency Gains**: Potential for better caching

## Implementation Steps

### Step 1: Read Cache Manifest
```bash
# Load current cache statistics
cat .claude/cache/cache-manifest.json
```

### Step 2: Analyze Git State  
```bash
# Check current Git status
git rev-parse HEAD  # Current commit
git status --porcelain  # Pending changes
git diff --name-only HEAD~1 HEAD  # Recent changes
```

### Step 3: Calculate Cache Effectiveness
For each agent:
- Count cache hits vs misses
- Calculate token savings (cached vs fresh execution costs)
- Determine average cache age and validity
- Identify most/least effective cache patterns

### Step 4: Storage Analysis
```bash
# Check cache storage usage
du -sh .claude/cache/  # Total cache size
find .claude/cache/agent-outputs/ -name "*.json" | wc -l  # Entry count
find .claude/cache/agent-outputs/ -mtime +7  # Old entries
```

### Step 5: Generate Report
Create formatted output showing:

```
=== Super Claude Code Cache Status ===

📊 Overall Performance:
   Cache Entries: 127 files
   Hit Rate: 73.2% (saves ~40% tokens)
   Token Savings: 15,420 tokens
   Storage: 45.2 MB

📈 Agent Performance:
   🏗️  Planner:     85% hit rate, 4,250 tokens saved
   🧪 Tester:       67% hit rate, 3,180 tokens saved  
   🔍 Reviewer:     71% hit rate, 2,890 tokens saved
   🏛️  Architect:   89% hit rate, 5,100 tokens saved

🔄 Git Integration:
   Last Analysis: abc123f (3 commits behind)
   Current Branch: feature/auth
   Stale Caches: 12 entries need refresh

💡 Recommendations:
   → Run cache-optimize to clean 8.3 MB of old entries
   → Tester cache scope too broad - consider feature-based scoping
   → High architect hit rate suggests good architectural stability
```

### Step 6: Detailed Analysis (--detailed flag)
When detailed flag is used:
- Show individual cache entries with metadata
- Display file dependency analysis
- Show cache invalidation patterns
- Provide scope optimization suggestions

### Step 7: Agent-Specific Analysis (--agent flag)
When specific agent requested:
- Deep dive into that agent's cache performance
- Show cache entry timeline
- Display invalidation patterns
- Suggest scope or TTL optimizations

### Step 8: Cleanup Recommendations (--cleanup flag)
When cleanup flag is used:
- Identify stale or low-value cache entries
- Calculate storage savings from cleanup
- Show safe-to-remove entries
- Provide cleanup commands

## Error Handling

### Cache Manifest Missing
If no cache manifest exists:
```
⚠️  No cache manifest found. Cache system not yet initialized.
   Run any agent command to initialize caching system.
```

### Git Repository Issues
If Git commands fail:
```
⚠️  Git repository access issues detected.
   Cache invalidation may not work correctly.
   Verify Git repository status.
```

### Storage Issues
If cache directory problems:
```
⚠️  Cache directory issues detected.
   Check permissions and disk space.
   Cache performance may be degraded.
```

This command provides comprehensive visibility into the caching system's performance and guides users toward optimal token efficiency.