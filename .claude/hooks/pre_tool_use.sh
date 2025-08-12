#!/bin/bash
# Simple pre-tool-use hook
TOOL="$1"
FILE_PATH="$2"

# Check if path is in denylist
if [[ "$FILE_PATH" =~ \.(git|env|claude)/ ]]; then
  echo "Blocked: Protected path"
  exit 1
fi

# Log the action
echo "$(/bin/date '+%Y-%m-%d %H:%M:%S') - $TOOL: $FILE_PATH" >> .claude/logs/tools.log
exit 0