#!/usr/bin/env python3
"""Deterministic terminology frequency report for The Underdoc corpus.

Evidence behind skill/references/voice-terminology.md. Run: python3 -I analysis/terminology_freq.py
"""
import re, glob, os, statistics, sys
from collections import Counter, defaultdict

CORPUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "terminology_freq.md")

def load(p):
    t = open(p, encoding="utf-8").read()
    slug = re.search(r'^slug:\s*"?([^"\n]+)"?', t, re.M).group(1)
    t = re.sub(r'\A---\n.*?\n---\n', '', t, flags=re.S)
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', t)
    t = re.sub(r'\[SCREENSHOT[^\]]*\]', ' ', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)   # keep link text
    t = re.sub(r'https?://\S+', ' ', t)
    t = re.sub(r'`[^`]*`', ' ', t)
    return slug, t

docs = {}
for p in sorted(glob.glob(CORPUS + "/*.md")):
    s, t = load(p); docs[s] = t
slugs = list(docs)
N = len(slugs)

def toks(t):
    return re.findall(r"[A-Za-z][A-Za-z0-9'’\-]*", t)
tok = {s: toks(docs[s]) for s in slugs}
words = {s: [w.lower().replace("’", "'") for w in tok[s]] for s in slugs}
wc = {s: len(words[s]) for s in slugs}

STOP = set("""a an the and or but if so as of at by for from in into on onto to with without about over under up down out off than then that this these those it its it's i i'm i've i'd i'll you you're you've you'll your yours we we're we've our us my me mine he she they them their his her is am are was were be been being have has had do does did done not no yes can could will would should may might must just also very more most much many some any all each every other another such only own same too there here what which who whom whose when where why how while because until still even like get got make made one two don't doesn't didn't isn't aren't wasn't can't won't it's that's there's what's let's thing things way""".split())

def ngrams(ws, n):
    return [" ".join(ws[i:i+n]) for i in range(len(ws)-n+1)
            if not (ws[i] in STOP and ws[i+n-1] in STOP) and ws[i] not in STOP and ws[i+n-1] not in STOP]

out = []
w = out.append
w(f"# W3 frequency output\n\nPosts: {N}. Total words (after stripping): {sum(wc.values())}. Median words/post: {statistics.median(wc.values())}.\n")

# (a) domain terms, bigrams, trigrams
dfu = defaultdict(set); tfu = Counter()
for s in slugs:
    for x in dict.fromkeys(words[s]):  # ordered dedupe: set order varies with the hash seed
        if x not in STOP and len(x) > 2: dfu[x].add(s)
    for x in words[s]:
        if x not in STOP and len(x) > 2: tfu[x] += 1
w("## (a) Recurring terms\n\n### Unigrams (content words, top 50 by post count, then total)\n")
w("| word | posts | total |\n|---|---|---|")
for x, d in sorted(dfu.items(), key=lambda kv: (-len(kv[1]), -tfu[kv[0]], kv[0]))[:50]:
    w(f"| {x} | {len(d)} | {tfu[x]} |")
for n, label, lim in ((2, "Bigrams", 45), (3, "Trigrams", 30)):
    df = defaultdict(set); tf = Counter()
    for s in slugs:
        for g in ngrams(words[s], n):
            df[g].add(s); tf[g] += 1
    rows = [(g, len(d), tf[g]) for g, d in df.items() if len(d) >= 3]
    rows.sort(key=lambda r: (-r[1], -r[2], r[0]))
    w(f"\n### {label} (in >=3 posts, top {lim})\n\n| phrase | posts | total |\n|---|---|---|")
    for g, a, b in rows[:lim]:
        w(f"| {g} | {a} | {b} |")

