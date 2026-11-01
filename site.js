/* ============================================================
   CliniPD — shared site script
   ------------------------------------------------------------
   SITE below is the SINGLE SOURCE OF TRUTH for navigation.
   To add a page to the whole site:
     1. create the .html file
     2. add one line to SITE.nav
   The top bar, the dropdowns, the mobile drawer and the footer
   all rebuild themselves from it. Never hand-edit nav markup
   inside a page.
   ============================================================ */

/* Every href below is its OWN page. Nothing in a dropdown is a same-page
   anchor — clicking a menu item always takes you somewhere new. */
const SITE = {
  nav: [
    {
      label: "Library",
      href: "library.html",
      menu: [
        { h: "Reference" },
        { t: "The library", d: "All nine sections, searched in one box", href: "library.html", i: "LIB", free: true },
        { t: "Conditions", d: "416 presentations across eight domains", href: "conditions.html", i: "CON", free: true },
        { t: "Special tests", d: "134 tests with sensitivity and specificity", href: "tests.html", i: "TST", free: true },
        { t: "Outcome measures", d: "99 measures, each with MCID and MDC", href: "measures.html", i: "OM", free: true },
        { t: "Exercises", d: "106 exercises with real sets, reps and load", href: "exercises.html", i: "EX", free: true },
        { sep: true },
        { h: "Browse by domain" },
        { t: "By body region & domain", d: "Musculoskeletal, neuro, cardioresp and five more", href: "domains.html", i: "DOM", free: true },
        { t: "Glossary", d: "151 terms — the words underlined site-wide", href: "glossary.html", i: "A-Z", free: true },
        { sep: true },
        { t: "Clinical calculators", d: "Post-test probability, MCID, 1RM, OSCE timer", href: "app.html", i: "CLC", free: true }
      ]
    },
    {
      label: "Learn",
      href: "cases.html",
      menu: [
        { h: "Practise" },
        { t: "Clinical cases", d: "22 cases worked end to end", href: "cases.html", i: "CS", free: true },
        { t: "OSCE stations", d: "28 stations with marking criteria", href: "osce.html", i: "OSC", free: true },
        { t: "Question bank", d: "Exam-style MCQs with worked reasoning", href: "qbank.html", i: "Q", pro: true },
        { sep: true },
        { h: "Plan & track" },
        { t: "Study plans", d: "Build a plan to your exam date, week by week", href: "studyplan.html", i: "PLN", free: true },
        { t: "Saved pages", d: "Your reading list", href: "collections.html", i: "SAV", free: true },
        { t: "Progress", d: "What you've read, and what you've been avoiding", href: "progress.html", i: "PRG", pro: true },
        { sep: true },
        { h: "Background & prep" },
        { t: "Foundations", d: "86 topics — anatomy, physiology, pathology, reasoning", href: "foundations.html", i: "FND", free: true },
        { t: "Placement", d: "26 pages of setting prep and the practical toolkit", href: "placement.html", i: "PLC", free: true },
        { t: "Video library", d: "Technique, assessment and exercise demos", href: "videos.html", i: "VID", free: true },
        { t: "Anki export", d: "Turn any page into a spaced-repetition deck", href: "anki.html", i: "AN", free: true }
      ]
    },
    {
      label: "Research & CPD",
      href: "research.html",
      menu: [
        { h: "Stay current" },
        { t: "Research feed", d: "New papers in your domains, as they publish", href: "research.html", i: "RF", pro: true },
        { t: "Professional development", d: "Log CPD hours, export an audit-ready record", href: "cpd.html", i: "PD", pro: true },
        { sep: true },
        { t: "Our evidence standard", d: "What we cite, and how claims are traced", href: "evidence.html", i: "STD", free: true }
      ]
    },
    {
      label: "Contribute",
      href: "upload.html",
      menu: [
        { h: "For the profession" },
        { t: "Submit content", d: "Share a resource — reviewed before it goes live", href: "upload.html", i: "UP", free: true },
        { t: "For universities", d: "Cohort pages mapped to your unit outlines", href: "universities.html", i: "UNI", free: true },
        { t: "For clinics", d: "Team accounts and shared CPD reporting", href: "clinics.html", i: "TM", free: true }
      ]
    },
    { label: "Pricing", href: "pricing.html" }
  ],
  foot: [
    { h: "Reference", links: [["Conditions", "conditions.html"], ["Special tests", "tests.html"], ["Outcome measures", "measures.html"], ["Exercises", "exercises.html"], ["By domain", "domains.html"], ["Glossary", "glossary.html"]] },
    { h: "Learn", links: [["Clinical cases", "cases.html"], ["OSCE stations", "osce.html"], ["Question bank", "qbank.html"], ["Study plans", "studyplan.html"], ["Foundations", "foundations.html"], ["Placement", "placement.html"]] },
    { h: "Professional", links: [["Research feed", "research.html"], ["CPD logging", "cpd.html"], ["Evidence standard", "evidence.html"], ["Submit content", "upload.html"]] },
    { h: "Account", links: [["Saved pages", "collections.html"], ["Progress", "progress.html"], ["Pricing", "pricing.html"], ["Log in", "login.html"], ["For universities", "universities.html"], ["For clinics", "clinics.html"]] }
  ]
};

