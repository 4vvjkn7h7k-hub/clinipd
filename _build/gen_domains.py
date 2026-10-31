#!/usr/bin/env python3
"""Generate one real page per dropdown target, from the library's own tree."""
import io, json, os, re, unicodedata

OUT = "/home/claude/clinipd"
TREE = json.load(io.open("/home/claude/clinipd/_build/tree.json", encoding="utf-8"))

def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("'", "").replace("’", "").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

# domain key -> (file, display name, tab root used by library ids, blurb)
DOM = {
  "MSK":    ("msk.html",    "Musculoskeletal", "msk",
             "Spine, limbs and everything load-related — the bulk of most caseloads, and the deepest part of the library."),
  "NEURO":  ("neuro.html",  "Neurological", "neuro",
             "Central and peripheral nervous system rehabilitation, from acute stroke through to long-term community management."),
  "CARDIO": ("cardio.html", "Cardiorespiratory", "cardio",
             "Acute care, surgical, chronic respiratory and cardiac rehabilitation — including the techniques and the investigations behind them."),
  "GERI":   ("geri.html",   "Geriatrics & falls", "geri",
             "Falls, frailty, deconditioning and fracture rehabilitation, plus the assessment tools that actually change management."),
  "SPORTS": ("sports.html", "Sports", "sports",
             "Return-to-sport frameworks, load management and acute sporting injury — criteria-driven rather than time-driven."),
  "PAEDS":  ("paeds.html",  "Paediatrics", "paeds",
             "Development, paediatric neurology, respiratory and musculoskeletal presentations across childhood and adolescence."),
  "PELVIC": ("pelvic.html", "Pelvic & women's health", "pelvic",
             "Continence, pelvic pain, pregnancy and postnatal care — an area most new graduates are least confident in."),
  "PAIN":   ("pain.html",   "Persistent pain & vestibular", "pain",
             "Pain mechanisms, education and graded exposure, alongside vestibular assessment and management."),
}

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — CliniPD</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="site.css">
{extra_css}</head>
<body>

<header class="top" id="site-top"></header>

<section class="phead">
  <div class="wrap">
    <div class="crumb"><a href="index.html">CliniPD</a> &nbsp;/&nbsp; <a href="library.html">Library</a> &nbsp;/&nbsp; {crumb}</div>
    <h1 class="h1">{h1}</h1>
    <p class="lede" style="margin-top:16px">{lede}</p>
    {badge}
  </div>
</section>

{body}

<footer class="foot" id="site-foot"></footer>
<script src="site.js"></script>
</body>
</html>
"""

DOM_CSS = """<style>
.regions{display:grid;gap:22px;margin-top:52px;text-align:left}
.region{border:1px solid var(--line);border-radius:var(--r-lg);background:var(--bg);overflow:hidden}
.region > h3{display:flex;align-items:center;gap:12px;flex-wrap:wrap;
  padding:20px 26px;margin:0;background:var(--bg-2);border-bottom:1px solid var(--line);
  font:600 18px/1.25 var(--display)}
.region > h3 .n{margin-left:auto;font:600 11px/1 var(--mono);color:var(--muted);letter-spacing:.08em}
.conds{list-style:none;margin:0;padding:12px;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:2px}
.conds a{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:11px;
  text-decoration:none;color:var(--ink-2);font-size:14.5px;line-height:1.4;
  transition:background .15s,color .15s}
.conds a:hover{background:var(--brand-soft);color:var(--ink)}
.conds a .d{width:6px;height:6px;border-radius:50%;background:var(--line-2);flex:none}
.conds a.red .d{background:var(--coral)}
.conds a.postop .d{background:var(--warn)}
.conds a.red{color:var(--coral-ink)}
.key{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-top:28px;
  font-size:13.5px;color:var(--muted)}