# (b) technical terms
TERMS = ["LLM","LLMs","RAG","MCP","uv","Cursor","Claude","Claude Code","ChatGPT","GPT","Gemini","OpenAI","Anthropic","Python","SQL","Pandas","football analytics","soccer analytics","football","soccer","xG","xA","xT","expected goals","StatsBomb","Opta","FBref","Transfermarkt","Streamlit","Gradio","Hugging Face","HF Spaces","LangChain","LangGraph","vector database","vector store","embedding","embeddings","chunking","prompt","prompts","context engineering","wordalisation","agent","agents","agentic","AI agent","tool calling","function calling","API","APIs","JSON","CSV","GitHub","Docker","Substack","LinkedIn","data engineering","data engineer","data scientist","data science","machine learning","ML","AI","IDE","IDEs","VS Code","Jupyter","notebook","evals","eval","faithfulness","hallucination","hallucinations","dashboard","scraping","scrape","pipeline","open source","open-source","real-time","real time","end-to-end","end to end","workflow","workflows","framework","Premier League","Eredivisie","Championship","Sheffield United"]
w("\n## (b) Technical terms: spelling and capitalization\n\nSurface forms found (case-sensitive, whole word), posts containing any form, total hits. `variants` lists each distinct spelling.\n")
w("| term | posts | total | surface forms (count) |\n|---|---|---|---|")
for term in TERMS:
    pat = re.compile(r'(?<![A-Za-z0-9])' + re.escape(term).replace(r'\ ', r'[\s\-]') + r'(?![A-Za-z0-9])', re.I)
    forms = Counter(); ps = set()
    for s in slugs:
        for m in pat.finditer(docs[s]):
            forms[re.sub(r'\s+', ' ', m.group(0))] += 1; ps.add(s)
    if not forms: continue
    w(f"| {term} | {len(ps)} | {sum(forms.values())} | " + ", ".join(f"`{k}` {v}" for k, v in forms.most_common()) + " |")

# (c) descriptive words / intensifiers / verbs, per 1000 words
SEEDS = {
 "intensifiers/adverbs": "really very actually honestly basically literally definitely truly super pretty quite simply just totally absolutely extremely incredibly especially seriously fairly highly mostly completely entirely clearly obviously probably maybe",
 "descriptive adjectives": "great good best better worse bad hard easy simple clean messy solid powerful useful helpful interesting amazing awesome cool nice fun weird wild huge big small tiny fast slow quick real raw rough practical actionable concrete specific important crucial key main huge massive heavy light cheap free expensive painful frustrating",
 "favored verbs": "build built building use used using try tried trying learn learned learning start started create created write wrote ship shipped find found looking look need want wanted think thought realized realize figure figured stumble stumbled break broke fix fixed run ran test tested pick picked switch switched move moved decide decided pull pulled grab grabbed scrape scraped feed feeding connect connected plug plugged play played explore explored dig dug",
}
w("\n## (c) Descriptive words, intensifiers, verbs\n\nRate = occurrences per 1000 words, per post. `median` = median of the per-post rates; `posts` = posts using it; `pooled` = total rate over the whole corpus; `top posts` = highest-rate posts (slug: rate).\n")
for label, lst in SEEDS.items():
    w(f"\n### {label}\n\n| word | posts | total | pooled /1k | median /1k | top posts |\n|---|---|---|---|---|---|")
    rows = []
    for x in lst.split():
        cnt = {s: words[s].count(x) for s in slugs}
        tot = sum(cnt.values())
        if tot == 0: continue
        rates = {s: 1000*cnt[s]/wc[s] for s in slugs}
        top = sorted(rates.items(), key=lambda kv: -kv[1])[:3]
        rows.append((x, sum(1 for v in cnt.values() if v), tot, 1000*tot/sum(wc.values()), statistics.median(rates.values()), top))
    rows.sort(key=lambda r: -r[3])
    for x, p, tot, pr, med, top in rows:
        w(f"| {x} | {p} | {tot} | {pr:.2f} | {med:.2f} | " + "; ".join(f"{a[:28]}: {b:.1f}" for a, b in top) + " |")