/* ============================================================
   DESIGN STUDIO — colour schemes + font sets
   Choices live in localStorage and are applied before first
   paint by the inline snippet in each page's <head>.
   ============================================================ */
const SCHEMES = [
  { id:"", name:"Clinical", note:"Teal \u00b7 the default", sw:["#0A7E70", "#DB3114", "#0C2F2B", "#A9D4CF"] },
  { id:"slate", name:"Slate", note:"Cool, institutional", sw:["#2563A8", "#D1462E", "#16222E", "#DDE1E4"] },
  { id:"warm", name:"Warm", note:"Paper and ink", sw:["#8A5A2B", "#B8452F", "#2A2318", "#D5D5D5"] },
  { id:"contrast", name:"Contrast", note:"Maximum legibility", sw:["#00563F", "#B3200E", "#000000", "#7AD0B9"] },
  { id:"indigo", name:"Indigo", note:"Deep blue-violet", sw:["#4A4FB5", "#D63E23", "#1B1C38", "#FAFAFA"] },
  { id:"forest", name:"Forest", note:"Dark green, natural", sw:["#2F6B41", "#AE5E28", "#17251B", "#C7C7C7"] },
  { id:"plum", name:"Plum", note:"Purple, editorial", sw:["#6D3B8E", "#CE3D68", "#241530", "#DFDFDF"] },
  { id:"crimson", name:"Crimson", note:"Red, high energy", sw:["#A8323C", "#1F6F7A", "#2B1416", "#E8E7E7"] },
  { id:"ocean", name:"Ocean", note:"Cyan and navy", sw:["#0E6E8C", "#BA581E", "#0E2430", "#B7D0D8"] },
  { id:"graphite", name:"Graphite", note:"Neutral, one accent", sw:["#44505C", "#C14E2D", "#1A1E22", "#CACACA"] }
];

const FONTS = [
  { id:"",            name:"Outfit / Figtree",            note:"Geometric · the default",
    css:"Outfit:wght@300;400;500;600;700&family=Figtree:wght@400;500;600;700" },
  { id:"jakarta",     name:"Plus Jakarta Sans",           note:"Modern, single family",
    css:"Plus+Jakarta+Sans:wght@300;400;500;600;700;800" },
  { id:"fraunces",    name:"Fraunces / Inter",            note:"Editorial serif display",
    css:"Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700" },
  { id:"grotesk",     name:"Space Grotesk / Inter",       note:"Technical, precise",
    css:"Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700" },
  { id:"baskerville", name:"Libre Baskerville / Source",  note:"Academic, journal-like",
    css:"Libre+Baskerville:wght@400;700&family=Source+Sans+3:wght@400;500;600;700" },
  { id:"dm",          name:"DM Serif / DM Sans",          note:"Classic editorial",
    css:"DM+Serif+Display&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700" }
];

const SCHEME_KEY = "clinipd:scheme";
const FONT_KEY   = "clinipd:font";
const MODE_KEY   = "clinipd:mode";

function getScheme(){ try{ return localStorage.getItem(SCHEME_KEY) || ""; }catch(e){ return ""; } }
function getFont(){   try{ return localStorage.getItem(FONT_KEY)   || ""; }catch(e){ return ""; } }
function getMode(){   try{ return localStorage.getItem(MODE_KEY)   || ""; }catch(e){ return ""; } }

/* pull in only the family files the chosen set needs */
function loadFont(id){
  const f = FONTS.find(x => x.id === id);
  if (!f) return;
  const href = "https://fonts.googleapis.com/css2?family=" + f.css + "&display=swap";
  if (document.querySelector('link[data-font-set="' + id + '"]')) return;
  const l = document.createElement("link");
  l.rel = "stylesheet"; l.href = href; l.setAttribute("data-font-set", id);
  document.head.appendChild(l);
}

function animateSwap(){
  const root = document.documentElement;
  if (window.matchMedia("(prefers-reduced-motion:reduce)").matches) return;
  root.classList.add("scheme-anim");
  clearTimeout(animateSwap._t);
  animateSwap._t = setTimeout(() => root.classList.remove("scheme-anim"), 480);
}

