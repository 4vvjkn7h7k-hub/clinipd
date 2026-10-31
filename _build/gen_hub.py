#!/usr/bin/env python3
"""
Build library.html — the library hub.

Not a split-pane app and not one long scroll: the same head / sticky
tools / centred body skeleton as the nine A to Z listings, so the hub
reads as the front door of that same family. The search box searches
all 927 pages at once; the filter pills scope that search AND, with no
search term typed, open that section's groups as rows you can click.
"""
import io, json, os

SCR = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/clinipd/library.html"

ITEMS = json.load(io.open(os.path.join(SCR, "index_all.json"), encoding="utf-8"))
META  = json.load(io.open(os.path.join(SCR, "index_meta.json"), encoding="utf-8"))
COUNTS, GROUPS = META["counts"], META["groups"]

# code, file, name, mono badge, blurb, tag
SECTIONS = [
    ("cond", "conditions.html", "Conditions",       "CON", "Clinical presentations, each answering the same seventeen questions in the same order.", "free"),
    ("test", "tests.html",      "Special tests",    "TST", "How to perform it, what it means, and the sensitivity, specificity and likelihood ratios.", "free"),
    ("meas", "measures.html",   "Outcome measures", "OM",  "Each with its MCID and MDC, so a change score means something to the patient.", "free"),
    ("exer", "exercises.html",  "Exercises",        "EX",  "Real sets, reps, load and progression criteria — not “strengthen the quads”.", "free"),
    ("case", "cases.html",      "Clinical cases",   "CS",  "Worked end to end, from the referral letter to the discharge summary.", "free"),
    ("osce", "osce.html",       "OSCE stations",    "OSC", "Marking criteria, examiner prompts and the eight minutes you actually get.", "free"),
    ("bank", "qbank.html",      "Question bank",    "Q",   "Exam-style questions with worked reasoning on every option, right and wrong.", "pro"),
    ("fnd",  "foundations.html","Foundations",      "FND", "Anatomy, physiology, pathology, biomechanics and clinical reasoning.", "free"),
    ("plac", "placement.html",  "Placement",        "PLC", "Setting-by-setting preparation, plus the toolkit you need on day one.", "free"),
]

BANDS = [
    ("Reference",  "Look it up between patients.",        ["cond", "test", "meas", "exer"]),
    ("Practise",   "Put it in front of a patient, on paper first.", ["case", "osce", "bank"]),
    ("Background", "The layer underneath the presentations.", ["fnd", "plac"]),
]

