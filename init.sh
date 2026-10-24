#!/usr/bin/env bash
# Install dependencies and run the baseline verification. Use --quick to skip `uv sync`.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

quick=0
[ "${1:-}" = "--quick" ] && quick=1

echo "==> Working directory: $PWD"

# The voice rules and gates live in voice/; Brown's slop gate reads them through UNDERDOC_HARNESS_PATH.
export UNDERDOC_HARNESS_PATH="${UNDERDOC_HARNESS_PATH:-$PWD/voice}"
if [ ! -f "${UNDERDOC_HARNESS_PATH}/checks/check.py" ]; then
  echo "ERROR: ${UNDERDOC_HARNESS_PATH}/checks/check.py not found. Point UNDERDOC_HARNESS_PATH at the voice/ folder." >&2
  exit 1
fi

if [ "$quick" -eq 0 ]; then
  echo "==> uv sync --all-packages"
  uv sync --all-packages
fi

echo "==> Feature list"
uv run python scripts/check_feature_list.py
echo "==> ruff check"
uv run ruff check .
echo "==> ruff format --check"
uv run ruff format --check .
echo "==> pytest"
uv run pytest -q
if [ -d packages/nova ]; then
  echo "==> pytest (packages/nova)"
  (cd packages/nova && uv run --package nova pytest -q)
fi
echo "==> voice gate tests"
(cd voice && python3 -I -m unittest discover -s tests -q)
if [ -d packages/brown ]; then
  echo "==> pytest (packages/brown)"
  (cd packages/brown && uv run --package brown pytest -q)
fi
echo "==> Certification report"
uv run python scripts/check_certification.py

echo "==> Baseline OK"
