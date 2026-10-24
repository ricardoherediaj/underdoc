# Underdoc Capstone Plan

Product and delivery plan for the Agentic AI Engineering capstone (Part 4 certification). The plan was shaped on 2026-10-04 with the Phase 14 "Product Judgment and Delivery" method (lessons 47 to 54 of aiengineeringfromscratch.com) and a grilling interview. Revision 2 (2026-10-04) applies the review in section 13.

Status: agreed, revision 2. It moves to `docs/product/` in the monorepo when the monorepo is created (slice S0).

## 1. Outcome frame (L47)

| Part | Definition |
| --- | --- |
| User | Ricardo, sole author of The Underdoc (Substack, 667 subscribers). |
| Situation | He has an idea captured in the Notion "Substack Content" articles database and wants it published. The idea can be any type he writes (see "Post types" below). |
| Current behavior | Claude with the underdoc-writer skill or the harness produces a generic draft. He pastes it into Substack and rewrites it slowly, then adds images and references. Build posts are the slowest: they take 1 to 2 weeks or die in drafts. Average gap between posts is about 20 days (9 to 32). |
| Desired outcome | Any post type goes from his approved angle and structure to a Substack draft with structure and images in place, sounding like him and with nothing invented. He only reviews and publishes, which sustains a fixed post every 15 days (stretch goal: weekly). Build posts are the hardest path, because they need build material read from repos, so they are the test case. |
| Constraints | He always publishes manually. There is one canonical voice definition. FastMCP in Python (certification). `uv init --python 3.14.0`. Public GitHub repo. Course-style CI/CD to GCP Cloud Run while trial credits last (until 2026-12-06). Low LLM cost. The AI never invents facts about his life or work. The 15-day publishing cadence is kept during the build itself. |
| Non-goals | Auto-publishing. Generated images or covers. Social media promotion. Topic ideation. Platform adaptations for X or LinkedIn. All of these are deferred, not rejected. |

Disproving observation: if a voice-matched draft still needs most of its sections rewritten, the bottleneck is not voice, and the frame must be revisited.

### Post types in the corpus

This is an approximate classification of the 26 posts by reading their titles; `analysis.json` does not record buckets.

| Type | Approx. count | Examples |
| --- | --- | --- |
| Builds: something he built, with code | ~13 | Transfermarkt scraping, football RAG series, tool-calling agent, finance automation, Claude skill for match reports |
| Explainers: teaching a concept or method, not a build | ~6 | Football data scouting I and II, data-driven strategies, MCP explained, uv, football framework for other industries |
| Bridge and personal: career, mindset, reflection | ~5 | Data learning diary, Embrace your weirdness, year-end thanks, Ryan Day interview |
| Field notes: news, events, opinion | ~2 (+2 recent) | Farewell FBref advanced stats, Venezuela earthquake, long-form writing, networking event |

Bucket decision (confirmed 2026-10-04): the taxonomy becomes builds / explainers / bridge / field-notes. The harness had no slot for explainers, even though they are a recurring type and drove some of the best engagement in 2025. The `explainers` bucket gets its own rules file in `voice/` during S1, before the dataset is labeled, because conditional routing by bucket is a declared workflow pattern and every dataset sample needs a bucket label. Explainers route to Nova without the build-reading tool: their sources are URLs and docs, not a repo.

## 2. Current workflow evidence (L48)

| Evidence | Strength | Finding |
| --- | --- | --- |
| `harness/drafts/2026-09-05-why-long-form...` vs. the post published on 2026-09-06 | Direct (artifact) | The text is about 95% identical. He gave the ideas and structure, the AI wrote it, he filtered it heavily, and it shipped in about 1 day. He rejected all three craft suggestions and reverted some phrasing fixes. |
| `harness/drafts/2026-08-23-how-to-look-for-a-mentor...` plus git history | Direct (artifact) | AI-drafted. The hook was rewritten twice and a rule was added to ban invented biographical premises. Unpublished after 6 weeks. |
| `harness/drafts/2026-09-13-bringing-attention-back` | Direct (artifact) | Stalled in drafting. |
| Substack RSS feed | Direct (system record) | 7 posts between May and Sep 2026; gaps of 32, 15, 27, 9, 20 and 17 days. |
| Ricardo's own description | Reported | Builds posts are the bottleneck: gathering the material and translating code into narrative. Bridge and field-notes posts come out fast. |

