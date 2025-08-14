---
description: Configure token efficiency modes - Conservative/Standard/YOLO with cache-aware agent scheduling
argument-hint: [conservative|standard|yolo] [--status] [--auto]
tools: [read, write, bash]
---

# Eco-Mode Configuration

Intelligent token usage management system with three efficiency modes and cache-aware agent scheduling.

## Usage Options

- `/eco-mode status` - Show current mode and efficiency metrics
- `/eco-mode conservative` - Maximum token efficiency, sequential execution
- `/eco-mode standard` - Balanced performance and efficiency (default)
- `/eco-mode yolo` - Maximum agent utilization, parallel execution
- `/eco-mode auto` - Automatically adjust based on project characteristics

## Mode Descriptions

### 🌿 Conservative Mode - Maximum Token Efficiency
**Philosophy**: "Every token counts - maximize cache usage and minimize redundant work"

**Characteristics:**
- **Sequential Agent Execution**: One agent at a time to maximize context reuse
- **Aggressive Cache Utilization**: Always check cache first, extend cache TTL
- **Minimal Parallel Processing**: Avoid parallel execution overhead
- **Scoped Agent Usage**: Only invoke agents when absolutely necessary
- **Cache Warming**: Proactively warm caches during idle time

**Agent Scheduling Strategy:**
```yaml
conservative_mode:
  parallel_execution: false
  cache_first_policy: strict
  agent_invocation: minimal
  cache_ttl_multiplier: 2.0
  
  agent_priorities:
    - context-synth     # Always run first to establish context
    - architect         # High cache hit rate, run early  
    - planner           # High cache hit rate, reusable
    - tester            # Only if no cached tests available
    - reviewer          # Only for final review
    - debugger          # On-demand only
    
  workflow_optimizations:
    skip_redundant_reviews: true
    batch_similar_operations: true
    extend_cache_validity: true
```

**Expected Efficiency**: 50-70% token savings vs. YOLO mode

### ⚖️ Standard Mode - Balanced Performance
**Philosophy**: "Balanced approach - good efficiency with reasonable speed"

**Characteristics:**
- **Selective Parallel Execution**: Parallel for independent operations only
- **Smart Cache Usage**: Check cache first, reasonable TTL
- **Moderate Agent Usage**: Invoke agents when beneficial
- **Adaptive Scheduling**: Adjust based on cache hit rates

**Agent Scheduling Strategy:**
```yaml
standard_mode:
  parallel_execution: selective
  cache_first_policy: normal
  agent_invocation: balanced
  cache_ttl_multiplier: 1.0
  
  parallel_groups:
    review_group:      # Independent review operations
      - static-analyzer
      - security-scanner
      - style-checker
    
    analysis_group:    # Can run together when cache miss
      - architect
      - context-synth
      
  workflow_optimizations:
    cache_aware_scheduling: true
    parallel_independent_ops: true
    moderate_cache_warming: true
```

**Expected Efficiency**: 30-45% token savings vs. YOLO mode

### 🚀 YOLO Mode - Maximum Agent Utilization
**Philosophy**: "Speed over efficiency - use all available agents and parallelization"

**Characteristics:**
- **Full Parallel Execution**: Run agents simultaneously whenever possible
- **Comprehensive Agent Usage**: Invoke all relevant agents for thorough analysis
- **Fresh Analysis Priority**: Prefer fresh execution over cache when unsure
- **Maximum Thoroughness**: Complete workflow coverage

**Agent Scheduling Strategy:**
```yaml
yolo_mode:
  parallel_execution: aggressive
  cache_first_policy: relaxed
  agent_invocation: comprehensive
  cache_ttl_multiplier: 0.5
  
  parallel_groups:
    full_analysis:
      - architect
      - planner  
      - context-synth
      
    comprehensive_review:
      - tester
      - reviewer
      - debugger
      - static-analyzer
      - security-scanner
      
  workflow_optimizations:
    run_all_agents: true
    fresh_analysis_bias: true
    comprehensive_coverage: true
```

**Expected Efficiency**: Baseline (maximum token usage for maximum thoroughness)

### 🤖 Auto Mode - Intelligent Adaptation
**Philosophy**: "Adapt mode based on project characteristics and cache performance"

**Adaptation Criteria:**
- **Project Size**: Large projects → Conservative, Small projects → Standard
- **Cache Hit Rate**: High hit rate → Conservative, Low hit rate → YOLO  
- **Development Phase**: Planning → YOLO, Maintenance → Conservative
- **Recent Activity**: High activity → Standard, Low activity → Conservative

