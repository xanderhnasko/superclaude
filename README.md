# Super CC

This project and accompanying package is my attempt to share my favorite Claude Code configuration.

*But why?*

The key to using AI-coding tools more effectively than the next person (crazy world!) really just boils down to **context management**. Claude Code is already really powerful, but by properly utilizing subagents (with their own context windows and unique tool permissions), CC feels much more like a capable dev team rather than an often-overburdened, generalist agent.

This package contains the subagents and worflows that I have *personally* found to be most useful for my projects (like forcing Test-Driven Development and context synthesis with file-level json summaries), but by no means is it a one-size-fits all setup. Feel free to use this config as a foundation and create/edit/delete subagents and worflows as you see fit.

**TLDR Quick Start:**

``` bash
pip install super-cc
cd your-project
super-cc init

# Open a fresh Claude Code chat and start, ex:
/tdd "implement a user auth system"
```

**What does this actually do?**

* Specialized subagents for most dev tasks (planning, testing, debugging, reviewing)
* Git-based cache system so unchanged files don't bloat context
* Complete TDD automation
* Multi-pass code quality gates
* Explicitly defined read/write and tool use permissions (i.e. no more "Claude deleted my database!")

## How to (Basic Workflow)

**1\. Initialize Your Repository and start claude chat**

``` bash
super-cc init  # Creates .claude/ directory with 9 specialized agents
claude chat  # Launch Claude with Super CC agents available
```

**2\. Example Command Usage:**

``` bash
/tdd "create user model"           # Full TDD cycle: tests → implementation → review
/review                           # Multi-pass quality check (static, security, AI)
/context-synth "src/**/*.py"      # Intelligent codebase summarization
/workflow feature-development     # Orchestrated multi-agent workflows
```

**3\. Natural Language Invocation**
Subagents activate automatically based on your requests:

``` text
"Plan the implementation of payment processing"     → Planner Agent
"Debug this test failure"                         → Debugger Agent
"Review this code for security issues"            → Reviewer Agent
"Design the system architecture"                  → Architect Agent
```

## Subagents

### Development Agents

* **Planner Agent**: Breaks complex features into testable tasks with acceptance criteria
* **Tester Agent**: Enforces test-driven development, writes comprehensive test suites
* **Reviewer Agent**: Multi-pass code quality checks (static analysis, security, style, AI review)
* **Debugger Agent**: Diagnoses test failures and runtime errors with fix recommendations

### Architecture & Design Agents

* **Architect Agent**: System design reviews, technical debt analysis, design pattern recommendations
* **Documenter Agent**: Generates and maintains documentation, README files, API docs

### Advanced Workflow Agents

* **Context Synthesizer**: Creates 300-token JSON summaries of large codebases for efficient context management
* **Workflow Orchestrator**: Coordinates complex multi-agent workflows with parallel execution
* **Cache Manager**: Intelligent caching system that saves tokens through Git-based incremental processing

### Agent Interaction Patterns

Either tell CC to use an agent, or make it *relatively* clear in your request (e.g. "help me plan this feature" -> planner agent)

Once a subagent is triggered, workflows are defined such that portions of the task are handed off to other subagents in parallel. For example:

1. Architect reviews system design
2. Planner creates implementation tasks
3. Tester writes failing tests
4. Implementation until tests pass
5. Reviewer performs quality gates
6. Documenter updates documentation

## Advanced Features

### Intelligent Context Synthesis

``` bash
/context-synth "src/**/*.py docs/**/*.md"
```

Produces structured \~300 token JSON summaries:

``` json
{
  "files": [
    {"path": "src/auth.py", "main_roles": ["authentication", "session management"], "apis": ["login", "logout"], "todos": ["add 2FA support"]}
  ],
  "cross_cutting": ["error handling patterns", "logging framework"],
  "open_questions": ["database migration strategy"]
}
```

**Benefits:**

