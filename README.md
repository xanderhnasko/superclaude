# Super CC

Transform any repository into a high-productivity AI development environment with specialized Claude Code agents, automated workflows, and intelligent caching.

## ✨ Features

**🤖 Specialized AI Agents:**
- **Planner**: Breaks down features into testable tasks
- **Tester**: Enforces test-driven development (TDD)
- **Reviewer**: Multi-pass code quality and security checks
- **Architect**: System design and architectural guidance
- **Debugger**: Test failure diagnosis and error analysis
- **Documenter**: Documentation generation and maintenance
- **Context Synthesizer**: Intelligent codebase summarization
- **Workflow Orchestrator**: Advanced multi-agent coordination
- **Cache Manager**: Token-efficient caching system

**⚡ Automated Workflows:**
- Complete TDD cycles (Red → Green → Refactor)
- Comprehensive code review pipelines
- Intelligent context synthesis for large codebases
- YAML-configurable workflow orchestration
- Parallel agent execution for efficiency

**🎯 Productivity Features:**
- 60-80% token savings through intelligent caching
- Git-based incremental processing
- Smart conflict resolution and backup management
- Cross-platform compatibility (Windows/Mac/Linux)
- Language-agnostic with framework detection

## 🚀 Quick Start

### Installation

```bash
pip install super-cc
```

### Initialize Your Repository

```bash
cd /path/to/your/project
super-cc init
```

### Start Developing

```bash
claude chat
```

Then use the powerful slash commands:

```bash
/tdd "implement user authentication"
/review
/context-synth "src/**/*.py"
/workflow feature-development --param feature_description="Add payment system"
```

## 📖 Usage

### Core Slash Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/tdd` | Start test-driven development cycle | `/tdd "create user model"` |
| `/review` | Run comprehensive code review | `/review --security-only` |
| `/context` | Analyze project structure | `/context` |
| `/context-synth` | Synthesize codebase into JSON digest | `/context-synth "src/**/*.py docs/**"` |
| `/workflow` | Execute predefined workflows | `/workflow bug-fix --param description="Login timeout"` |

### Specialized Agents

Agents are automatically triggered by natural language or can be explicitly invoked:

**Automatic Triggering:**
```bash
"Plan the implementation of user authentication"  # → Planner Agent
"Review this code for security issues"            # → Reviewer Agent
"Debug this test failure"                         # → Debugger Agent
"Design the system architecture"                  # → Architect Agent
```

**Explicit Invocation:**
```bash
"Use the tester agent to write comprehensive tests"
"Run the architect agent to review system design"
```

### Workflow Orchestration

Super CC includes predefined YAML workflows for common development patterns:

**Feature Development:**
```bash
/workflow feature-development --param feature_description="User notifications" --param major_feature=true
```

**Bug Fixing:**
```bash
/workflow bug-fix --param bug_description="Memory leak in authentication" --resume
```

**Code Refactoring:**
```bash
/workflow refactoring --param target_files="src/auth/**" --dry-run
```

## 🏗️ Architecture

Super CC leverages Claude Code's native capabilities:

- **Subagents**: Specialized AI assistants with focused expertise
- **Slash Commands**: Reusable workflow automation
- **Tool Permissions**: Security through restricted agent capabilities
- **Hooks**: Deterministic automation for file protection and logging
- **Context Management**: Intelligent codebase compression and caching

## 📁 Directory Structure

After initialization, your repository will have:

```
.claude/
├── agents/           # 9 specialized AI subagents
├── commands/         # Custom slash commands
├── hooks/            # Automation scripts (pre/post tool use)
├── workflows/        # YAML workflow configurations
├── context/          # Intelligent caching system
├── logs/             # Development audit trail
└── state/            # Session and workflow state
```

## 🔧 Advanced Configuration

### Cache Optimization

Super CC includes intelligent caching to reduce token usage by 60-80%:

```bash
# View cache status
/cache-status

# Optimize cache performance
/cache-optimize

# Test cache effectiveness
/cache-test
```

### Eco-Mode Settings

Control token efficiency vs. speed trade-offs:

```bash
# Conservative mode (maximum token savings)
/eco-mode conservative

# Standard mode (balanced performance)
/eco-mode standard

# YOLO mode (maximum speed)
/eco-mode yolo
```

### Token Usage Monitoring

Track and optimize your AI development efficiency:

```bash
# View detailed token usage statistics
/token-usage

# Agent-specific performance metrics
/agent-status
```

## 🛠️ CLI Commands

### Repository Management

```bash
# Initialize new repository
super-cc init

# Initialize specific directory
super-cc init /path/to/repo

# Force initialization (overwrite existing)
super-cc init --force

# Validate existing setup
super-cc validate

# Upgrade to latest version
super-cc upgrade
```

### Validation and Troubleshooting

```bash
# Check environment health
super-cc validate

# Validate specific repository
super-cc validate /path/to/repo
```

## 🧪 Testing and Quality

Super CC enforces rigorous development practices:

- **Test-First Development**: All features start with failing tests
- **Multi-Pass Reviews**: Static analysis, security scanning, and AI review
- **Automated Formatting**: Code style enforcement via hooks
- **Audit Trails**: Complete development history logging

## 🌍 Language Support

Super CC is language-agnostic with automatic detection for:

- **Python**: pytest, black, ruff, mypy
- **JavaScript/TypeScript**: vitest, eslint, prettier
- **Rust**: cargo test, rustfmt
- **Go**: go test, gofmt
- **And more**: Extensible for any language ecosystem

## 🤝 Contributing

We welcome contributions! See our development setup:

```bash
# Clone repository
git clone https://github.com/super-cc/super-cc.git
cd super-cc

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check .
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Documentation**: [GitHub README](https://github.com/super-cc/super-cc#readme)
- **Issues**: [GitHub Issues](https://github.com/super-cc/super-cc/issues)
- **PyPI**: [super-cc](https://pypi.org/project/super-cc/)

---

**Transform your development workflow today with Super CC! 🚀**