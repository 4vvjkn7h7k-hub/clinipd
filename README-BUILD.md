# CliniPD — how to build on this shell

Everything you need to extend the site without breaking it. Read this before editing.

---

## 1. What the files are

```
index.html        home page
library.html      THE LIBRARY HUB — search all 927 pages, section cards, groups
app.html          the old split-pane reference app, kept as the workspace
                  (calculators, Anki builder, case sim, OSCE timer; own CSS)

  Domain pages — one per dropdown item, generated from the library's own tree:
msk.html (161)    neuro.html (38)   cardio.html (36)   geri.html (22)
sports.html (40)  paeds.html (30)   pelvic.html (26)   pain.html (42)

  Section pages:
cases.html        questions.html    videos.html        anki.html
research.html     cpd.html          evidence.html
universities.html clinics.html      upload.html
pricing.html      login.html

conditions.html   all 416 conditions, live search + domain filters
glossary.html     all 151 glossary terms, searchable

site.css          ← ALL shared styling + the 10 colour schemes
listing.css       ← the A–Z listing skeleton, shared by the nine index
                    pages AND library.html (was duplicated nine times)
site.js           ← shared nav, footer, scroll reveal, counters, scheme switcher
glossary.js       ← the term bank + hover-tooltip engine

img/              pictures (swap these freely — see §4)
content/
  index.json      manifest: status, section count, refs, newest source, review date
  <page-id>.json  one file per written article, loaded on demand
```

---

## 2. The three rules

### Rule 1 — `SITE.nav` in `site.js` is the only place navigation exists
The top bar, every dropdown, the mobile drawer and the footer all build themselves
from that one object.

**Every dropdown item points at its own page.** Nothing in a menu is a same-page anchor —
clicking always takes you somewhere new. Keep it that way.

**To add a page to the whole site:**
1. Create `newpage.html` (copy any existing section page)
2. Add one line to `SITE.nav` in `site.js`

```js
{ t: "New thing", d: "One line describing it", href: "newpage.html", i: "NEW", pro: true }
```
`i` = the 2–3 letter chip. `pro: true` adds the PRO badge. `free: true` is the default.

**Never hand-edit nav markup inside a page.** It is generated.

### Rule 2 — all shared styling lives in `site.css`
Change a token at the top of `site.css` and all eleven pages change:

```css
--brand:#0B8C7D;    /* every teal button, link and accent */
--coral:#F0674F;    /* every PRO badge and secondary CTA */
--deep:#0A2E2B;     /* footer and hero panel */
--gap:clamp(76px,9vw,128px);   /* vertical space between sections */
--r-xl:30px;        /* corner roundness */
```

Page-specific CSS goes in that page's own `<style>` block. Never in `site.css`.

### Rule 3 — don't reuse a global class name as a page-level one
`site.css` styles 42 generic class names (`.card`, `.btn`, `.foot`, `.pill`, `.big`…).
If you write `.mysection .foot { }` in a page, it will **inherit the global `.foot`**
(which is the dark site footer) and you will get a mysterious dark box.

This bit me twice building this. Prefix page-level names: `.cfoot`, `.mnum`, not `.foot`, `.big`.

---

## 3. The animations, and how to use them

### Count-up numbers
```html
<b data-count="1063">0</b>                          → 1,063
<b data-count="30000000" data-fmt="compact">0</b>   → 30M
<b data-count="95" data-suffix="%">0</b>            → 95%
<b data-count="2.4" data-dp="1">0</b>               → 2.4
<b data-count="20" data-dur="2500">0</b>            → slower
```
Fires when it scrolls into view. Siblings inside a `.stats` block stagger automatically.
Turns teal while counting (`.counting`), settles to ink when done.

### Scroll reveal
Add `data-rev="0"` to any element. The number is the delay in ms — use `0`, `80`, `160`
on three cards in a row to cascade them.

```html
<div class="card" data-rev="0">…</div>
<div class="card" data-rev="80">…</div>
<div class="card" data-rev="160">…</div>
```

### Others (in `index.html`'s own `<script>`)
- **Spine** — rows light up as they pass the middle of the screen
- **Marquee** — edit the `items` array to change the scrolling tags
- Both respect `prefers-reduced-motion`

---

## 4. Swapping the pictures

The seven images are **original line-art illustrations**, drawn to match the brand. They
are not stock photos, so there is no licence to worry about and nothing to attribute.