* 300-token project summaries instead of loading entire codebases into context (for large feautures)
* Git-based incremental updates (only processes changed files)
* Human-readable cache files so you can see what's cached
* Much faster context building when you're working on the same stuff

### Token Efficiency Optimization

**A quick note here:** since CC is now deploying subagents in the background, this configuration is obviously going to be less token-friendly than the vanilla CC setup.

It's definitely preferable to use this config with the MAX plan, though it is entirely possible on the PRO plan if you don't mind having your workflow interrupted by usage limits slightly more often. I've done my best to optimize token usage here, but you can also restrict (or free!) how agressively CC will deploy subagents and tools as outlined in the Performance Modes section below.

**Cache-First Architecture:**

* Git-commit-based cache keys ensure consistency
* Smart invalidation based on actual file changes
* Cross-feature cache sharing and scoping
* Predictive cache warming based on development patterns

**Performance Modes:**

```bash
/eco-mode conservative  # Maximum token savings
/eco-mode standard     # Balanced performance (default)
/eco-mode yolo        # Maximum speed, minimal caching
```

**Monitoring:**

``` bash
/token-usage          # Detailed consumption analysis
/cache-status         # Hit rates and efficiency metrics
/agent-status         # Per-agent performance tracking
```

### YAML Workflow Orchestration

This is how we hand off tasks across subagents by defining complex dev tasks declaratively. It is also the place with the most room for customization.

``` yaml
# .claude/workflows/feature-development.yaml
name: feature-development
description: Complete TDD workflow for new features
steps:
  - agent: architect
    condition: major_feature
    description: "Review architectural implications"

  - agent: planner
    description: "Create implementation plan"

  - name: "TDD Loop"
    repeat_until: "tests_pass"
    substeps:
      - agent: tester
        description: "Write failing tests"
      - agent: main
        action: implement
        description: "Implement until tests pass"

  - parallel_group: review_checks
    agents: [static-analyzer, security-scanner, style-checker]
    description: "Run quality gates in parallel"
```

**Execute workflows:**

``` bash
/workflow feature-development --param feature_description="Add payment system" --param major_feature=true
/workflow bug-fix --param bug_description="Login timeout" --resume
```

**Comprehensive Rollback:**

``` bash
/revert                # Roll back code and agent cache state to last known good commit
/revert --commit abc123 # Revert to specific commit with cache synchronization
```

**State Persistence:**

* Workflow state survives session interruptions
* Resume capability for long-running processes
* Cache integrity validation and automatic repair
* **Complete audit trails in** `.claude/logs/`

## Technical Architecture

### Directory Structure

After initialization, your repository should contain:

```text
.claude/
├── agents/                    # 9 specialized agent definitions
│   ├── architect.md          # System design and architecture review
│   ├── cache-manager.md      # Token efficiency and cache optimization
│   ├── context-synth.md      # Large codebase summarization
│   ├── debugger.md           # Test failure and error diagnosis
│   ├── documenter.md         # Documentation generation
│   ├── incremental-analyzer.md # Git-based change analysis
│   ├── planner.md            # Feature breakdown and task planning
│   ├── reviewer.md           # Multi-pass code quality gates
│   ├── tester.md             # Test-driven development enforcement
│   └── workflow-orchestrator.md # Multi-agent workflow coordination
├── commands/                  # Custom slash commands
│   ├── context-synth.md      # Codebase summarization command
│   ├── context.md            # Project analysis command
│   ├── review.md             # Comprehensive review orchestration
│   ├── tdd.md                # TDD workflow initiation
│   └── workflow.md           # YAML workflow execution
├── hooks/                     # Event-driven automation
│   ├── pre_tool_use.sh       # File protection and access control
│   └── post_tool_use.sh      # Auto-formatting and validation
├── workflows/                 # YAML workflow definitions
│   ├── bug-fix.yaml          # Bug fixing and regression prevention
│   ├── feature-development.yaml # Complete feature development cycle
│   ├── refactoring.yaml      # Safe refactoring with test preservation
│   └── review-only.yaml      # Standalone code review process
├── context/                   # Intelligent caching system
│   ├── summaries/            # Human-readable cache files
│   └── last-build-commit     # Git-based cache invalidation tracking
├── logs/                      # Development audit trails
└── state/                     # Session and workflow state persistence
```

