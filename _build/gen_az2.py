#!/usr/bin/env python3
"""A–Z section listings with group filter, sort and pagination (client-rendered)."""
import io, json, os, re, unicodedata
from collections import OrderedDict

OUT = "/home/claude/clinipd"
SP  = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
ALL = json.load(io.open(SP + "/tree_full.json", encoding="utf-8"))
TERMS = [t["t"] for t in json.load(io.open(SP + "/terms.json", encoding="utf-8"))]
BY = {n["id"]: n for n in ALL}
try:
    MANIFEST = json.load(io.open(os.path.join(OUT, "content", "index.json"), encoding="utf-8"))
except Exception:
    MANIFEST = {}

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

def chain(n):
    out, cur = [], n
    while cur and cur.get("parent"):
        cur = BY.get(cur["parent"])
        if cur: out.append(cur)
    return list(reversed(out))

SECTIONS = OrderedDict([
 ("conditions", dict(file="conditions.html", title="Conditions", unit="conditions",
   h1="Conditions A to Z", filter_label="Domain",
   lede="Every clinical presentation in the library. Filter by domain, sort how you like, and open any one for the full page.")),
 ("tests", dict(file="tests.html", title="Special tests", unit="special tests",
   h1="Special tests A to Z", filter_label="Body region",
   lede="Orthopaedic and neurological special tests, each with its sensitivity, specificity and likelihood ratios.")),
 ("measures", dict(file="measures.html", title="Outcome measures", unit="outcome measures",
   h1="Outcome measures A to Z", filter_label="Category",
   lede="Patient-reported and performance measures, each with its MCID and MDC — so a change score means something.")),
 ("exercises", dict(file="exercises.html", title="Exercises", unit="exercises",
   h1="Exercises A to Z", filter_label="Category",
   lede="Exercises and loading principles, with actual sets, reps, load and progression.")),
 ("cases", dict(file="cases.html", title="Clinical cases", unit="cases",
   h1="Clinical cases A to Z", filter_label="Domain",
   lede="Work a real presentation end to end — the referral, the questions you choose, and what skipping something costs.")),
 ("osce", dict(file="osce.html", title="OSCE stations", unit="stations",
   h1="OSCE stations A to Z", filter_label="Category",
   lede="Practical exam stations with timing, marking criteria and the traps examiners use.")),
 ("qbank", dict(file="qbank.html", title="Question bank", unit="banks",
   h1="Question banks A to Z", filter_label="Category", pro=True,
   lede="Exam-style questions with worked reasoning, grouped by topic.")),
 ("foundations", dict(file="foundations.html", title="Foundations", unit="topics",
   h1="Foundations A to Z", filter_label="Area",
   lede="The underpinning science and professional knowledge — anatomy, physiology, pathology, biomechanics and practice.")),
 ("placement", dict(file="placement.html", title="Placement", unit="topics",
   h1="Placement A to Z", filter_label="Area",
   lede="Setting-by-setting preparation and the practical toolkit you actually use on the ward.")),
])

