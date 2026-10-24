# Underdoc

Turns an approved post idea into a Substack draft that sounds like Ricardo and invents nothing. Capstone project for the Agentic AI Engineering course (Part 4 certification).

Status: skeleton (phase S0, Monorepo). Nova and Brown are imported in the next steps.

## Layout

`(planned: <id>)` marks a folder that does not exist yet; the id is its feature in `feature_list.json`.

```
underdoc/
├── src/                  # the capstone FastMCP server (course template layout)
│   ├── server.py         #   creates the FastMCP app and registers the routers
│   ├── routers/          #   tools.py, resources.py, prompts.py (empty until s3-002 to s3-004)
│   ├── tools/ resources/ prompts/ app/ utils/
│   └── config/settings.py  # pydantic-settings, reads the env file from ENV_FILE_PATH
├── tests/                # pytest suite for src/ and scripts/
├── scripts/              # harness checks (feature list, certification) and the Stop hook
├── docs/
│   ├── product/          # capstone plan
│   ├── build-log/        # one ADR per decision
│   └── harness.md        # how the agent harness layers fit
├── AGENTS.md             # agent rules and session routine (CLAUDE.md imports it)
├── feature_list.json     # features, verification commands, status and evidence
├── progress.md           # current verified state and session log
├── init.sh               # install and baseline verification
├── Makefile              # `make help` lists every command
├── .cursor/mcp.json      # MCP client config for Cursor (.mcp.json for Claude Code)
├── .claude/settings.json # Claude Code Stop hook
├── packages/nova/        # research agent from the course (research_agent_part_3), git subtree
├── packages/brown/       # writing workflow from the course (writing_workflow), git subtree
├── voice/                # canonical voice: skill rules, gates (checks/), analysis, brief template, 26-post corpus
├── evals/                # dataset, metrics, experiments (planned: s3-007)
├── drafts/<slug>/        # per-post working files and draft snapshots (created by the first post)
└── .github/workflows/    # CI and CD (planned: s0-006, s4-003)
```

It is a uv workspace: every folder under `packages/` will be its own project, and all of them share one `uv.lock`.

## Setup

```bash
uv sync --all-packages
cp .env.sample .env   # then fill in the keys
```

## Working on this repo

Agents and contributors start from [AGENTS.md](AGENTS.md) (rules and session routine), then read [progress.md](progress.md) (current state and next step) and [feature_list.json](feature_list.json) (features, verification and evidence). `./init.sh` installs and runs the baseline verification; `make help` lists every command.
