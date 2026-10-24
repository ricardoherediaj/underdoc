# The Review Pass — craft review protocol

The judgment layer between the deterministic gates and human review. It runs on
`03_draft.md` after the no-ai-slop pass and the gate report (`04_review.md` steps 1–2).
The `no-ai-slop` skill edits mechanical AI patterns in place; this pass proposes
judgment-level improvements. Both are advisory: the pass proposes, Ricardo decides.
The voice files (`voice-tonality.md`, `voice-mechanics.md`, `voice-structure.md`) win on
any conflict. The pass never sands off ESL quirks or spoken rhythm to sound like a
professional editor.

Sources: Zinsser, *On Writing Well* (Z); Nicolas Cole, *The Art and Business of Online
Writing* (C). This file is the operating procedure; `on-writing-well.md` and
`nicolas-cole-structures.md` hold the reasoning behind each rule.

Two passes, run in this order:

- **Layout pass** — macro structure, when the piece's shape is the problem: buried
  lead, stalling sections, missing ending. Output is a proposed skeleton into
  `02_layout.md`, approved by Ricardo before anything is reordered.
- **Craft pass** — sentence and paragraph level, everything below the layout pass.

## The layout pass

1. **Thesis harvest.** Underline every sentence that carries the argument. If no
   sentence states the thesis, that is the finding: the piece is a draft of a draft.
2. **Cut-the-opening test (Z).** Mentally delete the first two or three paragraphs and
   reread. If the piece starts stronger, the lead was buried; the hook is usually the
   pivot sentence hiding at the top of the middle. Exception: if the candidate hook is
   a turn — it answers or reverses the setup above it ("the equation changes", "but",
   "yet") — it needs its runway. A turn without its antecedent reads standalone and
   incoherent. Restore the setup instead of promoting the turn.
3. **Block map.** One line per existing block: what it does for the reader (setup,
   evidence, turn, payoff). A block that does no work is a cut candidate.
4. **Reorder by momentum (C).** Strongest specific first; each block must earn the
   next. Setup keeps its place only if the payoff depends on it.
5. **Heading decision.** 3–8 flat functional headings for long builds (G-02). For
   400–900-word field notes: zero or one, with bold signpost sentences instead (C).
6. **Rhythm map.** Against the measured voice: paragraphs of one to two sentences, hard
   cap of four; short after long. A lecture-sized paragraph is a layout finding, not a
   wording one.

Output: thesis (one sentence), block map, proposed order, heading/signpost decision,
cut list — pasted into `02_layout.md` for approval. The skeleton is a proposal.

## The craft pass

## Reading protocol (craft pass)

1. **Scanner pass (C).** Headline, hook, headings, bold text, last paragraph. Would a
   stranger keep going at each checkpoint?
2. **Reader pass.** Full read at speaking pace. Mark every spot where attention dips.
   That list is the candidate pool.
3. **Findings.** At most **five**, ranked by reader-cost. Fewer is fine. **Zero is a
   valid result.** Never invent a problem to fill the quota; noise is the failure mode
   of review systems.

Calibration: test-run the pass on two corpus posts, one top performer and one
underperformer. A top performer should yield two findings at most; the five-part
RAG-series openers should light up `dead-lead`.

## Reader-cost ranking (highest first)

1. **Substance**: thesis muddled, or two theses fighting. One piece leaves one
   provocative thought (Z). The takeaway test is the substance check.
2. **Momentum**: hook, first sentence, the pull from paragraph to paragraph, the ending
   (C: rate of revelation; Z: the momentum chain).
3. **Clarity**: clutter, abstraction, missing steps, hedging.
4. **Polish**: rhythm, word choice, emphasis.

## The diseases (fixed vocabulary; every finding names exactly one)

| Disease | Symptom | Minimal fix | Src |
|---|---|---|---|
| `two-theses` | The piece argues two things; the second is usually the better post | Split it, or cut one thread to a single line | Z, C |
| `dead-lead` | The first sentence does not force the second | Cut the warm-up; start at the story; lead with the strongest specific | Z, C |
| `throat-clearing` | "In this post I'll cover..." | Delete; editors cut the first three paragraphs for a reason | Z |
| `summary-close` | The ending recaps what was already said | Nearest exit; echo the opening note or end forward | Z, C |
| `clutter` | Words doing no work; the sentence survives the bracket test | Cut it; long word to short word | Z |
| `hedging` | "a bit", "sort of", "quite", "I think maybe" | Commit or cut | Z, C |
| `weak-verb` | Vague verb propped by an adverb ("stepped down" vs was fired) | Pick the verb that reports the truth | Z |
| `abstraction` | Concept nouns, nobody doing anything | Put a person, tool, or number in the sentence | Z |
| `proof-gap` | A claim that could carry a number or a name carries nothing | Add the real one, or soften the claim | C |
| `merged-paragraphs` | One paragraph doing two ideas | Split it, or cut it | voice |
| `flat-rhythm` | Three same-length sentences, or same-size paragraphs in a row | Alternate; punch with a short one | C, voice |
| `ladder` | Every body sentence isolated on its own line, the page a staircase of stop dots — the visual signature of AI slop | Merge body sentences into two-to-three-sentence paragraphs; singles stay only as hook, turn, heading, or payoff. A floating section label is a heading — set it, don't ladder it | voice |
| `predictable-line` | The reader can see the next paragraph coming | Reorder so each paragraph reveals something new, or cut to the point | C |
| `unexplained-jump` | A step the reader needs is missing | Add the missing fact in its own sentence, in linear order | Z |
| `spec-sheet` | Feature list instead of mechanism | Explain how it works step by step; if you can't, you don't know it yet | Z |
| `unity-drift` | Point of view, tense, or tone switches mid-piece | Hold the declared unity; rewrite the drift | Z |
| `unearned-emphasis` | Bold or italics standing in for a strong sentence | Cut the formatting; make the sentence carry it | C |

## Edit discipline

- **Minimal diff.** Change the fewest words that cure the disease. Delete before
  rewriting; rewrite a sentence before adding one.
- **One disease per edit.** Every edit names what it treats, so patterns feed skill v3.
- **Voice test.** Would Ricardo have written it? ESL quirks and spoken rhythm stay.
  Never polish toward "correct American prose."
- **Typo vs voice.** Fix spelling and agreement errors freely (`trascendental`,
  `peoples`, `shot form`); never "correct" fragments, rhythm, repetition-for-emphasis,
  or word choice (`cause`, `you name it`, comma splices for pace) — that is voice,
  not error.
- **Gate safety.** No proposed edit may trip a gate: no "we", no blacklist words, no
  series opener, no new dramatic heading.
- **Read rewritten paragraphs aloud (Z).** Rhythm problems are heard before they are seen.
- **Last-word check (Z).** On any rewritten closing sentence, put the punch word last.
- **Re-run gates.** `python3 checks/check.py <draft>` after accepted edits.

## Output

Findings land in `04_review.md` step 3 as a table (Where, Disease, Quote, Proposed
fix, Accepted?). Nothing touches `03_draft.md` until Ricardo accepts, or tells the
harness to apply.

## What the pass is not

- It does not rewrite wholesale, reorder sections, or touch substance. Substance lives
  in `01_topic.md` and with Ricardo.
- It does not score, grade, or gate. Findings are proposals with a named disease; the
  human decides.