CSS = r"""
.az-head{padding:clamp(52px,6vw,92px) 0 clamp(34px,4vw,50px);background:var(--bg-2);text-align:center}
.az-head .h1{max-width:18ch;margin-inline:auto}
.az-head .lede{margin-top:20px}
.az-head .crumb{font:500 13.5px/1 var(--sans);color:var(--muted);margin-bottom:20px}
.az-head .crumb a{text-decoration:none;color:var(--brand-ink)}
.az-head .crumb a:hover{text-decoration:underline}

.az-tools{position:sticky;top:var(--top);z-index:40;background:var(--bg);
  border-bottom:1px solid var(--line);padding:20px 0 16px;transition:box-shadow .25s var(--e-out)}
.az-tools.stuck{box-shadow:0 4px 22px rgb(0 0 0 / .06)}

.az-srch{display:flex;align-items:center;gap:12px;background:var(--bg-2);
  border:1.5px solid var(--line);border-radius:999px;padding:5px 7px 5px 22px;
  max-width:540px;margin:0 auto;transition:border-color .2s var(--e-out),background .2s,box-shadow .2s}
.az-srch:focus-within{border-color:var(--brand);background:var(--bg);box-shadow:0 0 0 4px var(--brand-soft)}
.az-srch svg{width:18px;height:18px;color:var(--muted);flex:none}
.az-srch input{flex:1;min-width:0;border:0;outline:0;background:none;color:var(--ink);
  font:400 16px/1 var(--sans);padding:13px 0}
.az-srch input::placeholder{color:var(--muted)}
.az-srch .x{flex:none;width:34px;height:34px;border-radius:50%;border:0;cursor:pointer;
  background:none;color:var(--muted);display:none;place-items:center}
.az-srch .x:hover{background:var(--bg-3);color:var(--ink)}
.az-srch.has .x{display:grid}
.az-srch kbd{font:600 11px/1 var(--mono);color:var(--muted);background:var(--bg);
  border:1px solid var(--line);border-radius:6px;padding:5px 7px;flex:none}
.az-srch.has kbd{display:none}

/* ---- group filter pills ---- */
.az-filters{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:16px}
.az-filters button{
  display:inline-flex;align-items:center;gap:8px;
  padding:8px 15px;border-radius:999px;border:1px solid var(--line);
  background:var(--bg);color:var(--ink-2);font:550 13.5px/1 var(--sans);cursor:pointer;
  transition:background .18s var(--e-out),border-color .18s,color .18s,transform .12s var(--e-spring)}
.az-filters button:hover{border-color:var(--line-2);background:var(--bg-2);color:var(--ink)}
.az-filters button:active{transform:scale(.96)}
.az-filters button[aria-pressed="true"]{background:var(--brand);border-color:var(--brand);color:#fff}
.az-filters button .c{font:600 10.5px/1 var(--mono);opacity:.72}

/* ---- sort row ---- */
.az-sort{display:flex;gap:14px;justify-content:center;align-items:center;
  flex-wrap:wrap;margin-top:16px}
.az-sort label{display:inline-flex;align-items:center;gap:8px;
  font:600 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.az-sort select{
  border:1px solid var(--line);border-radius:999px;background:var(--bg);color:var(--ink);
  font:550 13.5px/1 var(--sans);padding:9px 34px 9px 15px;cursor:pointer;
  appearance:none;-webkit-appearance:none;
  background-image:url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' fill='none' stroke='%23718' stroke-width='1.6' stroke-linecap='round'%3E%3Cpath d='M3 4.5 6 7.5 9 4.5'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 13px center;background-size:11px;
  transition:border-color .18s var(--e-out),box-shadow .18s}
.az-sort select:hover{border-color:var(--line-2)}
.az-sort select:focus{outline:0;border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-soft)}

.az-bar{display:flex;flex-wrap:wrap;gap:3px;justify-content:center;margin-top:16px}
.az-bar[hidden]{display:none}
.az-bar button{
  min-width:32px;height:32px;display:grid;place-items:center;border:0;border-radius:9px;
  background:none;cursor:pointer;
  font:600 14px/1 var(--sans);color:var(--brand-ink);
  transition:background .16s var(--e-out),color .16s,transform .14s var(--e-spring)}
.az-bar button:hover:not(:disabled){background:var(--brand-soft);transform:translateY(-1px)}
.az-bar button:disabled{color:var(--line-2);cursor:default}

.az-count{text-align:center;margin:30px 0 0;
  font:500 12.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}

.az-body{max-width:820px;margin:0 auto;padding-bottom:10px}
.az-grp{margin-top:clamp(30px,3.4vw,46px);scroll-margin-top:calc(var(--top) + 190px)}
.az-l{display:flex;align-items:center;gap:16px;margin-bottom:4px}
.az-l b{width:44px;height:44px;flex:none;display:grid;place-items:center;border-radius:13px;
  background:var(--brand);color:#fff;font:600 19px/1 var(--display)}
.az-l i{flex:1;height:1px;background:var(--line);display:block}
.az-l span{font:600 11px/1 var(--mono);letter-spacing:.1em;color:var(--muted);flex:none}

.az-list{list-style:none;margin:0;padding:0;
  border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;background:var(--bg)}
.az-list li + li{border-top:1px solid var(--line)}
.az-row{display:flex;align-items:center;gap:16px;padding:19px 26px;
  text-decoration:none;color:inherit;min-width:0;
  transition:background .16s var(--e-out),padding-left .22s var(--e-out)}
.az-row:hover{background:var(--brand-soft);padding-left:34px}
.az-row .d{width:7px;height:7px;border-radius:50%;background:var(--line-2);flex:none}
.az-row.red .d{background:var(--coral)}
.az-row.postop .d{background:var(--warn)}
.az-row .tx{min-width:0;flex:1}
.az-row .tx b{display:block;font:550 17px/1.4 var(--sans);letter-spacing:-.005em}
.az-row.red .tx b{color:var(--coral-ink)}
.az-row .tx em{display:block;font-style:normal;font-size:13.5px;color:var(--muted);margin-top:3px}
.az-row .meta{flex:none;display:flex;align-items:center;gap:10px}
.az-row .yq{font:600 9.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;
  padding:5px 8px;border-radius:6px;border:1px solid var(--line-2);color:var(--muted)}
.az-row .yq.hi{color:var(--coral);border-color:var(--coral);background:var(--coral-soft)}
.az-row .yq.med{color:var(--warn);border-color:var(--warn);background:var(--warn-soft)}
.az-row .go{width:18px;height:18px;flex:none;color:var(--line-2);
  transition:transform .22s var(--e-spring),color .18s}
.az-row:hover .go{transform:translateX(4px);color:var(--brand)}
.az-row mark{background:var(--brand-soft);color:var(--brand-ink);border-radius:3px;padding:0 2px;font-weight:700}
.gl-link .lbl{border-bottom:1.5px dotted var(--brand);padding-bottom:1px}

/* ---- pagination ---- */
.pagi{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;align-items:center;
  margin-top:clamp(36px,4vw,54px)}
.pagi button{
  min-width:42px;height:42px;padding:0 13px;border-radius:12px;
  border:1px solid var(--line);background:var(--bg);color:var(--ink-2);
  font:600 14.5px/1 var(--sans);cursor:pointer;
  transition:background .16s var(--e-out),border-color .16s,color .16s,transform .12s var(--e-spring)}
.pagi button:hover:not(:disabled):not([aria-current]){background:var(--bg-2);border-color:var(--line-2);color:var(--ink)}
.pagi button:active:not(:disabled){transform:scale(.95)}
.pagi button[aria-current="page"]{background:var(--brand);border-color:var(--brand);color:#fff}
.pagi button:disabled{opacity:.4;cursor:default}
.pagi .gap{color:var(--muted);padding:0 4px;font-weight:600}
.pagi .nav{display:inline-flex;align-items:center;gap:7px}
.pagi .nav svg{width:15px;height:15px}
.pagi-note{text-align:center;margin-top:16px;font-size:13px;color:var(--muted)}

.az-none{text-align:center;padding:70px 20px;color:var(--muted)}
.az-none b{display:block;font:600 20px/1.3 var(--display);color:var(--ink);margin-bottom:8px}
.az-key{display:flex;gap:22px;justify-content:center;flex-wrap:wrap;margin-top:24px;
  font-size:13.5px;color:var(--muted)}
.az-key span{display:inline-flex;align-items:center;gap:8px}
.az-key i{width:7px;height:7px;border-radius:50%;display:block}
@media (max-width:620px){
  .az-row{padding:16px 18px;gap:12px}
  .az-row:hover{padding-left:24px}
  .az-row .yq{display:none}
  .az-l b{width:38px;height:38px;font-size:17px}
  .az-sort{gap:10px}
}
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — CliniPD</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="site.css">
<script>try{{var _s=localStorage.getItem("clinipd:scheme");if(_s)document.documentElement.setAttribute("data-scheme",_s);}}catch(e){{}}</script>
<style>{css}</style>
</head>
<body>
<header class="top" id="site-top"></header>

<section class="az-head">
  <div class="wrap">
    <nav class="crumb"><a href="index.html">CliniPD</a> &nbsp;/&nbsp; <a href="library.html">Library</a> &nbsp;/&nbsp; {title}</nav>
    <h1 class="h1">{h1}</h1>
    <p class="lede">{lede}</p>
    <p style="margin-top:22px">{badge}</p>
  </div>
</section>

<div class="az-tools" id="azTools">
  <div class="wrap">
    <div class="az-srch" id="sbox">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>
      <input id="q" type="search" placeholder="Search {n} {unit}…" aria-label="Search {title}" autocomplete="off" spellcheck="false">
      <kbd>/</kbd>
      <button class="x" id="x" type="button" aria-label="Clear search">
        <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>

    <div class="az-filters" id="filters" role="group" aria-label="{filter_label}"></div>

    <div class="az-sort">
      <label for="sort">Sort
        <select id="sort">
          <option value="az">A to Z</option>
          <option value="za">Z to A</option>
          <option value="upd">Recently updated</option>
          <option value="yld">Highest yield</option>
        </select>
      </label>
      <label for="per">Per page
        <select id="per">
          <option value="25">25</option>
          <option value="50" selected>50</option>
          <option value="100">100</option>
          <option value="0">All</option>
        </select>
      </label>
    </div>

    <nav class="az-bar" id="azbar" aria-label="Jump to letter"></nav>
  </div>
</div>

<main class="wrap">
  {key}
  <p class="az-count" id="count"></p>
  <div class="az-body" id="body"></div>
  <div class="az-none" id="none" hidden><b>Nothing matches that</b><p>Try a shorter word, or clear the filter.</p></div>
  <nav class="pagi" id="pagi" aria-label="Pagination"></nav>
  <p class="pagi-note" id="pnote"></p>
</main>

<footer class="foot" id="site-foot"></footer>
<script src="site.js"></script>
<script src="glossary.js"></script>
<script>
/* ============================================================
   Data for this index.
     t  title        g  top-level group      r  where it sits
     i  page id      f  flag (red|postop)    k  glossary term
     y  yield 3=high 2=medium 1=standard     u  updated (ISO) or null
   YIELD is provisional — see README §19. Override any id here.
   ============================================================ */
const ITEMS = {items};
const GROUPS = {groups};
const UNIT = "{unit}";

(function(){{
  var q=document.getElementById('q'), box=document.getElementById('sbox'),
      x=document.getElementById('x'), body=document.getElementById('body'),
      none=document.getElementById('none'), count=document.getElementById('count'),
      filters=document.getElementById('filters'), sortSel=document.getElementById('sort'),
      perSel=document.getElementById('per'), pagi=document.getElementById('pagi'),
      pnote=document.getElementById('pnote'), azbar=document.getElementById('azbar'),
      tools=document.getElementById('azTools');

  var state={{ term:'', group:'', sort:'az', per:50, page:1 }};

  function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  function norm(s){{return s.toLowerCase();}}
  function letter(t){{var c=t.trim().charAt(0).toUpperCase();return /[A-Z]/.test(c)?c:'#';}}

  /* ---- filter pills ---- */
  filters.innerHTML = '<button type="button" data-g="" aria-pressed="true">All'
    + '<span class="c">' + ITEMS.length + '</span></button>'
    + GROUPS.map(function(g){{
        var n=ITEMS.filter(function(it){{return it.g===g;}}).length;
        return '<button type="button" data-g="'+esc(g)+'" aria-pressed="false">'+esc(g)
             + '<span class="c">'+n+'</span></button>';
      }}).join('');

  function matches(){{
    var t=state.term.trim().toLowerCase();
    return ITEMS.filter(function(it){{
      if(state.group && it.g!==state.group) return false;
      if(!t) return true;
      return norm(it.t).indexOf(t)>=0 || norm(it.r).indexOf(t)>=0;
    }});
  }}

  function sorted(list){{
    var s=state.sort, out=list.slice();
    if(s==='az') out.sort(function(a,b){{return a.t.localeCompare(b.t);}});
    else if(s==='za') out.sort(function(a,b){{return b.t.localeCompare(a.t);}});
    else if(s==='upd') out.sort(function(a,b){{
      if(a.u&&b.u&&a.u!==b.u) return a.u<b.u?1:-1;
      if(a.u&&!b.u) return -1;
      if(!a.u&&b.u) return 1;
      return a.t.localeCompare(b.t);
    }});
    else out.sort(function(a,b){{
      if(b.y!==a.y) return b.y-a.y;
      return a.t.localeCompare(b.t);
    }});
    return out;
  }}

  function hi(label,t){{
    if(!t) return esc(label);
    var i=label.toLowerCase().indexOf(t);
    if(i<0) return esc(label);
    return esc(label.slice(0,i))+'<mark>'+esc(label.slice(i,i+t.length))+'</mark>'+esc(label.slice(i+t.length));
  }}

  var ARROW='<svg class="go" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13m0 0-5-5m5 5-5 5"/></svg>';

  function rowHTML(it,t){{
    var cls='az-row'+(it.f?' '+it.f:'')+(it.k?' gl-link':'');
    var gt=it.k?' data-gterm="'+esc(it.k)+'"':'';
    var meta='';
    if(state.sort==='yld' && it.y>1)
      meta='<span class="yq '+(it.y===3?'hi':'med')+'">'+(it.y===3?'High yield':'Medium')+'</span>';
    if(state.sort==='upd')
      meta='<span class="yq">'+(it.u?esc(it.u):'Not updated')+'</span>';
    return '<li><a class="'+cls+'" href="p/'+esc(it.i)+'.html"'+gt+'>'
      + '<span class="d"></span><span class="tx"><b class="lbl">'+hi(it.t,t)+'</b>'
      + '<em>'+esc(it.r)+'</em></span>'
      + (meta?'<span class="meta">'+meta+'</span>':'') + ARROW + '</a></li>';
  }}

  function render(){{
    var t=state.term.trim().toLowerCase();
    var list=sorted(matches());
    var total=list.length;
    var per=state.per||total||1;
    var pages=Math.max(1, Math.ceil(total/per));
    if(state.page>pages) state.page=pages;
    var from=(state.page-1)*per, to=state.per?Math.min(from+per,total):total;
    var slice=list.slice(from,to);

    var alpha=(state.sort==='az'||state.sort==='za');
    azbar.hidden = !alpha || !!t;

    if(!slice.length){{ body.innerHTML=''; none.hidden=false; }}
    else {{
      none.hidden=true;
      if(alpha){{
        var html='', cur=null, buf=[];
        slice.forEach(function(it){{
          var L=letter(it.t);
          if(L!==cur){{
            if(cur!==null) html+='<section class="az-grp" id="L'+(cur==='#'?'num':cur)+'"><div class="az-l"><b>'+cur+'</b><i></i><span>'+buf.length+'</span></div><ul class="az-list">'+buf.join('')+'</ul></section>';
            cur=L; buf=[];
          }}
          buf.push(rowHTML(it,t));
        }});
        if(cur!==null) html+='<section class="az-grp" id="L'+(cur==='#'?'num':cur)+'"><div class="az-l"><b>'+cur+'</b><i></i><span>'+buf.length+'</span></div><ul class="az-list">'+buf.join('')+'</ul></section>';
        body.innerHTML=html;
      }} else {{
        body.innerHTML='<section class="az-grp"><ul class="az-list">'
          + slice.map(function(it){{return rowHTML(it,t);}}).join('') + '</ul></section>';
      }}
    }}

    count.textContent = total
      ? (state.per ? (from+1)+'–'+to+' of '+total+' '+UNIT : total+' '+UNIT)
      : 'No '+UNIT;

    /* letters present anywhere in the current filter, for the jump bar */
    if(alpha && !t){{
      var have={{}};
      list.forEach(function(it){{ have[letter(it.t)]=true; }});
      var L='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
      azbar.innerHTML=L.map(function(c){{
        return '<button type="button" data-l="'+c+'"'+(have[c]?'':' disabled')+'>'+c+'</button>';
      }}).join('') + (have['#']?'<button type="button" data-l="#">#</button>':'');
    }}

    drawPagi(pages,total);
    if(window.glossLinks) glossLinks(body);
  }}

  function drawPagi(pages,total){{
    if(!state.per || pages<=1){{ pagi.innerHTML=''; pnote.textContent=''; return; }}
    var p=state.page, out=[];
    out.push('<button type="button" class="nav" data-p="'+(p-1)+'"'+(p===1?' disabled':'')+' aria-label="Previous page">'
      +'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H6m0 0 5-5m-5 5 5 5"/></svg>Prev</button>');
    var nums=[];
    for(var i=1;i<=pages;i++){{
      if(i===1||i===pages||Math.abs(i-p)<=1) nums.push(i);
      else if(nums[nums.length-1]!=='…') nums.push('…');
    }}
    nums.forEach(function(n){{
      if(n==='…') out.push('<span class="gap">…</span>');
      else out.push('<button type="button" data-p="'+n+'"'+(n===p?' aria-current="page"':'')+'>'+n+'</button>');
    }});
    out.push('<button type="button" class="nav" data-p="'+(p+1)+'"'+(p===pages?' disabled':'')+' aria-label="Next page">Next'
      +'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13m0 0-5-5m5 5-5 5"/></svg></button>');
    pagi.innerHTML=out.join('');
    pnote.textContent='Page '+p+' of '+pages;
  }}

  function toTop(){{
    var y=tools.getBoundingClientRect().top+window.scrollY-10;
    window.scrollTo({{top:y,behavior:'smooth'}});
  }}

  var tmr=null;
  q.addEventListener('input',function(){{
    box.classList.toggle('has',!!q.value);
    clearTimeout(tmr); tmr=setTimeout(function(){{ state.term=q.value; state.page=1; render(); }},80);
  }});
  x.addEventListener('click',function(){{ q.value=''; state.term=''; state.page=1; box.classList.remove('has'); render(); q.focus(); }});
  filters.addEventListener('click',function(e){{
    var b=e.target.closest('button[data-g]'); if(!b) return;
    state.group=b.dataset.g; state.page=1;
    [].forEach.call(filters.children,function(c){{ c.setAttribute('aria-pressed', String(c===b)); }});
    render();
  }});
  sortSel.addEventListener('change',function(){{ state.sort=sortSel.value; state.page=1; render(); }});
  perSel.addEventListener('change',function(){{ state.per=parseInt(perSel.value,10); state.page=1; render(); }});
  pagi.addEventListener('click',function(e){{
    var b=e.target.closest('button[data-p]'); if(!b||b.disabled) return;
    state.page=parseInt(b.dataset.p,10); render(); toTop();
  }});
  azbar.addEventListener('click',function(e){{
    var b=e.target.closest('button[data-l]'); if(!b||b.disabled) return;
    var L=b.dataset.l;
    /* find which page that letter starts on, go there, then scroll to it */
    var list=sorted(matches());
    var idx=list.findIndex(function(it){{ return letter(it.t)===L; }});
    if(idx<0) return;
    if(state.per) state.page=Math.floor(idx/state.per)+1;
    render();
    var el=document.getElementById('L'+(L==='#'?'num':L));
    if(el) el.scrollIntoView({{behavior:'smooth',block:'start'}});
  }});
  document.addEventListener('keydown',function(e){{
    if(e.key==='/' && document.activeElement!==q){{ e.preventDefault(); q.focus(); }}
    if(e.key==='Escape' && document.activeElement===q){{ q.value=''; state.term=''; state.page=1; box.classList.remove('has'); render(); }}
  }});

  var params=new URLSearchParams(location.search);
  if(params.get('q')){{ q.value=params.get('q'); state.term=q.value; box.classList.add('has'); }}
  if(params.get('g')){{ state.group=params.get('g');
    [].forEach.call(filters.children,function(c){{ c.setAttribute('aria-pressed', String(c.dataset.g===state.group)); }}); }}

  var onS=function(){{ tools.classList.toggle('stuck', window.scrollY>170); }};
  window.addEventListener('scroll',onS,{{passive:true}}); onS();
  render();
}})();
</script>
</body>
</html>
"""