OTHER = [
    ("DOM", "By domain",        "domains.html",     "Musculoskeletal, neuro, cardioresp and five more", ""),
    ("A-Z", "Glossary",         "glossary.html",    "151 terms — the words underlined site-wide", ""),
    ("VID", "Video library",    "videos.html",      "Technique, assessment and exercise demos", ""),
    ("PLN", "Study plans",      "studyplan.html",   "Build a plan to your exam date, week by week", ""),
    ("SAV", "Saved pages",      "collections.html", "Whatever you bookmarked as you read", ""),
    ("AN",  "Anki export",      "anki.html",        "Turn any page into a spaced-repetition deck", ""),
    ("CLC", "Clinical calculators", "app.html",     "Post-test probability, MCID, 1RM, OSCE timer", ""),
    ("STD", "Evidence standard","evidence.html",    "What we cite, and how every claim is traced", ""),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13m0 0-5-5m5 5-5 5"/></svg>')

BY = {c: (c, f, n, b, d, t) for c, f, n, b, d, t in SECTIONS}
TOTAL = sum(COUNTS.values())


def card(code, rev):
    _, href, name, badge, blurb, tag = BY[code]
    n = COUNTS[code]
    gs = GROUPS[code][:4]
    pills = "".join('<span>%s</span>' % g for g in gs)
    extra = len(GROUPS[code]) - len(gs)
    if extra > 0:
        pills += '<span class="more">+%d more</span>' % extra
    tagh = ('<span class="tag free">Free</span>' if tag == "free"
            else '<span class="tag pro">Pro</span>')
    return f"""      <a class="lib-card" href="{href}" data-rev="{rev}">
        <span class="code">{badge}</span>
        <b class="n" data-count="{n}" data-dur="1400">0</b>
        <h3>{name}</h3>
        <p>{blurb}</p>
        <div class="grps">{pills}</div>
        <span class="go">{tagh}<em>Browse A&nbsp;to&nbsp;Z {ARROW}</em></span>
      </a>"""


bands_html = []
for title, sub, codes in BANDS:
    cards = "\n".join(card(c, i * 70) for i, c in enumerate(codes))
    cls = " three" if len(codes) == 3 else (" two" if len(codes) == 2 else "")
    bands_html.append(f"""  <section class="lib-band">
    <header class="lib-bh" data-rev="0">
      <h2>{title}</h2><span>{sub}</span>
    </header>
    <div class="lib-cards{cls}">
{cards}
    </div>
  </section>""")

other_html = "\n".join(
    f"""      <a class="lib-min" href="{href}" data-rev="{i * 40}">
        <span class="mi">{badge}</span>
        <span class="tx"><b>{name}</b><span>{desc}</span></span>
        <span class="arw">{ARROW}</span>
      </a>""" for i, (badge, name, href, desc, _) in enumerate(OTHER))

filters = "".join(
    f'<button type="button" data-s="{c}">{n}<span class="c">{COUNTS[c]}</span></button>'
    for c, _, n, _, _, _ in SECTIONS)

SECMETA = {c: {"n": n, "f": f, "b": badge} for c, f, n, badge, _, _ in SECTIONS}

HTML = rf"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The library — CliniPD</title>
<meta name="description" content="{TOTAL} free, referenced physiotherapy pages — conditions, special tests, outcome measures, exercises, cases, OSCE stations, foundations and placement. Search them all in one box.">
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="listing.css">
<script>try{{var _r=document.documentElement,_s=localStorage.getItem("clinipd:scheme"),_f=localStorage.getItem("clinipd:font"),_m=localStorage.getItem("clinipd:mode");if(_s)_r.setAttribute("data-scheme",_s);if(_f)_r.setAttribute("data-font",_f);if(_m)_r.setAttribute("data-theme",_m);}}catch(e){{}}</script>
<style>
/* ---- hub-only: the section cards and the quick-links strip ---- */
.lib-band{{margin-top:clamp(52px,6vw,88px)}}
.lib-band:first-child{{margin-top:clamp(34px,4vw,54px)}}
.lib-bh{{text-align:center;margin-bottom:clamp(26px,3vw,38px)}}
.lib-bh h2{{font:600 clamp(23px,2.7vw,30px)/1.2 var(--display);letter-spacing:-.03em;margin:0}}
.lib-bh span{{display:block;margin-top:9px;font-size:15px;color:var(--muted)}}

.lib-cards{{display:grid;gap:18px;grid-template-columns:repeat(2,minmax(0,1fr));
  max-width:980px;margin-inline:auto}}
.lib-cards.three{{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:900px){{.lib-cards,.lib-cards.three{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:600px){{.lib-cards,.lib-cards.three{{grid-template-columns:minmax(0,1fr)}}}}

.lib-card{{position:relative;display:flex;flex-direction:column;
  padding:26px 26px 20px;min-width:0;
  border:1px solid var(--line);border-radius:var(--r-lg);background:var(--bg);
  text-decoration:none;color:inherit;overflow:hidden;
  transition:border-color .26s var(--e-out),box-shadow .26s var(--e-out),transform .26s var(--e-out)}}
/* a brand wash that wipes up from the bottom edge on hover, rather than
   a flat background swap — keeps the card quiet until you reach for it */
.lib-card::before{{content:"";position:absolute;inset:auto 0 0 0;height:100%;
  background:linear-gradient(to top,var(--brand-soft),transparent 62%);
  transform:translateY(101%);transition:transform .42s var(--e-out);z-index:0}}
.lib-card:hover::before{{transform:none}}
.lib-card > *{{position:relative;z-index:1}}
.lib-card:hover{{border-color:transparent;box-shadow:var(--shadow-lg);transform:translateY(-3px)}}
.lib-card:focus-visible{{outline:2px solid var(--brand);outline-offset:3px}}
.lib-card .code{{font:600 10px/1 var(--mono);letter-spacing:.16em;color:var(--brand);
  display:block;margin-bottom:14px}}
.lib-card .n{{font:600 clamp(34px,4.4vw,46px)/.95 var(--display);letter-spacing:-.045em;
  font-variant-numeric:tabular-nums;color:var(--ink)}}
.lib-card h3{{font:600 19px/1.28 var(--display);letter-spacing:-.025em;margin:10px 0 0}}
.lib-card p{{font-size:14.5px;line-height:1.58;color:var(--muted);margin:9px 0 0}}
.lib-card .grps{{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px}}
.lib-card .grps span{{font:500 11.5px/1 var(--sans);color:var(--ink-2);
  border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:var(--bg-2);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}}
.lib-card .grps .more{{color:var(--muted);border-style:dashed;background:none}}
.lib-card .go{{display:flex;align-items:center;gap:12px;margin-top:auto;padding-top:20px}}
.lib-card .go em{{font-style:normal;margin-left:auto;display:inline-flex;align-items:center;gap:7px;
  font:600 12.5px/1 var(--sans);color:var(--brand-ink);white-space:nowrap}}
.lib-card .go svg{{width:15px;height:15px;transition:transform .24s var(--e-spring)}}
.lib-card:hover .go svg{{transform:translateX(4px)}}

/* ---- group rows: what a filter pill opens when nothing is typed ---- */
.lib-groups{{max-width:820px;margin:clamp(30px,3.4vw,44px) auto 0}}
.lib-gh{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;
  justify-content:center;text-align:center;margin-bottom:20px}}
.lib-gh h2{{font:600 clamp(21px,2.5vw,27px)/1.2 var(--display);letter-spacing:-.03em;margin:0}}
.lib-gh a{{font:600 12.5px/1 var(--sans);color:var(--brand-ink);text-decoration:none}}
.lib-gh a:hover{{text-decoration:underline}}

/* ---- quick links ---- */
.lib-mins{{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr));
  max-width:860px;margin:clamp(26px,3vw,38px) auto 0}}
@media (max-width:620px){{.lib-mins{{grid-template-columns:minmax(0,1fr)}}}}
.lib-min{{display:flex;align-items:center;gap:14px;padding:16px 18px;min-width:0;
  border:1px solid var(--line);border-radius:16px;background:var(--bg);
  text-decoration:none;color:inherit;
  transition:border-color .2s var(--e-out),background .2s var(--e-out),transform .2s var(--e-out)}}
.lib-min:hover{{border-color:var(--brand);background:var(--brand-soft);transform:translateY(-2px)}}
.lib-min .mi{{width:32px;height:32px;border-radius:10px;flex:none;display:grid;place-items:center;
  background:var(--brand-soft);color:var(--brand-ink);font:700 10px/1 var(--mono);letter-spacing:.04em}}
.lib-min:hover .mi{{background:var(--brand);color:var(--on-brand)}}
.lib-min .tx{{min-width:0;flex:1}}
.lib-min .tx b{{display:block;font:600 15px/1.3 var(--sans)}}
.lib-min .tx span{{display:block;font-size:13px;line-height:1.45;color:var(--muted);margin-top:2px}}
.lib-min .arw{{flex:none;width:17px;height:17px;color:var(--line-2);
  transition:transform .22s var(--e-spring),color .2s}}
.lib-min .arw svg{{width:17px;height:17px}}
.lib-min:hover .arw{{transform:translateX(4px);color:var(--brand)}}

/* ---- the sticky tools, hub variant ---- */
.az-tools .hint{{text-align:center;margin:14px 0 0;font-size:13px;color:var(--muted);
  max-height:46px;opacity:1;overflow:hidden;
  transition:max-height .32s var(--e-out),opacity .2s var(--e-out),margin-top .32s var(--e-out)}}
/* once the bar is stuck it is furniture, not instruction — give the
   screen back, especially on a phone */
.az-tools.stuck .hint{{max-height:0;opacity:0;margin-top:0}}
.az-tools .hint b{{color:var(--ink-2);font-weight:600;
  font-family:var(--mono);font-size:11.5px;border:1px solid var(--line-2);
  border-radius:5px;padding:2px 5px}}
@media (prefers-reduced-motion:reduce){{.az-tools .hint{{transition:none}}}}
.az-row .sec-tag{{font:600 9.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;
  padding:5px 8px;border-radius:6px;border:1px solid var(--line-2);color:var(--muted);flex:none}}
@media (max-width:620px){{.az-row .sec-tag{{display:none}}}}

/* the whole hub trades places with the results list — crossfade, no jump */
#hub,#res{{animation:hubIn .34s var(--e-out) both}}
@keyframes hubIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{
  #hub,#res{{animation:none}}
  .lib-card::before{{display:none}}
  .lib-card:hover,.lib-min:hover{{transform:none}}
}}
</style>
</head>
<body>
<header class="top" id="site-top"></header>

