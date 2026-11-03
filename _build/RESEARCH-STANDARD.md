# Clinipd research and evidence standard

Permanent methodology standard for every piece of Clinipd clinical content —
all 395 condition pages and any future professional-development content.
This governs *how evidence is found, judged and cited*. `_build/STYLE-GUIDE.md`
governs *how a page is written and structured*; read both.

## 1. Four distinct concepts — never conflate these

Every source and every claim is judged on four separate axes. A high mark on
one never implies a high mark on another.

1. **Research design** — what kind of study it is (RCT, systematic review,
   prospective cohort, case series, narrative review, consensus statement).
   A property of the source — recorded in its research record as `design`.
2. **NHMRC evidence level** — the existing Clinipd taxonomy, unchanged,
   still recorded in each page's `refs[i].level` exactly as today.
3. **Methodological quality of that specific study** — `high` / `moderate` /
   `low` / `unclear`. A systematic review with a poor search strategy is not
   "high quality" just because systematic reviews rank well by design.
   Always assessed independently, never assumed from design or level.
4. **Certainty of the evidence behind one specific clinical recommendation** —
   `strong` / `moderate` / `limited` / `conflicting` / `insufficient`. A
   judgement about everything cited for *one claim*, never about a single
   source. Written into the article's own prose, never stored as metadata.

## 2. Research hierarchy — guidance for sourcing, not an automatic ranking

**Tier 1 — preferred**: high-quality systematic reviews/meta-analyses,
evidence-based clinical practice guidelines, high-quality RCTs, systematic
reviews of diagnostic accuracy or prognosis.

**Tier 2 — strong supporting**: prospective cohort studies, diagnostic
accuracy studies, well-designed observational studies, prognostic studies,
high-quality controlled trials.

**Tier 3 — supporting, used selectively**: narrative reviews, expert
consensus statements, cross-sectional studies, case-control studies, case
series and smaller clinical studies.

**Tier 4 — not acceptable as clinical evidence**: personal blogs, commercial
health websites, unreferenced educational articles, social media, unverified
AI-generated references or summaries, anecdotal opinion presented as fact,
research that cannot be independently verified.

**These tiers describe where to look first, not how to weigh what you
find.** A Tier 1 design does not automatically outrank a Tier 2 or 3 source
in an actual clinical decision — research design, NHMRC level,
methodological quality (§1.3), and relevance to the *specific* clinical
question (§5) must all be weighed together. A poorly conducted systematic
review must not automatically outweigh a well-designed individual study; a
higher tier only earns more weight when its execution and relevance
actually justify it.

## 3. Mandatory per-source quality criteria

Before citing any source, confirm:
- Relevance to the *specific* claim it's cited against.
- Credibility and publication integrity.
- Methodological quality (§1.3).
- Currency, and whether it has been superseded by later work.
- Traceability — DOI, PubMed ID, or an official source URL.
- Applicability to physiotherapy and the relevant population.
- Funding, conflicts of interest, potential commercial bias.
- That the claim extracted matches what the source actually found —
  re-read the relevant passage, don't cite from memory or a summary.

## 4. Currency

Prefer: clinical practice guidelines and systematic reviews from the last
5 years where possible; treatment-effectiveness research from the last
5–10 years where possible. **Do not automatically exclude older research** —
landmark studies, foundational work, and older evidence that remains
uncontradicted and un-superseded stay in. Judge currency by "has this been
superseded," not by date alone.