.key span{display:inline-flex;align-items:center;gap:7px}
.key i{width:7px;height:7px;border-radius:50%;display:block}
</style>
"""

def page(key):
    fname, name, tab, blurb = DOM[key]
    regions = TREE[key]
    total = sum(len(r["items"]) for r in regions)
    blocks = []
    for r in regions:
        rslug = slug(r["region"])
        links = []
        for raw in r["items"]:
            cls = ""
            label = raw
            if label.startswith("!"):
                cls, label = "red", label[1:]
            elif label.startswith("^"):
                cls, label = "postop", label[1:]
            cid = "%s-%s-%s" % (tab, rslug, slug(label))
            links.append(
                '<li><a class="%s" href="library.html#%s"><span class="d"></span>%s</a></li>'
                % (cls, cid, label.replace("&", "&amp;")))
        blocks.append(
            '<div class="region" data-rev="0"><h3>%s<span class="n">%d PAGES</span></h3>'
            '<ul class="conds">%s</ul></div>'
            % (r["region"].replace("&", "&amp;"), len(r["items"]), "".join(links)))

    body = """<section class="sec">
  <div class="wrap">
    <div class="stats" style="grid-template-columns:repeat(3,minmax(0,1fr));max-width:720px" data-rev="0">
      <div class="stat"><b data-count="%d">0</b><span>Presentations</span></div>
      <div class="stat"><b data-count="%d">0</b><span>Regions</span></div>
      <div class="stat"><b data-count="17">0</b><span>Sections each</span></div>
    </div>
    <div class="key" data-rev="0">
      <span><i style="background:var(--line-2)"></i>Standard presentation</span>
      <span><i style="background:var(--coral)"></i>Must not miss</span>
      <span><i style="background:var(--warn)"></i>Post-operative</span>
    </div>
    <div class="regions">%s</div>
    <p class="dim" style="font-size:13.5px;margin-top:34px">Every page opens in the library app. Pages not yet written say so on the page.</p>
  </div>
</section>""" % (total, len(regions), "".join(blocks))

    return fname, SHELL.format(
        title=name, desc=blurb, crumb=name.replace("&", "&amp;"),
        h1=name.replace("&", "&amp;"), lede=blurb,
        badge='<p style="margin-top:18px"><span class="pill t"><span class="dot"></span>Free · no account needed</span></p>',
        body=body, extra_css=DOM_CSS)

written = []
for key in DOM:
    fname, html = page(key)
    io.open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)
    written.append((fname, len(html.encode("utf-8"))))

# ---------- three more pages that were previously same-page anchors ----------
EXTRA = {}

EXTRA["evidence.html"] = dict(
    title="Our evidence standard", crumb="Evidence standard", h1="How we select and reference",
    desc="The evidence standard behind every CliniPD page — what gets cited, how claims are traced, and how ageing evidence is flagged.",
    lede="Every page in the library is written to the same evidence rules. These are them, in full, so you can judge the content rather than trust it.",
    badge='<p style="margin-top:18px"><span class="pill t"><span class="dot"></span>Free · no account needed</span></p>',
    body="""<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="max-width:900px;margin-inline:auto">
      <div class="card" data-rev="0"><h3>What gets in</h3><p>Randomised trials, systematic reviews, meta-analyses and clinical practice guidelines from indexed journals. Case reports and narrative reviews only where nothing better exists — and labelled as such on the page.</p></div>
      <div class="card" data-rev="60"><h3>How claims are tied to sources</h3><p>Every substantive statement carries a numbered reference. If a figure cannot be traced to a source it does not go on the page: it is flagged and held back until it can be.</p></div>
      <div class="card" data-rev="120"><h3>How ageing is handled</h3><p>Each page shows its newest source year. Where the best available evidence is more than seven years old, the page says so in a banner rather than quietly presenting it as current.</p></div>
      <div class="card" data-rev="180"><h3>Review cycle</h3><p>Every page is re-checked on a 24-month cycle, with the review date and reviewer initials shown. A page that is overdue is marked overdue, not hidden.</p></div>
      <div class="card" data-rev="0"><h3>Where evidence doesn't exist</h3><p>Plenty of what physiotherapists do has never been tested properly. Where that is true the page says so, instead of inventing a number or implying more certainty than there is.</p></div>
      <div class="card" data-rev="60"><h3>What we never do</h3><p>No copied wording, tables or figures from source papers — data is restated and redrawn with citation. No copyrighted outcome-measure instruments reproduced without licence.</p></div>
    </div>
    <div class="gate" style="max-width:760px;margin:44px auto 0" data-rev="0">
      <h3 class="h3">Found something wrong?</h3>
      <p>Errors in clinical content matter more than almost anything else here. If a figure looks wrong, tell us and it gets checked.</p>
      <a class="btn pri" href="mailto:hello@clinipd.com?subject=Content%20correction">Report a correction</a>
    </div>
  </div>
