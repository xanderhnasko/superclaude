---
description: Real-time agent activity monitoring with cache status and performance indicators
argument-hint: [--live] [--agent <agent-name>] [--history]
tools: [read, bash, task]
---

# Agent Status Monitor

Real-time visibility into agent execution, cache utilization, and performance metrics with visual indicators.

## Usage Options

- `/agent-status` - Current agent activity overview
- `/agent-status --live` - Live updating status during workflow execution  
- `/agent-status --agent planner` - Detailed status for specific agent
- `/agent-status --history` - Recent agent execution history with cache performance

## Status Display Features

### 1. Live Agent Activity Dashboard

```
🎯 Agent Activity Dashboard - Live View

🚀 Currently Active Agents:
   ⚡ planner          [LIVE] Analyzing authentication requirements...
      📍 Step: Reading existing auth patterns  
      ⏱️  Runtime: 1m 23s | Est. Remaining: ~45s
      🪙 Tokens: ~340 consumed | Est. Total: ~420
      
   ⚡ architect        [CACHED] Using cached analysis from commit def456a  
      📍 Result: Architectural review (cached, 0 tokens)
      ✅ Complete: Instant retrieval (1.2KB cached data)
      
🔄 Parallel Group: review_checks (2/3 complete)  
   ✅ static-analyzer [CACHED] Complete (commit abc123f, 0 tokens)
   ⚡ security-scanner [LIVE] Scanning for vulnerabilities... (1m 45s)
   ⚡ style-checker    [LIVE] Validating code style... (45s)
   
⏸️  Queued Agents:
   📝 tester           [PENDING] Waiting for planner results
   🔍 reviewer         [PENDING] Waiting for parallel group completion
   
📊 Session Efficiency:
   Cache Hit Rate: 4/7 agents (57%)
   Token Savings: 1,240 tokens saved
   Time Savings: ~8 minutes saved
```

### 2. Agent-Specific Detailed View

When using `--agent planner`:

```
🏗️ Planner Agent - Detailed Status

Current Status: ⚡ ACTIVE - Breaking down authentication feature

Execution Timeline:
   🚀 Started: 2m 15s ago
   📍 Current Phase: "Analyzing existing patterns"
   📈 Progress: ~65% complete (estimated)
   ⏱️  ETA: ~1m 30s remaining
   
Tool Usage Activity:
   ✅ Read: src/auth/current_auth.py (completed)
   ✅ Read: tests/auth/test_patterns.py (completed)  
   ⚡ Read: docs/ARCHITECTURE.md (in progress...)
   📋 Next: Generate implementation plan
   
Token Consumption:
   🪙 Current: 287 tokens consumed
   📊 Estimated Total: ~380 tokens  
   💾 Cache Status: Cache miss (new feature scope)
   🔄 Will Cache: Yes (expires in 7 days)
   
Performance Context:
   📈 Recent Avg: 420 tokens/execution
   ⚡ Cache Hit Rate: 85% (last 30 days)
   🎯 Efficiency Rank: #2 of 8 agents (excellent)
   
Input Context:
   📝 Feature: "Add user authentication with JWT tokens"
   📁 Scope: src/auth/, tests/auth/, docs/auth.md
   🔗 Dependencies: None (initial planning phase)
   
Expected Output:
   📋 Implementation plan with phases and tasks
   ✅ Clear acceptance criteria for each task
   🧪 TDD-compatible task breakdown
   ⏱️  Complexity estimates and dependencies
```

### 3. Cache Performance Indicators

```
💾 Cache Performance Overview:

Real-Time Cache Activity:
   🔍 Checking: architect agent cache for auth feature...
      ✅ HIT: Found cached analysis (commit def456a, 2 hours old)
      💾 Size: 2.1KB | 🪙 Saves: 450 tokens | ⚡ Instant retrieval
      
   🔍 Checking: planner agent cache for auth feature...
      ❌ MISS: No cache found (new feature scope)
      🚀 Executing: Fresh analysis needed
      
   🔍 Checking: tester agent cache for auth tests...
      ⚠️  EXPIRED: Cache found but invalidated (src/auth/ changed)
      🔄 Refreshing: Cache will be updated after execution

Cache Efficiency Trends:
   📊 Today: 67% hit rate (12 hits, 6 misses)
   📈 This Week: 73% hit rate (improving)
   🎯 Top Performers: architect (91%), planner (87%), context-synth (94%)
   📉 Improvement Needed: debugger (32%), tester (58%)
   
Cache Storage Health:
   💾 Total Size: 47.2 MB (healthy)
   📁 Total Entries: 134 cached results  
   🗑️  Cleanup Recommendation: 8.3 MB of old entries can be removed
   ⚡ Performance: Excellent (fast retrieval)
```

