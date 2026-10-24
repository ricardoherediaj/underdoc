# Underdoc

Turns an approved post idea into a Substack draft that sounds like Ricardo and invents nothing. Capstone project for the Agentic AI Engineering course (Part 4 certification).

Status: skeleton (phase S0, Monorepo). Nova and Brown are imported in the next steps.

## Layout

```
underdoc/
├── packages/nova/        # research agent (course research_agent_part_3), git subtree
├── packages/brown/       # writing workflow (course writing_workflow), git subtree
├── src/                  # the capstone FastMCP server (course template layout)
├── .cursor/mcp.json      # MCP client config for Cursor (.mcp.json for Claude Code)
├── voice/                # canonical voice: rules, gates, analysis, corpus (the harness)
├── evals/                # dataset, metrics, experiments
├── drafts/<slug>/        # per-post working files and draft snapshots
├── docs/product/         # capstone plan
├── docs/build-log/       # one ADR per decision
└── .github/workflows/    # CI and CD
```

It is a uv workspace: every folder under `packages/` is its own project, and all of them share one `uv.lock`.

## Setup

```bash
uv sync --all-packages
cp .env.sample .env   # then fill in the keys
```

## Working on this repo

Agents and contributors start from [AGENTS.md](AGENTS.md) (rules and session routine), then read [progress.md](progress.md) (current state and next step) and [feature_list.json](feature_list.json) (features, verification and evidence). `./init.sh` installs and runs the baseline verification; `make help` lists every command.
