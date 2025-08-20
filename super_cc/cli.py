#!/usr/bin/env python3
"""
Super CC Command Line Interface

Provides commands to initialize and manage Claude Code multi-agent environments.
"""

import argparse
import sys
from pathlib import Path

from .installer import SuperCCInstaller
from .validation import validate_environment


def show_help():
    """Display comprehensive help for Super CC commands and workflows."""
    print()
    print("🫧" * 52)
    print("🫧🫧 Super CC: Multi-Agent Claude Code Environment 🫧🫧")
    print("🫧" * 52)
    print()
    
    print("🧼 CLI COMMANDS:")
    print("  super-cc init [path]     Initialize Super CC environment")
    print("  super-cc validate [path] Validate current setup")
    print("  super-cc upgrade [path]  Update to latest agents/commands") 
    print("  super-cc help           Show this help information")
    print()
    
    print("🧼 CLAUDE CHAT COMMANDS (available after initialization):")
    print()
    
    print("  🫧 Core Development:")
    print("    /tdd \"feature description\"    Start complete TDD cycle")
    print("    /review                        Multi-pass code review")
    print("    /workflow <name> [options]     Execute YAML workflows")
    print()
    
    print("  🫧 Context & Analysis:")
    print("    /context \"pattern\"            Analyze project structure")
    print("    /context-synth \"glob/pattern\" Create JSON context digest")
    print("    /agent-status                  Per-agent performance tracking")
    print()
    
    print("  🫧 Performance & Optimization:")
    print("    /cache-status                  Cache hit rates and efficiency")
    print("    /cache-optimize                Performance optimization tips")
    print("    /token-usage                   Token consumption analysis")
    print("    /eco-mode <mode>               Set performance mode")
    print()
    
    print("  🫧 State Management:")
    print("    /revert                        Rollback to last good state")
    print("    /revert --commit <hash>        Revert to specific commit")
    print()
    
    print("🧼 AVAILABLE WORKFLOWS:")
    print("  /workflow feature-development  Complete TDD workflow for new features")
    print("  /workflow bug-fix             Diagnostic workflow for bug resolution")
    print("  /workflow refactoring         Code cleanup and improvement workflow")
    print("  /workflow review-only         Comprehensive code review pipeline")
    print()
    
    print("🧼 AGENT TRIGGER PATTERNS (use in natural language):")
    print("  \"Plan the implementation...\"   → Planner Agent")
    print("  \"Write tests for...\"          → Tester Agent")
    print("  \"Review this code...\"         → Reviewer Agent")
    print("  \"Debug this error...\"         → Debugger Agent")
    print("  \"Design the architecture...\"  → Architect Agent")
    print("  \"Document this feature...\"    → Documenter Agent")
    print("  \"Analyze the codebase...\"     → Context Synthesizer")
    print("  \"Orchestrate this workflow...\" → Workflow Orchestrator")
    print()
    
    print("🧼 QUICK START:")
    print("  1. cd your-project")
    print("  2. super-cc init")
    print("  3. claude chat")
    print("  4. Try: /tdd \"implement user authentication\"")
    print()
    
    print("🧼 More info: https://github.com/xanderhnasko/super-cc")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Transform any repository into a high-productivity AI development environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  super-cc init                    # Initialize current directory
  super-cc init /path/to/repo      # Initialize specific directory
  super-cc validate                # Check current setup
  super-cc upgrade                 # Update to latest agents/commands
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize Super CC environment")
    init_parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Path to repository (default: current directory)"
    )
    init_parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force initialization even if .claude directory exists"
    )
    init_parser.add_argument(
        "--backup", 
        action="store_true", 
        default=True,
        help="Create backup of existing .claude directory (default: True)"
    )
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate current setup")
    validate_parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Path to repository (default: current directory)"
    )
    
    # Upgrade command
    upgrade_parser = subparsers.add_parser("upgrade", help="Update to latest agents/commands")
    upgrade_parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Path to repository (default: current directory)"
    )
    
    # Help command
    subparsers.add_parser("help", help="Show all available commands and workflows")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "init":
            installer = SuperCCInstaller(Path(args.path))
            result = installer.install(force=args.force, backup=args.backup)
            if result:
                print("🫧 Super CC initialized successfully!")
                print(f"   Repository: {Path(args.path).resolve()}")
                print("   Next steps:")
                print("   1. cd to your repository")
                print("   2. Run: claude chat")
                print("   3. Try: /tdd 'your feature description'")
                print("   4. Use: super-cc help (to see all commands & workflows)")
            else:
                print("❌ Installation failed. Check error messages above.")
                return 1
                
        elif args.command == "validate":
            result = validate_environment(Path(args.path))
            if result:
                print("🫧 Super CC environment is valid and ready to use.")
            else:
                print("❌ Issues found with Super CC environment.")
                return 1
                
        elif args.command == "upgrade":
            installer = SuperCCInstaller(Path(args.path))
            result = installer.upgrade()
            if result:
                print("🫧 Super CC environment upgraded successfully!")
            else:
                print("❌ Upgrade failed. Check error messages above.")
                return 1
                
        elif args.command == "help":
            show_help()
            return 0
                
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user.")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())