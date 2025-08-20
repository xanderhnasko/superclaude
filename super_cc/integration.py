"""
Super CC Integration

Handles smart integration with existing repositories including .gitignore
management and .claude directory merging.
"""

import filecmp
import shutil
from pathlib import Path
from typing import Set


class GitignoreManager:
    """Manages .gitignore file integration for Claude Code entries."""
    
    # Standard Claude Code entries that should be in .gitignore
    CLAUDE_ENTRIES = {
        "# Claude Code specific",
        ".claude/logs/",
        ".claude/state/",
        ".claude/cache/",
        ".claude/*.log",
        ".claude/context/summaries/",
        ".claude/context/last-build-commit",
    }
    
    def __init__(self, repo_path: Path):
        """Initialize manager for repository.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = Path(repo_path)
        self.gitignore_path = self.repo_path / ".gitignore"
    
    def ensure_claude_entries(self) -> bool:
        """Ensure .gitignore contains Claude Code entries.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            existing_entries = self._read_existing_entries()
            missing_entries = self.CLAUDE_ENTRIES - existing_entries
            
            if not missing_entries:
                print(".gitignore already contains all Claude Code entries")
                return True
            
            self._append_missing_entries(missing_entries)
            print(f"🫧 Added {len(missing_entries)} entries to .gitignore")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update .gitignore: {e}")
            return False
    
    def _read_existing_entries(self) -> Set[str]:
        """Read existing .gitignore entries.
        
        Returns:
            Set of existing entries
        """
        if not self.gitignore_path.exists():
            return set()
        
        try:
            content = self.gitignore_path.read_text()
            # Normalize lines (strip whitespace, remove empty lines)
            lines = {line.strip() for line in content.splitlines() if line.strip()}
            return lines
        except Exception:
            return set()
    
    def _append_missing_entries(self, missing_entries: Set[str]) -> None:
        """Append missing entries to .gitignore.
        
        Args:
            missing_entries: Set of entries to add
        """
        # Ensure file exists
        if not self.gitignore_path.exists():
            self.gitignore_path.write_text("")
        
        # Read existing content
        existing_content = self.gitignore_path.read_text()
        
        # Prepare new content
        if existing_content and not existing_content.endswith('\n'):
            existing_content += '\n'
        
        # Add separator and comment if file has content
        if existing_content.strip():
            new_content = existing_content + '\n# Super CC additions:\n'
        else:
            new_content = '# Super CC additions:\n'
        
        # Add Claude Code entries
        new_content += '\n'.join(sorted(missing_entries)) + '\n'
        
        # Write back
        self.gitignore_path.write_text(new_content)


class ClaudeDirectoryManager:
    """Manages intelligent merging of .claude directories."""
    
    def __init__(self, existing_dir: Path, template_dir: Path):
        """Initialize manager for directory merge.
        
        Args:
            existing_dir: Path to existing .claude directory
            template_dir: Path to template .claude directory
        """
        self.existing_dir = Path(existing_dir)
        self.template_dir = Path(template_dir)
    
    def merge_directories(self) -> bool:
        """Merge template directory into existing directory.
        
        Returns:
            True if merge successful, False otherwise
        """
        try:
            print("🔄 Merging directory structures...")
            
            # Process each subdirectory
            for template_subdir in self.template_dir.iterdir():
                if template_subdir.is_dir():
                    self._merge_subdirectory(template_subdir)
            
            # Process root files
            for template_file in self.template_dir.iterdir():
                if template_file.is_file():
                    self._merge_file(template_file, self.existing_dir / template_file.name)
            
            print("🪐 Directory merge completed")
            return True
            
        except Exception as e:
            print(f"❌ Directory merge failed: {e}")
            return False
    
    def _merge_subdirectory(self, template_subdir: Path) -> None:
        """Merge a subdirectory from template to existing.
        
        Args:
            template_subdir: Template subdirectory to merge
        """
        subdir_name = template_subdir.name
        existing_subdir = self.existing_dir / subdir_name
        
        # Create subdirectory if it doesn't exist
        existing_subdir.mkdir(exist_ok=True)
        
        # Handle different merge strategies based on directory type
        if subdir_name in {"agents", "commands", "workflows"}:
            self._merge_config_directory(template_subdir, existing_subdir)
        elif subdir_name in {"logs", "state", "cache"}:
            # Don't overwrite user data directories
            print(f"⏭️  Skipping user data directory: {subdir_name}/")
        else:
            # Default: copy new files, don't overwrite existing
            self._merge_default_directory(template_subdir, existing_subdir)
    
    def _merge_config_directory(self, template_dir: Path, existing_dir: Path) -> None:
        """Merge configuration directory (agents, commands, workflows).
        
        Args:
            template_dir: Template configuration directory
            existing_dir: Existing configuration directory
        """
        for template_file in template_dir.iterdir():
            if template_file.is_file():
                existing_file = existing_dir / template_file.name
                
                if existing_file.exists():
                    # Compare files to see if update is needed
                    if not filecmp.cmp(template_file, existing_file):
                        # Files differ - could prompt user or create backup
                        backup_name = f"{template_file.name}.backup"
                        backup_path = existing_dir / backup_name
                        shutil.copy2(existing_file, backup_path)
                        shutil.copy2(template_file, existing_file)
                        print(f"🔄 Updated: {existing_file.relative_to(self.existing_dir)} (backup created)")
                    else:
                        print(f"🪐 Up to date: {existing_file.relative_to(self.existing_dir)}")
                else:
                    # New file
                    shutil.copy2(template_file, existing_file)
                    print(f"➕ Added: {existing_file.relative_to(self.existing_dir)}")
    
    def _merge_default_directory(self, template_dir: Path, existing_dir: Path) -> None:
        """Merge directory with default strategy (add new, keep existing).
        
        Args:
            template_dir: Template directory
            existing_dir: Existing directory
        """
        for template_file in template_dir.iterdir():
            existing_file = existing_dir / template_file.name
            
            if template_file.is_file():
                if not existing_file.exists():
                    shutil.copy2(template_file, existing_file)
                    print(f"➕ Added: {existing_file.relative_to(self.existing_dir)}")
            elif template_file.is_dir():
                existing_file.mkdir(exist_ok=True)
                self._merge_default_directory(template_file, existing_file)
    
    def _merge_file(self, template_file: Path, existing_file: Path) -> None:
        """Merge a single file.
        
        Args:
            template_file: Template file
            existing_file: Existing file path
        """
        if existing_file.exists():
            if not filecmp.cmp(template_file, existing_file):
                backup_name = f"{existing_file.name}.backup"
                backup_path = existing_file.parent / backup_name
                shutil.copy2(existing_file, backup_path)
                shutil.copy2(template_file, existing_file)
                print(f"🔄 Updated: {existing_file.relative_to(self.existing_dir)} (backup created)")
        else:
            shutil.copy2(template_file, existing_file)
            print(f"➕ Added: {existing_file.relative_to(self.existing_dir)}")