(The site already shows an automatic "ageing" indicator when a page's newest
reference is over 7 years old — a sitewide cosmetic signal, not a rule. It
does not replace this section's judgement-based currency standard.)

## 5. Match evidence type to the clinical question

| Section type | Appropriate evidence |
|---|---|
| Anatomy | Anatomical research, authoritative texts |
| Pathophysiology | Mechanistic research, high-quality reviews |
| Risk factors | Prospective cohorts, systematic reviews |
| Assessment / special tests | Diagnostic accuracy studies, systematic reviews |
| Differential diagnosis | Clinical guidelines, diagnostic studies |
| Management / rehabilitation | Guidelines, systematic reviews, RCTs |
| Prognosis | Prospective cohorts, systematic reviews |
| Return to sport/work | Guidelines, cohort studies, consensus statements |

A source must genuinely support the specific claim beside it. A study
showing improved muscle strength must not be cited as evidence of improved
injury recovery unless it actually measured recovery.

## 6. Citation requirements

Use as many relevant, credible in-text citations as reasonably possible
while maintaining natural readability. There is no fixed minimum or maximum
per paragraph — the objective is to make Clinipd exceptionally
well-referenced and evidence-traceable, without making the writing feel
mechanical.

- Place citations close to the specific statement they support, not bundled
  at the end of a paragraph as an afterthought.
- Where multiple independent sources genuinely support a claim, cite all of
  them where it adds real traceability.
- Distribute citations throughout the content rather than concentrating
  them at paragraph endings.
- Avoid citation padding, repetitive references, and citation density so
  high it compromises readability — more citations is only better when
  each one is doing real work.
- Every reference must support at least one identifiable claim on the page
  (`_build/add-page.py` already warns if a reference is never cited).
- Never fabricate a reference, DOI, author, finding, or publication detail.
- Verify every source against its original publication or an official
  bibliographic record before citing it — not against a summary, and never
  against an unverified AI-generated description of the paper.
- Synthesise in original language. Do not copy or closely paraphrase
  substantial material from any source, including open-licence ones.
- Roughly 15–30 references is a reasonable *starting point* for a
  comprehensive page — never a target to hit. Quality and relevance decide
  the count, not the reverse.

## 7. Conflicting or uncertain evidence

Do not hide disagreement between sources. Where evidence conflicts:
- Explain the disagreement in the text (population differences, study
  quality, recency, outcome measured).
- State the certainty level (§1.4) in the prose itself:
  **strong / moderate / limited / conflicting / insufficient** evidence.
- Do not issue a definitive recommendation the evidence doesn't actually
  support — say so explicitly instead.

These certainty descriptions sit alongside the NHMRC taxonomy, never
replace it. NHMRC still classifies each individual reference's design/level
in `refs[i].level`, exactly as today.

## 8. `[verify: ...]` — critical vs. non-critical uncertainty

Use `[verify: ...]` for anything not yet independently confirmed. It
renders as a visible amber flag — but **not all uncertainty is equal**, and
criticality is never decided by category alone.

Whether an unresolved claim is critical depends on **the potential harm if
it is wrong, the patient population, and the clinical context** — not on
what kind of information it happens to be. In particular:

- **Dosage, loading and exercise-progression guidance is not automatically
  non-critical.** An unsupported loading recommendation for a straightforward,
  self-limited presentation may be low-stakes. The same kind of unsupported
  guidance for a potentially serious presentation — a bone stress injury, a
  post-operative protocol, a condition where getting load wrong risks
  re-fracture or re-rupture — is safety-critical, even though it is
  technically "exercise dosage" in both cases. Judge the actual harm, not
  the label.
- **Non-critical uncertainty** (e.g. an MCID figure not yet independently
  confirmed, a minor historical detail, a dosage parameter for a
  low-risk, self-limiting presentation) may ship flagged with `[verify]`,
  **provided the surrounding wording is appropriately qualified** — framed
  as a pragmatic estimate, not stated as settled fact. This can be resolved
  after publication.
- **Safety-critical uncertainty** — anything in emergency referral advice,
  red-flag screening, contraindications, or any clinical recommendation
  that could cause harm if wrong given its actual population and context —
  **must be resolved before publication.** `[verify]` is never permission to
  publish a potentially unsafe or misleading treatment recommendation. If it
  can't be confirmed, it comes out of the page until it can.
- This judgement is made **per claim, individually** — never by
  automatically accepting or rejecting a whole category of flags. See the
  publication checklist for how this applies to ACJ's and PFP's existing
  `[verify]` markers.

## 9. The research record (internal, not public)

For any source worth annotating in depth, create a record under
`_build/research/<slug>.json`, where `<slug>` is a short, human-readable,
stable identifier (`<first-author-surname>-<year>-<topic>`) — **not** a DOI
or URL directly, so a DOI correction, a formatting inconsistency, or a
source with only a URL never requires renaming anything.

`_build/research/index.json` maps each source's **normalised** identifier
to its slug, so the same source is recognised consistently across every
page that cites it, however it's written on different pages:

- **DOIs**: lowercased; resolver prefixes (`https://doi.org/`,
  `http://dx.doi.org/`) stripped; surrounding whitespace and trailing
  punctuation removed.
- **Ordinary URLs**: scheme and domain lowercased; path case and meaningful
  query parameters preserved as-is (some URLs are case-sensitive).
- A single source may have **more than one** identifier in the index (e.g.
  both its DOI and a publisher URL) — all pointing at the same slug.
- Before creating a new record, check the index for both the normalised
  DOI and the normalised URL. **Never silently overwrite an existing
  record** — if the slug already exists, either reuse it or pick a new,
  distinct slug.

This file is **never fetched by the public website** — it's a separate,
optional, git-tracked inventory for traceability and reuse across pages.
Recommended for Tier 1/2 sources and anything reused across multiple pages
or carrying a `[verify]` flag; not required for every citation on day one.

## 10. AI-assisted research workflow

1. Identify relevant research for the specific claim.
2. Independently verify each candidate reference against its original
   publication or bibliographic record — never trust an AI-generated
   citation or summary as sufficient verification on its own.
3. Assess study design, methodological quality, limitations and relevance
   (§1, §3).
4. Extract the actual finding — re-read the relevant passage.
5. Link that finding to the specific clinical claim it supports (§6).
6. Draft original Clinipd content with citations.
7. Flag anything unresolved with `[verify: ...]`, classifying it as
   critical or non-critical by actual potential harm (§8) — never by
   category.
8. Complete human clinical and editorial review (`_build/PUBLICATION-CHECKLIST.md`)
   before publication.

AI may assist at every step above. AI is never treated as an authoritative
source in itself, and never substitutes for step 2's independent
verification.

## 11. Publication readiness

A page does not move past `draft` status while it contains: fabricated or
unverified references, unsupported substantive clinical claims, unresolved
*critical* safety concerns (§8), unverified clinical recommendations, or
material evidence limitations that have been concealed rather than stated.
Non-critical `[verify]` flags do not block publication, provided the
wording around them is appropriately qualified. See
`_build/PUBLICATION-CHECKLIST.md` for the full human sign-off checklist.
