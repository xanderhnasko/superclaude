# Super Claude Code - Multi-Agent Development Workflow

## Project Overview
This is a **meta-project** to enhance Claude Code with specialized subagents that work together in sophisticated development workflows. We're building the next evolution of Claude Code itself - a multi-agent system that turns any repository into a high-productivity, AI-assisted development environment.

## Current Status: Phase 1 - Core TDD Loop Implementation
**Active Development**: Building the foundational Test-Driven Development workflow with specialized agents.

## Key Documents (CRITICAL REFERENCES)

### 📖 Primary Architecture Reference (THE HOLY GRAIL)
- **`docs/Super CC Architecture.md`** - Complete architectural vision and design philosophy
  - Multi-agent workflow concepts
  - Subagent roles and responsibilities  
  - TDD-centric development patterns
  - Claude Code native capability usage

### 🔧 Technical Implementation Details
- **`docs/Super CC Technical Implementation Plan.json`** - Detailed technical specifications
  - Agent configurations and prompts
  - Directory structure definitions
  - Workflow patterns and examples
  - Tool permissions and restrictions

### 📝 Progress Tracking
- **`docs/Implementation-Progress.md`** - ADR-style development log (coming soon)

## Current Implementation Strategy

### Phase 1: Core TDD Loop (IN PROGRESS)
Building the essential agents first:
- **Planner Agent** - Breaks features into testable tasks
- **Tester Agent** - Enforces test-first development  
- **Reviewer Agent** - Code quality validation
- **`/tdd` Command** - Initiates the complete TDD cycle

### Future Phases
- Phase 2: Enhanced agents (debugger, architect)
- Phase 3: Automation hooks and advanced features
- Phase 4: Distribution-ready bootstrap system

## Quick Commands (When Available)
- `/tdd [feature description]` - Start TDD cycle for new feature
- `/review` - Comprehensive code review (future)
- `/context` - Project context summary (future)

## Directory Structure
```
.claude/
├── agents/           # Specialized AI subagents
├── commands/         # Custom slash commands  
├── hooks/            # Automation scripts
├── logs/             # Development audit trail
└── state/            # Context and session data

docs/
├── Super CC Architecture.md           # 📖 HOLY GRAIL
├── Super CC Technical Implementation Plan.json  # 🔧 SPECS
└── Implementation-Progress.md         # 📝 PROGRESS LOG
```

## Development Philosophy
- **Incremental Development**: Build and validate core functionality first
- **TDD-Driven**: All features start with tests
- **Agent Specialization**: Each agent has a focused, well-defined role
- **Native Integration**: Leverage Claude Code's built-in capabilities
- **Context Preservation**: Maintain development context across sessions

## Next Steps
1. ✅ Create foundation files (CLAUDE.md, progress tracking)
2. 🔄 Set up minimal directory structure  
3. ⏳ Implement core TDD agents
4. ⏳ Create `/tdd` slash command
5. ⏳ Validate workflow with sample feature

---
*This file serves as the primary context entry point for any Claude session working on this project. Always reference the architecture document for detailed design decisions.*