function setScheme(id, animate){
  const root = document.documentElement;
  if (animate) animateSwap();
  if (id) root.setAttribute("data-scheme", id); else root.removeAttribute("data-scheme");
  try{ localStorage.setItem(SCHEME_KEY, id); }catch(e){}
  $$("#dsCols .ds-col").forEach(b => b.setAttribute("aria-checked", String(b.dataset.scheme === id)));
}

function setFont(id, animate){
  const root = document.documentElement;
  if (animate) animateSwap();
  loadFont(id);
  if (id) root.setAttribute("data-font", id); else root.removeAttribute("data-font");
  try{ localStorage.setItem(FONT_KEY, id); }catch(e){}
  $$("#dsFonts .ds-font").forEach(b => b.setAttribute("aria-checked", String(b.dataset.font === id)));
}

function setMode(m){
  const root = document.documentElement;
  animateSwap();
  if (m) root.setAttribute("data-theme", m); else root.removeAttribute("data-theme");
  try{ localStorage.setItem(MODE_KEY, m); }catch(e){}
  $$("#dsMode button").forEach(b => b.setAttribute("aria-checked", String(b.dataset.mode === m)));
}

const X_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';

function buildStudio(){
  if (document.getElementById("dsPanel")) return;

  const scrim = document.createElement("div");
  scrim.className = "ds-scrim"; scrim.id = "dsScrim";

  const p = document.createElement("aside");
  p.className = "ds"; p.id = "dsPanel";
  p.setAttribute("aria-label", "Design studio"); p.setAttribute("aria-hidden", "true");

  const cols = SCHEMES.map(s =>
    `<button type="button" class="ds-col" role="radio" data-scheme="${s.id}" aria-checked="false">
       <span class="ds-sw"><i style="background:${s.sw[0]}"></i><i style="background:${s.sw[1]}"></i>` +
    `<i style="background:${s.sw[2]}"></i><i style="background:${s.sw[3]}"></i></span>
       <span style="min-width:0"><b>${esc(s.name)}</b><span>${esc(s.note)}</span></span>
     </button>`).join("");

  const fonts = FONTS.map(f =>
    `<button type="button" class="ds-font" role="radio" data-font="${f.id}" aria-checked="false">
       <span class="fd">Patellofemoral pain</span>
       <span class="fb">A clinical diagnosis of pattern plus exclusion.</span>
       <span class="fn">${esc(f.name)} · ${esc(f.note)}</span>
     </button>`).join("");

  p.innerHTML = `
    <div class="ds-head">
      <div style="flex:1;min-width:0">
        <h2>Design studio</h2>
        <p>Try a look. Only you see this.</p>
      </div>
      <button class="ds-x" id="dsClose" aria-label="Close">${X_SVG}</button>
    </div>
    <div class="ds-body">
      <div class="ds-sec">
        <h3>Appearance</h3>
        <div class="ds-seg" id="dsMode" role="radiogroup" aria-label="Appearance">
          <button type="button" role="radio" data-mode="" aria-checked="true">System</button>
          <button type="button" role="radio" data-mode="light" aria-checked="false">Light</button>
          <button type="button" role="radio" data-mode="dark" aria-checked="false">Dark</button>
        </div>
      </div>
      <div class="ds-sec">
        <h3>Colour · ${SCHEMES.length} options</h3>
        <div class="ds-cols" id="dsCols" role="radiogroup" aria-label="Colour scheme">${cols}</div>
      </div>
      <div class="ds-sec">
        <h3>Type · ${FONTS.length} options</h3>
        <div class="ds-fonts" id="dsFonts" role="radiogroup" aria-label="Font set">${fonts}</div>
      </div>
    </div>
    <div class="ds-foot">
      <button class="btn" type="button" id="dsReset">Reset</button>
      <button class="btn pri" type="button" id="dsCopy">Copy my choice</button>
    </div>
    <p class="ds-note">Choices are saved in this browser only — they don't change the site for anyone else. Paste your copied choice into the chat and I'll make it the permanent default.</p>`;

  document.body.appendChild(scrim);
  document.body.appendChild(p);

  /* each font button previews in its own face, once that face has loaded */
  FONTS.forEach(f => {
    const btn = p.querySelector('.ds-font[data-font="' + f.id + '"]');
    if (!btn) return;
    const fam = f.name.split(" / ")[0];
    const generic = /Fraunces|Baskerville|DM Serif/.test(fam) ? "Georgia, serif" : "system-ui, sans-serif";
    btn.querySelector(".fd").style.fontFamily = '"' + fam + '", ' + generic;
    btn.addEventListener("mouseenter", () => loadFont(f.id), { once: true });
  });

  const open = () => {
    p.classList.add("on"); scrim.classList.add("on");
    p.setAttribute("aria-hidden", "false");
    FONTS.forEach(f => loadFont(f.id));           /* so the previews render */
    document.body.style.overflow = "hidden";
  };
  const close = () => {
    p.classList.remove("on"); scrim.classList.remove("on");
    p.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  };

  $("#dsOpen") && $("#dsOpen").addEventListener("click", e => { e.stopPropagation(); open(); });
  $("#dsClose").addEventListener("click", close);
  scrim.addEventListener("click", close);
  document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });

  $("#dsCols").addEventListener("click", e => {
    const b = e.target.closest("button[data-scheme]"); if (b) setScheme(b.dataset.scheme, true);
  });
  $("#dsFonts").addEventListener("click", e => {
    const b = e.target.closest("button[data-font]"); if (b) setFont(b.dataset.font, true);
  });
  $("#dsMode").addEventListener("click", e => {
    const b = e.target.closest("button[data-mode]"); if (b) setMode(b.dataset.mode);
  });
  $("#dsReset").addEventListener("click", () => {
    setScheme("", true); setFont("", true); setMode("");
  });
  $("#dsCopy").addEventListener("click", async () => {
    const s = SCHEMES.find(x => x.id === getScheme()) || SCHEMES[0];
    const f = FONTS.find(x => x.id === getFont()) || FONTS[0];
    const m = getMode() || "system";
    const txt = `CliniPD design: colour "${s.name}", type "${f.name}", appearance ${m}.`;
    try{ await navigator.clipboard.writeText(txt); }catch(e){}
    const btn = $("#dsCopy"), was = btn.textContent;
    btn.textContent = "Copied"; btn.classList.add("ds-copied");
    setTimeout(() => { btn.textContent = was; btn.classList.remove("ds-copied"); }, 1600);
  });

  /* reflect what is already stored */
  setScheme(getScheme(), false);
  setFont(getFont(), false);
  setMode(getMode());
}

