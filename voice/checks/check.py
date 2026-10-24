#!/usr/bin/env python3
"""Deterministic voice gates for The Underdoc drafts.

Stdlib only, no network, no LLM calls. Gates are defined in SPEC.md section 4
and carry stable IDs (G-01..G-08) that skill rules and review records cite.

Usage:
    python3 checks/check.py drafts/2026-08-25-mentor/03_draft.md
    python3 checks/check.py --json drafts/.../03_draft.md
    python3 checks/check.py --corpus
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKS = ROOT / "checks"

PASS, WARN, FAIL, INFO = "PASS", "WARN", "FAIL", "INFO"

VALID_BUCKETS = {"builds", "explainers", "bridge", "field-notes"}
VALID_STATUS = {
    "drafting", "slop-pass", "checked", "human-review",
    "ready", "published", "killed",
}

SERIES_OPENERS = [
    r"\bin\s+my\s+last\s+(post|article|newsletter)\b",
    r"\bin\s+the\s+previous\s+(post|article)\b",
    r"\bas\s+I\s+mentioned\s+(last|in\s+the\s+last)\b",
    r"\bpart\s+\d+\s+of\b",
    r"\bcontinuing\s+(from|where)\b",
    r"\bin\s+part\s+\d+\b",
    r"\bif\s+you\s+(read|followed)\s+(my\s+)?last\b",
]


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

def parse(path):
    """Split a markdown file into frontmatter dict and body text."""
    raw = Path(path).read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            block = raw[3:end]
            body = raw[end + 4:]
            for line in block.splitlines():
                if ":" not in line:
                    continue
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body.strip()


def strip_code(text):
    """Remove fenced code blocks and inline code, which no prose gate should see."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    return text


def strip_trailer(text):
    """Drop Substack chrome that scraping leaves after the article body.

    Published corpus files end with avatar-image link blocks, share widgets and
    a "N Likes" counter. These sit after the sign-off and would otherwise push
    it out of the window G-03 inspects. Drafts have none of this, so the
    function is a no-op there.
    """
    lines = text.rstrip().splitlines()
    junk = re.compile(
        r"^\s*(?:"
        r"(?:\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)\s*)+"      # avatar image links
        r"|\[(?:Share|Subscribe|Leave a comment)[^\]]*\]\([^)]*\)"
        r"|\d+\s+Likes.*"
        r"|!\[[^\]]*\]\([^)]*\)"                           # trailing bare images
        r"|[-*_\s]*"
        r")\s*$", re.I)
    while lines and junk.match(lines[-1]):
        lines.pop()
    return "\n".join(lines)


def prose(text):
    """Body reduced to readable prose: no code, no image syntax, no heading marks."""
    text = strip_code(text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)      # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)   # links keep their text
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_>]+", "", text)
    return text


def words(text):
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text)


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [s.strip() for s in parts if s.strip()]


def headings(body):
    """All markdown headings with their level. Ricardo uses H3/H4, not H2."""
    return [
        (len(m.group(1)), m.group(2).strip())
        for m in re.finditer(r"^\s{0,3}(#{2,6})\s+(.*)$", strip_code(body), flags=re.M)
    ]


# --------------------------------------------------------------------------
# Blacklists
# --------------------------------------------------------------------------

def load_words(path=None):
    path = Path(path or CHECKS / "blacklist-words.txt")
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def load_patterns(path=None):
    """Load `regex<TAB>label` lines with their level: `fail` (default) or `warn`.

    A line `# level: fail|warn` sets the level for the lines that follow.
    Returns a list of `(compiled regex, label, level)`.
    """
    path = Path(path or CHECKS / "blacklist-patterns.txt")
    out = []
    level = "fail"
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        marker = re.fullmatch(r"#\s*level:\s*(fail|warn)\s*", line.strip(), re.I)
        if marker:
            level = marker.group(1).lower()
            continue
        if line.lstrip().startswith("#"):
            continue
        pattern, _, label = line.partition("\t")
        out.append((re.compile(pattern.strip(), re.I), (label or pattern).strip(), level))
    return out


def line_of(text, index):
    return text.count("\n", 0, index) + 1


# --------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------

def gate(gid, name, status, value, detail=""):
    return {"id": gid, "name": name, "status": status, "value": value, "detail": detail}


