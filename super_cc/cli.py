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
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "init":
            installer = SuperCCInstaller(Path(args.path))
            result = installer.install(force=args.force, backup=args.backup)
            if result:
                print("🧿Super CC initialized successfully!")
                print(f"   Repository: {Path(args.path).resolve()}")
                print("   Next steps:")
                print("   1. cd to your repository")
                print("   2. Run: claude chat")
                print("   3. Try: /tdd 'your feature description'")
            else:
                print("❌ Installation failed. Check error messages above.")
                return 1
                
        elif args.command == "validate":
            result = validate_environment(Path(args.path))
            if result:
                print("🧿 Super CC environment is valid and ready to use.")
            else:
                print("❌ Issues found with Super CC environment.")
                return 1
                
        elif args.command == "upgrade":
            installer = SuperCCInstaller(Path(args.path))
            result = installer.upgrade()
            if result:
                print("🧿 Super CC environment upgraded successfully!")
            else:
                print("❌ Upgrade failed. Check error messages above.")
                return 1
                
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user.")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())