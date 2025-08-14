---
description: Execute YAML-defined workflows with orchestrated agent coordination
argument-hint: workflow-name [--param key=value] [--resume] [--dry-run]
tools: [read, bash, task]
bash-allowlist: ["find", "cat", "ls", "git status", "pytest"]
---

# Workflow Orchestrator Command

**ROLE:** Workflow Orchestrator  
**GOAL:** Execute complex multi-agent workflows based on YAML configurations.

## Command Usage

Execute workflow: `/workflow <workflow-name> [options]`

**Available Workflows:**
- `feature-development` - Standard TDD workflow for new features
- `bug-fix` - Diagnostic workflow for bug resolution  
- `refactoring` - Code cleanup and improvement workflow
- `review-only` - Comprehensive code review pipeline

**Options:**
- `--param key=value` - Set workflow parameters
- `--resume` - Resume interrupted workflow from last state
- `--dry-run` - Show workflow steps without execution
- `--parallel` - Enable parallel execution where possible

## Workflow Execution Process

### Step 1: Load and Validate Workflow
```bash
# Load workflow YAML from .claude/workflows/
WORKFLOW_FILE=".claude/workflows/${WORKFLOW_NAME}.yaml"
```

Parse workflow parameters and validate required inputs.

### Step 2: Initialize Workflow State
Create state tracking in `.claude/state/workflow-${WORKFLOW_NAME}-${TIMESTAMP}.json`:
```json
{
  "workflow_name": "feature-development",
  "status": "running",
  "current_step": 0,
  "parameters": {...},
  "step_outputs": {},
  "started_at": "2025-01-14T10:00:00Z"
}
```

### Step 3: Execute Workflow Steps
For each step in the workflow:

**Sequential Steps:**
- Load step configuration and inputs
- Check conditions (if any)
- Execute agent or command
- Store output variables
- Update workflow state

**Parallel Groups:**
- Identify parallel execution opportunities
- Launch parallel agents/commands
- Coordinate result aggregation
- Handle partial failures gracefully

**Loop Steps:**
- Track iteration count
- Evaluate loop conditions
- Execute substeps
- Handle max iteration limits

### Step 4: State Management
Track workflow progress with persistent state:
- Current step position
- Variable bindings
- Agent outputs
- Error conditions
- Completion status

### Step 5: Error Handling
- Retry failed steps based on configuration
- Implement fallback strategies
- Preserve state for manual intervention
- Enable workflow resumption

## Agent Coordination Patterns

### Variable Substitution
Replace template variables in workflow steps:
- `{{parameters.feature_description}}` → actual parameter value
- `{{project_context}}` → output from context-synth agent
- `{{test_results}}` → output from test execution

### Conditional Execution
Evaluate conditions before step execution:
- `{{parameters.major_feature}}` → boolean parameter
- `on_test_failure` → execute only when tests fail
- `on_tests_pass` → execute only when tests pass

### Agent Delegation
Use Claude's Task tool to invoke specialized agents:
```text
"Use the {agent_name} agent to {description} with inputs: {inputs}"
```

## Implementation Example

```text
Executing workflow: feature-development
Parameters: feature_description="Add user authentication", files="src/**/*.py"

Step 1: context_setup (context-synth agent)
→ Analyzing files matching: src/**/*.py
→ Generated project context (stored as {{project_context}})

Step 2: planning (planner agent)  
→ Creating implementation plan for: Add user authentication
→ Plan generated with 5 tasks (stored as {{implementation_plan}})

Step 3: tdd_loop (iterative)
→ Iteration 1: Writing tests for authentication module
→ Tests created, running pytest... FAILED (expected)
→ Implementing authentication logic...
→ Tests running... PASSED
→ TDD loop complete

Step 4: parallel_reviews (parallel execution)
→ Running static-analyzer, security-scanner, style-checker in parallel
→ All checks passed

Step 5: ai_code_review (reviewer agent)
→ Comprehensive code review completed
→ No critical issues found

Workflow completed successfully in 12 minutes.
```

## Resume Capability

If workflow is interrupted:
```bash
/workflow feature-development --resume
```

Loads previous state and continues from last completed step.

## Dry Run Mode

Preview workflow execution:
```bash
/workflow feature-development --dry-run
```

Shows step sequence without execution for validation.

---

**Processing workflow: ${ARGUMENT}...**