/* ---------- helpers ---------- */
const $  = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const CHEV = '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

/* current file name, so the active page highlights itself */
const HERE = (location.pathname.split("/").pop() || "index.html").toLowerCase();

/* Article pages live in /p/, so every nav link needs stepping back up.
   BASE is "" at the site root and "../" one level down. */
const BASE = (function () {
  const parts = location.pathname.split("/").filter(Boolean);
  parts.pop();                                   /* drop the filename */
  return parts.length && parts[parts.length - 1] === "p" ? "../" : "";
})();
const url = h => (/^(https?:|mailto:|#|\/)/.test(h) ? h : BASE + h);

/* ---------- build the top bar ---------- */
function buildNav() {
  const host = $("#site-top");
  if (!host) return;

  const navHtml = SITE.nav.map((n, i) => {
    if (!n.menu) {
      const on = n.href.toLowerCase() === HERE ? " on" : "";
      return `<div class="nav-item"><a class="nav-a${on}" href="${url(n.href)}">${esc(n.label)}</a></div>`;
    }
    const items = n.menu.map(m => {
      if (m.sep) return '<div class="menu-sep"></div>';
      if (m.h) return `<div class="menu-h">${esc(m.h)}</div>`;
      const lock = m.pro ? '<span class="lock">PRO</span>' : "";
      return `<a href="${url(m.href)}"><span class="mi">${esc(m.i)}</span>`
        + `<span style="min-width:0"><b>${esc(m.t)}</b><span>${esc(m.d)}</span></span>${lock}</a>`;
    }).join("");
    const on = n.menu.some(m => m.href && m.href.split("#")[0].toLowerCase() === HERE) ? " on" : "";
    return `<div class="nav-item">
      <button class="nav-a${on}" aria-expanded="false" aria-controls="menu-${i}">${esc(n.label)}${CHEV}</button>
      <div class="menu" id="menu-${i}" role="group">${items}</div>
    </div>`;
  }).join("");

  host.innerHTML = `<div class="top-in">
    <a class="brand" href="${url('index.html')}" aria-label="CliniPD — clinical reference for physiotherapists">
      <span class="brand-mk">C</span>
      <span class="brand-wm">
        <span class="brand-tx">Clini<em>PD</em></span>
        <span class="brand-for">for physios</span>
      </span>
    </a>
    <nav class="nav" aria-label="Main">${navHtml}</nav>
    <div class="top-r">
      <button class="ds-open" id="dsOpen" aria-label="Design studio" title="Design studio">
        <span class="ds-dot"></span>
      </button>
      <a class="btn ghost" href="${url('login.html')}">Log in</a>
      <a class="btn pri" href="${url('pricing.html#trial')}">Start free</a>
      <button class="burger" aria-label="Menu" aria-expanded="false"><span></span></button>
    </div>
  </div>
  <div class="prog" id="prog" aria-hidden="true"></div>`;

  buildStudio();

  /* dropdowns — click to open, hover to open, click-away / Escape to close.
     A close is DELAYED and cancellable, so moving the mouse from the button
     down into the menu (across the gap) never shuts it. */
  let closeTimer = null;
  const cancelClose = () => { if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; } };
  const closeNow = () => {
    cancelClose();
    $$(".menu.open").forEach(m => m.classList.remove("open"));
    $$('.nav-a[aria-expanded="true"]').forEach(b => b.setAttribute("aria-expanded", "false"));
  };
  const closeSoon = () => { cancelClose(); closeTimer = setTimeout(closeNow, 220); };
  const openOne = (btn, menu) => {
    cancelClose();
    $$(".menu.open").forEach(m => { if (m !== menu) m.classList.remove("open"); });
    $$('.nav-a[aria-expanded="true"]').forEach(b => { if (b !== btn) b.setAttribute("aria-expanded", "false"); });
    menu.classList.add("open");
    btn.setAttribute("aria-expanded", "true");
  };

  $$(".nav-a[aria-controls]").forEach(btn => {
    const menu = $("#" + btn.getAttribute("aria-controls"));
    const item = btn.parentElement;
    const canHover = () => window.matchMedia("(hover:hover)").matches;

    btn.addEventListener("click", e => {
      e.stopPropagation();
      if (menu.classList.contains("open")) closeNow(); else openOne(btn, menu);
    });
    item.addEventListener("mouseenter", () => { if (canHover()) openOne(btn, menu); });
    item.addEventListener("mouseleave", () => { if (canHover()) closeSoon(); });
    /* keep it open while the pointer is anywhere inside the menu itself */
    menu.addEventListener("mouseenter", cancelClose);
    menu.addEventListener("mouseleave", () => { if (canHover()) closeSoon(); });
    /* and while tabbing through its links */
    menu.addEventListener("focusin", cancelClose);
    menu.addEventListener("focusout", e => {
      if (!menu.contains(e.relatedTarget) && e.relatedTarget !== btn) closeSoon();
    });
  });
  document.addEventListener("click", closeNow);
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeNow(); });

  /* mobile drawer */
  const drawer = document.createElement("div");
  drawer.className = "drawer";
  drawer.innerHTML = SITE.nav.map(n => {
    if (!n.menu) return `<a href="${url(n.href)}">${esc(n.label)}</a>`;
    return `<h4>${esc(n.label)}</h4>` + n.menu
      .filter(m => !m.sep && !m.h)
      .map(m => `<a href="${url(m.href)}">${esc(m.t)}${m.pro ? '<span class="lock">PRO</span>' : ""}</a>`)
      .join("");
  }).join("") + `<h4>Account</h4><a href="${url('login.html')}">Log in</a><a href="${url('pricing.html#trial')}">Start free trial</a>`;
  document.body.appendChild(drawer);

  const burger = $(".burger", host);
  burger.addEventListener("click", e => {
    e.stopPropagation();
    const open = drawer.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open ? "hidden" : "";
  });

  /* shadow on scroll */
  const onScroll = () => host.classList.toggle("stuck", window.scrollY > 6);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ---------- build the footer ---------- */