<section class="az-head">
  <div class="wrap">
    <nav class="crumb"><a href="index.html">CliniPD</a> &nbsp;/&nbsp; Library</nav>
    <h1 class="h1">The physiotherapy library</h1>
    <p class="lede">{TOTAL} pages written to one template — conditions, tests, measures, exercises, cases, stations, foundations and placement. Referenced throughout, and dated so you can see how current the evidence is.</p>
    <p style="margin-top:22px"><span class="pill t"><span class="dot"></span>Free &middot; no account needed</span></p>
  </div>
</section>

<div class="az-tools" id="azTools">
  <div class="wrap">
    <div class="az-srch" id="sbox">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>
      <input id="q" type="search" placeholder="Search all {TOTAL} pages&hellip;" aria-label="Search the whole library" autocomplete="off" spellcheck="false">
      <kbd>/</kbd>
      <button class="x" id="x" type="button" aria-label="Clear search">
        <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
    <div class="az-filters" id="filters" role="group" aria-label="Section">
      <button type="button" data-s="" aria-pressed="true">All<span class="c">{TOTAL}</span></button>{filters}
    </div>
    <p class="hint" id="hint">Pick a section below, or search across all of them at once. Press <b>/</b> to jump to the search box.</p>
  </div>
</div>

<main class="wrap">

  <!-- ============ search results ============ -->
  <div id="res" hidden>
    <p class="az-count" id="rcount"></p>
    <ul class="az-list" id="rlist"></ul>
    <div class="az-none" id="rnone" hidden><b>Nothing matches that</b><p>Try a shorter word, or clear the section filter.</p></div>
    <p class="pagi-note" id="rmore"></p>
  </div>

  <!-- ============ one section's groups ============ -->
  <div id="grp" hidden>
    <div class="lib-groups">
      <div class="lib-gh"><h2 id="ghName"></h2><a id="ghAll" href="#">See the full A to Z &rarr;</a></div>
      <ul class="grouplist" id="glist"></ul>
    </div>
  </div>

  <!-- ============ the hub ============ -->
  <div id="hub">
{chr(10).join(bands_html)}

    <section class="lib-band">
      <header class="lib-bh" data-rev="0">
        <h2>Other ways in</h2><span>Same pages, different door.</span>
      </header>
      <div class="lib-mins">
{other_html}
      </div>
    </section>
  </div>