KEY = """<div class="az-key">
    <span><i style="background:var(--line-2)"></i>Standard presentation</span>
    <span><i style="background:var(--coral)"></i>Must not miss</span>
    <span><i style="background:var(--warn)"></i>Post-operative</span>
  </div>"""

built = []
for tab, cfg in SECTIONS.items():
    leaves = [n for n in ALL if n["tab"] == tab and not n["kids"]]
    leaves.sort(key=lambda n: n["title"].lower())

    items, groups = [], []
    for n in leaves:
        parents = [p for p in chain(n) if p["id"] != tab]
        group = parents[0]["title"] if parents else cfg["title"]
        where = " · ".join(p["title"] for p in parents) or cfg["title"]
        if group not in groups: groups.append(group)
        flag = n.get("flag") or ""
        yld = 3 if flag == "red" else (2 if flag == "postop" else 1)
        man = MANIFEST.get(n["id"]) or {}
        upd = man.get("reviewed") or None
        term = match_term(n["title"])
        rec = {"t": n["title"], "i": n["id"], "g": group, "r": where,
               "f": flag, "y": yld, "u": upd}
        if term: rec["k"] = term
        items.append(rec)

    badge = ('<span class="pill c"><span class="dot"></span>Pro feature</span>'
             if cfg.get("pro") else
             '<span class="pill t"><span class="dot"></span>Free · no account needed</span>')

    html = PAGE.format(
        title=cfg["title"], h1=cfg["h1"], lede=cfg["lede"], desc=cfg["lede"][:155],
        css=CSS, badge=badge, n=len(leaves), unit=cfg["unit"],
        filter_label=cfg["filter_label"],
        key=KEY if tab == "conditions" else "",
        items=json.dumps(items, ensure_ascii=False, separators=(",", ":")),
        groups=json.dumps(groups, ensure_ascii=False, separators=(",", ":")))
    io.open(os.path.join(OUT, cfg["file"]), "w", encoding="utf-8").write(html)
    built.append((cfg["file"], len(items), len(groups), len(html) // 1024))

for f, n, g, k in built:
    print("%-20s items=%-4d groups=%-3d %dKB" % (f, n, g, k))
print("TOTAL:", sum(x[1] for x in built))
