#!/usr/bin/env python3
"""One real page per library item — 927 of them — plus A–Z section listings."""
import io, json, os, re, shutil
from collections import defaultdict

OUT = "/home/claude/clinipd"
SP  = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
PDIR = os.path.join(OUT, "p")
ALL  = json.load(io.open(SP + "/tree_full.json", encoding="utf-8"))
TPL  = json.load(io.open(SP + "/tpl.json", encoding="utf-8"))
TERMS = [t["t"] for t in json.load(io.open(SP + "/terms.json", encoding="utf-8"))]

BY = {n["id"]: n for n in ALL}
KIDS = defaultdict(list)
for n in ALL:
    if n["parent"]: KIDS[n["parent"]].append(n)

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def _norm(s): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()
_NT   = {_norm(t): t for t in TERMS}
_LONG = sorted(((_norm(t), t) for t in TERMS if len(_norm(t)) >= 5), key=lambda x: -len(x[0]))
def match_term(label):
    l = _norm(label)
    if not l: return None
    if l in _NT: return _NT[l]
    for kk, orig in _LONG:
        if re.search(r"\b" + re.escape(kk) + r"s?\b", l): return orig
    return None

SECTION_OF = {
  "conditions": ("Conditions", "conditions.html"),
  "tests": ("Special tests", "tests.html"),
  "measures": ("Outcome measures", "measures.html"),
  "exercises": ("Exercises", "exercises.html"),
  "cases": ("Clinical cases", "cases.html"),
  "osce": ("OSCE stations", "osce.html"),
  "qbank": ("Question bank", "qbank.html"),
  "foundations": ("Foundations", "foundations.html"),
  "placement": ("Placement", "placement.html"),
}
KIND_LABEL = {"presentation":"Presentation","test":"Special test","measure":"Outcome measure",
  "exercise":"Exercise","technique":"Technique","topic":"Topic","case":"Clinical case",
  "station":"OSCE station","bank":"Question bank","placement":"Placement setting","glossary":"Glossary"}

def chain(n):
    out, cur = [], n
    while cur and cur.get("parent"):
        cur = BY.get(cur["parent"])
        if cur: out.append(cur)
    return list(reversed(out))

# ------------------------------------------------------------------ article page
ART = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — CliniPD</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../site.css">
<link rel="stylesheet" href="../article.css">
<script>try{{var _s=localStorage.getItem("clinipd:scheme");if(_s)document.documentElement.setAttribute("data-scheme",_s);}}catch(e){{}}</script>
</head>
<body>
<header class="top" id="site-top"></header>

<article>
<section class="art-head">
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb">{crumbs}</nav>
    <p class="kind">{kind}</p>
    <h1 class="h1">{title}</h1>
    {blurb}
    <div class="chips">{chips}</div>
  </div>
</section>

<div class="wrap art-wrap">
  {video}

  <nav class="toc" aria-label="On this page">
    <h2>On this page</h2>
    <ol>{toc}</ol>
  </nav>

  {sections}

  <section class="refs" id="references">
    <h2>References</h2>
    <p class="none">No references yet. Every claim on this page will carry a numbered source before it is marked written.</p>
  </section>

  <nav class="pager" aria-label="Nearby pages">{pager}</nav>

  <p class="pid">Page id <code>{pid}</code> · <a href="../{sec_file}">All {sec_name_lower}</a> · <a href="../library.html#{pid}">Open in the library app</a></p>
</div>
</article>