To use your own photos instead: **overwrite the file, keep the filename.** Nothing else
changes — no HTML edit, no CSS edit.

| File | Size | Where it appears |
|---|---|---|
| `img/hero.jpg` | 1600×900 | Hero panel. A dark teal wash sits over it, so almost any photo works |
| `img/card-library.jpg` | 900×560 | "The library" card — layered pages |
| `img/card-questions.jpg` | 900×560 | "The question bank" card — options with one correct |
| `img/card-cpd.jpg` | 900×560 | "CPD and compliance" card — progress ring |
| `img/give-students.jpg` | 900×560 | "Individuals" card — radiating node |
| `img/give-clinicians.jpg` | 900×560 | "Universities" card — colonnade |
| `img/give-teams.jpg` | 900×560 | "Clinics" card — team progress grid |
| `img/shot-*.png` | — | Real screenshots of the library app. Retake these as the app changes. |

**Free photo sources:** Unsplash, Pexels, Pixabay — all free for commercial use, no
attribution required. Search "physiotherapy", "rehabilitation", "clinic", "exercise".

**Don't** use photos of identifiable patients, or anything from Google Images.

---

## 5. Common edits

**Change the headline** → `index.html`, the `<h1>` inside `.hero-in`

**Change the stat numbers** → `index.html`, the `.stats` block, edit `data-count`

**Add a section page** → copy `cases.html`, change the `<title>`, `.phead` and body,
add a line to `SITE.nav`

**Change what's free vs paid** → three places: `index.html` plans block, `pricing.html`,
and the `pro: true` flags in `SITE.nav`

**Add an article** → write `content/<id>.json`, add its entry to `content/index.json`.
The library app picks it up with no code change.

---

## 6. Before you deploy — the checklist

Run these checks on anything you change:

1. **Phone width.** Resize the browser to 400px. Nothing should scroll sideways.
2. **Click every nav link.** They should all resolve.
3. **Dark mode.** Toggle your OS to dark. The site has a full dark theme; check nothing
   goes invisible.
4. **Hard refresh** (Ctrl+Shift+R / Cmd+Shift+R) — `site.css` caches aggressively.

### Deploying
1. Select the **contents** of the folder, not the folder itself
2. Drag into Cloudflare Pages
3. The file must be exactly `index.html` — not `index (1).html`

**Better, when you're ready:** put the folder in a GitHub repo and connect it to
Cloudflare Pages. Then deploying is `git push` and there's no drag-and-drop at all.

---

## 7. Known gaps

| Gap | What it blocks | Fix |
|---|---|---|
| No accounts | Questions, research feed, CPD logging — all three paid features | Cloudflare Workers + D1 |
| Articles have no real URLs | Google only indexes the section pages, not the 395 articles | Per-article URLs + sitemap. **Do this before 50 written pages.** |
| 1 of 1,063 pages written | Everything | Write them. The **structure** is complete — all 395 presentations across 8 domains already exist in the tree. |
| Fonts load from Google | A blocked network shows fallback fonts | Self-host Outfit + Figtree if it matters |

**The one that matters most:** real article URLs. Every page you write before that change
is invisible to Google.


---

## 8. Regenerating the domain pages

The 8 domain pages are generated from `library.html`'s own tree, so they can never drift
out of sync by hand. If you add conditions to the tree, re-run the generator rather than
editing `msk.html` and friends directly.

The generator reads the `const MSK = [...]` style arrays out of `library.html`, builds the
article IDs the same way the app does (`<domain>-<region>-<condition>`, lowercased and
hyphenated), and writes one page per domain.

Leaf prefixes in the tree carry meaning and the domain pages colour-code them:
- `!` — must-not-miss / serious pathology → coral dot
- `^` — post-operative → amber dot
- no prefix → standard presentation → grey dot

## 9. The workspace app is styled separately

`app.html` has its own CSS (it predates `site.css`), so it can't link `site.css` —
the class names collide. Instead it carries a **brand override block at the end of
`<body>`** that re-points its tokens (`--accent`, `--ink`, `--bg`, `--f-display`…) at the
same values `site.css` uses.

**If you change a brand colour in `site.css`, change it in that override block too.**
It is the one place the design system is duplicated.

`library.html` used to be this file. It is now the hub (§25); the app moved to
`app.html` and is linked from Library → Clinical calculators and from the hub's
"Other ways in" strip.

The five-theme picker has been removed, and any theme a previous visit stored is cleared
on load.