</section>""")

EXTRA["clinics.html"] = dict(
    title="For clinics", crumb="For clinics", h1="For clinics",
    desc="Team accounts for physiotherapy clinics — shared CPD reporting, clinic protocols and one invoice.",
    lede="As a practice principal you carry the risk if a staff member cannot produce a CPD portfolio. A team account shows you where everyone sits, all year, without anyone having to be asked.",
    badge="",
    body="""<section class="sec">
  <div class="wrap">
    <div class="grid g3" style="max-width:1000px;margin-inline:auto">
      <div class="card" data-rev="0"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-5 6-5s6 1.7 6 5"/><path d="M16 5.2a3 3 0 0 1 0 5.6M18 20c0-2.3-.8-3.9-2-4.7"/></svg></div><h3>Whole-team visibility</h3><p>Every clinician's CPD hours, by domain, updated as they read. You see gaps in March rather than discovering them in November.</p></div>
      <div class="card" data-rev="70"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h14v16H5z"/><path d="M9 9h6M9 13h6M9 17h3"/></svg></div><h3>Your own protocols</h3><p>Clinic-specific pages sitting alongside the library, so new staff read your way of doing things from day one.</p></div>
      <div class="card" data-rev="140"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11m0 0 4-4m-4 4-4-4M5 19h14"/></svg></div><h3>Export everyone at once</h3><p>Audit-ready portfolios for the whole team in one export, rather than chasing eight people for eight documents.</p></div>
    </div>

    <div class="card" style="max-width:720px;margin:34px auto 0" data-rev="0">
      <h3>Example — a team of eight</h3>
      <div class="grid" style="gap:9px;margin-top:18px">
        <div class="card" style="padding:12px 16px;font-size:14.5px;display:flex;justify-content:space-between;gap:12px"><span>A. Nguyen</span><b style="color:var(--ok)">18.2 / 20 hrs</b></div>
        <div class="card" style="padding:12px 16px;font-size:14.5px;display:flex;justify-content:space-between;gap:12px"><span>J. Patel</span><b style="color:var(--ok)">20.0 / 20 hrs</b></div>
        <div class="card" style="padding:12px 16px;font-size:14.5px;display:flex;justify-content:space-between;gap:12px"><span>S. Okafor</span><b style="color:var(--warn)">11.4 / 20 hrs</b></div>
        <div class="card" style="padding:12px 16px;font-size:14.5px;display:flex;justify-content:space-between;gap:12px"><span>M. Rossi</span><b style="color:var(--coral)">6.1 / 20 hrs</b></div>
      </div>
      <p class="dim" style="font-size:12.5px;margin-top:16px">Illustrative. Team accounts need the accounts backend, which is not built yet.</p>
    </div>

    <div style="margin-top:38px"><a class="btn pri big" href="mailto:hello@clinipd.com?subject=Clinic%20team%20account">Talk to us about a team account</a></div>
  </div>
</section>""")

EXTRA["anki.html"] = dict(
    title="Anki export", crumb="Anki export", h1="Turn any page into a deck",
    desc="Export any CliniPD page as an Anki deck — Basic, Reversed or Cloze, with deck and tag naming handled automatically.",
    lede="Spaced repetition is the only study method with a serious evidence base behind it. Every page in the library exports straight into Anki, already named and tagged.",
    badge='<p style="margin-top:18px"><span class="pill t"><span class="dot"></span>Free · no account needed</span></p>',
    body="""<section class="sec">
  <div class="wrap">
    <div class="grid g3" style="max-width:1000px;margin-inline:auto">
      <div class="card" data-rev="0"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16v12H4z"/><path d="M8 10h8M8 14h5"/></svg></div><h3>Three card types</h3><p>Basic, Basic (and reversed), and Cloze — chosen per card, not per deck, so a definition and a list don't get forced into the same shape.</p></div>
      <div class="card" data-rev="70"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg></div><h3>Named and tagged for you</h3><p>Deck name and tags come from the page's position in the tree, so your collection stays organised without you doing it.</p></div>
      <div class="card" data-rev="140"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11m0 0 4-4m-4 4-4-4M5 19h14"/></svg></div><h3>Back-length meter</h3><p>Warns you when an answer is getting long enough that hitting "Show Answer" will jump you to the bottom of the card.</p></div>
    </div>
    <div style="margin-top:44px"><a class="btn pri big" href="library.html#anki">Open the Anki builder</a></div>
    <p class="dim" style="font-size:13.5px;margin-top:22px">Exports as a tab-separated <code>.txt</code> with Anki's import headers already set — File &rarr; Import in Anki and it lands correctly.</p>
  </div>
</section>""")

for fname, p in EXTRA.items():
    html = SHELL.format(title=p["title"], desc=p["desc"], crumb=p["crumb"], h1=p["h1"],
                        lede=p["lede"], badge=p.get("badge", ""), body=p["body"], extra_css="")
    io.open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)
    written.append((fname, len(html.encode("utf-8"))))

for f, n in written:
    print("wrote %-18s %6d bytes" % (f, n))
