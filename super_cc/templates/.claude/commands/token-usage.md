---
description: Display comprehensive token usage statistics with cache hit/miss analysis and efficiency metrics
argument-hint: [--detailed] [--agent <agent-name>] [--session] [--feature <feature-name>]
tools: [read, bash, task]
---

# Token Usage Analysis

Comprehensive token usage tracking with cache efficiency analysis for cost optimization.

## Usage Options

- `/token-usage` - Overall token usage summary with cache impact
- `/token-usage --detailed` - Detailed breakdown by agent and operation
- `/token-usage --agent planner` - Token usage for specific agent
- `/token-usage --session` - Current session token consumption
- `/token-usage --feature auth` - Token usage for specific feature development

## Token Tracking Features

### 1. Overall Usage Summary

**High-Level Metrics:**
```
🪙 Token Usage Summary (Last 7 Days):

Total Consumed: 45,230 tokens
Cache Savings: 15,420 tokens (25.4% efficiency)
Actual Cost: 29,810 tokens  
Est. Without Caching: 45,230 tokens

Daily Breakdown:
   Mon: 8,420 tokens (3,200 cached) - 38% efficiency
   Tue: 6,890 tokens (2,100 cached) - 30% efficiency  
   Wed: 9,230 tokens (3,800 cached) - 41% efficiency
   ...

Top Token Consumers:
   🏗️  Architect: 12,450 tokens (4,200 saved via cache)
   🧪 Tester: 10,230 tokens (3,800 saved via cache)
   🔍 Reviewer: 8,940 tokens (2,900 saved via cache)
   📋 Planner: 7,120 tokens (2,850 saved via cache)
```

### 2. Cache Efficiency Analysis

**Cache Impact on Token Consumption:**
```
📊 Cache Efficiency Breakdown:

By Agent Type:
   🏛️  Architect:  Hit Rate 89% → 4,200 tokens saved
   🧪 Tester:     Hit Rate 67% → 3,800 tokens saved
   📋 Planner:    Hit Rate 85% → 2,850 tokens saved
   🔍 Reviewer:   Hit Rate 71% → 2,900 tokens saved
   🐛 Debugger:   Hit Rate 45% → 1,100 tokens saved (low due to context-specific debugging)

Cache ROI Analysis:
   Cache Storage: 45.2 MB
   Token Savings: 15,420 tokens/week
   Efficiency Gain: 34.1% cost reduction
   
   🎯 Optimization Opportunity: Tester cache hit rate improvement could save additional 1,800 tokens/week
```

### 3. Feature-Based Token Tracking

**Token Usage by Development Feature:**
```
🎯 Feature Development Token Usage:

Authentication Feature (auth):
   Total Investment: 8,450 tokens
   Breakdown:
   - Planning: 1,200 tokens (850 cached)
   - Architecture: 1,800 tokens (1,400 cached)
   - Testing: 2,400 tokens (1,200 cached)
   - Implementation: 1,950 tokens (0 cached - main agent)
   - Review: 1,100 tokens (650 cached)
   
   Cache Efficiency: 49.3% (4,100 tokens saved)
   Feature ROI: High (complex feature, excellent cache utilization)

API Integration Feature (api):
   Total Investment: 6,230 tokens
   Cache Efficiency: 31.2% (1,950 tokens saved)
   Feature ROI: Medium (straightforward feature, moderate caching)
```

### 4. Session-Based Tracking

**Current Session Analysis:**
```
⚡ Current Session Token Usage:

Session Started: 2 hours 15 minutes ago
Total Tokens: 2,340 tokens
Cache Hits: 8 operations (1,450 tokens saved)
Cache Misses: 3 operations (890 tokens fresh execution)

Session Efficiency: 62.0% cache hit rate

Agent Activity This Session:
   📋 Planner: 450 tokens (cache hit - feature planning reused)
   🧪 Tester: 890 tokens (cache miss - new test scenarios)
   🔍 Reviewer: 680 tokens (cache hit - similar code patterns)
   🏛️ Architect: 320 tokens (cache hit - architectural context reused)

Projected Session Savings: 2,340 tokens consumed vs 3,790 without caching (38.3% savings)
```

### 5. Cost Analysis & Projections

