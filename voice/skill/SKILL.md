---
name: underdoc-writer
description: Use when writing, outlining, or reviewing posts for "The Underdoc" Substack — drafting a post, proposing a layout, picking a topic bucket, checking a draft's voice, or improving a headline. Covers AI engineering, RAG, data engineering, football-analytics-as-sandbox, and career-transition topics in Ricardo's voice.
---

# The Underdoc Writer (v2)

Voice rules measured from Ricardo's 26 published posts (engagement data attached), not invented. Every rule carries the deterministic gate that enforces it (`G-01`…`G-08`, run `python3 checks/check.py <draft>` in the harness repo) or the tag `[advisory]` — meaning it is applied here and at human review, never claimed as automated.

**Core principle: the numbers are descriptive, never targets.** They say what Ricardo's writing looks like ("paragraphs tend to run one or two sentences"), not quotas to hit. A draft that chases the metrics and reads dead has failed; a draft that breaks a band for a reason is Ricardo's call.

## Buckets

| Bucket (frontmatter slug) | What it is | Artifact the reader leaves with |
|---|---|---|
| **Builds** (`builds`) | Something Ricardo built, end to end, with the mess shown | A template, repo, or skill they can use |
| **Explainers** (`explainers`) | Teaches a concept, tool, or method from docs and sources; no repo is the subject | A mental model plus a worked example they can reuse |
| **Bridge** (`bridge`) | Career/mindset for non-traditional paths into tech | A method they can apply |
| **Field notes** (`field-notes`) | A tool, paper, event, or opinion — shorter, 400–900 words | A take they can act on |

Target mix: **2 Builds : 1 Bridge**. A Field note that shows up today beats a Build the ratio wanted. `[advisory]`

**Topic scope** `[advisory]`: football is the sandbox, never the axis. Conversational AI, voice, healthtech are in scope as *patterns only* — never Tucuvi internals. No active-interview references, no negative framing of any employer (see `references/voice-tonality.md`, Professional discretion).

## Gate zero: the takeaway test

*What does the reader do differently tomorrow?* No concrete answer → no article. This is the only test that touches substance; every gate below only touches form. A post can pass all eight gates and still be worthless — this question is what stops that. `[advisory]`

## Drafting workflow

1. **Topic** (`01_topic.md`): thesis, bucket, takeaway answer, artifact, standalone check.
2. **Layout** (`02_layout.md`): flat functional headings, `[SCREENSHOT: ...]` slots, hook sketched. Human approves before drafting. For a Brown run, the approved layout becomes `article_guideline.md` (template in `pipeline/`), with Ricardo's `## Experience notes`; first person without a source becomes `[EXPERIENCE: ...]`.
3. **Draft** (`03_draft.md`): apply the three voice files below. End with `Till next time, Ricardo.` Frontmatter (`G-08`):

   ```yaml
   ---
   title: "..."
   bucket: builds | explainers | bridge | field-notes   # hyphenated slugs, machine-checked
   status: drafting | slop-pass | checked | human-review | ready | published | killed
   target_words: 1100
   ---
   ```
4. **Slop pass**: run the `no-ai-slop` skill in voice-preserving edit mode, then do the **two-beat sweep** by hand — `no-ai-slop` under-catches this family and the gates cannot see it at all. Read every pair of adjacent short sentences, especially the hook and the closer, and ask whether the second exists only to reverse, mirror, or label the first. Four of the first four live corrections on this pipeline were this one shape. See `references/voice-mechanics.md`. Log it in `04_review.md` step 1b (checkboxed, so it can't be skipped).
5. **Gates**: `python3 checks/check.py` — canonical blacklists live in `checks/blacklist-words.txt` and `checks/blacklist-patterns.txt`.
6. **Craft review**: run the protocol in `references/review-pass.md` — one scanner-first read, then at most five findings ranked by reader-cost, each a short quote, one named disease, and a minimal voice-preserving fix. When the piece's shape is the problem (buried lead, stalling sections, missing ending), run the layout pass first — same file; it outputs a proposed skeleton into `02_layout.md` for approval. Fewer is fine; zero is a result. Advisory; the voice files win on any conflict.
7. **Human review**: the only real gate before publishing.

## Voice references (orthogonal — each rule lives in exactly one file)

| File | Covers |
|---|---|
| `references/voice-tonality.md` | Formality, honest-admission pattern, specificity, story mode, professional discretion |
| `references/voice-mechanics.md` | I-not-we (`G-04`), slop words and patterns (`G-05`), punctuation, active voice |
| `references/voice-structure.md` | Paragraph rhythm, sentence length, headings (`G-02`), word count (`G-01`), sign-off (`G-03`), standalone rule (`G-06`), images (`G-07`) |

## Structure templates (Nicolas Cole framework, `[advisory]`)

- `references/nicolas-cole-structures.md` — technical posts (lead with problem or metric)
- `references/build-story-structure.md` — "I automated X" posts (pain → manual process → build → what broke → takeaway)
- `references/explainer-post-structure.md` — concept/tool/method posts sourced from docs and URLs, not a repo (friction → definition + analogy → worked example → takeaway)
- `references/conceptual-post-structure.md` — idea-led posts (idea → framework → story as evidence → reader's mirror)
- `references/headline-formulas.md` — headline answers What / Who / Promise
- `references/on-writing-well.md` — Zinsser distilled for the review pass; all advisory, voice files take precedence
- `references/review-pass.md` — craft-review protocol: scanner pass, max five findings, fixed disease vocabulary, minimal voice-preserving fixes

## Common mistakes

- Treating the measured numbers as quotas — produces metrically perfect, dead prose.
- Opening on series context ("In my last post…") — the five-part RAG series median 5 reactions, all opened this way. `G-06`
- Writing "we" for solo work — the four posts where we ≥ I averaged 4.5 reactions. `G-04`
- Merging one-sentence paragraphs into "proper" ones — the one-sentence paragraph IS the voice (≈32 per post). See `voice-structure.md`.
- Re-explaining a framework a previous post covered — one linked line, move on.
