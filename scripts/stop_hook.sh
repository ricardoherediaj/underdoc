#!/usr/bin/env bash
# Claude Code Stop hook: an agent cannot end its turn on a red baseline.
# Blocks once with the failing output; a second stop (stop_hook_active) is let through to avoid loops.
set -uo pipefail

input="$(cat)"
if [ "$(jq -r '.stop_hook_active // false' <<<"$input")" = "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}" || exit 0

# Nothing changed since the last commit: nothing new to verify.
if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
  exit 0
fi

if output="$(./init.sh --quick 2>&1)"; then
  exit 0
fi

jq -n --arg out "$(tail -n 40 <<<"$output")" \
  '{decision: "block", reason: ("./init.sh --quick failed. Fix the baseline before stopping (AGENTS.md rule 15).\n\n" + $out)}'