### 4. Visual Progress Indicators

During active agent execution, show dynamic progress:

```
⚡ architect agent: [LIVE] Analyzing system architecture...

Progress Visualization:
   Reading Files    ████████████████████ 100% ✅
   Pattern Analysis ███████████▒▒▒▒▒▒▒▒▒  60% ⚡
   Recommendations  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   0% ⏳
   
Tool Activity:
   [09:42:15] 📖 Reading src/core/models.py... ✅
   [09:42:18] 📖 Reading src/auth/middleware.py... ✅
   [09:42:22] 🔍 Analyzing authentication patterns... ⚡
   [09:42:25] 🔍 Checking architectural constraints... ⚡
   [09:42:28] 📝 Generating recommendations... ⏳
   
Performance Metrics:
   🪙 Tokens: 234 consumed (est. 380 total)
   ⏱️  Time: 1m 45s elapsed (est. 2m 30s total)
   📊 Efficiency: Good (on track for estimates)
```

### 5. Historical Activity Analysis

When using `--history`:

```
📈 Agent Execution History (Last 24 Hours):

Recent Executions:
   [2 hours ago] 🏗️ planner → ✅ Complete (auth feature) 
      💾 Cache: MISS | 🪙 Tokens: 387 | ⏱️ Duration: 2m 15s
      
   [2 hours ago] 🏛️ architect → ✅ Complete (auth review)
      💾 Cache: HIT | 🪙 Tokens: 0 (saved 445) | ⏱️ Duration: instant
      
   [3 hours ago] 🧪 tester → ✅ Complete (auth tests)
      💾 Cache: MISS | 🪙 Tokens: 423 | ⏱️ Duration: 2m 45s
      
   [4 hours ago] 🔍 reviewer → ✅ Complete (code review)
      💾 Cache: HIT | 🪙 Tokens: 0 (saved 398) | ⏱️ Duration: instant

Performance Summary:
   🎯 Total Executions: 12 agents
   💾 Cache Hit Rate: 58% (7 hits, 5 misses)
   🪙 Total Tokens: 2,340 consumed (would be 4,180 without cache)
   💰 Token Savings: 1,840 tokens (44% efficiency)
   ⏱️  Time Savings: ~14 minutes saved via caching
   
Efficiency Insights:
   🏆 Best Cache Performance: architect (100% hit rate)
   📈 Improving: planner cache hit rate up 23% this week
   ⚠️  Attention Needed: debugger cache effectiveness low (context-dependent)
   💡 Optimization Opportunity: tester scope refinement could improve hit rate
```

### 6. Agent Health Monitoring

```
🔧 Agent System Health:

Agent Availability:
   ✅ planner          [READY] Tools: read | Trigger patterns: active
   ✅ architect        [READY] Tools: read, grep | Cache: optimal  
   ✅ tester          [READY] Tools: read, write, bash | Write paths: valid
   ✅ reviewer        [READY] Tools: read, bash | All systems functional
   ⚠️  debugger        [READY] Tools: read, grep, bash | Cache suboptimal
   ✅ documenter      [READY] Tools: read, write | Ready for documentation
   ✅ context-synth   [READY] Tools: read, glob | Cache excellent
   ✅ workflow-orchestrator [READY] All tools available
   
System Integration:
   ✅ Git Integration: Repository accessible, commit tracking functional
   ✅ Cache System: Storage healthy, invalidation rules active
   ✅ Workflow Engine: All workflows validated and ready
   ✅ Token Tracking: Monitoring active, statistics updating
   
Performance Indicators:
   🚀 Response Time: Excellent (avg 0.3s startup per agent)
   💾 Cache Performance: Good (73% overall hit rate)
   🔧 Tool Usage: Optimal (agents actively using assigned tools)
   📊 Error Rate: Excellent (<1% agent failures)
```

This agent status system provides comprehensive visibility into the multi-agent system's operation with clear cache indicators and performance metrics.