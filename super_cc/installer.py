"""
Super CC Installer

Handles intelligent installation of Claude Code multi-agent environments
with backup, merge, and conflict resolution capabilities.
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from .integration import GitignoreManager, ClaudeDirectoryManager


class SuperCCInstaller:
    """Installer for Super CC multi-agent environment."""
    
    def __init__(self, target_path: Path):
        """Initialize installer for target repository.
        
        Args:
            target_path: Path to the target repository
        """
        self.target_path = Path(target_path).resolve()
        self.claude_dir = self.target_path / ".claude"
        self.templates_dir = Path(__file__).parent / "templates" / ".claude"
        
    def install(self, force: bool = False, backup: bool = True) -> bool:
        """Install Super CC environment.
        
        Args:
            force: Force installation even if .claude exists
            backup: Create backup of existing .claude directory
            
        Returns:
            True if installation successful, False otherwise
        """
        try:
            print(f"🧼 Installing Super CC environment in: {self.target_path}")
            
            # Validate target directory exists
            if not self.target_path.exists():
                print(f"❌ Target directory does not exist: {self.target_path}")
                return False
                
            # Check if .claude directory already exists
            if self.claude_dir.exists() and not force:
                print(f"⚠️  .claude directory already exists at: {self.claude_dir}")
                if backup:
                    if self._create_backup():
                        print("🪐 Existing .claude directory backed up")
                    else:
                        print("❌ Failed to create backup")
                        return False
                else:
                    print("❌ Use --force to overwrite existing installation")
                    return False
            
            # Install template files
            if not self._install_template_files():
                return False
                
            # Handle .gitignore integration
            gitignore_manager = GitignoreManager(self.target_path)
            if not gitignore_manager.ensure_claude_entries():
                print("⚠️  Warning: Could not update .gitignore file")
            
            # Make hooks executable
            self._make_hooks_executable()
            
            # Create initial state files
            self._create_initial_state()
            
            # Detect and suggest language-specific tools
            self._suggest_language_tools()
            
            print("� Super CC environment installed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def upgrade(self) -> bool:
        """Upgrade existing Super CC environment to latest version.
        
        Returns:
            True if upgrade successful, False otherwise
        """
        try:
            print(f"🔄 Upgrading Super CC environment in: {self.target_path}")
            
            if not self.claude_dir.exists():
                print("❌ No existing Super CC installation found. Use 'init' instead.")
                return False
            
            # Create backup before upgrade
            if not self._create_backup():
                print("❌ Failed to create backup before upgrade")
                return False
            
            # Use directory manager for intelligent merge
            manager = ClaudeDirectoryManager(self.claude_dir, self.templates_dir)
            if not manager.merge_directories():
                return False
            
            # Ensure hooks are executable
            self._make_hooks_executable()
            
            print("� Super CC environment upgraded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Upgrade failed: {e}")
            return False
    
    def _create_backup(self) -> bool:
        """Create timestamped backup of existing .claude directory.
        
        Returns:
            True if backup successful, False otherwise
        """
        if not self.claude_dir.exists():
            return True
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.target_path / f".claude.backup.{timestamp}"
        
        try:
            shutil.copytree(self.claude_dir, backup_path)
            print(f"📦 Backup created: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def _install_template_files(self) -> bool:
        """Install template files from package.
        
        Returns:
            True if installation successful, False otherwise
        """
        try:
            if not self.templates_dir.exists():
                print(f"❌ Template directory not found: {self.templates_dir}")
                return False
            
            # Remove existing directory if it exists
            if self.claude_dir.exists():
                shutil.rmtree(self.claude_dir)
            
            # Copy template directory
            shutil.copytree(self.templates_dir, self.claude_dir)
            print("� Template files installed")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install template files: {e}")
            return False
    
    def _make_hooks_executable(self) -> None:
        """Make hook scripts executable."""
        hooks_dir = self.claude_dir / "hooks"
        if hooks_dir.exists():
            for hook_file in hooks_dir.glob("*.sh"):
                try:
                    os.chmod(hook_file, 0o755)
                    print(f"� Made executable: {hook_file.name}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not make {hook_file.name} executable: {e}")
    
    def _create_initial_state(self) -> None:
        """Create initial state files."""
        state_dir = self.claude_dir / "state"
        state_dir.mkdir(exist_ok=True)
        
        # Create initial context file if it doesn't exist
        context_file = state_dir / "context.json"
        if not context_file.exists():
            context_file.write_text("{}")
            print("📄 Initial context file created")
        
        # Create logs directory
        logs_dir = self.claude_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        print("� Logs directory ready")
    
    def _suggest_language_tools(self) -> None:
        """Suggest language-specific tools based on project files."""
        suggestions = []
        
        # Check for different language ecosystems
        if (self.target_path / "package.json").exists():
            suggestions.append("Node.js detected - Consider: npm install --save-dev vitest eslint prettier typescript")
        
        if (self.target_path / "requirements.txt").exists() or (self.target_path / "pyproject.toml").exists():
            suggestions.append("Python detected - Consider: pip install pytest black ruff mypy")
        
        if (self.target_path / "Cargo.toml").exists():
            suggestions.append("Rust detected - Consider: cargo install cargo-watch")
        
        if (self.target_path / "go.mod").exists():
            suggestions.append("Go detected - Built-in tools available: go test, go fmt")
        
        if suggestions:
            print("💡 Suggested development tools:")
            for suggestion in suggestions:
                print(f"   {suggestion}")