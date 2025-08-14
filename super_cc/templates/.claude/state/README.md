# Workflow State Management

This directory contains state management for Super Claude Code workflows.

## Directory Structure

```
state/
├── README.md                      # This file
├── workflow-state-schema.json     # JSON schema for workflow state
├── context.json                   # General project context state
├── workflows/                     # Workflow execution states
│   ├── feature-development-*.json # Feature development workflow states
│   ├── bug-fix-*.json            # Bug fix workflow states
│   ├── refactoring-*.json        # Refactoring workflow states
│   └── review-only-*.json        # Review workflow states
└── checkpoints/                   # Workflow resume checkpoints
    └── *.checkpoint.json
```

## State File Naming Convention

Workflow state files follow the pattern:
`{workflow-name}-{unix-timestamp}.json`

Examples:
- `feature-development-1705234567.json`
- `bug-fix-1705234890.json`
- `refactoring-1705235123.json`

## State Persistence Features

### Automatic State Tracking
- Every workflow step completion updates state
- Parallel execution progress tracked independently
- Loop iterations and conditions monitored
- Resource usage metrics collected

### Resume Capability
- Workflows can be resumed from any completed step
- State integrity validation before resume
- Checkpoint creation at critical workflow points
- Rollback support for failed operations

### State Queries
Workflow states can be queried for:
- Current execution status
- Step completion history
- Variable bindings and outputs
- Error conditions and recovery attempts
- Performance metrics and resource usage

## Example State File

```json
{
  "workflow_metadata": {
    "id": "feature-development-1705234567",
    "name": "feature-development",
    "version": "1.0",
    "status": "running",
    "started_at": "2025-01-14T10:00:00Z",
    "git_commit": "abc123def456"
  },
  "execution_context": {
    "current_step": 5,
    "total_steps": 12,
    "parameters": {
      "feature_description": "Add user authentication",
      "files": "src/**/*.py",
      "major_feature": false
    },
    "variables": {
      "project_context": {...},
      "implementation_plan": {...},
      "test_results": {...}
    }
  },
  "step_history": [
    {
      "step_index": 0,
      "step_name": "context_setup",
      "agent_name": "context-synth",
      "status": "completed",
      "started_at": "2025-01-14T10:00:00Z",
      "completed_at": "2025-01-14T10:01:30Z",
      "duration_seconds": 90,
      "outputs": {
        "project_context": "Generated context summary"
      }
    }
  ]
}
```

## State Management Commands

### View Active Workflows
```bash
find .claude/state/workflows/ -name "*.json" -exec jq -r '.workflow_metadata | "\(.id) \(.status) \(.started_at)"' {} \;
```

### Resume Workflow
```bash
/workflow resume feature-development-1705234567
```

### Query Workflow Status
```bash
jq '.workflow_metadata.status' .claude/state/workflows/feature-development-1705234567.json
```

## State Cleanup

Workflow states are automatically retained for analysis and debugging. Old state files can be cleaned up:

```bash
# Remove completed workflows older than 30 days
find .claude/state/workflows/ -name "*.json" -mtime +30 -exec jq -e '.workflow_metadata.status == "completed"' {} \; -delete
```

## Security Considerations

- State files may contain sensitive information from workflow outputs
- Access to state directory should be restricted appropriately  
- Consider encrypting state files for sensitive projects
- State files are git-ignored by default to prevent accidental commits