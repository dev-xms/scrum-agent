#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

mkdir -p \
  "$ROOT/adr" \
  "$ROOT/backlog" \
  "$ROOT/logs" \
  "$ROOT/requirements" \
  "$ROOT/src" \
  "$ROOT/tests" \
  "$ROOT/scripts" \
  "$ROOT/references"

touch \
  "$ROOT/adr/.gitkeep" \
  "$ROOT/backlog/.gitkeep" \
  "$ROOT/logs/.gitkeep" \
  "$ROOT/requirements/.gitkeep" \
  "$ROOT/src/.gitkeep" \
  "$ROOT/tests/.gitkeep" \
  "$ROOT/references/.gitkeep"

echo "Project skeleton created at: $ROOT"
