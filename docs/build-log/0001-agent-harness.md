# 0001 - Adopt an agent harness for the build

Status: accepted 2026-10-24

## Context

The project is built mostly by coding agents across many short sessions, in parallel worktrees, over about six weeks and with a hard deadline (cloud trial credits end 2026-12-06). Past work showed the usual failure modes: an agent declares a feature done without running anything, a new session starts without knowing the state, and rules drift between chat, memory and files. The Part 4 certification also requires explicit, checkable deliverables. The method comes from the "Learn Harness Engineering" material (walkinglabs).

## Decision

Adopt a repo-based harness:

- `AGENTS.md` is a short router with 15 hard rules; `CLAUDE.md` only imports it.
- `feature_list.json` is the single record of project state. A feature is `passing` only with recorded evidence, enforced by `scripts/check_feature_list.py`.
- `progress.md` is the session handoff.
- `init.sh` installs and runs the baseline verification (feature list, ruff, pytest, certification report).
- `scripts/check_certification.py` tracks the Part 4 requirements as an executable report.
- Work in progress is limited to one feature per branch or worktree. Large features use SDD with openspec artifacts in the repo.
- Engram keeps the why and pointers; the repo wins on any disagreement.

## Consequences

- Every session starts the same way and ends with an updated handoff.
- Verification is executable; claims without evidence are rejected by a script, not by trust.
- Overhead per feature: updating the list and progress file. This is accepted as cheaper than rediscovering state.
- The checks themselves need tests (they have them) and must never be weakened to pass.
- Rules in `AGENTS.md` are stable; changing one needs a new ADR.
