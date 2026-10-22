# Underdoc

Turns an approved post idea into a Substack draft that sounds like Ricardo and invents nothing. Capstone project for the Agentic AI Engineering course (Part 4 certification).

Status: skeleton (phase S0, Monorepo). The packages are imported in the next steps.

## Layout

```
underdoc/
├── packages/nova/        # research agent (course research_agent_part_3), git subtree
├── packages/brown/       # writing workflow (course writing_workflow), git subtree
├── packages/underdoc/    # the capstone FastMCP server (course src/ layout)
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
