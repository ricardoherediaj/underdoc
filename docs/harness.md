# Harness

The repo is the system of record. Each concern has one owner; the other layers only point at it.

| Concern | Owner | What the other layer does |
| --- | --- | --- |
| Project state | `feature_list.json` | `progress.md` and PRs reference feature ids; Engram never holds status |
| Session handoff | `progress.md` | Engram keeps a pointer to it, not a copy |
| Project rules | `AGENTS.md` | The user-level gentle-ai CLAUDE.md governs how the agent works and is never duplicated here |
| Large features | SDD with openspec artifacts in the repo, linked to a feature id | Small features skip SDD and go straight to code |
| Verification | `make verify` (`init.sh`) + `scripts/check_*.py` + pytest + voice evals | Claude Code hooks run them; a claim without a command and result does not count |
| Checking | Separate reviewer agents and evals | The author never grades their own work |
| Code navigation | CodeGraph, one index per worktree | Never copy or symlink another checkout's `.codegraph/` |
| Decisions | `docs/build-log/` ADRs | Engram holds the raw record and the why, with pointers to the ADR |
| Memory | Engram | Why and pointers only; when it disagrees with the repo, the repo wins |

## Feature lifecycle

`not_started` -> `in_progress` (at most one per branch or worktree) -> `passing`. A feature may be `passing` only with its verification commands and observed results in `evidence`. `blocked` records the blocker in `notes`. `scripts/check_feature_list.py` runs inside `./init.sh` and fails on a `passing` feature without evidence, on two `in_progress` features, and on unknown ids, statuses or certification tags.

## How work speeds up

- Parallel worktrees: one feature per worktree under `~/Documents/underdoc-worktrees/<name>`, started from Orca, each with its own `.codegraph/` index and its own `in_progress` feature.
- Loops with a machine-checkable stop condition: a loop ends when the feature's verification passes and its evidence is recorded, or when the call budget runs out. A loop never ends on the agent's own judgment.
- Delegation by role: an explorer maps code, one writer changes it, a verifier runs the checks. Keep a single writer per worktree.
- Long evals run in the background and write results to files; the session continues and reads them later.
- Small PRs with evidence: human review is the real bottleneck, so each PR is one feature and lists the verification commands and their results.

## Certification tracking

`scripts/check_certification.py` reports the Part 4 mandatory items and counts passing `custom:*` features (4 needed). `--strict` exits 1 on any failure; `./init.sh` runs it in report mode until the final phase. Besides the README and secrets items, it checks the root `src/` layout, `.cursor/mcp.json` and that `src/config/settings.py` reads `ENV_FILE_PATH`.

## Commands

`make help` lists the targets. The ones the harness relies on: `verify` and `verify-quick` (wrap `init.sh`), `test`, the `format-fix`/`lint-fix`/`format-check`/`lint-check` quartet, and `cert-check` (strict certification report). `run` and `inspect` start the server and fail early with a clear message when `.env` is missing.