---

## 10. The four colour schemes

Defined at the bottom of `site.css`. Each has a light and a dark variant.

| Scheme | `data-scheme` | Character |
|---|---|---|
| Clinical | *(none — the default)* | Teal. The house look. |
| Slate | `slate` | Cool blue. More institutional. |
| Warm | `warm` | Paper and ink, brown accent. Editorial. |
| Contrast | `contrast` | Near-black on white. Maximum legibility. |

**How it works:** the switcher writes `data-scheme` onto `<html>` and saves the choice to
`localStorage` under `clinipd:scheme`. Every page carries a tiny inline script in `<head>`
that applies it *before first paint*, so there is no flash of the wrong colours.

**To add a fifth scheme:**
1. Copy a `:root[data-scheme="x"]` block in `site.css` and change the values
2. Add one entry to the `SCHEMES` array at the top of `site.js`
3. Add the same token block to the override near the end of `library.html`

**All four pass WCAG AA** (4.5:1) on body text, muted text and primary buttons. If you
change a brand colour, re-check it — contrast is easy to break and hard to notice.

---

## 11. The hover glossary

`glossary.js` holds 86 terms and the tooltip engine. Terms are detected automatically in
page prose and given a dotted underline; hover (or tap on mobile) shows the definition.

**To add a term — one line, nothing else:**
```js
"capsular pattern": { d: "A characteristic proportional loss of passive range…" },
```

Rules the matcher follows so it never makes a mess:
- only the **first** occurrence of a term per page is marked
- never inside headings, links, buttons, code or form fields
- longest term wins, so "likelihood ratio" beats "ratio"
- whole words only, case-insensitive, plurals handled automatically

The tooltip flips above/below depending on room, clamps to the viewport, and its arrow
tracks the term even when the box has been nudged sideways. Keyboard accessible (Tab to
focus, Escape to dismiss).

**The library app has its own copy** in its `GLOSS` object, kept in sync with the same
86 terms. If you add a term to `glossary.js`, add it there too.

---

## 12. Video slots

Every **condition** and **special test** in the library has a video spot — 395 + 134 of them.
Empty slots show a short prompt rather than a broken player; nothing loads a YouTube frame
until you fill it.

**To fill one**, find `const VIDEOS = {};` in `library.html` and add an entry:
```js
const VIDEOS = {
  "msk-knee-patellofemoral-pain": { y: "dQw4w9WgXcQ", t: "Assessment and loading" },
  "tests-knee-lachman-test":      { y: "abc123xyz99" }
};
```
- `y` — the **11-character YouTube id**, not the whole URL
- `t` — an optional caption underneath

The page id is shown in the empty slot itself, and at the bottom of every article, so you
never have to guess it.

Videos embed via `youtube-nocookie.com` with `loading="lazy"`. Embedding is fine legally —
the creator keeps the view and the revenue, nothing is re-hosted — **but YouTube's developer
policy prohibits charging for access to embedded content**, which is why the video library
stays free.

---

## 13. Motion

Three easing curves are defined as tokens in `site.css` — `--e-out`, `--e-in-out`,
`--e-spring` — plus `--t-fast`, `--t-mid`, `--t-slow`. **Use these rather than inventing new
timings**; it is what keeps the whole site feeling like one thing.

Everything collapses to no motion under `prefers-reduced-motion`, enforced globally.


---

## 14. The nine section pages

Each library section now has its own page, so nothing is crowded onto one list.

| Page | Items | Groups |
|---|---|---|
| `conditions.html` | 416 | 8 domains → 60 regions |
| `tests.html` | 134 | 12 |
| `measures.html` | 99 | 12 |
| `exercises.html` | 106 | 11 |
| `foundations.html` | 86 | 12 |
| `osce.html` | 28 | 7 |
| `placement.html` | 26 | 2 |
| `cases.html` | 22 | 8 |
| `qbank.html` | 10 | 1 |
| | **927** | |

Plus `domains.html`, a hub for the eight body-region pages.

Every page has: animated counts, a sticky search box (`/` focuses it), Open all / Collapse all,
accordion groups with region sub-headings, and a colour key for must-not-miss and post-operative.

**These are generated, not hand-written.** They are built from the library app's own tree,
dumped at runtime so the ids are guaranteed to match. Don't edit them by hand — add the item
to the tree in `library.html` and re-run the generator, or all 927 links will drift out of sync.

## 15. Hover terms on list items

