#!/usr/bin/env bash
# Local build only. Never uploads or pushes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/build.py" "${1:?Pass the upstream SKILL.md path}" "$ROOT/skills/meeting-notes/SKILL.md"
bash "$ROOT/scripts/guard.sh"