def g01_word_count(body, bucket):
    """Reports length. Never fails.

    Calibration: the 900-word floor would have blocked the second-best post in
    the corpus (641 words, 36 reactions) and an 8-reaction field note at 441.
    Length is an editorial choice, so this gate warns and steps aside.
    """
    n = len(words(prose(body)))
    low = 400 if bucket == "field-notes" else 900
    if n > 1600:
        return gate("G-01", "word_count", WARN, n, f"{n} words, well past the usual 1400")
    if n < low or n > 1400:
        return gate("G-01", "word_count", WARN, n, f"{n} words, band is {low}-1400")
    return gate("G-01", "word_count", PASS, n, f"{n} words")


def g02_sections(body):
    """Style is the signal; count is not. Never fails.

    Calibration: heading count does not track performance. Top performers run a
    median of 6 headings against 5 for the rest, spanning 0 to 14 at the top —
    the best post in the corpus has 12, the next two have one each. Structure is
    an editorial choice, so this gate warns and steps aside.
    """
    hs = headings(body)
    n = len(hs)
    dramatic = [t for _, t in hs if ":" in t or "—" in t]
    deep = [t for lv, t in hs if lv > 4]
    notes = []
    if n > 14:
        notes.append(f"{n} headings, the post may be fragmenting")
    if not 3 <= n <= 8 and n <= 14:
        notes.append(f"{n} headings, usual band is 3-8")
    if dramatic:
        notes.append("two-part headings: " + "; ".join(dramatic))
    if deep:
        notes.append("deeper than H4: " + "; ".join(deep))
    if notes:
        return gate("G-02", "sections", WARN, n, " | ".join(notes))
    return gate("G-02", "sections", PASS, n, f"{n} headings")


CANONICAL_SIGNOFF = re.compile(r"till\s+next\s+time\s*,\s*\n*\s*ricardo", re.I)
SIGNOFF_VARIANTS = re.compile(
    r"(?:till|til'?|until|see\s+you)\s+next\s+time\s*,\s*\n*\s*ricardo", re.I)


def g03_signoff(body):
    """Canonical form passes, a known variant warns, absence fails.

    The corpus uses four spellings ("Till", "Til", "Til'", "See you"). Skill v2
    standardizes on one, so the gate accepts the family but flags drift.
    """
    tail = prose(strip_trailer(body))[-400:]
    if CANONICAL_SIGNOFF.search(tail):
        return gate("G-03", "signoff", PASS, "canonical", "'Till next time, Ricardo.'")
    m = SIGNOFF_VARIANTS.search(tail)
    if m:
        variant = " ".join(m.group(0).split())
        return gate("G-03", "signoff", WARN, variant,
                    f"non-standard variant '{variant}' — standardize on 'Till next time, Ricardo.'")
    return gate("G-03", "signoff", FAIL, None, "missing 'Till next time, Ricardo.'")


def g04_i_we_ratio(body):
    w = [x.lower() for x in words(prose(body))]
    n = max(len(w), 1)
    i = sum(1 for x in w if x in {"i", "i'm", "i've", "i'll", "i'd", "my", "me", "mine"})
    we = sum(1 for x in w if x in {"we", "we're", "we've", "we'll", "our", "us", "ours"})
    ip, wp = round(i * 1000 / n, 1), round(we * 1000 / n, 1)
    ok = ip > wp
    return gate("G-04", "i_we_ratio", PASS if ok else FAIL, {"i_per_1k": ip, "we_per_1k": wp},
                f"I {ip}/1k vs we {wp}/1k")


def g05_slop(body, word_terms, patterns):
    """Banned vocabulary and sentence shapes. Word hits and fail-level patterns fail; warn-level reports."""
    text = prose(body)
    hits = []
    for term in word_terms:
        pat = r"\b" + r"\s+".join(re.escape(p) for p in term.split()) + r"\b"
        for m in re.finditer(pat, text, re.I):
            hits.append({"tier": "word", "level": "fail", "match": m.group(0), "label": term,
                         "line": line_of(text, m.start())})
    for rx, label, level in patterns:
        for m in re.finditer(rx, text):
            hits.append({"tier": "pattern", "level": level, "match": m.group(0)[:70], "label": label,
                         "line": line_of(text, m.start())})
    if not hits:
        return gate("G-05", "slop_blacklist", PASS, 0, "clean")
    summary = "; ".join(f"L{h['line']} {h['label']}" for h in hits[:8])
    if len(hits) > 8:
        summary += f" (+{len(hits) - 8} more)"
    failing = [h for h in hits if h["level"] != "warn"]
    g = gate("G-05", "slop_blacklist", FAIL if failing else WARN, len(hits), summary)
    g["hits"] = hits
    return g