## 3. Assumptions and risk (L49)

Slices are ordered by risk: the riskiest assumption is tested first, before any infrastructure work.

| ID | Class | Falsifiable assumption | Risk | Resolved by |
| --- | --- | --- | --- | --- |
| A2 | Value / feasibility | With the unified voice, Brown output beats the current harness baseline on VoiceAdherence, FollowsGT and UserIntent by more than measured noise. | Highest. It already failed in August, and Brown's profiles enforce the opposite voice. | S1 (first) |
| A1 | Feasibility / safety | Nova can reconstruct a build story from README, `docs/build-log/` and git history, with every claim traceable to a source. | High | S2 (`research_anchoring`) |
| A3 | Viability | Drafts with images can be created through the unofficial Substack API (cookie auth) and keep working, including from a datacenter IP (Cloud Run). | Medium. The capability was verified in the marcomoauro/substack-mcp docs; datacenter IP behavior is unverified. | Spike in S0, full in S3 |
| A4 | Feasibility | Nova, Brown and Opik dependencies run on Python 3.14. | Medium. Not yet verified. | S0 spike |

## 4. Architecture

### Components

| Component | Role | Origin |
| --- | --- | --- |
| Nova | Research agent. Gains a new tool, `process_local_build_tool`, that reads README, `docs/build-log/`, git log, and the repo tree when no docs exist. Every claim cites its source. Claude Code sessions are not an input in v1 (see section 9). | Course (`research_agent_part_3`), extended |
| Brown | Writing workflow with an evaluator-optimizer loop. Its profiles are replaced so they read the canonical `voice/`. It already generates Mermaid diagrams. | Course (`writing_workflow`), adapted |
| Underdoc MCP | The capstone server: exposes the voice as MCP resources, provides the HITL prompt (approve the angle and structure as a diff), and creates the Substack draft with images. | New |
| `voice/` | The single source of truth for the voice: harness rules, `check.py` gates, `analysis.json`, the 26-post corpus. | Harness, promoted |
| Substack | Draft creation, body structure, image upload. | marcomoauro/substack-mcp capabilities (integration approach decided in S3) |

### Invariant: extend Nova and Brown, never rewrite them

This decision is locked (L51). Nova and Brown keep their course workflows: Nova's research loop, Brown's nodes and evaluator-optimizer loop, and the `article_guideline` contract. They change only through extensions:

- New tools. Example: `process_local_build_tool` in Nova.
- New sources declared in the article guideline. Nova already reads URLs, GitHub repos, YouTube and web search; Notion is just where the idea is seeded. X posts work as plain URLs through Nova's Firecrawl scraper. This was verified on 2026-10-04 with one public post; threads and protected accounts are untested.
- Replaced inputs. Brown's profile files read the canonical `voice/` instead of the course's team-voice profiles. The content changes; the mechanism does not.

Upstream mergeability: Nova and Brown are imported with `git subtree`, so their history is kept and upstream course fixes can still be pulled. If no upstream merge has been needed by the end of S4, drop this promise and treat both packages as owned code.

### Repository layout (uv workspace monorepo)

```
underdoc/
├── packages/nova/        # research (course + build-reading tool), git subtree
├── packages/brown/       # writing (course, profiles read voice/), git subtree
├── packages/underdoc/    # capstone FastMCP server (course src/ layout)
├── voice/                # canonical voice: rules, gates, analysis, corpus
├── evals/                # dataset, metrics, Opik experiments
├── drafts/<slug>/        # per-post working files and draft snapshots
├── docs/product/         # this plan and the L47-L54 artifacts
├── docs/build-log/       # ADR per decision (raw material for the final post)
└── .github/workflows/    # CI + CD
```

The certification accepts an adapted structure if the README explains it.

### Flow

1. Ricardo picks an idea from Notion. The system creates `drafts/<slug>/01_topic.md` and an article guideline, which is Nova and Brown's native input.
2. HITL 1: Ricardo approves the angle and structure as a diff in Claude Code.
3. Nova builds `research.md` from the build material.
4. Brown writes in the canonical voice. The evaluator-optimizer loop runs with `check.py` gates.
5. Underdoc MCP uploads the images, renders Mermaid in the black-and-white brand theme, and creates the Substack draft. It stores a snapshot as a file in `drafts/<slug>/`.
6. HITL 2: Ricardo reviews in Substack and publishes.
7. The online metrics compare the snapshot with the published post.