**Cost Impact Analysis:**
```
💰 Token Cost Analysis:

Current Consumption Pattern:
   Weekly Average: 45,230 tokens
   Monthly Projection: ~190,000 tokens
   
   With Current Cache (34% efficiency):
   Actual Weekly: 29,810 tokens  
   Monthly Projection: ~125,000 tokens
   Monthly Savings: ~65,000 tokens

Optimization Scenarios:
   📈 If Tester Cache Improved to 80%:
      Additional Weekly Savings: 1,800 tokens
      Monthly Impact: ~7,500 tokens
      
   📈 If Incremental Review Caching Added:
      Additional Weekly Savings: 2,200 tokens  
      Monthly Impact: ~9,200 tokens
      
   🎯 Fully Optimized Potential:
      Total Monthly Savings: ~81,700 tokens (43% efficiency)
```

### 6. Agent Performance Analysis

**Agent-Specific Token Efficiency:**
```
🔍 Agent Performance Deep Dive:

Architect Agent:
   ├── Total Usage: 12,450 tokens (weekly)
   ├── Cache Hits: 89% (excellent)
   ├── Cache Savings: 4,200 tokens
   ├── Avg. Operation: 420 tokens
   └── Efficiency Notes: High stability, architectural changes infrequent

Tester Agent:
   ├── Total Usage: 10,230 tokens (weekly)  
   ├── Cache Hits: 67% (improvement opportunity)
   ├── Cache Savings: 3,800 tokens
   ├── Avg. Operation: 380 tokens
   └── Efficiency Notes: Scope too broad, feature-based caching recommended

Planner Agent:
   ├── Total Usage: 7,120 tokens (weekly)
   ├── Cache Hits: 85% (very good)
   ├── Cache Savings: 2,850 tokens  
   ├── Avg. Operation: 290 tokens
   └── Efficiency Notes: Good feature-based reuse, architectural integration effective

Reviewer Agent:
   ├── Total Usage: 8,940 tokens (weekly)
   ├── Cache Hits: 71% (good)
   ├── Cache Savings: 2,900 tokens
   ├── Avg. Operation: 450 tokens
   └── Efficiency Notes: Incremental review could improve efficiency significantly
```

### 7. Trend Analysis

**Usage Trends Over Time:**
```
📈 Token Usage Trends (Last 30 Days):

Usage Pattern:
   Week 1: 52,400 tokens (28% cache efficiency)
   Week 2: 48,900 tokens (31% cache efficiency)  
   Week 3: 46,200 tokens (33% cache efficiency)
   Week 4: 45,230 tokens (34% cache efficiency)
   
   Trend: ↓ 13.7% reduction in token usage
          ↑ 21.4% improvement in cache efficiency

Cache Evolution:
   Initial Cache Size: 12.1 MB, 47 entries
   Current Cache Size: 45.2 MB, 127 entries  
   Cache Growth: 273% increase in cached knowledge
   
   Quality Metrics:
   - Hit Rate Improvement: 28% → 34% (+21.4%)
   - Storage Efficiency: 2.8 tokens saved per MB → 3.4 tokens saved per MB
```

### 8. Recommendations

**Token Optimization Recommendations:**
```
💡 Optimization Recommendations:

High Impact (>1,000 tokens/week savings):
   🎯 Improve Tester cache scoping (potential: 1,800 tokens/week)
   🎯 Add incremental Review caching (potential: 2,200 tokens/week)
   🎯 Cross-session Architect context reuse (potential: 1,200 tokens/week)

Medium Impact (500-1,000 tokens/week):
   🔄 Optimize Debugger caching strategy (potential: 800 tokens/week)
   🔄 Add feature-based Planner inheritance (potential: 600 tokens/week)

Low Impact (<500 tokens/week):
   ⚡ Context synthesis result sharing (potential: 300 tokens/week)
   ⚡ Workflow step result caching (potential: 200 tokens/week)

Immediate Actions:
   1. Run /cache-optimize --analyze for detailed improvement plan
   2. Update invalidation-rules.yaml with tester scoping improvements
   3. Enable incremental review mode for small changes
   4. Set up automated cache warming for common workflows
```

## Error Handling

### Missing Data
- Handle missing cache manifest gracefully
- Provide estimates when exact data unavailable
- Suggest initialization steps for comprehensive tracking

### Git Integration Issues  
- Fallback to basic usage tracking without Git-based analysis
- Warn about reduced accuracy
- Provide manual cache management options

This comprehensive token usage analysis enables data-driven optimization of the agent caching system for maximum cost efficiency.