def g06_standalone(body):
    opening = "\n\n".join(paragraphs(prose(body))[:3])
    for pat in SERIES_OPENERS:
        m = re.search(pat, opening, re.I)
        if m:
            return gate("G-06", "standalone", FAIL, m.group(0),
                        f"series opener in first 3 paragraphs: '{m.group(0)}'")
    return gate("G-06", "standalone", PASS, 0, "stands alone")


def g07_image_slots(body, bucket):
    slots = len(re.findall(r"\[SCREENSHOT:", body, re.I))
    imgs = len(re.findall(r"!\[[^\]]*\]\(", body))
    total = slots + imgs
    if bucket == "builds" and total < 3:
        return gate("G-07", "image_slots", WARN, total,
                    f"{total} image slots, Builds posts usually carry 3+ (corpus median 7)")
    return gate("G-07", "image_slots", INFO, total, f"{total} image slots")


def g08_frontmatter(meta):
    missing = [k for k in ("title", "bucket", "status") if not meta.get(k)]
    problems = list(missing and [f"missing: {', '.join(missing)}"] or [])
    b, s = meta.get("bucket", "").lower(), meta.get("status", "").lower()
    if b and b not in VALID_BUCKETS:
        problems.append(f"bad bucket '{b}'")
    if s and s not in VALID_STATUS:
        problems.append(f"bad status '{s}'")
    if problems:
        return gate("G-08", "frontmatter", FAIL, problems, "; ".join(problems))
    return gate("G-08", "frontmatter", PASS, {"bucket": b, "status": s}, f"{b} / {s}")


def run_gates(meta, body, word_terms, patterns, skip=()):
    bucket = (meta.get("bucket") or "").lower()
    gates = [
        g01_word_count(body, bucket),
        g02_sections(body),
        g03_signoff(body),
        g04_i_we_ratio(body),
        g05_slop(body, word_terms, patterns),
        g06_standalone(body),
        g07_image_slots(body, bucket),
        g08_frontmatter(meta),
    ]
    return [g for g in gates if g["id"] not in skip]


# --------------------------------------------------------------------------
# Calibration statistics (SPEC 4, feeds skill v2 section 5.3)
# --------------------------------------------------------------------------

def stats(body):
    p = prose(body)
    sw = [len(words(s)) for s in sentences(p) if words(s)]
    pw = [len(words(x)) for x in paragraphs(p) if words(x)]
    ps = [len(sentences(x)) for x in paragraphs(p) if words(x)]
    hs = headings(body)
    return {
        "words": len(words(p)),
        "sent_mean": round(sum(sw) / len(sw), 1) if sw else 0,
        "sent_p90": sorted(sw)[int(len(sw) * 0.9)] if sw else 0,
        "sent_max": max(sw) if sw else 0,
        "para_words_mean": round(sum(pw) / len(pw), 1) if pw else 0,
        "para_words_max": max(pw) if pw else 0,
        "para_sents_mean": round(sum(ps) / len(ps), 1) if ps else 0,
        "para_sents_max": max(ps) if ps else 0,
        "headings": len(hs),
        "heading_levels": sorted({lv for lv, _ in hs}),
        "em_dashes": p.count("—"),
        "semicolons": p.count(";"),
        "one_sentence_paras": sum(1 for x in ps if x == 1),
    }


def median(xs):
    xs = sorted(xs)
    if not xs:
        return 0
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else round((xs[m - 1] + xs[m]) / 2, 1)


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

MARK = {PASS: "PASS", WARN: "WARN", FAIL: "FAIL", INFO: "INFO"}


def report(path, gates):
    print(f"\n{path}")
    print("-" * 72)
    for g in gates:
        print(f"  {MARK[g['status']]:<4}  {g['id']}  {g['name']:<16}  {g['detail']}")
    bad = [g for g in gates if g["status"] == FAIL]
    warn = [g for g in gates if g["status"] == WARN]
    print("-" * 72)
    print(f"  {len(bad)} failed, {len(warn)} warned, "
          f"{sum(1 for g in gates if g['status'] == PASS)} passed")
    return 1 if bad else 0