function buildFoot() {
  const host = $("#site-foot");
  if (!host) return;
  const cols = SITE.foot.map(c =>
    `<div><h5>${esc(c.h)}</h5>${c.links.map(l => `<a href="${url(l[1])}">${esc(l[0])}</a>`).join("")}</div>`
  ).join("");
  host.innerHTML = `<div class="wrap">
    <div class="foot-g">
      <div>
        <a class="brand" href="${url('index.html')}" style="margin-bottom:12px">
          <span class="brand-mk">C</span>
          <span class="brand-wm">
            <span class="brand-tx">Clini<em>PD</em></span>
            <span class="brand-for">for physios</span>
          </span>
        </a>
        <p style="font-size:14px;line-height:1.62;color:#9FC4BD;max-width:32ch;margin-top:12px">
          Clinical physiotherapy development — a reference library written for physiotherapists and physiotherapy students. Every page referenced, dated, and reviewed on a two-year cycle.
        </p>
        <h5 style="margin-top:28px">Get the research digest</h5>
        <form class="news" onsubmit="event.preventDefault();this.innerHTML='<p style=&quot;font-size:14px;color:#9FC4BD&quot;>Thanks — list isn\\'t live yet, but you\\'re noted.</p>';">
          <input type="email" required placeholder="Email address" aria-label="Email address">
          <button type="submit" aria-label="Subscribe">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13m0 0-5-5m5 5-5 5"/></svg>
          </button>
        </form>
      </div>${cols}
    </div>
    <div class="foot-b">
      <span>© ${new Date().getFullYear()} CliniPD · Perth, Western Australia</span>
      <span>Educational resource for registered practitioners. Not a substitute for clinical judgement.</span>
    </div>
  </div>`;
}

