#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
# Activate virtual environment if present
if [ -f "$DIR/venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "$DIR/venv/bin/activate"
fi
# Run main.py with the venv python if available
if [ -x "$DIR/venv/bin/python" ]; then
  "$DIR/venv/bin/python" "$DIR/main.py"
else
  python "$DIR/main.py"
fi