### Runtime

Course-style deployment: Docker, Descope auth, GitHub Actions CI, and CD to Cloud Run. In the cloud, build material reaches Nova through GitHub URLs or file upload, as in the course. Draft snapshots and scores are stored as files; a database is added only if file storage blocks a real need (see section 6). Migrating back to local with docker-compose after the credits run out is deferred.

## 5. Canonical voice

Verdict: the harness is canonical because it is the only source grounded in measured corpus data. Its calibration already rejected rules that the data contradicted.

| Source | Decision |
| --- | --- |
| `harness/skill` + `analysis/` + `checks/` | Promote to `voice/`. This is the canonical source. |
| Older claude.ai-synced underdoc-writer | Retire it, then re-sync the claude.ai skill from `voice/`. Merge useful prose from `headline-formulas.md` and `nicolas-cole-structures.md` if it adds anything. |
| codemarketers `voice_fingerprint.json` | It is uncalibrated by its own `_meta`. Later, generate it from `voice/`; its platform-adaptation ideas are deferred. |
| Brown `inputs/profiles/*.md` | Replace them. `mechanics_profile.md` mandates the team "we" and forbids singular first person, the opposite of Ricardo's voice. |

Rule changes:

- Fix real grammar and typos; Ricardo wants to improve his English. Preserve voice, not errors.
- Keep G-04 (I/we ratio) advisory. "We" is legitimate when it means Ricardo plus named others.
- Re-check the length ceiling, because 2026 technical posts run longer than the 2025 posts that set it.

## 6. Certification mapping

### Mandatory (all required)

FastMCP Python server. At least one meaningful tool. At least one MCP prompt that chains tools with a human approval step. Public GitHub repo. `uv init --python 3.14.0`. An organized `src/` layout explained in the README. The README template fully filled in, including the Cursor JSON config. `.env.sample` with no secrets.

### Custom features (at least 4 required)

The certification needs 4. Features are tiered so the build effort goes where the outcome needs it, and the list is cut from the bottom when time runs short.

| Tier | Feature | How |
| --- | --- | --- |
| Core: the outcome needs it anyway | HITL generation to validation UX | Angle and structure approved as diffs |
| Core | Evals: dataset + LLM judge | See section 7 |
| Core | Opik observability | Traces for Nova, Brown and Underdoc |
| Core | Cloud deployment | Cloud Run CD, as in L34 |
| Free: falls out of existing work | Third-party APIs | Gemini, Substack, GitHub |
| Free | MCP resources | Canonical voice and corpus exposed as resources |
| Free | Workflow patterns (2-3) | Sequential pipeline, evaluator-optimizer, conditional routing by bucket |
| Free | CAG | Voice rules and corpus examples loaded into context |
| Free | Custom domain data | 26-post corpus and voice analysis |
| Free | Pydantic structured outputs | Judges and pipeline outputs |
| Course-style, needed by deployment | ruff, pre-commit, CI, Docker | As in L31 and L32 |
| Course-style, needed by deployment | Descope auth | As in L32 and L34 |
| Cut first | Database + docker-compose | Snapshots and scores live in files until a real need appears |
| Candidate | Multi-agent | Nova and Brown collaborating may qualify; not targeted |
| Out | MCP client, ReAct, RAG, 3 memory types, multimodal | Not needed for the outcome. Multimodal returns with the brand visual system. |

## 7. Measurement plan (L52, translated from course L27-L30)

### Method (Evaluation-Driven Development)

- Binary 0/1 criteria, judged per H2 section, never Likert scales.
- The judge treats the generator as a black box over input, output and ground truth.
- Baseline first: run the current harness with Brown before any change.
- Noise: rerun a fixed subset of 5 posts (at least one per bucket) 5 times and record the standard deviation of each metric. The full test set runs once per iteration.
- Decision rule: a change improves the system only if it beats the baseline by more than the measured noise.

### Offline metrics

| Metric | Criteria | Reference |
| --- | --- | --- |
| FollowsGT | content, flow, structure vs. the published post | `brown/evals/metrics/follows_gt/` |
| UserIntent | guideline_adherence, research_anchoring (nothing invented) | `brown/evals/metrics/user_intent/` |
| VoiceAdherence (new) | Granular binary criteria derived from `voice/` rules | New, same base class and pattern |