/* ---------- scroll reveal ---------- */
function reveal() {
  const els = $$("[data-rev]");
  if (!els.length) return;
  if (!("IntersectionObserver" in window) ||
      window.matchMedia("(prefers-reduced-motion:reduce)").matches) {
    els.forEach(e => e.classList.add("in"));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      const d = parseInt(en.target.getAttribute("data-rev") || "0", 10) || 0;
      setTimeout(() => en.target.classList.add("in"), d);
      io.unobserve(en.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
  els.forEach(e => io.observe(e));
}

/* ---------- count-up numbers ----------
   Markup:  <b data-count="1063">0</b>
            <b data-count="30000000" data-fmt="compact">0</b>   → 30M
            <b data-count="99" data-suffix="%">0</b>
            <b data-count="2.4" data-dp="1">0</b>
   Add data-dur="1800" to slow one down.
-------------------------------------------------------------- */
function counters() {
  const els = $$("[data-count]");
  if (!els.length) return;
  const reduce = window.matchMedia("(prefers-reduced-motion:reduce)").matches;

  const fmt = (v, el) => {
    const dp = parseInt(el.getAttribute("data-dp") || "0", 10);
    const pre = el.getAttribute("data-prefix") || "";
    const suf = el.getAttribute("data-suffix") || "";
    let out;
    if (el.getAttribute("data-fmt") === "compact") {
      if (v >= 1e9)      out = (v / 1e9).toFixed(v >= 1e10 ? 0 : 1).replace(/\.0$/, "") + "B";
      else if (v >= 1e6) out = (v / 1e6).toFixed(v >= 1e7 ? 0 : 1).replace(/\.0$/, "") + "M";
      else if (v >= 1e3) out = (v / 1e3).toFixed(v >= 1e4 ? 0 : 1).replace(/\.0$/, "") + "K";
      else               out = String(Math.round(v));
    } else {
      out = dp > 0 ? v.toFixed(dp) : Math.round(v).toLocaleString();
    }
    return pre + out + suf;
  };

  const run = el => {
    const to = parseFloat(el.getAttribute("data-count"));
    if (!isFinite(to)) return;
    if (reduce) { el.textContent = fmt(to, el); return; }
    const dur = parseInt(el.getAttribute("data-dur") || "1750", 10);
    const t0 = performance.now();
    el.classList.add("counting");
    const step = now => {
      const p = Math.min(1, (now - t0) / dur);
      /* easeOutExpo — fast off the mark, long graceful settle */
      const e = p === 1 ? 1 : 1 - Math.pow(2, -10 * p);
      el.textContent = fmt(to * e, el);
      if (p < 1) requestAnimationFrame(step);
      else { el.textContent = fmt(to, el); el.classList.remove("counting"); el.classList.add("counted"); }
    };
    requestAnimationFrame(step);
  };

  if (!("IntersectionObserver" in window)) { els.forEach(run); return; }
  const io = new IntersectionObserver(es => {
    es.forEach(en => {
      if (!en.isIntersecting) return;
      /* stagger siblings so a row of four cascades rather than firing as one */
      const row = Array.from(en.target.closest(".stats") ? $$("[data-count]", en.target.closest(".stats")) : [en.target]);
      const i = Math.max(0, row.indexOf(en.target));
      setTimeout(() => run(en.target), i * 110);
      io.unobserve(en.target);
    });
  }, { threshold: 0.45 });
  els.forEach(e => io.observe(e));
}

/* ---------- scroll-fade photo bands ----------
   As a [data-band] section crosses the viewport its progress runs
   0 → 1. The photo fades up and settles from a slight zoom; the
   text follows a beat later, holds through the middle, then both
   fade away again. Pure transform/opacity, rAF-throttled.
-------------------------------------------------------------- */
function bands() {
  const els = $$("[data-band]");
  if (!els.length) return;
  if (window.matchMedia("(prefers-reduced-motion:reduce)").matches) return;

  let ticking = false;
  const clamp = v => Math.min(1, Math.max(0, v));
  /* ramps up over the first third, holds, ramps down over the last third */
  const envelope = p => {
    if (p < 0.34) return clamp(p / 0.30);
    if (p > 0.70) return clamp((1 - p) / 0.26);
    return 1;
  };

  const paint = () => {
    ticking = false;
    const vh = window.innerHeight;
    els.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      /* 0 when the section's top hits the bottom of the screen,
         1 when its bottom leaves the top */
      const p = clamp((vh - r.top) / (vh + r.height));
      const tx = el.querySelector(".band-tx");
      const e = envelope(p);
      /* set on the section so the image AND the ::after wash both read it */
      el.style.setProperty("--img-o", (0.18 + e * 0.82).toFixed(3));
      el.style.setProperty("--img-s", (1.10 - e * 0.10).toFixed(4));
      if (tx) {
        /* text trails the image slightly */
        const te = envelope(clamp(p - 0.05));
        tx.style.setProperty("--tx-o", te.toFixed(3));
        tx.style.setProperty("--tx-y", ((1 - te) * 26).toFixed(1) + "px");
      }
    });
  };

  window.addEventListener("scroll", () => {
    if (!ticking) { ticking = true; requestAnimationFrame(paint); }
  }, { passive: true });
  window.addEventListener("resize", paint);
  paint();
}

