# Calibration report — checks/check.py against the published corpus

Run date: 2026-08-22 · 26 published posts · regenerate with `python3 checks/check.py --corpus`

Purpose, per SPEC §4: validate the gates against reality before trusting them on drafts, and gather the descriptive statistics skill v2 depends on (§5.3). Raw output is in `checks/calibration.txt`.

**Headline result: two gate thresholds written into the spec were not supported by the corpus, and both have been corrected.** Details in "Findings that changed the gates" below.

---

## Gate pass rates

| Gate | Pass | Rate | Reading |
|---|---|---|---|
| G-01 `word_count` | 14/26 | 54% | 12 warn, 0 fail. Warn-only gate. |
| G-02 `sections` | 8/26 | 31% | 18 warn, 0 fail. Warn-only gate. Most warnings are heading counts outside 3–8, which turned out not to matter. |
| G-03 `signoff` | 11/26 | 42% | Plus 5 warnings for non-canonical variants. 16 of 26 posts sign off somehow. |
| G-04 `i_we_ratio` | 22/26 | 85% | Matches the audit exactly: 4 posts where `we ≥ I`. |
| G-05 `slop_blacklist` | 13/26 | 50% | 32 word hits, 0 pattern hits. |
| G-06 `standalone` | 24/26 | 92% | 2 posts open on series context. |

---

## Findings that changed the gates

### 1. The 3–8 heading rule has no support in the data

The rule was carried into the spec from the audit. The corpus disagrees:

| Post | Reactions | Headings |
|---|---|---|
| `building-your-own-football-analytics` | 204 | 12 |
| `how-to-use-fbref-for-football-scouting` | 36 | 1 |
| `how-to-scrape-transfermarkt-with` | 28 | 1 |
| `farewell-fbref-advanced-stats-when` | 8 | 0 |

Top performers run a median of 6 headings; everyone else runs 5. That difference is noise. The best post in the corpus has 12, and the second and third best have one each.

**Change:** G-02 never fails. It warns outside 3–8, warns again past 14 where the two runaway posts sit (19 and 20 headings, 5 and 4 reactions), and warns on dramatic two-part titles or nesting deeper than H4. The signal the gate carries is heading *style*, not count.

### 2. The 900-word floor would have blocked the second-best post in the corpus

`how-to-use-fbref-for-football-scouting` is 641 words and earned 36 reactions, the second-highest ever. `farewell-fbref-advanced-stats-when` is 441 words and earned 8, above the corpus median.

Top performers median 1,029 words against 895 for the rest, so the band is directionally right, but nothing justifies failing a draft for being short.

**Change:** G-01 never fails. It warns outside the band and warns again past 1,600 words. That ceiling rested on thin evidence anyway (n=2).

### 3. `analysis.json` recorded a false positive

The audit's count of 15 slop hits included one for `"the world of"`. The actual sentence is *"what can the world offer me?"* — matched because the original scan used substring matching without word boundaries. The real count for those eight terms is **14**.

`check.py` matches on word boundaries and correctly does not flag it. The gate is stricter than the analysis that motivated it.

### 4. The sign-off has four spellings, not one

| Variant | Posts |
|---|---|
| `Till next time, Ricardo.` | 11 |
| `Til next time,` / `Til' next time,` | 2 |
| `See you next time,` | 3 |
| No sign-off | 10 |

The audit reported 15 of 26; the true figure is 16 of 26 across all variants.

**Change:** G-03 passes on the canonical form, warns on a known variant, fails on absence. Calibration measures what exists; the gate pushes drafts toward one form.

### 5. The pattern tier finds nothing in the corpus, and that is a real result

Zero hits from 22 structural patterns across 26 posts. Verified against a probe containing ten planted slop structures, all ten caught. Ricardo does not write binary contrasts, faux-insight setups, or fake-profound endings. The tier exists to keep it that way once drafting is assisted — the risk it guards against is new.

### 6. Slop is concentrated in three word families

Of 32 hits, 19 are `leverage`/`leveraging`/`harness`. Fixing that habit alone removes 59% of the problem.

---

## Descriptive statistics for skill v2

Medians, split at 8 reactions (top n=11, rest n=15).

| Measure | Top | Rest | Use in skill v2 |
|---|---|---|---|
| Words | 1,029 | 895 | Band of 900–1,400 stands as guidance. |
| Sentence words, mean | 19.6 | 17.5 | Target 15–22 average. |
| Sentence words, p90 | 32 | 35 | Occasional long sentence is normal; keep p90 under ~32. |
| Paragraph words, mean | 20.8 | 19.2 | Short paragraphs. Cap around 45 words. |
| Paragraph sentences, mean | 1.4 | 1.5 | **One to two sentences per paragraph.** |
| Paragraph sentences, max | 4 | 4 | Hard cap of 4. |
| One-sentence paragraphs | 32 | 35 | The dominant unit. This is the voice's signature rhythm. |
| Headings | 6 | 5 | Guidance only, see finding 1. |
| Em dashes | 0 | 0 | Already absent. |
| Semicolons | 0 | 0 | Already absent. |

Heading levels in use across the corpus: H2 in 7 posts, H3 in 16, H4 in 15, H5 in 4. Ricardo writes at H3/H4, not H2.

**Resolved, per SPEC §5.3:** the em-dash and semicolon ban was to be adopted only if the corpus already avoided them. Median zero in both bands, so the rule is adopted — it describes existing practice rather than imposing a new constraint.

**Strongest undocumented finding:** the one-sentence paragraph is the core rhythm of this voice, roughly 32 per post against a mean of 1.4 sentences per paragraph. Skill v1 permitted fragments "for emphasis, max ~3 per post." That understates it by an order of magnitude. Skill v2 should treat the one-to-two-sentence paragraph as the default unit, not the exception.

---

## Caveats

n=26, and reactions are heavily skewed (one post at 204, next at 36, median 5). Differences between the top and rest bands are mostly within noise. These numbers describe what Ricardo has written; only the largest gaps should be read as anything about what works.