Separate from the prose matcher in §11. A list item whose own title is a glossary term —
"Sarcopenia", "Cervical radiculopathy", "Compartment syndrome of the forearm" — gets
`data-gterm` on the link and a dotted underline, and shows the same tooltip on hover.

Currently **71 of the 927 items** are wired this way. It happens automatically at generation
time: add a term to `glossary.js` and any matching item picks it up next time the sections
are generated.

Clicking still navigates — the tooltip never swallows the click.

## 16. Glossary size

**151 terms**, covering:
- reasoning and assessment · pain mechanisms · measurement and evidence
- exercise and loading · anatomy and signs · cardiorespiratory · neurological
- **tissue and histology · physiology · pathology · healing · biomechanics**

The last five groups were added specifically so physiology and pathology language is
hoverable anywhere it appears.


---

## 17. Real pages — the big architectural change

**Every item now has its own HTML page.** Clicking a condition opens a new page on the
website; it no longer jumps into the library app's split-pane view.

```
p/                        1,054 pages
  msk-knee-patellofemoral-pain.html
  msk-knee-acl-reconstruction.html
  tests-knee-lachman-test.html
  …
article.css               styling for everything under p/
```

- **927 leaf pages** — one per condition, test, measure, exercise, case, station, topic
- **127 group pages** — one per region or domain, listing its children
- Average 5.9 KB each; 6.4 MB in total

**This is the SEO fix I kept flagging.** Google can now index all 927 pages instead of one.

### What's on each page
Breadcrumb · kind · centred title · status chips · video slot · "on this page" index ·
the full section template with every field as a labelled placeholder · references ·
previous/next within the region · page id and a link back into the app.

### Depth-aware navigation
`site.js` detects it is running inside `/p/` and prefixes every shared nav and footer link
with `../`. If you add more subfolders, extend `BASE` at the top of `site.js`.

### Regenerating
Pages are generated from the library's own runtime tree, so ids always match.
**Never hand-edit a file in `p/`** — it will be overwritten. Change the tree in
`library.html` and re-run the generator.

## 18. The A–Z listings

The nine section pages are now alphabetical indexes rather than dense accordion grids:

- Centred, one item per row, generous padding, divider lines
- Letter jump bar at the top; letters with no entries are greyed out
- Letter-grouped sections with a count per letter
- Live search filters across every letter at once and renumbers the count
- Each row shows where the item sits (domain · region) under its name
- Terms that are in the glossary keep their dotted underline and hover definition

| Page | Items | Letters used |
|---|---|---|
| `conditions.html` | 416 | 24 |
| `tests.html` | 134 | 23 |
| `exercises.html` | 106 | 17 |
| `measures.html` | 99 | 23 |
| `foundations.html` | 86 | 22 |
| `osce.html` | 28 | 15 |
| `placement.html` | 26 | 12 |
| `cases.html` | 22 | 13 |
| `qbank.html` | 10 | 7 |


---

## 19. Filter, sort and pagination on the A–Z pages

The nine index pages are now rendered client-side from an `ITEMS` array embedded in each
page. That one change makes filtering, sorting and paging trivial — and halved the file size.

### Group filter
A row of pills, each showing its own count. On `conditions.html` these are the eight
domains (Musculoskeletal 161, Sports 40, Cardiorespiratory 57, …). On the other pages they
are that section's top-level groups — body region for tests, category for measures.

Deep-linkable: `conditions.html?g=Neurological`

### Sort
| Option | Behaviour |
|---|---|
| **A to Z** | Alphabetical, with letter headers and the jump bar |
| **Z to A** | Reverse, same headers |
| **Recently updated** | Newest review date first; never-updated items fall to the bottom |
| **Highest yield** | High → medium → standard, alphabetical within each tier |

Letter headers and the jump bar appear only in the two alphabetical modes — they are
meaningless in the others, so they hide themselves.

### Pagination
25 / 50 / 100 / All per page, defaulting to 50. Prev · 1 2 3 … 9 · Next, with the current
page marked and ellipses for the gap. Changing page scrolls back to the top of the controls.

**The letter bar is pagination-aware:** clicking "T" works out which page T starts on, jumps
there, *then* scrolls to the letter. Tested — "T" correctly lands on page 8 of 9.

### ⚠ Two sorts need real data before they mean anything

**"Highest yield" is provisional.** Nothing in the library carries an editorial high-yield
rating yet, so yield is currently derived from a rule:

- **High** — flagged must-not-miss (32 conditions)
- **Medium** — flagged post-operative (16)
- **Standard** — everything else

That rule is defensible (must-not-miss genuinely is high-yield for exams) but it is *not*
your judgement. To set real ratings, change the `y` value on any item in the `ITEMS` array,
or better, add a yield field to the tree in `library.html` and re-run the generator.

**"Recently updated" currently has almost nothing to sort.** It reads the `reviewed` date
from `content/index.json`, and right now exactly one page has an entry — with a null date.
So every item shows "Not updated". It will become useful as you verify pages and set
`"reviewed": "YYYY-MM-DD"`.

Both controls are wired and working; they are waiting on content, not code.


---

## 20. Photography

### The treatment
All photos get one filter in `site.css`: `saturate(.62) contrast(1.06) brightness(.98)` —
muted and slightly lifted. That is what makes images from nine different stock sources read
as one set. Card photos warm up slightly on hover. Dark mode drops brightness so they
don't glare.

To change the look for the whole site, edit that one `.photo` rule.

### The slots — overwrite the file, keep the name
| File | Size | Where |
|---|---|---|
| `img/hero.jpg` | 2000×1200+ | Hero panel (brand wash over it) |
| `img/break-1.jpg` | 2000×1200+ | First scroll-fade band |
| `img/break-2.jpg` | 2000×1200+ | Second scroll-fade band |
| `img/card-library.jpg` | 900×560 | "The library" card |
| `img/card-questions.jpg` | 900×560 | "The question bank" card |
| `img/card-cpd.jpg` | 900×560 | "CPD and compliance" card |
| `img/give-students.jpg` | 900×560 | "Individuals" card |
| `img/give-clinicians.jpg` | 900×560 | "Universities" card |
| `img/give-teams.jpg` | 900×560 | "Clinics" card |

**Brief:** hands and equipment, faces mostly out of frame. Landscape only. Ages better than
stock models and avoids the generic-stock problem.

**Never use photos of real patients**, including from placement and including with faces
cropped. Clinical photography consent does not transfer to a commercial website. Stock, or
people who have explicitly agreed to this use.

**Sources:** Unsplash and Pexels — free for commercial use, no attribution required.

## 21. The scroll-fade bands

`<section class="band-img" data-band>` with an `<img>` and a `.band-tx` block. The script
in `site.js` (`bands()`) writes a 0→1 progress envelope as the section crosses the viewport:

- The photo fades from 18% to full and settles from a 1.10 zoom to 1.00
- The text follows about 5% later, rising 26px as it arrives
- Both hold through the middle of the pass, then fade back out

Measured across a scroll: image 0.18 → 1.00 → 0.65, text 0.00 → 1.00 → 0.77.

A dark gradient sits over the photo so the headline stays readable whatever image you drop
in — you do not need to pick photos with convenient empty space.

Under `prefers-reduced-motion` both are shown plainly with no choreography.

**To add another band**, copy either section, point it at a new image, change the words.
No script changes — it picks up any `[data-band]`.

### Removed
The browser-mockup product screenshot that used to sit in the "Seventeen sections" block is
gone, along with its CSS. The first scroll-fade band replaced it.


---

## 22. Photo blending — what's actually applied

**Edge fades.** Band images are masked top and bottom
(`transparent 0% → #000 16% → #000 84% → transparent 100%`) so they melt into the page
rather than ending on a hard line. The dark legibility wash carries the *same* mask, or it
would draw the hard edge the image no longer has. Card photos get a bottom-only mask so they
dissolve into the card body.

**Brightness, by role:**
| | Filter |
|---|---|
| Cards | `saturate(.62) contrast(1.06) brightness(.98)` |
| Hero | `saturate(.58) contrast(1.05) brightness(.92)` |
| Bands | `saturate(.46) contrast(1.02) brightness(.58)` |

Bands sit furthest back because white type has to hold over them. The hero keeps more
presence — it is the first thing anyone sees.

**A trap worth knowing about.** The generic `img[loading="lazy"]` fade-in uses
`animation-fill-mode: both`, and an animation's final state beats a declared `opacity`.
That silently pinned the band images at full opacity and killed the scroll fade — it looked
fine in a screenshot and was only caught by measuring rendered opacity across a scroll.
`.band-img img` now carries `animation:none !important`. **If you add another scroll-driven
opacity effect, check for the same collision.**

