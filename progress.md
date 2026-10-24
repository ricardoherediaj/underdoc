# Progress

## Current verified state

- Repo root: `/Users/ricardoheredia/Documents/underdoc` (uv workspace, Python 3.14.0, public repo `ricardoherediaj/underdoc`).
- Startup path: `./init.sh` (`./init.sh --quick` skips `uv sync`).
- Verification path: `./init.sh` runs the feature-list check, ruff, pytest and the certification report. `uv run python scripts/check_certification.py --strict` is the certification gate (expected to fail until S3/S4 and cert-001).
- Highest-priority unfinished feature: `s0-002` (import Nova). `s0-001` and `s3-001` are passing, commit pending owner review.
- Current blocker: none.

## Open decisions

- Writer model: GLM-5.3 vs DeepSeek V4 Pro, being measured 2026-10-24.
- Import Nova from `research_agent_part_3` (deployable, auth and Docker) or `research_agent_part_2`.
- S1.1 voice hardening still lives in the course repo `agentic-ai-engineering-course/odd/tasks/s1-1-hardening.md`.

## Session log

### Session 001 (2026-10-24)

- Goal: build the agent harness only (no feature code).
- Completed: AGENTS.md, CLAUDE.md, feature_list.json (25 features), progress.md, init.sh, scripts/check_feature_list.py, scripts/check_certification.py, tests for both, ruff and pytest config, docs/harness.md, ADR 0001, docs/product/capstone-plan.md (verbatim copy), README "Working on this repo" section. `cert-003` set to `passing` with observed evidence.
- Verification run:
  - `./init.sh`: passed. feature_list.json OK (25 features); ruff check and format clean; pytest 13 passed; warning that UNDERDOC_HARNESS_PATH is unset (expected until s0-004).
  - `uv run python scripts/check_certification.py --strict`: exit 1. OK: uv on Python 3.14, .env.sample, .env untracked, no secrets. FAIL: README Cursor JSON block, src layout in packages/underdoc, @mcp.prompt registration, custom features 0/4.
  - `wc -l AGENTS.md docs/harness.md`: 51 and 31 lines.
  - `git status --short`: modified README.md, pyproject.toml, uv.lock; new AGENTS.md, CLAUDE.md, docs/, feature_list.json, init.sh, scripts/, tests/. Nothing committed.
- Files updated: see Completed.
- Risks: the README placeholder check treats any `[text]` outside code fences and links as a placeholder. (The secret scan now also covers untracked, non-ignored files.)
- Next best step: review and commit this harness (s0-001 to `passing` once a fresh-session orientation test is recorded), then s0-002 (import Nova with git subtree).

### Session 001, phase A (harness finish)

- `scripts/check_certification.py` now checks the root `src/` layout (including `src/resources` and `src/prompts`), `@mcp.prompt`/`mcp.prompt(` registration under `src/`, `.cursor/mcp.json` (valid JSON, server running `src.server`), `ENV_FILE_PATH` in `src/config/settings.py`, and the full README template (12 headings, no placeholders, Architecture >= 250 words). Tests were written first and failed before the implementation.
- Added `Makefile` (`make help` default; `.env` guard only on `run` and `inspect`), `LICENSE` (MIT), restructured `.env.sample` (Required/Optional), `.cursor/mcp.json`, `.mcp.json`. Updated AGENTS.md (55 lines), README layout, docs/harness.md, and appended the layout amendment to the capstone plan.
- `make verify-quick`: Baseline OK. `s0-001` set to `passing`.

### Session 001, phase B (s3-001 skeleton)

- `uv add "fastmcp>=2.13.1" pydantic-settings` resolved on Python 3.14 (fastmcp 4.1.3).
- Created flat `src/` (server, three empty routers, settings, empty `tools/ resources/ prompts/ app/ utils/`) and tests in `tests/test_server.py` and `tests/config/test_settings.py`. Added `pythonpath = ["."]` to pytest config.
- `make verify-quick`: Baseline OK, 29 passed. Server starts over stdio and exits 0 on EOF. `s3-001` set to `passing`.
- API keys in `src/config/settings.py` are `SecretStr` (test asserts the key never appears in `repr`).
- `make cert-check` still fails: README template (cert-001), HITL prompt (s3-003), custom features 0/4.
- Next best step: review and commit phases A and B, then s0-002 (import Nova).
