# Clinipd publication checklist

Human sign-off checklist, completed per page before its `content/index.json`
status moves past `draft`. Pairs with `_build/RESEARCH-STANDARD.md`, which
this checklist assumes you've read. `_build/add-page.py` catches structural
problems automatically; this checklist catches everything it can't.

## Clinical accuracy
- [ ] Every substantive clinical claim is accurate and current as of today,
  not just as of when it was drafted.
- [ ] No claim overstates what its cited source(s) actually found.
- [ ] Red-flag / "when to refer" / contraindication content has been read
  line-by-line, not skimmed.

## Reference verification
- [ ] Every reference has been opened, or independently confirmed against
  its bibliographic record — not taken on trust from an AI draft.
- [ ] Every DOI/URL resolves to the paper actually being cited.
- [ ] No reference's design, NHMRC level, or methodological quality was
  assumed rather than checked against the actual source.
- [ ] Spot-checked that references are cited for claims they actually
  support (not just the first reference on the page — sample several).

## Research limitations
- [ ] Key limitations of Tier 1/2 sources (sample size, population
  mismatch, risk of bias, funding/conflicts of interest) have been
  considered, not just the headline finding.
- [ ] Any limitation that matters to a claim is reflected in the page's own
  wording, not silently absorbed into an unqualified, confident statement.

## Conflicting findings
- [ ] Where sources disagree, the page says so explicitly, with a stated
  certainty level (strong / moderate / limited / conflicting /
  insufficient) — never a one-sided summary of only the sources that
  agree.
- [ ] No recommendation on the page is more definitive than the underlying
  evidence actually justifies.

## Clinical safety — critical vs. non-critical uncertainty
Criticality is judged **per claim**, by potential harm given the actual
population and clinical context — never automatically by category (dosage
guidance is not inherently non-critical; see `RESEARCH-STANDARD.md` §8).

- [ ] Every `[verify]` marker on the page has been individually reviewed
  and classified as critical or non-critical — including markers inherited
  from an existing page. **ACJ's and PFP's existing `[verify]` markers are
  not exempt**: re-review each one on its own merits before relying on any
  prior classification.
- [ ] **Zero** safety-critical `[verify]` markers remain. Red-flag
  screening, emergency referral criteria, contraindications, and any
  recommendation that could cause harm if wrong — for the population and
  context this page actually addresses — are fully resolved, not flagged
  and shipped.
- [ ] Every remaining non-critical `[verify]` marker sits next to wording
  that is appropriately qualified (framed as a pragmatic estimate or
  extrapolation) — never presented as settled fact.
- [ ] `[verify]` has not been used, anywhere on the page, as a substitute
  for resolving a potentially unsafe or misleading treatment
  recommendation.

## Physiotherapy relevance
- [ ] Every claim is relevant to physiotherapy scope of practice, and to
  Australian context where that matters (referral pathways, funding
  schemes, regulatory bodies).
- [ ] Evidence drawn from a different population or clinical setting is
  explicitly flagged as such, not presented as directly generalisable.

## Mechanical (re-confirm even though `add-page.py` already checks these)
- [ ] `_build/add-page.py` passes with zero unresolved errors, and every
  warning it produced has been consciously accepted or fixed.
- [ ] No fabricated reference, DOI, author, or finding anywhere on the
  page.
