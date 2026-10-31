#!/usr/bin/env python3
"""Pull every ITEMS array out of the nine A-Z pages into one compact search index."""
import io, json, re, os

ROOT = "/home/claude/clinipd"
PAGES = [
    ("conditions.html", "Conditions",       "cond"),
    ("tests.html",      "Special tests",    "test"),
    ("measures.html",   "Outcome measures", "meas"),
    ("exercises.html",  "Exercises",        "exer"),
    ("cases.html",      "Clinical cases",   "case"),
    ("osce.html",       "OSCE stations",    "osce"),
    ("qbank.html",      "Question bank",    "bank"),
    ("foundations.html","Foundations",      "fnd"),
    ("placement.html",  "Placement",        "plac"),
]

STOP = {"and","the","of","for","to","in","with","a","an","on","by","or","&"}

def acronym(title):
    """TUG from 'Timed Up and Go', NPRS from 'Numeric Pain Rating Scale'.
    Physios type the short form; the page titles carry the long one."""
    import re as _re
    words = [w for w in _re.split(r"[^A-Za-z0-9]+", title) if w]
    keep = [w for w in words if w.lower() not in STOP]
    if len(keep) < 3:
        return ""
    # a title that is ALREADY an acronym needs no second one
    if sum(1 for w in keep if w.isupper() and len(w) > 1) >= 2:
        return ""
    # Only named instruments and eponymous tests get one. Sentence-case
    # titles ("Hamstring injury prevention") would produce abbreviations
    # nobody uses, which is noise in the results rather than a shortcut.
    caps = sum(1 for w in keep[1:] if w[0].isupper())
    if caps < 2 or caps < (len(keep) - 1) / 2:
        return ""
    out = ""
    for w in keep:
        out += w if w[0].isdigit() else w[0].upper()
    return out if 3 <= len(out) <= 7 and out.lower() != title.lower() else ""


out, counts, groups = [], {}, {}
for fn, label, code in PAGES:
    s = io.open(os.path.join(ROOT, fn), encoding="utf-8").read()
    m = re.search(r"^const ITEMS = (\[.*?\]);$", s, re.M | re.S)
    items = json.loads(m.group(1))
    g = re.search(r"^const GROUPS = (\[.*?\]);$", s, re.M | re.S)
    groups[code] = json.loads(g.group(1))
    counts[code] = len(items)
    for it in items:
        row = {"t": it["t"], "i": it["i"], "s": code, "g": it.get("g", "")}
        if it.get("f"): row["f"] = it["f"]
        if it.get("k"): row["k"] = it["k"]
        a = acronym(it["t"])
        if a: row["a"] = a
        out.append(row)

out.sort(key=lambda r: r["t"].lower())
io.open("index_all.json", "w", encoding="utf-8").write(json.dumps(out, separators=(",", ":")))
io.open("index_meta.json", "w", encoding="utf-8").write(json.dumps({"counts": counts, "groups": groups}, indent=1))
print("items:", len(out), "| bytes:", os.path.getsize("index_all.json"))
for fn, label, code in PAGES:
    print("  %-18s %4d  %d groups" % (label, counts[code], len(groups[code])))