/* ---------- reading progress ----------
   A hairline that fills along the BOTTOM edge of the sticky header,
   rather than a separate bar fixed over the top of it. On a long
   article page it is the only honest answer to "how much is left".
-------------------------------------------------------------- */
function progress() {
  const bar = $("#prog");
  if (!bar) return;
  let ticking = false;
  const paint = () => {
    ticking = false;
    const doc = document.documentElement;
    const max = doc.scrollHeight - window.innerHeight;
    const p = max > 120 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
    bar.parentElement.classList.toggle("has-prog", p > 0.004);
  };
  window.addEventListener("scroll", () => {
    if (!ticking) { ticking = true; requestAnimationFrame(paint); }
  }, { passive: true });
  window.addEventListener("resize", paint);
  paint();
}

/* ---------- hero parallax ----------
   The hero photo drifts at roughly a third of page speed. Small
   enough that nobody names it, large enough that the panel stops
   feeling like a flat sticker.
-------------------------------------------------------------- */
function heroDrift() {
  const panel = $(".hero-panel");
  if (!panel) return;
  const img = panel.querySelector("img");
  if (!img || window.matchMedia("(prefers-reduced-motion:reduce)").matches) return;

  img.style.willChange = "transform";
  let ticking = false;
  const paint = () => {
    ticking = false;
    const r = panel.getBoundingClientRect();
    if (r.bottom < -100 || r.top > window.innerHeight + 100) return;
    /* -0.5 above the fold → +0.5 well below it */
    const p = (window.innerHeight - r.top) / (window.innerHeight + r.height) - 0.5;
    img.style.transform = "scale(1.13) translate3d(0," + (p * 7.5).toFixed(2) + "%,0)";
  };
  window.addEventListener("scroll", () => {
    if (!ticking) { ticking = true; requestAnimationFrame(paint); }
  }, { passive: true });
  window.addEventListener("resize", paint);
  paint();
}

