# Build Story Structure

For posts about automating a personal or business workflow ("I built X so I don't have to do Y manually"). Distinct from both Technical Deep-Dive (leads with a system/metric) and Conceptual/Career (leads with an idea). This one leads with a tedious, relatable process.

## Shape

1. **The manual process** — Concrete, specific, mildly tedious. Named tools, real cadence ("every month," "twenty to thirty entries"). End on the honest admission that it worked but was annoying.
2. **The discovery** — Where the better tool/approach came from (a community, a coworker, a doc someone shared). One or two sentences. Don't dramatize it.
3. **The build** — What you actually built, named tools included (MCP, Claude Code skill, specific APIs). Explain the mechanism in plain terms, not a feature list.
4. **The real problems, named** — Every build like this has at least one non-obvious design problem (idempotency, a mapping/classification step, a race condition, a trust boundary). Name it, explain the trade-off you made, and admit the honest limitation. This section is where technical credibility lives — skip it and the post reads as a product pitch.
5. **The first real run** — Concrete numbers from an actual run: how much had piled up, what got processed, how long it took versus before.
6. **What to steal** — Generalize the pattern one level up so it's not just "use my exact tools." End forward: an open question, a known rough edge, or what happens next. Not a summary of what was covered.

## Anti-patterns specific to this structure

- Turning step 3 into a feature list ("it does X, Y, and Z"). Explain the mechanism, not the spec sheet.
- Skipping step 4. A build post with no acknowledged trade-off reads as marketing.
- Ending on enthusiasm ("this changed how I think about automation!") instead of the concrete next question.
- Screenshots or data that reveal real personal information — use fictional-but-realistic placeholder data instead (see workflow note below).

## Workflow note

When the post needs screenshots of tools with real personal data (finance trackers, private dashboards), populate a throwaway or duplicate view with fictional-but-realistic data before capturing — not obviously-fake placeholders ("Expense 1 - $100"), but data that reads like a real row without being one.