```yaml
auto_mode:
  adaptation_rules:
    project_size:
      large_project: conservative    # >1000 files
      medium_project: standard       # 100-1000 files
      small_project: yolo           # <100 files
      
    cache_performance:
      high_hit_rate: conservative    # >80% hit rate
      medium_hit_rate: standard      # 50-80% hit rate
      low_hit_rate: yolo            # <50% hit rate
      
    development_phase:
      planning: yolo                # Comprehensive analysis needed
      active_development: standard   # Balanced approach
      maintenance: conservative      # Incremental changes
      
    recent_activity:
      high_activity: standard       # >10 commits/week
      low_activity: conservative    # <3 commits/week
```

## Mode Configuration Files

### Current Mode Storage
Mode configuration is stored in `.claude/settings/eco-mode.json`:

```json
{
  "current_mode": "standard",
  "mode_history": [
    {
      "mode": "conservative", 
      "set_at": "2025-01-14T10:00:00Z",
      "reason": "user_request"
    }
  ],
  "auto_mode_settings": {
    "enabled": false,
    "last_evaluation": "2025-01-14T09:00:00Z",
    "adaptation_reasons": []
  },
  "performance_tracking": {
    "conservative": {
      "sessions": 5,
      "avg_tokens_saved": 67,
      "avg_completion_time": "15min"
    },
    "standard": {
      "sessions": 12, 
      "avg_tokens_saved": 38,
      "avg_completion_time": "8min"
    },
    "yolo": {
      "sessions": 3,
      "avg_tokens_saved": 0,
      "avg_completion_time": "4min"
    }
  }
}
```

### Workflow Integration
Each workflow can be modified based on eco-mode:

```yaml
# .claude/workflows/feature-development.yaml
steps:
  - name: context_setup
    agent: context-synth
    eco_mode_overrides:
      conservative: 
        cache_first: strict
        scope: minimal
      yolo:
        cache_first: relaxed
        scope: comprehensive
```

## Status Display

### Current Mode Status
```
🔧 Eco-Mode Status:

Current Mode: 🌿 Conservative
Set: 2 hours ago (user request)
Next Auto Evaluation: Disabled

Performance This Session:
   Tokens Saved: 420 tokens (67% efficiency)
   Cache Hits: 15/18 operations (83% hit rate)
   Completion Time: +8 minutes vs Standard mode
   
Recent History:
   Last 7 days: 5 Conservative, 2 Standard sessions
   Average Efficiency: 64% token savings
   User Satisfaction: High (based on usage patterns)

Mode Recommendations:
   💡 Current cache hit rate (83%) excellent for Conservative mode
   💡 Project size (240 files) well-suited for Conservative approach
   ⚠️ Consider Standard mode if completion time becomes critical
```

### Auto Mode Analysis
When in auto mode, show adaptation reasoning:

```
🤖 Auto-Mode Analysis:

Current Recommendation: 🌿 Conservative Mode

Factors Analyzed:
   📏 Project Size: 240 files (Medium) → Standard preference
   📊 Cache Hit Rate: 83% (High) → Conservative preference  
   🏗️ Dev Phase: Maintenance (Low activity) → Conservative preference
   📈 Recent Activity: 2 commits this week → Conservative preference
   
   Final Decision: Conservative (3/4 factors favor it)

Adaptation History:
   Yesterday: Switched Standard → Conservative (cache hit rate improved)
   3 days ago: Initial Auto mode enabled
   
Next Evaluation: In 6 hours (or on significant project changes)
```

## Mode Change Implementation

### Switching Modes
When changing modes:

1. **Save Current State**: Store performance metrics for current mode
2. **Update Configuration**: Write new mode to settings file
3. **Adjust Active Workflows**: Update any running workflows
4. **Warm Caches**: Pre-warm caches if switching to Conservative
5. **Log Change**: Track mode changes for analysis

### Performance Tracking
Each mode change logs:
- Token usage before/after
- Completion times
- User satisfaction indicators
- Cache performance changes

### Validation
Mode changes are validated:
- Ensure mode is appropriate for current project
- Warn about performance trade-offs
- Provide recommendations for optimal usage

This eco-mode system provides fine-grained control over token efficiency vs. speed trade-offs with intelligent automation options.