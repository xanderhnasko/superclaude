#!/bin/bash
# Simple post-tool-use hook
TOOL="$1"
EXIT_CODE="$2"

# Auto-format if code was edited
if [[ "$TOOL" == "write" || "$TOOL" == "edit" ]]; then
  # Try formatters if available
  command -v black >/dev/null && black --quiet . 2>/dev/null
  command -v prettier >/dev/null && prettier --write . 2>/dev/null
fi

# If tests failed, suggest debugger
if [[ "$EXIT_CODE" != "0" && "$TOOL" == "bash" ]]; then
  echo "Tests failed. Consider using: 'Run debugger agent to diagnose'"
fi

exit 0