<footer class="foot" id="site-foot"></footer>
<script src="../site.js"></script>
<script src="../glossary.js"></script>
</body>
</html>
"""

def field_html(f):
    return ('<div class="fld"><b>%s</b><span>Not written yet</span></div>' % esc(f))

def build_article(n):
    tab = n["tab"]
    sec_name, sec_file = SECTION_OF.get(tab, ("Library", "library.html"))
    tpl = TPL.get(n["type"]) or TPL.get("topic") or []
    parents = chain(n)

    crumbs = ['<a href="../index.html">CliniPD</a>']
    crumbs.append('<a href="../%s">%s</a>' % (sec_file, esc(sec_name)))
    for p in parents:
        if p["id"] == tab: continue
        crumbs.append('<a href="%s.html">%s</a>' % (p["id"], esc(p["title"])))
    crumbs.append('<span aria-current="page">%s</span>' % esc(n["title"]))
    crumbs_html = '<span class="sep">/</span>'.join(crumbs)

    flag = n.get("flag") or ""
    chips = ['<span class="chip empty">Not written yet</span>',
             '<span class="chip">%d sections</span>' % len(tpl),
             '<span class="chip">0 references</span>']
    if flag == "red":    chips.insert(0, '<span class="chip red">Must not miss</span>')
    if flag == "postop": chips.insert(0, '<span class="chip warn">Post-operative</span>')

    toc = "".join('<li><a href="#s%d">%s</a></li>' % (i + 1, esc(s["t"]))
                  for i, s in enumerate(tpl))
    toc += '<li><a href="#references">References</a></li>'

    secs = []
    for i, s in enumerate(tpl):
        fields = "".join(field_html(f) for f in s["f"]) or \
                 '<div class="fld wide"><span>Not written yet</span></div>'
        secs.append(
            '<section class="sec-a" id="s%d">'
            '<h2><span class="sn">%02d</span>%s</h2>'
            '<div class="flds">%s</div></section>' % (i + 1, i + 1, esc(s["t"]), fields))

    # video slot, only where it earns one
    if n["type"] in ("presentation", "test", "exercise", "technique"):
        label = "Technique demonstration" if n["type"] in ("test", "technique") else "Video overview"
        video = ('<section class="vid">'
                 '<h2>%s <span class="chip">Slot empty</span></h2>'
                 '<div class="vid-box">'
                 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
                 '<rect x="2.5" y="5" width="19" height="14" rx="3.5"/>'
                 '<path d="M10 9.5l5 2.5-5 2.5z" fill="currentColor" stroke="none"/></svg>'
                 '<b>No video yet</b>'
                 '<p>Add <code>"%s"</code> to <code>VIDEOS</code> in <code>library.html</code> '
                 'with a YouTube id to fill this slot.</p>'
                 '</div></section>' % (label, esc(n["id"])))
    else:
        video = ""

    # prev / next among siblings
    sibs = [k for k in KIDS.get(n["parent"], []) if not k["kids"]]
    pager = []
    try:
        idx = [k["id"] for k in sibs].index(n["id"])
    except ValueError:
        idx = -1
    if idx > 0:
        p = sibs[idx - 1]
        pager.append('<a class="pg prev" href="%s.html"><span>Previous</span><b>%s</b></a>'
                     % (p["id"], esc(p["title"])))
    if idx >= 0 and idx < len(sibs) - 1:
        p = sibs[idx + 1]
        pager.append('<a class="pg next" href="%s.html"><span>Next</span><b>%s</b></a>'
                     % (p["id"], esc(p["title"])))
    if not pager:
        pager.append('<a class="pg next" href="../%s"><span>Back to</span><b>All %s</b></a>'
                     % (sec_file, esc(sec_name.lower())))

    parent_titles = " · ".join(esc(p["title"]) for p in parents if p["id"] != tab)
    blurb = ('<p class="lede">%s</p>' % parent_titles) if parent_titles else ""

    return ART.format(
        title=esc(n["title"]), desc=esc("%s — %s. %s on CliniPD." %
            (n["title"], parent_titles or sec_name, KIND_LABEL.get(n["type"], "Page")))[:155],
        crumbs=crumbs_html, kind=esc(KIND_LABEL.get(n["type"], "Page")),
        blurb=blurb, chips="".join(chips), toc=toc, video=video,
        sections="".join(secs), pager="".join(pager), pid=esc(n["id"]),
        sec_file=sec_file, sec_name_lower=esc(sec_name.lower()))

# ------------------------------------------------------------------ write them
if os.path.isdir(PDIR): shutil.rmtree(PDIR)
os.makedirs(PDIR)

leaves = [n for n in ALL if not n["kids"] and n["tab"] in SECTION_OF]
total_bytes = 0
for n in leaves:
    html = build_article(n)
    total_bytes += len(html.encode("utf-8"))
    io.open(os.path.join(PDIR, n["id"] + ".html"), "w", encoding="utf-8").write(html)

# group pages (a region/domain) also get a page, listing their children
for n in ALL:
    if n["kids"] and n["tab"] in SECTION_OF and n["id"] != n["tab"]:
        kids = KIDS[n["id"]]
        rows = "".join(
            '<li><a href="%s"><b>%s</b>%s</a></li>' % (
                (k["id"] + ".html"),
                esc(k["title"]),
                '<span class="n">%d pages</span>' % len(KIDS[k["id"]]) if k["kids"] else "")
            for k in kids)
        sec_name, sec_file = SECTION_OF[n["tab"]]
        parents = chain(n)
        crumbs = ['<a href="../index.html">CliniPD</a>',
                  '<a href="../%s">%s</a>' % (sec_file, esc(sec_name))]
        for p in parents:
            if p["id"] == n["tab"]: continue
            crumbs.append('<a href="%s.html">%s</a>' % (p["id"], esc(p["title"])))
        crumbs.append('<span aria-current="page">%s</span>' % esc(n["title"]))
        html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t} — CliniPD</title>
<meta name="description" content="{t} — {sn} on CliniPD.">
<link rel="stylesheet" href="../site.css"><link rel="stylesheet" href="../article.css">
<script>try{{var _s=localStorage.getItem("clinipd:scheme");if(_s)document.documentElement.setAttribute("data-scheme",_s);}}catch(e){{}}</script>
</head><body>
<header class="top" id="site-top"></header>
<section class="art-head"><div class="wrap">
  <nav class="crumb">{c}</nav>
  <p class="kind">Group</p>
  <h1 class="h1">{t}</h1>
  <p class="lede">{n} pages in this group.</p>
</div></section>
<div class="wrap art-wrap">
  <ul class="grouplist">{rows}</ul>
  <p class="pid">Page id <code>{pid}</code> · <a href="../{sf}">All {snl}</a></p>
</div>
<footer class="foot" id="site-foot"></footer>
<script src="../site.js"></script><script src="../glossary.js"></script>
</body></html>""".format(t=esc(n["title"]), sn=esc(sec_name),
            c='<span class="sep">/</span>'.join(crumbs), n=len(kids), rows=rows,
            pid=esc(n["id"]), sf=sec_file, snl=esc(sec_name.lower()))
        total_bytes += len(html.encode("utf-8"))
        io.open(os.path.join(PDIR, n["id"] + ".html"), "w", encoding="utf-8").write(html)

files = os.listdir(PDIR)
print("pages written: %d  (%d leaf, %d group)" % (len(files), len(leaves), len(files) - len(leaves)))
print("total size: %.1f MB  avg %.1f KB" % (total_bytes / 1e6, total_bytes / len(files) / 1024))
