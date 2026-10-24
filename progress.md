# Progress

## Current verified state

- Repo root: `/Users/ricardoheredia/Documents/underdoc` (uv workspace, Python 3.14.0, public repo `ricardoherediaj/underdoc`).
- Startup path: `./init.sh` (`./init.sh --quick` skips `uv sync`).
- Verification path: `./init.sh` runs the feature-list check, ruff, pytest and the certification report. `uv run python scripts/check_certification.py --strict` is the certification gate (expected to fail until S3/S4 and cert-001).
- Highest-priority unfinished feature: `s0-004` (voice rules into `voice/`). `s0-001`, `s0-002`, `s0-003` and `s3-001` are passing.
- Current blocker: none.

## Decisions

- 2026-10-24 writer and editor model: `opencode_go:deepseek-v4-pro`. On the 3-post tuning set it wrote every post (VoiceAdherence 0.896 / 0.800 / 0.778, `no_invented_biography` 1.0 on the bridge post); GLM-5.3 took about 43 minutes per post and was stopped.
- 2026-10-24 Nova is imported from `research_agent_part_3` (deployable: auth and Docker, needed by S4 anyway).

## Open items

- S1.1 voice hardening still lives in the course repo `agentic-ai-engineering-course/odd/tasks/s1-1-hardening.md`, uncommitted. s0-002 and s0-003 need that work committed first, because `git subtree` imports committed history only.

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

### Session 002 (2026-10-25)

- s0-002 passing: Nova imported from the course repo `lessons/research_agent_part_3` with git subtree (61691c6). `requires-python` bumped to >=3.14.0, package renamed `nova`, its own uv.lock dropped (one workspace lock), own pytest config so `src` resolves to Nova and not the root server. Root ruff excludes `packages/` (course code keeps its style). `init.sh` now also runs Nova tests.
- Verification: `./init.sh --quick` Baseline OK (root 29 passed, Nova 17 passed); the Nova MCP server starts over stdio (FastMCP 4.1.3).
- Known gaps before Nova can research locally: its models are Gemini-only (free tier 20 req/day) and it stores research in Postgres (docker compose).
- Next best step: s0-003 (import Brown), then run Nova locally with OpenCode Go and Postgres.
- s0-003 passing: Brown imported from `lessons/writing_workflow` with git subtree (20b3d2e, 35 upstream commits). requires-python >=3.14.0, fastmcp >=2.13.1 (4.1.3), own uv.lock dropped. Brown suite 318 passed, 0 failed with no API keys: the 27 failures carried since S1 were a test-isolation bug (`s1.apply_config_file` leaked CONFIG_FILE into os.environ), fixed with an autouse fixture. `init.sh` also runs Brown tests.
- Next best step: s0-004 (voice rules into `voice/`), then run Nova and Brown from this repo for the T10 post.