### Agent Tool Permissions

Each agent has carefully scoped permissions outlined below:

**Tester Agent:**

* `Write`: Only to `tests/` directory
* `Read`: Everywhere (to understand code being tested)
* `Bash`: Only test runners (`pytest`, `npm test`, `go test`)

**Reviewer Agent:**

* `Read`: Source code and Git diffs
* `Bash`: Static analysis tools (`ruff`, `eslint`, `mypy`)
* No write permissions (review-only)

**Debugger Agent:**

* `Read`: All files for analysis
* `Bash`: Diagnostic commands only
* No modification capabilities (diagnosis-focused)

**Cache Manager:**

* `Read`: Git status and file metadata
* `Bash`: Git commands for change detection
* `Write`: Only to `.claude/context/` directory

### Hook System Architecture

**Pre-Tool-Use Hook:**

* File path protection (blocks `.claude/`, `.git/`, `.env/` modifications)
* Tool usage logging with timestamps
* Access control validation

**Post-Tool-Use Hook:**

* Automatic code formatting (`black`, `prettier`, `rustfmt`)
* Test failure detection and debugger suggestions
* Cache optimization triggers

``` bash
# Example hook execution flow:
User action → Pre-hook (validation) → Tool execution → Post-hook (cleanup) → Result
```

## Workflow Deep Dive

### Complete TDD Implementation

**Red Phase (Failing Tests):**

``` bash
/tdd "implement user authentication"
```

1. Planner Agent breaks feature into testable tasks
2. Tester Agent writes comprehensive failing tests
3. Tests execute and fail (confirming test validity)

**Green Phase (Implementation):**
4\. Minimal code implementation to pass tests
5\. Iterative development with frequent test runs
6\. Debugger Agent assists with any test failures

**Refactor Phase (Quality):**
7\. Code review by Reviewer Agent
8\. Static analysis\, security scanning\, style checking
9\. Documentation updates by Documenter Agent
10\. Final validation and commit preparation

### Multi-Pass Review Pipeline

The `/review` command orchestrates comprehensive quality gates:

**Static Analysis Pass:**

* Language-specific linters (`ruff`, `eslint`, `rustfmt`)
* Type checking (`mypy`, `typescript`)
* Complexity analysis and code metrics

**Security Pass:**

* Vulnerability scanning (`bandit`, `safety`)
* Input validation analysis
* Authentication and authorization review

**Style Pass:**

* Code formatting validation
* Naming convention compliance
* Documentation completeness

**AI Review Pass:**

* Semantic code analysis by Reviewer Agent
* Logic error detection
* Performance and maintainability suggestions
* Security best practice validation

### Large Codebase Management

**Context Synthesis Workflow:**

``` bash
# Initial synthesis (processes all files)
/context-synth "src/**/*.py docs/**/*.md" 

# Subsequent runs (only processes changed files since last Git commit)
/context-synth "src/**/*.py docs/**/*.md"  # 95% faster due to caching
```

**Cache Management:**

* Human-readable cache files: `src_auth_py_summary.json`
* Git-based invalidation: only re-analyze changed files
* Cross-reference detection: identifies dependencies between files
* Memory-efficient: supports repositories with thousands of files

### State Management and Recovery

**Session Persistence:**
All workflow state persists across Claude Code sessions. What this really means is that you **don't have to explain a feature/task again to CC when you open a new CC window.**

* Current workflow step and parameters
* Agent cache state and validity
* Partial task completion status
* Context synthesis results

**Resume Capabilities:**

``` bash
/workflow feature-development --resume  # Continue interrupted workflow
/context-synth --incremental           # Update only changed context
```

**Recovery Systems:**