### Dataset (following `lessons/28_ai_evals_offline_dataset`)

- 26 published posts as ground truth.
- Each sample contains `article_guideline.md` and `article_ground_truth.md`. `research.md` is reconstructed only for posts that depend on external material (builds and explainers), because only UserIntent needs it. Bridge and field-notes posts are scored on VoiceAdherence and FollowsGT only.
- Leakage control: each `article_guideline.md` is written as a short brief, the way the original idea would have been captured before writing (angle, audience, 3 to 6 section intents, sources). It must not copy phrasing, examples or conclusions from the published post. A guideline longer than about 300 words is a leakage warning.
- Split: 2 few-shot (labeled, embedded in judge prompts), 2 validation (Ricardo labels them section by section to align the judge with his judgment), 22 test.

### LLM budget (Gemini free tier, about 1,500 requests per day)

Rough count per full iteration: about 22 Brown generations at 6 or more calls each (about 130 calls), plus judge calls of 22 posts × about 6 sections × 3 metrics (about 400 calls). The noise subset adds 5 posts × 5 runs of generation and judging (about 600 calls), but it runs once per mechanism change, not every iteration. One iteration fits in a day; the noise measurement may take a second day. Judges batch all criteria of one metric for one section in one call. If a run hits the quota, it resumes from cached outputs instead of restarting.

### Online metrics (per real post)

| Metric | Source |
| --- | --- |
| Section survival rate: % of H2 sections that keep at least 70% of their text from the draft snapshot to the published post | Snapshot file + RSS |
| Calendar days from draft to publish | Substack timestamps |
| "Published with 2 hours or less of editing" (yes/no) | Ricardo |
| Generation time | Opik traces |

Section survival definition: split both versions on H2 headings. Match sections by normalized heading text; unmatched sections fall back to matching by position. A section survives when `difflib.SequenceMatcher(None, draft, published).ratio()` is 0.7 or higher on whitespace-normalized text. A draft section with no match counts as not surviving. The script lives in `evals/` and has one test.

The first 3 posts form the online baseline; later posts compare against it. If offline VoiceAdherence is high but sections get rewritten, the judge is misaligned, and that becomes a ratchet action (section 10).

### Capstone success

The test post (this build) reaches a Substack draft within 2 days or less, needs 2 hours or less of editing, invents nothing, follows the approved structure, and sounds like Ricardo.

### Amendment: metric admission rule (2026-10-17, S1.1)

FollowsGT keeps being reported but no longer decides. In the S1 setup, flow and structure score 0.000 in both arms with zero noise and content noise is 0.236, so the metric cannot move: it does not discriminate, and a metric that cannot move cannot decide. The rule: a metric enters a decision rule only when it shows measurable noise or a measurable delta against the baseline. Structure is owned by the outline approved at HITL 1, `guideline_adherence` and the online section-survival rate. The course metric itself is untouched.

The amendment is not a reaction to the S1 result and does not bias it: the S1 verdict was written under the strict three-metric rule, and under that rule A2 was not fully proven.

Two corrections from the S1 verdict also belong to this section: the Gemini free tier allows 20 requests per day for `gemini-3.7-flash`, not about 1,500, so the evals run on OpenCode Go; and the course judge makes one call per article per metric, not one per section, so the per-section count above overestimates by about 6×.

## 8. Slices and stages (L50, L53)

Order is by risk, not by layer: S1 runs first in the existing course repo, and the monorepo (S0) is built only after A2 holds. Every slice ends by serving a real post.

| Order | Slice | Scope | Proves | Real post served | Stage |
| --- | --- | --- | --- | --- | --- |
| 1 | S1 | In the current course repo: unified voice (harness files read by Brown), Brown profiles replaced, `explainers` bucket rules, dataset labeled with 4 buckets, three metrics in Opik, baseline vs. new | A2 | Next post written with the new Brown voice, edited and published by hand | Prototype |
| 2 | S0 | Monorepo with `git subtree` imports, uv with Python 3.14 spike, harness promoted to `voice/`, CI with ruff and tests, Substack cookie auth check from a Cloud Run job | A4, A3 (partial), everything runs together | Next post produced from the monorepo | Prototype |
| 3 | S2 | `process_local_build_tool` in Nova (README, build-log, git log, repo tree) | A1 | A build post researched by Nova | Prototype |
| 4 | S3 | Underdoc MCP: voice resources, HITL prompt, Substack draft with images, Mermaid black-and-white theme | A3 | A post that arrives in Substack as a draft | Prototype |
| 5 | S4 | Docker, Descope, CD to Cloud Run | Course-style deployment | A post produced through the deployed server | Pilot |
| 6 | S5 | Write the post about this build; online metrics vs. baseline | The full outcome | This build's post | Pilot |

