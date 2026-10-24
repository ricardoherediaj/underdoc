# AI Slop Blacklist (adapted for The Underdoc)

> **Canonical, machine-checked copies live in `checks/blacklist-words.txt` and `checks/blacklist-patterns.txt`** (gate `G-05`, run via `checks/check.py`). Edit those files to change enforcement; this document is the judgment-side reference with the reasoning and the [R] voice exceptions.

Source: Louis-François Bouchard's Anti-Slop Prompt Template (Towards AI), adapted to Ricardo's voice.
Rules marked **[R]** override the original template because they conflict with Ricardo's signature patterns.

## Banned opening moves
- "In this era of...", "In today's fast-paced world...", "As we navigate the complexities..."
- "In this post, I'll cover..." (throat-clearing — Cole's rule)
- Rhetorical question immediately answered as a hook. **[R]** Exception: the Eyebrow Raise pattern — external skepticism quoted in italics ("*Why tech? You are a doctor.*") is allowed; it's someone else's question, not a self-answered hook.
- "Imagine...", "Think of it like this..." analogy openers.

## Banned sentence structures
- "It isn't just X, it's Y." / "X is more than just Y; it's Z."
- "It wasn't X, it was Y."
- "This is where X comes in."
- Meta transitions: "Now that we've explored X, let's move on to Y."
- Compulsive rule-of-three (three parallel clauses in every other sentence).

## Banned vocabulary (unless quoting or technically required)
amazing, fascinating, mind-blowing, must-read, game-changer, groundbreaking, paradigm-shifting, transformative, pivotal, paramount, outstanding, a significant leap, delve, dive into, embark, endeavour, realm, tapestry, vibrant, leverage, harness, seamlessly, seamlessly integrates, effortlessly, robust, supercharge, elevate, unlock, "unlock the real power", "the best part is", "real magic happens", "recipe for disaster", thrive, cut through the noise/hype, crucial, critical, invaluable, significant/significantly, surprisingly, simply, neatly, "Whether you're X or Y".

## Style rules
- Plain concrete verbs and named tools over vague or dramatic wording ("Claude Haiku 3.5", not "a powerful LLM").
- Adjectives only when they add concrete information (scale, constraint, performance).
- **[R]** POV is "I" — Ricardo's voice, not the template's "we/you consistency" rule.
- **[R]** One-sentence fragments ARE allowed for emphasis ("Something clicked.") — max ~3 per post so they keep their punch.
- Em dashes: max 1–2 per post. Prefer commas or periods.
- Bold only for first mention of key terms and main-point statements (Cole). Never for general emphasis.
- Bullet lists only for genuinely enumerable items (steps, trade-offs). No bullet-point prose.
- Subheadings sparingly; short and factual; no dramatic two-part headings.
- No overstated certainty: if a fact is uncertain, omit it or mark it as uncertain.

## Editor-pass checklist (run as a separate review, not while writing)
1. Opening: does the first sentence earn attention without throat-clearing?
2. Scan for every banned phrase/structure/word above.
3. Repeated sentence openings? Vary them.
4. Any paragraph with zero new information? Delete it.
5. Any claim without a number, name, or concrete detail that could carry one? Add it.
6. Read-aloud test: does any sentence sound like a press release?
7. Does it end forward (next step, reader, open question) — not with a summary?
