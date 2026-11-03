# Clinipd clinical content style guide

Permanent writing/review standard for every condition page. Applies to all 395
condition pages in the production catalogue. Not a technical document —
`_build/add-page.py` enforces what can be machine-checked; everything else
here is a human/process standard for whoever is writing or reviewing a page.

## 1. Master template

`content/msk-shoulder-acromioclavicular-joint-injury.json` (the ACJ page) is
the master clinical content template. Copy its `sections` key list and `refs`
schema exactly for every new page — same 16 section headings, same reference
object shape (`cite`, `doi`, `design`, `level`, `licence`, `used`).

Do not use `content/msk-knee-patellofemoral-pain.json` (PFP) as a template —
it is a worked example of what review must catch (see §3), not a model to
copy.

## 2. Page structure

- **Prominent heading** — the page's own `<h1>`; nothing to write, it's
  already there.
- **Short, accessible explanation** — the `Overview` section's
  `Definition (1–2 sentences)` field. Write this first, in plain language.
- **Quick-information section, immediately underneath** — the `Overview`
  section's `Three-point summary` field (with `Also known as` /
  `Classification or grading` alongside it). This is the reader's "at a
  glance" digest before the detailed sections begin.
- **Detailed clinical information further down** — sections 2–16
  (epidemiology through evidence summary), in the fixed order given by
  `_build/tpl.json`'s `presentation` entry.

## 3. Evidence standards (permanent, non-negotiable)

1. **Current and traceable** — prefer guidelines, systematic reviews and
   primary research; use the most recent adequate source, not the oldest
   one you found first.
2. **Clickable in-text citations** — every citation is a literal
   `<sup>n</sup>` (or `<sup>n,m</sup>`) marker, 1-indexed into `refs`. This is
   handled automatically by the site (becomes a `#refN` link) — just write
   the `<sup>` tag.
3. **At least two genuinely relevant citations per substantive clinical
   paragraph, wherever the evidence supports it.** Do not pad a single-source
   claim with a second citation that says nothing new just to hit the count —
   the requirement is "wherever supported," not "always."
4. **Genuine, traceable references that directly support the claim beside
   them.** Every reference must be a real, independently findable
   paper/guideline/fact-sheet. Open it and confirm it actually says what the
   page claims it says.
5. **Consistent evidence-level classification: NHMRC, sitewide.** Use the
   NHMRC levels (e.g. `NHMRC I`, `NHMRC II`, `NHMRC III-2`, `NHMRC IV`,
   `Expert consensus` only for genuine consensus statements) in every
   reference's `level` field — the same way the ACJ page already does. Do
   not mix in GRADE/Oxford CEBM wording (the PFP page's "Guideline" /
   "Expert consensus" free text is the mistake to avoid).
6. **No fabricated references, ever.** If a claim can't be sourced, it does
   not get a citation — it gets a `[verify: ...]` flag (§5) or is left out
   of the page entirely. Never invent a DOI, a study, or a finding.
7. **Original synthesis, not reproduction.** Write in your own words and
   structure. Substantial copying of a source's text (even a freely
   licensed one) is not acceptable — synthesise across sources instead.
8. **Explicitly flag uncertainty.** Anything not yet fully verified gets a
   `[verify: ...]` marker (§5) rather than being stated as settled fact.

## 4. Reference object fields

```json
{
  "cite": "Full citation, Vancouver-style",
  "doi": "10.xxxx/xxxxx",
  "design": "RCT / systematic review / consensus statement / cohort / etc.",
  "level": "NHMRC II",
  "licence": "Open access / All rights reserved / CC BY 4.0 / etc.",
  "used": "Section names this reference supports"
}
```
If a source genuinely has no DOI (e.g. a professional-body fact sheet), put
its real, resolvable URL in the `doi` field rather than leaving it empty —
but note this is a known gap in `add-page.py`'s validation (it only checks
non-empty, not DOI-shaped) and is flagged as a human-review point until that
hardening is added.

## 5. The `[verify: ...]` marker

Use `[verify: short note on what needs checking]` inline, anywhere in a
section's HTML, for any claim you have not fully confirmed yet — a dosage
figure extrapolated rather than sourced, a reference whose full text you
haven't read, an MCID you couldn't independently verify. It renders as a
visible amber flag on the live page (`<mark class="verify">`), so it is never
silently lost. A page can ship with `[verify]` markers; it must never ship
with an invented fact in their place.

## 6. Videos (optional, per page)

Top-level `videos` array, sitting alongside `sections`/`refs` (never inline
inside section HTML):

```json
"videos": [
  { "category": "anatomy", "youtubeId": "dQw4w9WgXcQ", "title": "Optional caption" }
]
```

- `category` must be one of: `anatomy`, `pathology`, `assessment`,
  `special-tests`, `rehabilitation`.
- `youtubeId` is the 11-character id from the video's URL (the part after
  `watch?v=`), never the full URL.
- Only include a video when it is genuinely relevant and appropriate —
  anatomy, pathology, assessment, special tests and rehabilitation "where
  appropriate" means omit the category entirely if there's nothing suitable,
  rather than forcing a weak match.
- Embeds are privacy-enhanced (`youtube-nocookie.com`), lazy-loaded, and
  never autoplay — this is handled by the site; just supply the id.

## 7. Images (optional, per page — architecture ready now, sourcing later)

Top-level `images` array:

```json
"images": [
  {
    "section": "Pathoanatomy & mechanism",
    "file": "msk-shoulder-acromioclavicular-joint-injury-01.jpg",
    "alt": "Rockwood classification of ACJ injury, types I-VI",
    "caption": "Rockwood grades I-VI (redrawn from Gorbaty et al. 2017).",
    "credit": "Illustration: Clinipd, after Gorbaty et al. 2017",
    "sourceUrl": "https://doi.org/10.1007/s11999-016-5079-6",
    "licence": "CC BY 4.0"
  }
]
```

- `section` must match one of the page's own 16 section headings exactly —
  the image renders at the end of that section's content.
- Store the file at `img/conditions/<page-id>/<file>` before referencing it.
- `alt`, `credit`, `sourceUrl` and `licence` are all required — never add an
  image without a traceable source and a clear licence. `caption` is
  optional but recommended whenever it adds clinical context.
- Do not source or add large numbers of real images yet — this section
  describes the format for when that production stage starts.

## 8. Before submitting any page

Run `python3 _build/add-page.py content/<page-id>.json <page-id>` and read
the full report:
- **Any ERROR must be fixed** — the page cannot install until errors are
  resolved (or `--force`, which should not be used for real content).
- **Read every WARNING** — a missing DOI, an unused reference, an empty
  section. Each one is a genuine gap, not noise.
- Then view the page in a browser (`node server.mjs`, open
  `/p/<page-id>.html`) and confirm it reads correctly at both desktop and
  mobile widths before considering the page done.