The stage is visible in the system itself: config flag, README and telemetry tags. Production (SLO, on-call) does not apply.

Cadence rule: one post every 15 days continues during the build. A slice that is not ready by a publishing date does not block the post; the post ships with whatever pipeline state exists, and its online metrics still count.

S1 stop rule: if the new voice does not beat the baseline by more than the noise after 2 iterations, change the mechanism (for example, from rules to corpus examples in context) before continuing.

### Timeline

| Date | Target |
| --- | --- |
| 2026-10-30 (internal, soft) | S1 done well, one post published with the new voice, S0 started. |
| November 2026 | S0, S2 to S4, then S5 (the post). Two posts published along the way. |
| Before 2026-12-06 | Cloud deployment demonstrated on trial credits; certification submitted. |

## 9. Guardrails and known risks

- Claude Code sessions are out of v1: transcripts can hold API keys, env values or private data, and a sanitization miss leaks them into a public repo. Nova reads README, `docs/build-log/` and git history instead. Sessions are added only if A1 fails without them, and then with local sanitization and never committed raw.
- Substack cookie auth: the API is unofficial and fragile in the cloud, and Substack may treat datacenter IPs differently. This is checked in S0, not discovered in S3. Failures must be loud, and the substack-mcp version must be pinned. Publishing tools stay disabled.
- Python 3.14: dependency compatibility is unverified until the S0 spike.
- Gemini free tier quota: see the budget in section 7.
- Small online sample: one post every 15 days gives about 3 posts by mid-December, which is only enough for a baseline.

## 10. Feedback ratchet (L54)

Every signal is routed to the earliest layer that owns it:

| Signal | Destination |
| --- | --- |
| Section rewritten by Ricardo | VoiceAdherence criteria or a `voice/` rule |
| Invented fact | Nova sourcing or the `research_anchoring` threshold |
| A gate he overrides when publishing | Rule review (candidate for retirement) |
| Substack or API failure | Runtime control |
| New wish (images, X threads, topic radar) | Shaped backlog item |

Each action has an owner (Ricardo), a verification step and a retirement condition. A failure is fixed with a test or rule, not with another prompt paragraph.

## 11. Build documentation

- `docs/build-log/`: one short ADR per decision, written as it is made.
- Engram as the raw record of decisions.
- Both feed Nova for the final post. This planning session is chapter 1.

## 12. Deferred backlog

Brand visual system and generated images (via codemarketers). X and LinkedIn derivations. Topic radar from Substack feeds. Refreshing voice stats from Substack analytics. Database + docker-compose. Claude Code sessions as a Nova source (only if A1 fails without them). Local docker-compose migration after the credits run out. Deciding whether Underdoc calls substack-mcp as an MCP client or reimplements the needed calls (decided in S3).

## 13. Revision 2 changes (2026-10-04)

1. Slice order follows L49: S1 (riskiest assumption, A2) runs first in the current repo; the monorepo (S0) comes after A2 holds.
2. Custom features are tiered (core, free, course-style, cut first). Database + docker-compose moved to the backlog; snapshots live in files.
3. Every slice serves a real post, and the 15-day cadence continues during the build, so the outcome is tested from October instead of December.
4. Eval budget made explicit against the Gemini free tier; noise measured on a 5-post subset; guideline leakage control added.
5. Claude Code sessions removed from S2 v1 (secret-leak risk in a public repo); README, build-log and git history are the sources.
6. Nova and Brown are imported with `git subtree` to keep upstream mergeability, with an exit condition.
7. The `explainers` bucket is added (confirmed); its rules are written in S1, before dataset labeling.
8. Section survival rate has a reproducible definition.
9. Substack cookie auth from a datacenter IP is checked in S0.

## 14. Amendment 2026-10-24: layout

The capstone FastMCP server moved from `packages/underdoc` to the repo root `src/` to match the course template (`uv run python -m src.server`). `packages/` now holds only Nova (`packages/nova`) and Brown (`packages/brown`). Wherever this plan says `packages/underdoc`, read root `src/`.
