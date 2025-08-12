#!/bin/bash
# Simple pre-tool-use hook
TOOL="$1"
PATH="$2"

# Check if path is in denylist
if [[ "$PATH" =~ \.(git|env|claude)/ ]]; then
  echo "Blocked: Protected path"
  exit 1
fi

# Log the action
echo "$(date '+%Y-%m-%d %H:%M:%S') - $TOOL: $PATH" >> .claude/logs/tools.log
exit 0