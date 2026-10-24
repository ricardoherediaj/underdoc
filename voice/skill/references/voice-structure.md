# Voice — Structure

Rhythm, headings, length, sign-off. Gates: `G-01`, `G-02`, `G-03`, `G-06`, `G-07`. All numbers are medians measured from the 26-post corpus (`checks/calibration.md`) — descriptive, never quotas.

## The one-to-two-sentence paragraph is the default unit `[advisory, measured]`

The signature rhythm of this voice, and the finding no earlier document recorded: ≈32 one-sentence paragraphs per post, mean 1.4 sentences per paragraph, observed hard cap of 4 sentences (~45 words). Skill v1 said fragments were "for emphasis, max ~3 per post" — wrong by an order of magnitude. Do not merge short paragraphs into "proper" ones; the white space is doing work.

- Good (four consecutive paragraphs, `embrace-your-weirdness`):
  > So I started exploring other things on the side: bartending, mobile app development, whatever I could get my hands on.
  >
  > Then the pandemic hit, and I stumbled upon Python.
  >
  > Something clicked.
  >
  > I started applying it to football analytics and got immediately hooked.
- Bad: the same four beats fused into one six-sentence block paragraph.

The reverse failure is the ladder: every sentence isolated on its own line, the whole page a staircase of stop dots. That shape is the current visual signature of AI-generated posts, and it reads as slop no matter what the sentences say. The singles in the Good example land because they sit between two-sentence paragraphs. **Workhorse paragraphs run two to three sentences; one-sentence paragraphs are rationed to structural moments — the hook, a turn, the payoff — rarely more than two singles in a row, never a full ladder. A standalone line that functions as a section label is a heading — set it as H4, don't leave it floating.** [advisory, corrected 2026-09-05 after the long-form draft read as slop; refined same day from Ricardo's own section-label lines]

One idea per paragraph. A paragraph reaching its fourth sentence is almost always two paragraphs.

## Sentence length `[advisory, measured]`

Mean 15–22 words; the occasional 30-word story sentence is normal, but keep the long tail rare (corpus p90 ≈ 32). Alternate short and long — the one-liner lands because the sentence before it ran long.

## Headings: flat and functional. `G-02` (warn-only)

Style is the signal, not count. Calibration killed the 3–8 rule: the best post (204 reactions) has 12 headings, the second and third best have one each.

- Plain functional labels, often questions: "What's a match dashboard?", "Where to get the data from?", "What's Next?", "Key Takeaways".
- Never dramatic two-part titles with `:` or `—` ("The Hidden Cost: Why Your Pipeline Is Lying to You").
- Write at H3/H4 (corpus practice), never deeper than H4.
- The gate warns outside 3–8 and past 14; it never fails. The two 19–20-heading posts earned 5 and 4 reactions — past ~14, sections have stopped being sections.

## Word count. `G-01` (warn-only)

Guidance band 900–1,400 (top-performer median 1,029). Field notes run 400–900. Past 1,600 the gate warns again. Nothing about length blocks a draft — the second-best post ever is 641 words.

## Standalone rule: no series openers. `G-06`

Every post lands with zero prior posts read. Series context, if any, is one linked line placed after the hook — never the opening.

- Bad: "In my last post, I shared the big picture of the Football RAG system I've launched... and today, I want to talk about..." (`rag-is-a-data-engineering-heavy-problem`, 5 reactions — the whole five-part series opened this way, median 5)
- Good: open on the problem, then later: "I also integrated the FBRef data with the Transfermarkt data, a process I described in my last post: [link]" (`how-to-use-fbref`, 36 reactions — reference sits mid-post, after the hook did its job)

Gate fails on series-opener phrases in the first three paragraphs. Auto-revise up to twice, then hand over.

## Sign-off. `G-03`

Exactly: `Till next time, Ricardo.` The corpus has four spellings (Till/Til/Til'/See you); the gate passes the canonical form, warns on variants, fails on absence and auto-fixes.

## Images. `G-07` (warn-only)

Evidence-driven screenshots, marked `[SCREENSHOT: what to capture]` in layout and draft — median 7 per Builds post; the gate warns under 3 for Builds only. Bridge and Field notes carry slots only where evidence demands one (gate reports INFO). Ricardo captures them manually; never generate body images. Cover slot marked `[COVER]`.

## Lists `[advisory]`

Bullets for genuine enumerations (tools used, metrics available) — corpus uses them freely. Never bullet-point prose that should be sentences, and never a bulleted argument: reasoning happens in paragraphs.
