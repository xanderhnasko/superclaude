---
description: Optimize cache performance through cleanup, invalidation analysis, and efficiency improvements
argument-hint: [--cleanup] [--analyze] [--warm] [--force-refresh]
tools: [read, write, bash, task]
---

# Cache Optimization Command

Optimize the agent cache system for maximum token efficiency and performance.

## Usage Options

- `/cache-optimize` - Run full optimization analysis
- `/cache-optimize --cleanup` - Remove stale and low-value cache entries
- `/cache-optimize --analyze` - Deep analysis of cache patterns and efficiency
- `/cache-optimize --warm` - Pre-warm commonly used caches
- `/cache-optimize --force-refresh` - Force refresh all caches for current commit

## Optimization Operations

### 1. Cache Cleanup (--cleanup)

**Identify Cleanup Candidates:**
- Entries older than configured TTL
- Caches for commits no longer in Git history
- Low hit-rate entries consuming significant space
- Duplicate or redundant cache entries

**Safe Cleanup Process:**
```bash
# Find old cache entries
find .claude/cache/agent-outputs/ -name "*.json" -mtime +7

# Check which commits still exist in Git
git log --oneline --since="1 month ago"

# Remove caches for non-existent commits safely
```

**Cleanup Report:**
```
🧹 Cache Cleanup Results:
   Removed: 23 stale entries (12.4 MB freed)
   Kept: 104 active entries (32.8 MB)
   Space Saved: 27.4% reduction in cache size
   
   By Age:
   - >7 days: 15 entries removed (8.1 MB)
   - >30 days: 8 entries removed (4.3 MB)
   
   By Agent:
   - debugger: 12 entries removed (debugger results expire quickly)
   - tester: 6 entries removed (test scope changed)
   - planner: 3 entries removed (old feature plans)
```

### 2. Cache Analysis (--analyze)

**Performance Analysis:**
- Cache hit rate trends over time
- Agent-specific efficiency patterns  
- File change impact on cache invalidation
- Storage efficiency and fragmentation

**Scope Analysis:**
- Identify overly broad cache scopes
- Find opportunities for feature-based scoping
- Analyze file dependency patterns
- Suggest invalidation rule improvements

**Token Efficiency Analysis:**
- Calculate actual token savings from caching
- Project efficiency improvements from better scoping
- Identify agents benefiting most/least from caching
- Recommend workflow optimizations

**Analysis Report:**
```
📊 Cache Efficiency Analysis:

Hit Rate Trends (Last 30 Days):
   Overall: 68% → 73% (improving)
   Planner: 82% → 85% (stable, high performance)
   Tester: 45% → 67% (improved with scope refinement)
   Architect: 89% → 91% (excellent stability)

Scope Optimization Opportunities:
   🔍 Tester: Current scope too broad (src/**/*) 
      → Recommend feature-based scoping (30% improvement potential)
   
   🏗️ Planner: Good scoping for feature work
      → Consider architecture-change invalidation refinement
   
   🔍 Reviewer: High invalidation rate from broad source patterns
      → Consider diff-based incremental review caching

Token Savings Projection:
   Current: 15,420 tokens saved (40% efficiency)
   Optimized: ~22,000 tokens saved (55% efficiency potential)
   
   Improvement Areas:
   - Better tester scoping: +2,800 tokens/month
   - Incremental reviewer caching: +3,200 tokens/month  
   - Cross-session context reuse: +1,600 tokens/month
```

### 3. Cache Warming (--warm)

**Predictive Warming:**
- Identify commonly used agent/scope combinations
- Pre-run agents for frequently accessed patterns
- Warm caches for current branch's likely needs
- Build caches for common development scenarios

**Warm Targets:**
- Context synthesis for main project files
- Architecture analysis for core components
- Planning for typical feature patterns
- Review preparation for active development areas

**Warming Process:**
```bash
# Identify warming candidates
git log --name-only --since="1 week ago" | sort | uniq -c | sort -nr

# Common file patterns from recent development
# Run lightweight agent operations to warm caches
```

### 4. Force Refresh (--force-refresh)

**Complete Cache Refresh:**
- Invalidate all current caches
- Force fresh agent execution for current Git state
- Rebuild cache manifest from scratch
- Update all cache metadata

**Use Cases:**
- After major codebase changes
- When cache corruption is suspected
- After updating agent definitions
- For establishing baseline performance

## Smart Invalidation Analysis

### File Pattern Impact Analysis
Analyze which file changes cause the most cache invalidations:

```
📈 Invalidation Pattern Analysis:

High-Impact Files (frequent invalidations):
   📄 docs/ARCHITECTURE.md → Invalidates: architect, planner (4x this week)
   📄 src/core/models.py → Invalidates: architect, reviewer, tester (6x this week)
   📄 .claude/agents/*.md → Invalidates: all agents (2x this week)

Low-Impact Files (rare invalidations):
   📄 tests/unit/* → Minimal invalidation outside tester
   📄 docs/README.md → Only documenter invalidation
   📄 src/utils/* → Limited architect impact

Optimization Recommendations:
   → Consider more granular scoping for core/models.py changes
   → Architect cache very sensitive to architecture doc changes (expected)
   → Test file changes appropriately scoped
```

### Dependency Chain Analysis
Show how file changes cascade through agent dependencies:

```
🔗 Cache Dependency Chains:

src/auth/models.py changed →
   ├── architect (invalidated - model structure analysis)
   ├── planner (invalidated - feature dependencies)  
   ├── tester (invalidated - test scope includes models)
   └── reviewer (invalidated - source code review)
   
docs/API.md changed →
   ├── documenter (invalidated - documentation scope)
   ├── planner (cached - no implementation impact)
   └── architect (cached - no structural changes)

Optimization Potential:
   → Model changes have appropriate broad impact
   → Documentation changes well-isolated
   → Consider API documentation separate from implementation planning
```

## Performance Recommendations

Based on analysis, provide specific optimization suggestions:

### Scope Refinement
```yaml
# Suggested invalidation rule improvements
agent_rules:
  tester:
    patterns:
      - "tests/**/*"
      - "src/{{feature_scope}}/**/*"  # Feature-scoped instead of src/**/*
      
  reviewer:
    patterns:
      - "src/**/*"
    incremental: true  # Enable diff-based review for small changes
```

### Workflow Optimizations
```yaml
# Cache-aware workflow improvements
workflows:
  feature-development:
    cache_strategy: "aggressive"  # Use all available caches
    cache_scope: "feature"       # Limit cache scope to feature files
    
  bug-fix:
    cache_strategy: "conservative"  # Quick fixes, minimal caching overhead
    cache_scope: "minimal"         # Only cache expensive operations
```

This command provides comprehensive cache optimization to maximize token efficiency while maintaining agent effectiveness.