</main>

<footer class="foot" id="site-foot"></footer>

<script src="site.js"></script>
<script src="glossary.js"></script>
<script>
/* ============================================================
   One compact index of every page in the library.
     t  title     i  page id (p/<i>.html)
     s  section code     g  group it sits in     f  flag
   Built by scratchpad/build_index.py straight out of the nine
   A to Z pages, so the hub can never drift from the listings.
   ============================================================ */
const ALL = {json.dumps(ITEMS, separators=(',', ':'))};
const SEC = {json.dumps(SECMETA, separators=(',', ':'))};
const SGROUPS = {json.dumps(GROUPS, separators=(',', ':'))};
const CAP = 60;   /* results shown before "refine, or open the A to Z" */

(function(){{
  var q=document.getElementById('q'), box=document.getElementById('sbox'),
      x=document.getElementById('x'), filters=document.getElementById('filters'),
      hub=document.getElementById('hub'), res=document.getElementById('res'),
      grp=document.getElementById('grp'), glist=document.getElementById('glist'),
      ghName=document.getElementById('ghName'), ghAll=document.getElementById('ghAll'),
      rlist=document.getElementById('rlist'), rcount=document.getElementById('rcount'),
      rnone=document.getElementById('rnone'), rmore=document.getElementById('rmore'),
      hint=document.getElementById('hint'), tools=document.getElementById('azTools');

  var state={{ term:'', sec:'' }};

  function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{
    return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}

  /* highlight every typed word wherever it lands in the title */
  function mark(t,term){{
    term=(term||'').trim();
    if(!term) return esc(t);
    var words=term.toLowerCase().split(/\s+/).filter(Boolean);
    if(!words.length) return esc(t);
    var low=t.toLowerCase(), hit=new Array(t.length).fill(false), i, at, w;
    for(i=0;i<words.length;i++){{
      w=words[i]; at=0;
      while((at=low.indexOf(w,at))>-1){{
        for(var k=at;k<at+w.length;k++) hit[k]=true;
        at+=w.length;
      }}
    }}
    var out='', run='';
    for(i=0;i<=t.length;i++){{
      var on = i<t.length && hit[i];
      var was = i>0 && hit[i-1];
      if(i===t.length || on!==was){{
        if(run) out += was ? '<mark>'+esc(run)+'</mark>' : esc(run);
        run='';
      }}
      if(i<t.length) run+=t.charAt(i);
    }}
    return out;
  }}

  /* Every typed word has to appear somewhere, so "rot cuff" and
     "knee oa" both land. Results are then ranked: a title that STARTS
     with what you typed beats one that merely contains it, and a title
     match always beats a match on the group name alone. */
  function score(it,words){{
    var t=it.t.toLowerCase(), g=(it.g||'').toLowerCase(),
        a=(it.a||'').toLowerCase(), best=0;
    for(var i=0;i<words.length;i++){{
      var w=words[i], at=t.indexOf(w);
      if(at<0 && g.indexOf(w)<0 && a.indexOf(w)!==0) return -1;  /* word missing */
      var s;
      if(at===0)                      s=5;           /* title starts with it */
      else if(at>0 && !/[a-z0-9]/.test(t.charAt(at-1))) s=4;  /* starts a word */
      else if(a && a.indexOf(w)===0)  s=3;           /* its abbreviation — TUG, 6MWT */
      else if(at>0)                   s=2;           /* buried inside a word */
      else                            s=1;           /* group name only */
      if(s>best) best=s;
    }}
    return best;
  }}

  function matches(){{
    var term=state.term.toLowerCase().trim(), sec=state.sec;
    if(!term) return [];
    var words=term.split(/\s+/).filter(Boolean);
    var out=[];
    for(var i=0;i<ALL.length;i++){{
      var it=ALL[i];
      if(sec && it.s!==sec) continue;
      var sc=score(it,words);
      if(sc>0) out.push([sc,it]);
    }}
    /* ALL is already A to Z, and sort is stable, so equal scores stay alphabetical */
    out.sort(function(a,b){{ return b[0]-a[0]; }});
    return out.map(function(r){{ return r[1]; }});
  }}

  var ARROW='<svg class="go" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13m0 0-5-5m5 5-5 5"/></svg>';

  function row(it){{
    var s=SEC[it.s]||{{}};
    var cls='az-row'+(it.f?' '+it.f:'')+(it.k?' gl-link':'');
    var gt=it.k?' data-gterm="'+esc(it.k)+'"':'';
    return '<li><a class="'+cls+'" href="p/'+it.i+'.html"'+gt+'>'
      + '<span class="d"></span>'
      + '<span class="tx"><b class="lbl">'+mark(it.t,state.term)+'</b><em>'+esc(it.g||'')+'</em></span>'
      + '<span class="meta"><span class="sec-tag">'+esc(s.b||'')+'</span>'+ARROW+'</span>'
      + '</a></li>';
  }}

  /* ---- which of the three views is on ---- */
  function show(which){{
    hub.hidden = which!=='hub';
    res.hidden = which!=='res';
    grp.hidden = which!=='grp';
  }}

  function renderGroups(){{
    var s=SEC[state.sec], gs=SGROUPS[state.sec]||[];
    ghName.textContent = s.n;
    ghAll.href = s.f;
    glist.innerHTML = gs.map(function(g){{
      var n=ALL.filter(function(it){{return it.s===state.sec && it.g===g;}}).length;
      return '<li><a href="'+s.f+'?g='+encodeURIComponent(g)+'">'
        + '<b>'+esc(g)+'</b><span class="n">'+n+'</span></a></li>';
    }}).join('');
    hint.innerHTML = 'Showing the <b>'+esc(s.n.toLowerCase())+'</b> sections. '
      + 'Type to search inside them, or <a href="'+s.f+'" style="color:var(--brand-ink);font-weight:600">open the full A to Z</a>.';
  }}

  function render(){{
    var term=state.term.trim();

    if(!term){{
      if(state.sec){{ renderGroups(); show('grp'); }}
      else {{
        hint.innerHTML='Pick a section below, or search across all of them at once. Press <b>/</b> to jump to the search box.';
        show('hub');
      }}
      return;
    }}

    var list=matches();
    show('res');
    hint.innerHTML = state.sec
      ? 'Searching <b>'+esc((SEC[state.sec]||{{}}).n||'')+'</b> only — clear the pill to search everything.'
      : 'Searching all <b>'+ALL.length+'</b> pages.';

    if(!list.length){{
      rlist.innerHTML=''; rcount.textContent=''; rmore.textContent='';
      rnone.hidden=false; return;
    }}
    rnone.hidden=true;
    var shown=list.slice(0,CAP);
    rcount.textContent = list.length===1 ? '1 page' : list.length+' pages';
    rlist.innerHTML = shown.map(row).join('');
    if(list.length>shown.length){{
      rmore.innerHTML='Showing the first '+CAP+'. Keep typing to narrow it, '
        + 'or open a section&rsquo;s full A to Z from a pill above.';
    }} else {{ rmore.textContent=''; }}
    if(window.glossLinks) glossLinks(rlist);
  }}

  /* ---- events ---- */
  var t=null;
  q.addEventListener('input',function(){{
    box.classList.toggle('has', !!q.value);
    clearTimeout(t);
    t=setTimeout(function(){{ state.term=q.value; render(); }}, 90);
  }});
  x.addEventListener('click',function(){{
    q.value=''; state.term=''; box.classList.remove('has'); q.focus(); render();
  }});
  filters.addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b) return;
    var s=b.dataset.s;
    if(s===state.sec && s!==''){{ s=''; }}        /* click the live pill to clear it */
    state.sec=s;
    [].forEach.call(filters.children,function(c){{
      c.setAttribute('aria-pressed', String(c.dataset.s===state.sec));
    }});
    render();
    if(!state.term) window.scrollTo({{top:0,behavior:'smooth'}});
  }});
  document.addEventListener('keydown',function(e){{
    if(e.key==='/' && document.activeElement!==q){{ e.preventDefault(); q.focus(); }}
    if(e.key==='Escape' && document.activeElement===q){{
      q.value=''; state.term=''; box.classList.remove('has'); render();
    }}
  }});

  /* ---- deep links: library.html?q=acl  /  ?s=test ---- */
  var params=new URLSearchParams(location.search);
  if(params.get('q')){{ q.value=params.get('q'); state.term=q.value; box.classList.add('has'); }}
  if(params.get('s') && SEC[params.get('s')]){{
    state.sec=params.get('s');
    [].forEach.call(filters.children,function(c){{
      c.setAttribute('aria-pressed', String(c.dataset.s===state.sec));
    }});
  }}

  var onS=function(){{ tools.classList.toggle('stuck', window.scrollY>170); }};
  window.addEventListener('scroll',onS,{{passive:true}}); onS();
  render();
}})();
</script>
</body>
</html>
"""

io.open(OUT, "w", encoding="utf-8").write(HTML)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
print("total items:", TOTAL)
