#!/bin/bash
# Claude Code Environment Setup
set -e

echo "Setting up Claude Code environment..."

# Create directory structure
mkdir -p .claude/{agents,commands,hooks,logs,state}
mkdir -p {src,tests,docs}

# Create .gitignore for Claude files
cat > .claude/.gitignore << 'EOF'
logs/
state/
*.log
.DS_Store
EOF

# Detect language and install tools
if [ -f "package.json" ]; then
  echo "Node.js project detected"
  npm install --save-dev vitest eslint prettier typescript @types/node
elif [ -f "requirements.txt" ]; then
  echo "Python project detected"
  pip install pytest black ruff mypy
else
  echo "No package file found, skipping dependency installation"
fi

# Make hooks executable
chmod +x .claude/hooks/*.sh 2>/dev/null || true

# Create initial context file
echo "{}" > .claude/state/context.json

# Success message
echo "✓ Claude Code environment ready!"
echo "  - Agents in: .claude/agents/"
echo "  - Commands in: .claude/commands/"
echo "  - Logs in: .claude/logs/"
echo ""
echo "Start with: claude chat"
echo "Then use: /tdd 'your feature description'"
