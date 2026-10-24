#!/usr/bin/env bash
# Install dependencies and run the baseline verification. Use --quick to skip `uv sync`.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

quick=0
[ "${1:-}" = "--quick" ] && quick=1

echo "==> Working directory: $PWD"

if [ -z "${UNDERDOC_HARNESS_PATH:-}" ] || [ ! -f "${UNDERDOC_HARNESS_PATH}/checks/check.py" ]; then
  echo "WARNING: UNDERDOC_HARNESS_PATH is unset or has no checks/check.py (voice gates unavailable until s0-004)."
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
echo "==> Certification report"
uv run python scripts/check_certification.py

echo "==> Baseline OK"