### Photos in place
`hero.jpg` · `break-1.jpg` · `break-2.jpg` · `card-library.jpg` · `card-questions.jpg` ·
`card-cpd.jpg`

Still original artwork: `give-students.jpg` (Individuals), `give-clinicians.jpg` (Universities),
`give-teams.jpg` (Clinics).

**Band 2's copy was rewritten** to match its photo — it shows a CPD seminar, not someone
reading, so the headline is now "The learning you already do should count for something."


---

## 23. Design studio — 10 colours × 6 fonts

The scheme switcher in the top bar is now a full panel: appearance (system/light/dark),
ten colour schemes, six font sets. Choices persist per browser and apply before first paint.

**Colours:** Clinical · Slate · Warm · Contrast · Indigo · Forest · Plum · Crimson · Ocean · Graphite

**Fonts:** Outfit/Figtree · Plus Jakarta Sans · Fraunces/Inter · Space Grotesk/Inter ·
Libre Baskerville/Source Sans · DM Serif/DM Sans

Font files load **on demand** — only the chosen set is downloaded, so adding five options
cost nothing in page weight.

### These are generated, not hand-picked
`_build/gen_schemes.py` computes every token and **walks each colour darker or lighter
until it clears WCAG AA against its background.** All 20 variants (10 schemes × light/dark)
pass on body text, secondary text, muted text, and both button fills. Re-run the generator
rather than editing the scheme CSS by hand.

### The `--on-brand` trap
`.btn.pri` originally hard-coded `color:#fff`. That is correct in light mode, where `--brand`
is dark — but in dark mode `--brand` is a *light* colour, so white-on-light gave **3.3:1 on
all ten dark schemes.** Every brand and coral fill now takes its text colour from
`--on-brand` / `--on-coral`, which the generator computes per scheme. Dark buttons went
3.3 → 6.1.

**If you add a component with a `var(--brand)` background, use `var(--on-brand)` for its
text.** Never `#fff`.

### Picking a permanent default
Open the panel, try combinations, press **Copy my choice**, and paste it into the chat.
To hard-code it instead, set `data-scheme` / `data-font` on `<html>` and remove the trigger
button from `site.js`.

## 24. The AMBOSS-style features

| Page | What it does | Works today? |
|---|---|---|
| `studyplan.html` | Build a plan to a target date — weeks, sessions, pages | **Yes, fully** |
| `collections.html` | Saved reading list, with a Save button on all 927 article pages | **Yes** (this browser only) |
| `progress.html` | Domain coverage, CPD ring, recent reads | Shell with sample data |

**Study plans are genuinely functional.** Pick a date, days per week, minutes per session
and domains; it allocates pages across weeks at roughly 7 minutes per page, and **tells you
honestly when the plan doesn't fit** — "you will reach 420 of 416 pages by 2 Feb" rather
than silently truncating. Three orderings: by domain, highest-yield-first, or interleaved.
Saves to the browser and prints cleanly.

**Collections work today** via localStorage, with a clear note that they don't sync.

**Progress is a shell** and says so with a "Sample data" badge — real progress needs accounts.

### The overflow trap worth knowing
The design-studio panel was originally parked off-screen with `transform:translateX(102%)`.
A `position:fixed` element off the right edge **extends the horizontal scroll area on every
page** — 408px of overflow site-wide. `overflow-x:clip` on `<html>` fixes that but **breaks
`position:sticky`**, which killed every sticky header. The panel now scales up from the right
edge instead, which can't extend bounds. Both were caught by measurement, not by looking.

---

## 25. The library hub — `library.html`

The split-pane app was the one page on the site that behaved like an app: every
section lived inside it, nothing had a URL, and on a phone it was a wall. It is now
`app.html`, and `library.html` is a hub built from the **same skeleton as the nine
A–Z listings** — same head, same sticky tools bar, same centred body, same row
styling. That is deliberate: the hub should read as the front door of that family,
not as a different website.

### Three views, one page

| What you do | What you see |
|---|---|
| Arrive | the hub — nine section cards in three bands, then a quick-links strip |
| Click a section pill | that section's groups as clickable rows (each deep-links to `<section>.html?g=<group>`) |
| Type anything | live results from all 927 pages, or from the pilled section only |

Clicking the pill that is already lit clears it and returns you to the hub.
Deep links work: `library.html?q=acl`, `library.html?s=test`.

### The search index