# auto: words with outsized, widespread use (spread >=8 posts, pooled rate high)
w("\n### Auto-detected frequent content words (>=10 posts, by pooled rate)\n\n| word | posts | pooled /1k | median /1k |\n|---|---|---|---|")
tot_w = sum(wc.values()); rows = []
for x, d in dfu.items():
    if len(d) >= 10 and len(x) > 3:
        rates = [1000*words[s].count(x)/wc[s] for s in slugs]
        rows.append((x, len(d), 1000*tfu[x]/tot_w, statistics.median(rates)))
rows.sort(key=lambda r: (-r[2], r[0]))
for x, p, pr, med in rows[:60]:
    w(f"| {x} | {p} | {pr:.2f} | {med:.2f} |")

# contraction + register
w("\n### Register markers (per 1000 words, median across posts)\n\n| marker | posts | median /1k | pooled /1k |\n|---|---|---|---|")
MARK = {"contractions (n't, 're, 've, 'm, 'll, 'd, 's)": r"\b\w+(?:n't|'re|'ve|'m|'ll|'d)\b|\b(?:it|that|there|here|what|let|he|she)'s\b",
        "first person I": r"\bI\b", "second person you/your": r"\b(?:you|your|you're|you've)\b",
        "we/our": r"\b(?:we|our|we've|we're|let's)\b", "questions (?)": r"\?",
        "exclamation (!)": r"!", "bold spans (**)": r"\*\*[^*]+\*\*", "parenthetical (": r"\(",
        "em-dash": "—", "semicolon": ";", "ellipsis": r"\.\.\.|…", "emoji-ish": r"[\U0001F300-\U0001FAFF☀-➿]"}
for k, pat in MARK.items():
    r = re.compile(pat, re.I if k.startswith("contr") else 0)
    c = {s: len(r.findall(docs[s])) for s in slugs}
    rates = [1000*c[s]/wc[s] for s in slugs]
    w(f"| {k} | {sum(1 for v in c.values() if v)} | {statistics.median(rates):.2f} | {1000*sum(c.values())/tot_w:.2f} |")

# (d) naming
w("\n## (d) How he names things\n")
def ctx(pattern, label, flags=re.I, width=45, maxn=14, per_post=2):
    r = re.compile(pattern, flags); ps = set(); forms = Counter(); ex = []
    for s in slugs:
        k = 0
        for m in r.finditer(docs[s]):
            ps.add(s); forms[m.group(0)] += 1
            if k < per_post and len(ex) < maxn:
                a = max(0, m.start()-width); b = min(len(docs[s]), m.end()+width)
                snippet = re.sub(r'\s+', ' ', docs[s][a:b])
                ex.append(f"`{s[:34]}`: …{snippet}…"); k += 1
    w(f"\n### {label}\n\nPosts: {len(ps)}. Forms: " + (", ".join(f"`{a}` {b}" for a, b in forms.most_common(10)) or "none") + "\n")
    for e in ex: w(f"- {e}")
ctx(r"the underdoc|underdoc", "The newsletter (Underdoc)")
ctx(r"\b(?:my|this|the) (?:newsletter|substack|blog|publication|series|diary)\b", "Newsletter/series self-reference")
ctx(r"\b(?:readers?|subscribers?|folks|friends|everyone|guys)\b", "Reader address nouns")
ctx(r"\b(?:I|I've|I'm) (?:built|created|made|call|called|named|wrote|automated|developed)\b", "'I built / I called' (naming own projects)", maxn=16)
ctx(r"\b(?:my|our) (?:own |little |first |latest )?(?:project|app|tool|system|dashboard|workflow|pipeline|framework|skill|agent|side project|data project)s?\b", "'my X' possessive project nouns", maxn=16)
ctx(r"\b(?:let's|let us|we'll|we can|we will|we're going to|we've|we are)\b", "we/let's constructions (check vs I rule)", maxn=10)
ctx(r"\b(?:the Underdoc|Gaffer|Nova|Brown|harness)\b", "Named internal projects (Nova/Brown/harness)", flags=0)

open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote", OUT, len(out), "lines")