/* ---------- live article content ----------
   An article page under /p/ ships as a skeleton of "Not written
   yet" fields. If content/<page-id>.json exists, this swaps the
   written prose in: sections, references, citation links and the
   status chips. If it does not exist, the page is left exactly as
   it is — an honest empty page, not a broken one.
-------------------------------------------------------------- */
async function articleContent() {
  const tag = $(".pid code");
  if (!tag) return;                       /* not an article page */
  const id = tag.textContent.trim();
  if (!id) return;

  let data;
  try {
    const r = await fetch(BASE + "content/" + id + ".json", { cache: "no-cache" });
    if (!r.ok) return;                    /* nothing written yet */
    data = await r.json();
  } catch (e) { return; }                 /* offline or file:// — leave the skeleton */
  if (!data || !data.sections) return;

  const refs = Array.isArray(data.refs) ? data.refs : [];

  /* --- 1. the sections ------------------------------------- */
  let filled = 0, missing = [];
  $$("section.sec-a").forEach(sec => {
    const h = sec.querySelector("h2");
    const body = sec.querySelector(".flds");
    if (!h || !body) return;
    const clone = h.cloneNode(true);
    const n = clone.querySelector(".sn");
    if (n) n.remove();
    const name = clone.textContent.trim();
    const html = data.sections[name];
    if (html == null || !String(html).trim()) { missing.push(name); return; }

    const live = document.createElement("div");
    live.className = "fld-live";
    live.innerHTML = String(html);
    body.replaceWith(live);
    filled++;
  });
  if (!filled) return;

  /* --- 2. citation superscripts become links ---------------- */
  if (refs.length) {
    $$(".fld-live sup").forEach(sup => {
      const raw = sup.textContent.trim();
      if (!/^[\d\s,]+$/.test(raw)) return;
      sup.innerHTML = raw.split(",").map(s => s.trim()).filter(Boolean).map(nStr => {
        const n = parseInt(nStr, 10);
        if (!(n >= 1 && n <= refs.length)) return esc(nStr);
        return `<a href="#ref${n}" title="Jump to reference ${n}">${n}</a>`;
      }).join("");
    });
  }

  /* --- 3. unverified figures stay visible ------------------- */
  $$(".fld-live").forEach(el => {
    el.innerHTML = el.innerHTML.replace(
      /\[verify([^\]]*)\]/gi,
      (m, rest) => `<mark class="verify" title="Unverified — check the source${esc(rest)}">verify${esc(rest)}</mark>`
    );
  });

  /* --- 4. the reference list -------------------------------- */
  const rsec = $("section.refs");
  if (rsec && refs.length) {
    const rows = refs.map((r, i) => {
      const doi = (r.doi || "").trim().replace(/^https?:\/\/(dx\.)?doi\.org\//i, "");
      const bits = [r.design, r.level, r.licence].filter(Boolean)
        .map(b => `<em>${esc(b)}</em>`).join("");
      const link = doi
        ? `<a class="open" href="https://doi.org/${encodeURI(doi)}" target="_blank" rel="noopener noreferrer">doi:${esc(doi)} &nearr;</a>`
        : `<em class="open" style="color:var(--coral);border-color:var(--coral)">No DOI</em>`;
      return `<li id="ref${i + 1}"><span class="rc">${esc(r.cite || "")}</span>`
        + `<span class="rm">${bits}${link}</span></li>`;
    }).join("");
    rsec.innerHTML = `<h2>References</h2><ol class="reflist">${rows}</ol>`;
  }

  /* --- 5. the status chips ---------------------------------- */
  const chips = $(".chips");
  if (chips) {
    /* A citation's page range ("29:2039-2045") looks exactly like a year,
       so cap at next year and ignore anything implausible. */
    const CAP = new Date().getFullYear() + 1;
    const years = refs.map(r => {
      const m = String(r.cite || "").match(/\b(19|20)\d{2}\b/g) || [];
      const ok = m.map(Number).filter(y => y >= 1900 && y <= CAP);
      return ok.length ? Math.max(...ok) : 0;
    });
    const newest = years.length ? Math.max(...years) : 0;
    const stale = newest && (new Date().getFullYear() - newest) > 7;

    const empty = chips.querySelector(".chip.empty");
    if (empty) {
      empty.classList.remove("empty");
      empty.textContent = missing.length ? `${filled} of 16 sections written` : "Written · unverified";
    }
    chips.querySelectorAll(".chip").forEach(c => {
      if (/^\d+ references?$/.test(c.textContent.trim()))
        c.textContent = refs.length === 1 ? "1 reference" : `${refs.length} references`;
    });
    if (newest) {
      const c = document.createElement("span");
      c.className = "chip" + (stale ? " warn" : "");
      c.textContent = stale ? `Newest source ${newest} · ageing` : `Newest source ${newest}`;
      chips.appendChild(c);
    }
    const nv = $$(".fld-live mark.verify").length;
    if (nv) {
      const c = document.createElement("span");
      c.className = "chip warn";
      c.textContent = nv === 1 ? "1 figure to verify" : `${nv} figures to verify`;
      chips.appendChild(c);
    }
  }

  /* --- 6. hover glossary over the new prose ----------------- */
  if (window.glossInit) $$(".fld-live").forEach(el => glossInit(el));
}

/* ---------- clinical pathway rail ------------------------- */
function clinicalPathway() {
  const wrap = document.querySelector(".art-wrap");
  if (!wrap || wrap.querySelector(".pathway-rail")) return;

  const rail = document.createElement("div");
  rail.className = "pathway-rail";
  rail.setAttribute("aria-label", "Physiotherapy clinical pathway");
  rail.innerHTML = `
    <span class="pathway-kicker">Physiotherapy clinical pathway</span>
    <ol>
      <li><b>01</b><span>Understand</span></li>
      <li><b>02</b><span>Assess</span></li>
      <li><b>03</b><span>Investigate</span></li>
      <li><b>04</b><span>Manage</span></li>
      <li><b>05</b><span>Rehabilitate</span></li>
      <li><b>06</b><span>Reason</span></li>
    </ol>`;
  wrap.insertBefore(rail, wrap.firstElementChild);
}

/* ---------- boot ---------- */
document.addEventListener("DOMContentLoaded", () => {
  buildNav();
  buildFoot();
  reveal();
  counters();
  bands();
  progress();
  heroDrift();
  articleContent();
  clinicalPathway();
});