`ALL` near the bottom of the file is one compact array — `{t,i,s,g,f,k,a}` — built by
`_build/build_index.py`, which reads the `ITEMS` arrays straight out of the nine
A–Z pages. **Never hand-edit it.** Add a page to a listing, re-run the two scripts, and
the hub picks it up:

```bash
python3 _build/build_index.py   # rebuild the index from the nine listings
python3 _build/gen_hub.py       # rewrite library.html around it
```

### How search ranks

Every typed word must appear somewhere, so `rot cuff` and `hip oa` both land. Then:

| Tier | Match | Example |
|---|---|---|
| 5 | title **starts with** it | `knee` → Knee osteoarthritis |
| 4 | starts a word in the title | `cuff` → Rotator **cuff** repair |
| 3 | the page's **abbreviation** | `tug` → Timed Up and Go · `6mwt`, `bbs`, `odi`, `psfs` |
| 2 | buried inside a word | `spin` → supra**spin**atus |
| 1 | the group name only | `vestibular` |

The abbreviations in tier 3 are generated, not typed. `build_index.py` takes the
initials of any **Title Case** instrument name with three or more significant words —
64 of the 927 pages qualify. Sentence-case titles are skipped on purpose, because
"Hamstring injury prevention" → HIP is noise, not a shortcut.

### Editing the hub

Everything is in `_build/gen_hub.py`:

- `SECTIONS` — the nine cards: code, file, name, mono badge, blurb, free/pro tag
- `BANDS` — which cards group under Reference / Practise / Background
- `OTHER` — the quick-links strip at the bottom

Change one, re-run `gen_hub.py`. Editing `library.html` by hand works but gets
overwritten the next time anyone regenerates.

---

## 26. `listing.css` — the listing skeleton, now shared

The nine A–Z pages each carried a byte-identical 8 KB `<style>` block. That block is
now `listing.css` and all nine link it, as does `library.html`. It saved 72 KB and,
more usefully, means the hub cannot drift from the lists.

Two things changed when it moved:

- **Phone filter pills scroll horizontally.** Twelve wrapped pills turned the sticky
  bar into a third of a phone screen. They are now one swipeable row, bled to the
  viewport edges and masked at both ends so it reads as scrollable.
- Anything you add here lands on all ten pages at once. Check both viewports.

---

## 27. Motion added in this pass

| Thing | Where | What it does |
|---|---|---|
| Hero stagger | `index.html` `<style>` | badge → headline → sub → search → buttons arrive in sequence **on load**, not on scroll (the hero is already in view, so `data-rev` was the wrong tool) |
| Hero parallax | `heroDrift()` in `site.js` | the photo drifts at ~⅓ page speed. Base `scale(1.13)` leaves room so no edge is ever exposed |
| Reading progress | `progress()` in `site.js` | a 2px gradient hairline along the **bottom edge of the sticky header**, so it costs no vertical space. Appears only once you have scrolled |
| Card wash | `.lib-card::before` | a brand gradient wipes up from the bottom edge on hover, instead of a flat background swap |
| Hint collapse | `.az-tools.stuck .hint` | the "press / to search" line folds away once the bar sticks |

All of it is rAF-throttled and all of it is off under `prefers-reduced-motion`. The
reduced-motion state is tested, not assumed: `_build/anim.py` loads the page with
`reduced_motion="reduce"` and asserts every animated element ends at opacity 1.

---

## 28. "For physios" — where it is said

The brand wordmark is a **two-line lockup** (`.brand-wm`): `CliniPD` over a small mono
`FOR PHYSIOS`. Stacking it means the line costs no horizontal width, so it survives
every breakpoint — including a 360px phone, which is the one place it matters most.
Edit it in `buildNav()` and `buildFoot()` in `site.js`, and `.brand-for` in `site.css`.

It is also said in the hero badge (`.hero-for` in `index.html`) and in the footer
blurb. Three places, each a different register: mark, promise, fine print.

---

## 29. What was cut from the home page, and where it went

The home page ran ten sections. It now runs eight plus the footer — about 23% shorter.

| Cut | Why | Where it lives now |
|---|---|---|
| The 17-row template spine | ~1,000px, and it is an evidence argument, not a sales one | `evidence.html`, with its CSS and its row-lighting script |
| The "20 hrs" big-number block | said the same thing as the CPD scroll band two sections below it | nowhere — the band carries it |
| The two 5-item pricing feature lists | the full comparison is a click away | `pricing.html`; the home page now has a one-line summary per plan and a "See the full comparison" link |

