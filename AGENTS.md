# AGENTS.md

Underdoc turns an approved post idea into a Substack draft in Ricardo's voice that invents nothing. It combines Nova (research agent MCP), Brown (LangGraph writing workflow) and a capstone FastMCP server (root `src/`), with the voice rules in `voice/`. It is also the capstone for the Agentic AI Engineering course (Part 4 certification). This file is a router: follow the links for detail.

## Start of session

1. `pwd` (confirm you are in the repo root or a worktree of it).
2. Read `progress.md` (current state and next step).
3. Read `feature_list.json` (what is done, what is in progress).
4. `git log --oneline -5`.
5. Run `./init.sh` (use `./init.sh --quick` to skip `uv sync`).
6. If the baseline fails, fix it first. Do not start new work on a red baseline.

## Hard rules

1. One feature `in_progress` per branch or worktree. Finish or mark `blocked` before starting another.
2. A feature becomes `passing` only when its verification ran and the evidence (command and observed result) is recorded in `feature_list.json`. `scripts/check_feature_list.py` enforces this.
3. Never remove, weaken or skip a test or a verification step to make work look done.
4. Extend Nova and Brown, never rewrite their workflows (new tools, new guideline sources, replaced inputs only).
5. Voice rules live only in `voice/`. Brown and the judges read them; never copy rules elsewhere.
6. No secrets in the repo. `.env` stays local; `.env.sample` holds fake values only.
7. Substack tools create drafts only. Publishing tools stay disabled.
8. Claude Code session transcripts are never an input and never committed.
9. Conventional commits. No AI attribution or Co-Authored-By lines, even if a tool default adds them.
10. The repo is the system of record. Engram memory keeps the why and pointers to repo files; when they disagree, the repo wins.
11. Large or ambiguous features go through SDD with the file-based (openspec) artifact store, linked to a feature id. Small features are implemented directly.
12. The author does not grade their own work: risky diffs get a separate reviewer agent; voice changes count only if the evals beat the baseline by more than the measured noise.
13. Every feature ends in a small PR whose description lists the verification commands and their results.
14. Parallel agents use one git worktree each, under `~/Documents/underdoc-worktrees/<name>`, each with its own `.codegraph/` index.
15. Before ending a session: update `progress.md` and `feature_list.json`, record blockers, leave `./init.sh` passing.

## Where things are

- Plan: [docs/product/capstone-plan.md](docs/product/capstone-plan.md)
- How the harness layers fit: [docs/harness.md](docs/harness.md)
- Decisions (one ADR each): [docs/build-log/](docs/build-log/)
- Session handoff: [progress.md](progress.md)
- Feature state and evidence: [feature_list.json](feature_list.json)
- Startup and baseline verification: [init.sh](init.sh)
- Harness checks (feature list, certification): [scripts/](scripts/)
- `src/` is the capstone FastMCP server (course template layout, `uv run python -m src.server`); `make help` lists the commands
- `packages/nova` (research agent) and `packages/brown` (writing workflow): course code imported with git subtree; each has its own tests, run by `init.sh`
- `voice/`: the canonical voice (skill rules, `checks/check.py` gates, brief template in `pipeline/`, corpus). `UNDERDOC_HARNESS_PATH` points here; `init.sh` sets it when unset. The `underdoc-writer` skill reads `voice/skill/`
- Planned, not created yet: `evals/`, `drafts/<slug>/`
- Claude Code Stop hook (`.claude/settings.json` + `scripts/stop_hook.sh`): with uncommitted changes, an agent cannot end its turn while `./init.sh --quick` fails
- Deadline: cloud deployment and certification submitted before 2026-12-06 (trial credits end)

## Definition of done

A feature is done when all of these hold:

- The target behavior is implemented.
- Every command in the feature's `verification` ran, and its result is in `evidence`.
- `./init.sh` passes with the change applied.
- `feature_list.json` and `progress.md` are updated, and the repo can be resumed from a clean session.
- The change is a small PR with the verification results in its description.
