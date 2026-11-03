#!/usr/bin/env python3
"""
add-page.py — install a written page into the site.

    python3 _build/add-page.py ~/Downloads/acj.json

Validates the JSON against the actual article page, writes it to content/,
and updates content/index.json. Refuses to install anything malformed, so a
bad file from an AI can never quietly half-land.

Pass --force to install despite warnings (never despite errors).
"""
import json, io, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = set("p b i ul ol li sup table thead tbody tr th td code a div br strong em".split())
CAP = datetime.date.today().year + 1

VIDEO_CATEGORIES = {"anatomy", "pathology", "assessment", "special-tests", "rehabilitation"}
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def die(msg):
    print("\n  ERROR  " + msg)
    print("\nNothing was installed.\n")
    sys.exit(1)


def guess_page_id(data, path):
    """Match the file to one of the 1,054 article pages.

    An AI will hand back a filename like
    "9daee553-clinipd-acromioclavicular-joint-injury.json", which is not the
    page id. Score every page id by how many of its words appear in the
    filename and take a clear winner; otherwise show the candidates.
    """
    name = re.sub(r"[^a-z0-9]+", " ", os.path.basename(path).lower())
    words = set(w for w in name.split() if len(w) > 2)

    pages = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, "p")) if f.endswith(".html"))
    if not words:
        return None

    scored = []
    for pid in pages:
        toks = [t for t in pid.split("-") if len(t) > 2]
        if not toks:
            continue
        hit = sum(1 for t in toks if t in words)
        if hit:
            # reward covering the page id, and covering the filename
            scored.append((hit / len(toks) + hit / max(len(words), 1), hit, pid))

    if not scored:
        return None
    scored.sort(reverse=True)
    best = scored[0]
    runner = scored[1] if len(scored) > 1 else (0, 0, "")

    if best[1] >= 2 and best[0] - runner[0] > 0.18:
        return best[2]

    print("\n  Could not pick a page with confidence. Closest matches:")
    for sc, hit, pid in scored[:6]:
        print("      %s" % pid)
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if not args:
        die("give me the JSON file: python3 _build/add-page.py <file.json>")
    src = os.path.expanduser(args[0])
    if not os.path.exists(src):
        die("no such file: " + src)

    try:
        data = json.load(io.open(src, encoding="utf-8"))
    except Exception as e:
        die("that is not valid JSON — %s" % e)

    if "sections" not in data:
        die('no "sections" key in the file')

    pid = args[1] if len(args) > 1 else guess_page_id(data, src)
    if not pid:
        die("could not work out which page this is for.\n         "
            "Pass it explicitly:  python3 _build/add-page.py file.json <page-id>\n         "
            "The page id is printed at the bottom of the article page.")

    page_path = os.path.join(ROOT, "p", pid + ".html")
    if not os.path.exists(page_path):
        die("no article page called %s.html — check the page id" % pid)

    print("\n  Page      %s" % pid)
    print("  Source    %s" % src)

    # ---- section names, read off the real page ----
    page = io.open(page_path, encoding="utf-8").read()
    want = [m.replace("&amp;", "&") for m in
            re.findall(r'<h2><span class="sn">\d+</span>(.*?)</h2>', page)]
    got = list(data["sections"].keys())

    errors, warnings = [], []
    missing = [w for w in want if w not in got]
    extra = [g for g in got if g not in want]
    if extra:
        errors.append("section names the page does not have: %s" % ", ".join(extra))
    if missing:
        warnings.append("%d section(s) not written: %s" % (len(missing), ", ".join(missing)))
    empty = [k for k, v in data["sections"].items() if not str(v).strip()]
    if empty:
        warnings.append("%d section(s) empty: %s" % (len(empty), ", ".join(empty)))

    # ---- markup ----
    tags = set()
    for html in data["sections"].values():
        tags |= {t.lower() for t in re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)", str(html))}
    bad = sorted(tags - ALLOWED)
    if bad:
        errors.append("disallowed tags: %s" % ", ".join(bad))
    if re.search(r'\sstyle\s*=', json.dumps(data["sections"])):
        warnings.append("inline style= found — it will be ignored by the site CSS")

    # ---- citations ----
    refs = data.get("refs") or []
    sups = set()
    for html in data["sections"].values():
        for m in re.findall(r"<sup>([\d,\s]+)</sup>", str(html)):
            sups |= {int(n) for n in m.split(",") if n.strip()}
    over = sorted(n for n in sups if n > len(refs))
    if over:
        errors.append("superscript(s) %s point past the end of a %d-item reference list"
                      % (", ".join(map(str, over)), len(refs)))
    unused = sorted(set(range(1, len(refs) + 1)) - sups)
    if unused:
        warnings.append("reference(s) %s are never cited in the text"
                        % ", ".join(map(str, unused)))
    nodoi = [i + 1 for i, r in enumerate(refs) if not str(r.get("doi", "")).strip()]
    if nodoi:
        warnings.append("reference(s) %s have no DOI — you cannot verify those"
                        % ", ".join(map(str, nodoi)))
    if not refs:
        warnings.append("no references at all")

    nverify = sum(len(re.findall(r"\[verify", str(h), re.I)) for h in data["sections"].values())

    # ---- videos (optional top-level "videos" array) ----
    videos = data.get("videos") or []
    if not isinstance(videos, list):
        errors.append('"videos" must be a list')
        videos = []
    for i, v in enumerate(videos):
        if not isinstance(v, dict):
            errors.append("videos[%d] is not an object" % i)
            continue
        cat = v.get("category")
        if cat not in VIDEO_CATEGORIES:
            errors.append("videos[%d] category %r is not one of %s"
                          % (i, cat, ", ".join(sorted(VIDEO_CATEGORIES))))
        yid = v.get("youtubeId")
        if not yid or not YOUTUBE_ID_RE.match(str(yid)):
            errors.append("videos[%d] youtubeId %r is not a valid 11-character YouTube id "
                          "(paste the id from the URL, not the whole link)" % (i, yid))

    # ---- images (optional top-level "images" array) ----
    images = data.get("images") or []
    if not isinstance(images, list):
        errors.append('"images" must be a list')
        images = []
    img_dir = os.path.join(ROOT, "img", "conditions", pid)
    for i, im in enumerate(images):
        if not isinstance(im, dict):
            errors.append("images[%d] is not an object" % i)
            continue
        if im.get("section") not in want:
            errors.append("images[%d] section %r does not match any section on this page"
                          % (i, im.get("section")))
        f = im.get("file")
        if not f:
            errors.append("images[%d] has no file" % i)
        elif not os.path.isfile(os.path.join(img_dir, str(f))):
            errors.append("images[%d] file not found: img/conditions/%s/%s" % (i, pid, f))
        for field in ("alt", "credit", "sourceUrl", "licence"):
            if not str(im.get(field, "")).strip():
                errors.append("images[%d] is missing required field %r" % (i, field))

    # ---- newest source year (a page range looks exactly like a year) ----
    years = []
    for r in refs:
        ys = [int(y) for y in re.findall(r"\b(?:19|20)\d{2}\b", str(r.get("cite", "")))]
        ys = [y for y in ys if 1900 <= y <= CAP]
        if ys:
            years.append(max(ys))
    newest = max(years) if years else None

    # ---- report ----
    print("  Sections  %d of %d written" % (len(want) - len(missing) - len(empty), len(want)))
    print("  Refs      %d (%d cited, newest source %s)"
          % (len(refs), len(sups), newest or "unknown"))
    print("  Tables    %d" % sum(str(h).count('<table') for h in data["sections"].values()))
    if nverify:
        print("  Verify    %d figure(s) still marked [verify]" % nverify)
    if videos:
        print("  Videos    %d" % len(videos))
    if images:
        print("  Images    %d" % len(images))

    for w in warnings:
        print("\n  WARNING  " + w)
    for e in errors:
        print("\n  ERROR    " + e)

    if errors and not force:
        print("\nNothing was installed. Fix the errors above, or re-run with --force.\n")
        sys.exit(1)

    # ---- install ----
    out = os.path.join(ROOT, "content", pid + ".json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=1))

    man_path = os.path.join(ROOT, "content", "index.json")
    man = json.load(io.open(man_path, encoding="utf-8")) if os.path.exists(man_path) else {}
    prev = man.get(pid, {})
    man[pid] = {
        "status": prev.get("status", "draft"),
        "sections": len(want) - len(missing) - len(empty),
        "refs": len(refs),
        "newestSource": newest,
        "videos": len(videos),
        "images": len(images),
        "reviewed": prev.get("reviewed"),
        "reviewedBy": prev.get("reviewedBy"),
    }
    io.open(man_path, "w", encoding="utf-8").write(json.dumps(man, indent=1, sort_keys=True))

    print("\n  Installed content/%s.json" % pid)
    print("  Manifest updated — status is \"%s\"" % man[pid]["status"])
    written = sum(1 for v in man.values() if v.get("sections"))
    print("  %d page(s) written across the site\n" % written)
    print("  Next:")
    print("    1. open every DOI and check the numbers match the papers")
    if nverify:
        print("    2. resolve the %d [verify] marker(s) — they show in amber on the page" % nverify)
    print("    3. _build/deploy.sh\n")


main()
