"""
Super CC Validation

Validates Claude Code environment and checks for compatibility issues.
"""

import subprocess
from pathlib import Path
from typing import List, Tuple


def validate_environment(repo_path: Path) -> bool:
    """Validate Super CC environment setup.
    
    Args:
        repo_path: Path to the repository to validate
        
    Returns:
        True if environment is valid, False otherwise
    """
    repo_path = Path(repo_path).resolve()
    claude_dir = repo_path / ".claude"
    
    print(f"🔍 Validating Super CC environment: {repo_path}")
    
    issues = []
    warnings = []
    
    # Check if .claude directory exists
    if not claude_dir.exists():
        issues.append("❌ .claude directory not found")
        print("❌ No Super CC installation found. Run 'super-cc init' to install.")
        return False
    
    # Validate directory structure
    required_dirs = ["agents", "commands", "hooks", "logs", "state", "workflows"]
    for dir_name in required_dirs:
        dir_path = claude_dir / dir_name
        if not dir_path.exists():
            issues.append(f"❌ Missing directory: .claude/{dir_name}/")
        else:
            print(f"🪐 Found: .claude/{dir_name}/")
    
    # Validate agents
    agent_issues, agent_warnings = _validate_agents(claude_dir / "agents")
    issues.extend(agent_issues)
    warnings.extend(agent_warnings)
    
    # Validate commands
    command_issues, command_warnings = _validate_commands(claude_dir / "commands")
    issues.extend(command_issues)
    warnings.extend(command_warnings)
    
    # Validate hooks
    hook_issues, hook_warnings = _validate_hooks(claude_dir / "hooks")
    issues.extend(hook_issues)
    warnings.extend(hook_warnings)
    
    # Validate workflows
    workflow_issues, workflow_warnings = _validate_workflows(claude_dir / "workflows")
    issues.extend(workflow_issues)
    warnings.extend(workflow_warnings)
    
    # Check Claude Code installation
    claude_issues, claude_warnings = _validate_claude_code()
    issues.extend(claude_issues)
    warnings.extend(claude_warnings)
    
    # Display results
    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"   {warning}")
    
    if issues:
        print("\n❌ Issues found:")
        for issue in issues:
            print(f"   {issue}")
        return False
    
    print("\n🫧 Super CC environment is valid and ready to use!")
    return True


def _validate_agents(agents_dir: Path) -> Tuple[List[str], List[str]]:
    """Validate agent files."""
    issues = []
    warnings = []
    
    expected_agents = [
        "architect.md", "cache-manager.md", "context-synth.md", "debugger.md",
        "documenter.md", "incremental-analyzer.md", "planner.md", "reviewer.md",
        "tester.md", "workflow-orchestrator.md"
    ]
    
    if not agents_dir.exists():
        issues.append("❌ Agents directory missing")
        return issues, warnings
    
    for agent_file in expected_agents:
        agent_path = agents_dir / agent_file
        if not agent_path.exists():
            issues.append(f"❌ Missing agent: {agent_file}")
        else:
            # Validate agent file format
            try:
                content = agent_path.read_text()
                if not content.startswith("---"):
                    warnings.append(f"⚠️  Agent {agent_file} missing YAML frontmatter")
            except Exception:
                warnings.append(f"⚠️  Could not read agent file: {agent_file}")
    
    print(f"🪐 Found {len(list(agents_dir.glob('*.md')))} agent files")
    return issues, warnings


def _validate_commands(commands_dir: Path) -> Tuple[List[str], List[str]]:
    """Validate command files."""
    issues = []
    warnings = []
    
    expected_commands = [
        "context-synth.md", "context.md", "review.md", "tdd.md", "workflow.md"
    ]
    
    if not commands_dir.exists():
        issues.append("❌ Commands directory missing")
        return issues, warnings
    
    for command_file in expected_commands:
        command_path = commands_dir / command_file
        if not command_path.exists():
            issues.append(f"❌ Missing command: {command_file}")
    
    print(f"🪐 Found {len(list(commands_dir.glob('*.md')))} command files")
    return issues, warnings


def _validate_hooks(hooks_dir: Path) -> Tuple[List[str], List[str]]:
    """Validate hook files."""
    issues = []
    warnings = []
    
    expected_hooks = ["pre_tool_use.sh", "post_tool_use.sh"]
    
    if not hooks_dir.exists():
        issues.append("❌ Hooks directory missing")
        return issues, warnings
    
    for hook_file in expected_hooks:
        hook_path = hooks_dir / hook_file
        if not hook_path.exists():
            issues.append(f"❌ Missing hook: {hook_file}")
        else:
            # Check if executable
            if not hook_path.stat().st_mode & 0o111:
                warnings.append(f"⚠️  Hook not executable: {hook_file}")
    
    print(f"🪐 Found {len(list(hooks_dir.glob('*.sh')))} hook files")
    return issues, warnings


def _validate_workflows(workflows_dir: Path) -> Tuple[List[str], List[str]]:
    """Validate workflow files."""
    issues = []
    warnings = []
    
    if not workflows_dir.exists():
        issues.append("❌ Workflows directory missing")
        return issues, warnings
    
    workflow_files = list(workflows_dir.glob("*.yaml"))
    if not workflow_files:
        warnings.append("⚠️  No workflow files found")
    
    print(f"🪐 Found {len(workflow_files)} workflow files")
    return issues, warnings


def _validate_claude_code() -> Tuple[List[str], List[str]]:
    """Validate Claude Code installation."""
    issues = []
    warnings = []
    
    try:
        # Check if claude command exists
        result = subprocess.run(
            ["claude", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            version_output = result.stdout.strip()
            print(f"🪐 Claude Code found: {version_output}")
            
            # Check for minimum version if needed
            # This would require parsing version string
            
        else:
            issues.append("❌ Claude Code command failed")
            
    except subprocess.TimeoutExpired:
        warnings.append("⚠️  Claude Code command timed out")
    except FileNotFoundError:
        issues.append("❌ Claude Code not installed or not in PATH")
    except Exception as e:
        warnings.append(f"⚠️  Could not verify Claude Code: {e}")
    
    return issues, warnings