**Counts were wrong and are now right:** 1,063 → 927 pages, 395 → 416 presentations.
Fixed on `index.html`, `pricing.html` and `domains.html`.


---

## 30. `_build/` — the generators ship with the site

The scripts the README names now live in `_build/`, so you can actually re-run them:

```
build_index.py    rebuild the hub's search index from the nine A–Z listings
gen_hub.py        rewrite library.html around that index
gen_schemes.py    regenerate the 10 colour schemes with contrast verified
gen_pages_all.py  regenerate the 1,054 article pages under p/
gen_az2.py        regenerate the nine A–Z listings
gen_domains.py    regenerate the eight domain pages
test_site.py      every root page, both viewports: overflow, JS errors, links
test_art.py       the article pages and their links
all_schemes.py    contrast across all 10 schemes x light/dark
anim.py           the animations, including under prefers-reduced-motion
hubtest.py        the hub's three views, its pills and its deep links
```

They expect to be run from a checkout of this folder, and several write their output
straight into it. **Delete `_build/` before you deploy** — it is a thousand lines of
Python nobody should be able to fetch from clinipd.com, and it counts against
Cloudflare's file limit.


---

## 31. Housekeeping done in this pass

- `img/shot-*.png` deleted — 1.3 MB of product screenshots left over from the
  section you asked me to remove. Nothing referenced them.
- `library.html` is the hub; the old app is `app.html`. Every breadcrumb on the
  site already said "Library → library.html", so they all now point at the hub,
  which is what they should have meant all along.
- The nine listings lost their duplicated 8 KB `<style>` block to `listing.css`.

**Deployable file count: 1,112.** Still over Cloudflare's 1,000-file dashboard
limit, so deploy with Wrangler or from GitHub:

```bash
cd clinipd
rm -rf _build          # don't ship the generators
npx wrangler pages deploy . --project-name clinipd
```

---

## 32. Writing a page — how content actually reaches the article pages

**This was broken until now and is worth understanding.** There are two
renderers, and only one of them used to read your written content:

- `app.html` (the workspace) fetched `content/<id>.json` — always did
- `p/*.html` (the 1,054 real article pages, the ones the A–Z lists and
  Google point at) did **not**. They were static skeletons with
  "Not written yet" baked in, and dropping a JSON file in did nothing to them

`articleContent()` in `site.js` closes that. Every article page already loads
`site.js`, so **no page needed regenerating** — the function detects an
article by the page-id element in the footer and takes it from there.

### What it does

1. Fetches `content/<page-id>.json`. **404 → it stops and leaves the
   skeleton alone.** An unwritten page stays honestly unwritten
2. Swaps each `.flds` placeholder block for the written prose, matching on
   the section's `<h2>` text
3. Turns every `<sup>4</sup>` into a link to `#ref4` in the reference list
4. Wraps any `[verify…]` marker in `<mark class="verify">` so an unchecked
   figure is impossible to miss on the page
5. Rebuilds the References section: numbered, with design / NHMRC level /
   licence tags and a clickable `doi.org` button per entry
6. Updates the chips: *Written · unverified*, reference count, newest source
   year (ageing flag past 7 years), and a count of figures still to verify
7. Re-runs the hover glossary over the new prose

### Adding a page, start to finish

```bash
# 1. drop the JSON in
cp acj.json content/msk-shoulder-acromioclavicular-joint-injury.json

# 2. add its manifest row to content/index.json
# 3. (optional) add a YouTube id to VIDEOS in app.html
# 4. redeploy
npx wrangler pages deploy . --project-name clinipd --branch main
```

Nothing is regenerated. No build step. The page fills itself on load.

### The year trap

A Vancouver citation's page range (`29:2039-2045`) matches a year regex
exactly. Both the manifest script and `articleContent()` cap extracted years
at next year, or every page claims a newest source of 2045.

### Styles

`article.css` carries `.fld-live`, `.tbl-wrap`, `table.tpl`, `.reflist` and
`mark.verify`. They were previously only inside `app.html`'s private
stylesheet, which is why written content had nowhere to render.

### Tested by

`_build/acj.py` — asserts 16/16 sections swap in, no placeholders survive,
10 references render with 10 DOI links, 47 citation superscripts become
working anchors, clicking one lands on its reference, both verify markers
show, and **an unwritten page still shows all 16 placeholders with no JS
errors**. Desktop and phone.