* Automatic cache integrity validation
* Corrupt state detection and repair
* Safe rollback to last known good state
* Complete audit trails for debugging

## Example Usage Patterns

This all can seem a bit hard to keep track of, so here are some example workflows I think outline the capabilities of this configuration.

### General Feature Development

**Scenario:** Adding authentication to an existing API

``` bash
# 1. Architectural review for major features
"Review the architectural implications of adding JWT authentication to our REST API"
# → Architect Agent analyzes system, recommends patterns

# 2. Create implementation plan
"Plan the implementation of JWT authentication with refresh tokens"
# → Planner Agent creates phased approach with acceptance criteria

# 3. Start TDD cycle
/tdd "implement JWT token service with refresh capability"
# → Tester Agent writes comprehensive tests
# → Implementation guided by failing tests

# 4. Comprehensive review
/review
# → Multi-pass quality gates ensure production readiness

# 5. Update documentation
"Document the new authentication flow and API endpoints"
# → Documenter Agent creates API docs and usage examples
```

### Bug Fixing

**Scenario:** Investigating a production authentication timeout

``` bash
# 1. Reproduce and analyze
"Debug why users are getting authentication timeouts after 30 minutes"
# → Debugger Agent analyzes logs, identifies session management issue

# 2. Create regression test
/tdd "add test for session timeout edge case"
# → Tester Agent writes test reproducing the bug

# 3. Implement fix guided by test
# → Code until test passes

# 4. Validate fix doesn't break existing functionality
/review --regression-focus
# → Comprehensive validation of change impact
```

### Refactoring

**Scenario:** Improving code organization without breaking functionality

``` bash
# 1. Architectural analysis
"Review the current service layer architecture and identify refactoring opportunities"
# → Architect Agent identifies coupling issues, suggests improvements

# 2. Ensure test coverage before refactoring
/review --test-coverage-focus
# → Reviewer Agent identifies untested code paths

# 3. Safe incremental refactoring
/workflow refactoring --param target_files="src/services/**"
# → Workflow Orchestrator coordinates safe refactoring steps
# → Each change validated by test suite
```

## Performance and Optimization

**Token Usage Dashboard:**

``` bash
/token-usage
```

This gives you a breakdown of where your tokens are going and how much the caching system is helping. The cache is particularly effective for repetitive tasks like code reviews and architectural analysis.

```bash
/cache-status  # See what's cached and hit rates

/cache-optimize  # Get suggestions for improving cache efficiency
```

### Eco-Mode Configuration

**Conservative Mode:** Maximum token efficiency

```bash
/eco-mode conservative
```

* Aggressive caching with longer retention
* Batch agent operations where possible
* Skip redundant analysis steps

**Standard Mode:** Balanced performance (default)

```bash
/eco-mode standard
```

* Intelligent caching with reasonable retention
* Real-time agent invocation as needed
* Standard analysis depth

**YOLO Mode:** Maximum speed and thoroughness

```bash
/eco-mode yolo
```

* Minimal caching to ensure fresh analysis
* Parallel agent execution where beneficial
* Maximum analysis depth and validation

## Language and Frameworks

### Python Projects

**Detection:** `requirements.txt`, `pyproject.toml`, `setup.py`
**Tools Integration:**

* Test Framework: `pytest`, `unittest`
* Code Quality: `ruff`, `black`, `mypy`
* Security: `bandit`, `safety`

### JavaScript/TypeScript Projects

**Detection:** `package.json`, `tsconfig.json`
**Tools Integration:**

* Test Framework: `vitest`, `jest`, `mocha`
* Code Quality: `eslint`, `prettier`
* Type Checking: `typescript`

### Rust Projects

**Detection:** `Cargo.toml`
**Tools Integration:**

* Test Framework: `cargo test`
* Code Quality: `rustfmt`, `clippy`
* Build System: `cargo build`

### Go Projects

**Detection:** `go.mod`
**Tools Integration:**

