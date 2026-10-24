# Explainer Post Structure

For posts that teach a concept, tool, or method ("what X is and how to use it"). No repo is the subject: the sources are URLs, docs, a course, or a spec, and Ricardo is the guide, not the builder. Distinct from Build Story (a thing Ricardo made) and Conceptual (an idea argued from his own story).

Every rule below is observed in the corpus, cited by filename. Numbers are descriptive, not quotas.

## Shape

1. **Open on the reader's friction or the old assumption.** First lines name a frustration the reader has had, or a mistaken habit Ricardo used to have. Not a definition. (`2025-08-31-uv-the-tool-that-helps-you-manage`: "conflicting package versions, virtual environment headaches"; `2025-09-29-understanding-model-context-protocol`: copy-pasting data into a model; `2026-03-09-how-a-football-framework-for-measuring`: "I used to think starting a data project was about jumping straight to the data.")
2. **Define the thing in one bolded sentence, then an analogy.** One plain definition, then a single everyday comparison. (`2025-09-29-understanding-model-context-protocol`: MCP as a USB-C port; `2025-08-31-uv-the-tool-that-helps-you-manage`: Swiss Army knife; `2025-06-27-the-art-of-football-data-scouting`: Moneyball as the entry point.)
3. **Name the source of the knowledge.** A docs site, a course, a spec, a quote from the person who built it. Link it. (`2026-03-09-how-a-football-framework-for-measuring`: the Twelve course and its quoted line; `2025-09-29-understanding-model-context-protocol`: spec, Anthropic docs, GitHub org listed under resources; `2025-06-27-the-art-of-football-data-scouting`: Rasmus Ankersen quote.)
4. **Flat headings that read like the questions the reader would ask.** "What is X?", "Why X beats Y", "How to use it", "Key takeaways". No clever section names. (`2025-08-31-uv-the-tool-that-helps-you-manage`, `2025-09-29-understanding-model-context-protocol`: 7 to 10 `##`/`###` headings each.)
5. **Break the concept into named parts, one short block each.** Three files, three primitives, five metrics: enumerate, give each one or two sentences. (`2025-08-31-uv-the-tool-that-helps-you-manage`: `pyproject.toml` / `uv.lock` / `.venv`; `2025-09-29-understanding-model-context-protocol`: host / client / server, then resources / tools / prompts.)
6. **Compare against what the reader already uses.** Place the thing next to the incumbents, with one honest line per rival. (`2025-08-31-uv-the-tool-that-helps-you-manage`: pip, Poetry, Conda, including Ricardo's own Conda history.)
7. **Show the concept working on one concrete example, then transfer it.** One worked example carries the abstraction; a second domain proves it travels. (`2025-06-27-the-art-of-football-data-scouting`: Como 1907 case study; `2026-03-09-how-a-football-framework-for-measuring`: Passing Quality score with its weights, then diabetic patient monitoring; `2025-08-31-uv-the-tool-that-helps-you-manage`: step-by-step setup of his tutorials repo.)
8. **Put commands, weights, or numbers in the example, not adjectives.** "30%, 20%, 20%, 20%, 10%"; `uv sync`; "66.5% of possessions". (`2026-03-09-how-a-football-framework-for-measuring`, `2025-08-31-uv-the-tool-that-helps-you-manage`, `2025-06-27-the-art-of-football-data-scouting`.)
9. **Close on what the reader takes away, as a short list or one rule.** Key Takeaways or a stated principle, or a "do this next" list with the docs link. Not a recap of every section. (`2026-03-09-how-a-football-framework-for-measuring`: "Start with the human question"; `2025-08-31-uv-the-tool-that-helps-you-manage`: "Getting Started Today" steps; `2025-09-29-understanding-model-context-protocol`: resources and takeaways.)
10. **Part two assumes part one and does not re-explain.** A follow-up opens with one recap list, then goes straight to the new step. (`2025-07-06-the-art-of-football-data-scouting-d2a`: three-step recap, then steps 2 and 3.)

## Length observed

About 700 to 1,450 words across the five posts: `2026-03-09-how-a-football-framework-for-measuring` (702), `2025-07-06-the-art-of-football-data-scouting-d2a` (936), `2025-08-31-uv-the-tool-that-helps-you-manage` (1,137), `2025-06-27-the-art-of-football-data-scouting` (1,172), `2025-09-29-understanding-model-context-protocol` (1,452). The shortest carried the single-idea framework; the longest carried a tool plus a code walkthrough.

## Anti-patterns specific to this structure

- Opening on a definition or "In this post I will explain". Open on the friction (rule 1).
- A feature list with no worked example. `2025-09-29-understanding-model-context-protocol` leans toward this in its tool inventory; the example must carry the weight.
- Treating one tool's repo as the subject. If the repo is what you built, it is a Build, not an Explainer.
- Re-explaining a concept covered in an earlier post (rule 10).
- Unattributed claims. Explainers borrow authority from sources, so link them (rule 3).

## Checklist before publishing

- [ ] Opens on a reader's friction or an old assumption
- [ ] One bolded definition and one analogy
- [ ] Sources named and linked (docs, course, spec)
- [ ] One worked example with real commands or numbers
- [ ] Compared against what the reader already uses
- [ ] Ends on a takeaway or next step, not a recap
- [ ] Gate zero: the reader can do something specific tomorrow
