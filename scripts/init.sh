#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

mkdir -p \
  "$ROOT/adr" \
  "$ROOT/backlog" \
  "$ROOT/logs" \
  "$ROOT/logs/archive" \
  "$ROOT/requirements" \
  "$ROOT/src" \
  "$ROOT/tests" \
  "$ROOT/tests/unit" \
  "$ROOT/tests/e2e" \
  "$ROOT/tests/results" \
  "$ROOT/scripts" \
  "$ROOT/references"

touch \
  "$ROOT/adr/.gitkeep" \
  "$ROOT/backlog/.gitkeep" \
  "$ROOT/logs/.gitkeep" \
  "$ROOT/logs/archive/.gitkeep" \
  "$ROOT/requirements/.gitkeep" \
  "$ROOT/src/.gitkeep" \
  "$ROOT/tests/.gitkeep" \
  "$ROOT/tests/unit/.gitkeep" \
  "$ROOT/tests/e2e/.gitkeep" \
  "$ROOT/tests/results/.gitkeep" \
  "$ROOT/references/.gitkeep"

# Append-only audit log entries for scripts-records.log
LOGFILE="$ROOT/logs/scripts-records.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INVOKE] init.sh args=[$ROOT]" >> "$LOGFILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [RESULT] init.sh status=OK detail=skeleton created at $ROOT" >> "$LOGFILE"

echo "Project skeleton created at: $ROOT"