* Test Framework: `go test`
* Code Quality: `gofmt`, `go vet`
* Build System: `go build`

### Custom Configurations

Override detection or add custom tool integration:

``` bash
# .claude/config.toml
[tools]
test_command = "npm run test:coverage"
lint_command = "npm run lint:strict"
format_command = "npm run format:check"

[agent_config.tester]
custom_tools = ["bash:npm run test:integration"]
```

## CLI Commands Reference

### Repository Management

``` bash
super-cc init [path]           # Initialize Super CC in repository
super-cc init --force          # Force overwrite existing installation
super-cc validate [path]       # Validate installation and configuration
super-cc upgrade [path]        # Update agents and commands to latest version
```

### Development Workflow Commands

Available within `claude chat` after initialization:

``` bash
/tdd "feature description"     # Start complete TDD cycle
/review                        # Multi-pass code review
/review --static-only         # Only static analysis
/review --security-only       # Only security scanning
/context "pattern"            # Analyze project structure
/context-synth "glob/pattern" # Create JSON context digest
```

### Advanced Workflow Commands

``` bash
/workflow <name> [--param key=value] [--resume] [--dry-run]
/workflow feature-development --param feature_description="Add auth"
/workflow bug-fix --param bug_description="Timeout error" --resume
/workflow refactoring --param target_files="src/**" --dry-run
```

### Performance and Monitoring Commands

``` bash
/token-usage                  # Detailed token consumption analysis
/cache-status                 # Cache hit rates and efficiency metrics
/cache-optimize              # Performance optimization suggestions
/agent-status                # Per-agent performance tracking
/eco-mode <conservative|standard|yolo>  # Configure performance mode
```

### State Management Commands

``` bash
/revert                      # Rollback code and cache to last good state
/revert --commit <hash>      # Revert to specific commit with cache sync
/save-state <name>          # Save current workflow state
/load-state <name>          # Restore workflow state
```

## Agent Trigger Word Reference

You can force (or avoid) the use of subagents by using some of the following trigger words in your requests:

### Planner Agent

**Triggers:** "plan", "planning", "roadmap", "implementation plan", "task breakdown", "feature breakdown"
**Example:** "Create an implementation plan for the payment processing feature"

### Architect Agent

**Triggers:** "architecture", "design", "system design", "technical debt", "refactor strategy", "design patterns"
**Example:** "Review the architecture and suggest improvements for scalability"

### Tester Agent

**Triggers:** "write tests", "unit test", "test coverage", "TDD", "test first", "testing strategy"
**Example:** "Write comprehensive unit tests for the authentication module"

### Reviewer Agent

**Triggers:** "review code", "code review", "PR review", "check changes", "audit code", "quality check"
**Example:** "Review this code for potential security vulnerabilities"

### Debugger Agent

**Triggers:** "debug", "fix bug", "test failing", "error", "stack trace", "diagnose", "troubleshoot"
**Example:** "Debug why the integration tests are failing in CI"

### Documenter Agent

**Triggers:** "document", "write docs", "update README", "API docs", "documentation"
**Example:** "Update the API documentation to reflect the new authentication endpoints"

### Context Synthesizer

**Triggers:** "summarize", "context", "overview", "analyze codebase", "project structure"
**Example:** "Analyze the codebase structure and provide a high-level overview"

### Workflow Orchestrator

**Triggers:** "workflow", "orchestrate", "coordinate", "multi-step", "process automation"
**Example:** "Orchestrate a complete feature development workflow for user profiles"

### Cache Manager

**Triggers:** "cache", "optimize", "performance", "token efficiency", "speed up"
**Example:** "Optimize the cache configuration to improve token efficiency"

## Configuration and Customization

### Agent Configuration

Customize agent behavior by editing their Markdown files:

``` markdown
---
# .claude/agents/tester.md
description: Test-driven development specialist
trigger: write tests, create unit tests, test-driven development
tools: [read, write, bash]
write_paths: ["tests/**"]
bash_allowlist: ["pytest", "npm test", "go test"]
---

Enhanced system prompt with custom instructions...
```