def corpus_run(word_terms, patterns):
    posts = sorted((ROOT / "corpus").glob("*.md"))
    meta_by_slug = {}
    apath = ROOT / "analysis" / "analysis.json"
    if apath.exists():
        for row in json.loads(apath.read_text(encoding="utf-8")):
            meta_by_slug[row["slug"]] = row

    rows, slop_total = [], {}
    for p in posts:
        meta, body = parse(p)
        gates = run_gates(meta, body, word_terms, patterns, skip=("G-08", "G-07"))
        st = stats(body)
        slug = meta.get("slug", p.stem)
        reactions = int(meta.get("reactions") or meta_by_slug.get(slug, {}).get("reactions") or 0)
        g5 = next(g for g in gates if g["id"] == "G-05")
        for h in g5.get("hits", []):
            key = f"{h['tier']}:{h['label']}"
            slop_total[key] = slop_total.get(key, 0) + 1
        rows.append({"slug": slug, "reactions": reactions, "stats": st,
                     "gates": {g["id"]: g["status"] for g in gates},
                     "slop_hits": len(g5.get("hits", []))})

    rows.sort(key=lambda r: -r["reactions"])
    print(f"\nCALIBRATION — {len(rows)} published posts")
    print("=" * 78)
    print(f"{'slug':<44}{'rx':>4}  {'G-01':>4}{'G-02':>5}{'G-03':>5}{'G-04':>5}{'G-05':>5}{'G-06':>5}")
    print("-" * 78)
    for r in rows:
        g = r["gates"]
        cells = "".join(f"{g[k][0]:>5}" for k in
                        ("G-01", "G-02", "G-03", "G-04", "G-05", "G-06"))
        print(f"{r['slug'][:43]:<44}{r['reactions']:>4} {cells}")

    print("\nGate pass rates across the published corpus")
    print("-" * 78)
    for gid in ("G-01", "G-02", "G-03", "G-04", "G-05", "G-06"):
        passed = sum(1 for r in rows if r["gates"][gid] == PASS)
        print(f"  {gid}  {passed:>2}/{len(rows)} pass"
              f"   ({round(100 * passed / len(rows))}%)")

    print(f"\nG-05 slop hits by term  (total {sum(slop_total.values())})")
    print("-" * 78)
    for k, v in sorted(slop_total.items(), key=lambda kv: -kv[1]):
        print(f"  {v:>3}  {k}")

    top = [r for r in rows if r["reactions"] >= 8]
    rest = [r for r in rows if r["reactions"] < 8]

    def band(label, group):
        if not group:
            return
        s = [r["stats"] for r in group]
        print(f"\n  {label}  (n={len(group)})")
        for key, fmt in (("words", "words"), ("sent_mean", "sentence words, mean"),
                         ("sent_p90", "sentence words, p90"),
                         ("para_words_mean", "paragraph words, mean"),
                         ("para_sents_mean", "paragraph sentences, mean"),
                         ("para_sents_max", "paragraph sentences, max"),
                         ("headings", "headings"), ("em_dashes", "em dashes"),
                         ("semicolons", "semicolons"),
                         ("one_sentence_paras", "one-sentence paragraphs")):
            print(f"    {fmt:<32} median {median([x[key] for x in s])}")

    print("\nDescriptive statistics, split by performance")
    print("-" * 78)
    band("Top performers (8+ reactions)", top)
    band("Rest (<8 reactions)", rest)

    levels = {}
    for r in rows:
        for lv in r["stats"]["heading_levels"]:
            levels[lv] = levels.get(lv, 0) + 1
    print("\n  heading levels used, posts per level: "
          + ", ".join(f"H{k}: {v}" for k, v in sorted(levels.items())))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Deterministic voice gates for The Underdoc.")
    ap.add_argument("path", nargs="?", help="draft markdown file")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--corpus", action="store_true", help="calibrate against corpus/")
    args = ap.parse_args()

    word_terms, patterns = load_words(), load_patterns()

    if args.corpus:
        return corpus_run(word_terms, patterns)
    if not args.path:
        ap.error("give a draft path, or --corpus")

    meta, body = parse(args.path)
    gates = run_gates(meta, body, word_terms, patterns)
    if args.json:
        print(json.dumps({"path": str(args.path), "gates": gates,
                          "stats": stats(body)}, indent=2))
        return 1 if any(g["status"] == FAIL for g in gates) else 0
    return report(args.path, gates)


if __name__ == "__main__":
    sys.exit(main())