### Workflow Customization

Create project-specific workflows:

``` yaml
# .claude/workflows/custom-api-development.yaml
name: custom-api-development
description: API development with OpenAPI spec generation
steps:
  - agent: architect
    description: "Design API architecture and data models"

  - agent: documenter
    description: "Generate OpenAPI specification"

  - name: "Implementation Loop"
    repeat_until: "all_endpoints_implemented"
    substeps:
      - agent: tester
        description: "Write API endpoint tests"
      - agent: main
        action: implement
        description: "Implement endpoint"

  - agent: reviewer
    description: "API security and performance review"
```

### Hook Customization

Extend automation with custom hooks:

``` bash
#!/bin/bash
# .claude/hooks/pre_tool_use.sh
# Add custom validation logic

TOOL="$1"
FILE_PATH="$2"

# Custom protection rules
if [[ "$FILE_PATH" =~ \.env ]]; then
  echo "Blocked: Environment file modification not allowed"
  exit 1
fi

# Custom logging with project context
echo "$(date) - Project: $(basename $(pwd)) - $TOOL: $FILE_PATH" >> .claude/logs/detailed.log

exit 0
```

## Troubleshooting and Validation

### Common Issues and Solutions

**Agents not triggering automatically**

```bash
# Validate agent configuration
super-cc validate

# Check for trigger word conflicts
grep -r "description:" .claude/agents/

# Explicit agent invocation as fallback
"Use the tester agent to write unit tests"
```

**Cache not working well**

```bash
# Check cache status
/cache-status

# Validate Git integration
cd .claude/context && ls -la

# Force cache rebuild
rm -rf .claude/context/summaries/ && /context-synth "src/**"
```

**Issue: Hooks not executing**

```bash
# Check hook permissions
ls -la .claude/hooks/

# Make executable if needed
chmod +x .claude/hooks/*.sh

# Test hook execution
./.claude/hooks/pre_tool_use.sh "test" "/tmp/test"
```

### Validation Commands

**Environment Health Check:**

``` bash
super-cc validate
```

**Cache Integrity Check:**

``` bash
/cache-status --detailed
```

### Advanced Diagnostics

**Debug Agent Behavior:**

``` bash
# Enable verbose agent logging
echo "CLAUDE_DEBUG=1" >> .claude/config

# Check agent selection logic
"Why wasn't the debugger agent triggered for this error analysis?"

# Review recent agent activity
tail -f .claude/logs/agent_activity.log
```

**Performance Profiling:**

``` bash
# Profile token usage over time
/token-usage --timeline

# Analyze workflow bottlenecks
/workflow feature-development --dry-run --profile

# Cache efficiency trends
/cache-status --history
```

## Contributing and Development

### Contributing to Super CC

**Repository Structure:**

``` text
super_cc/
├── cli.py              # CLI interface and argument parsing
├── installer.py        # Repository initialization and upgrade logic
├── validation.py       # Environment validation and health checks
├── integration.py      # Git integration and smart merging
└── templates/          # Agent, command, and workflow templates
    └── .claude/        # Template directory structure
```

**Development Setup:**

``` bash
git clone https://github.com/your-username/super-cc.git
cd super-cc
pip install -e ".[dev]"

# Run tests
pytest

# Validate code quality
black .
ruff check .
mypy .
```

**Adding New Agents:**

1. Create agent definition in `templates/.claude/agents/new-agent.md`
2. Add validation rules in `validation.py`
3. Update trigger word documentation
4. Add tests for agent functionality

**Creating Custom Workflows:**

1. Define YAML schema in `templates/.claude/workflows/`
2. Add workflow validation logic
3. Update documentation with usage examples
4. Test with `--dry-run` mode

## License and Support

**License:** MIT License - see [LICENSE](LICENSE) file for details.
**Issues and Feature Requests:** [GitHub Issues](https://github.com/xanderhnasko/issues)
