#!/usr/bin/env python3
"""Generate 10 colour schemes (light + dark) with contrast verified, not guessed."""
import colorsys, io, json

# ---------- colour helpers ----------
def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(r, g, b):
    return "#%02X%02X%02X" % (max(0, min(255, round(r))),
                              max(0, min(255, round(g))),
                              max(0, min(255, round(b))))

def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = hex2rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def shift(h, dl=0.0, ds=0.0):
    """Nudge lightness / saturation in HLS space."""
    r, g, b = [v / 255 for v in hex2rgb(h)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = max(0.0, min(1.0, ll + dl))
    ss = max(0.0, min(1.0, ss + ds))
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return rgb2hex(r * 255, g * 255, b * 255)

def mix(a, b, t):
    """Blend b into a by t (0..1) — far more controllable than shifting lightness."""
    ra, ga, ba = hex2rgb(a); rb, gb, bb = hex2rgb(b)
    return rgb2hex(ra + (rb - ra) * t, ga + (gb - ga) * t, ba + (bb - ba) * t)

def darken_until(fg, bg, target, step=0.02, limit=60):
    """Walk a colour darker until it clears `target` contrast on bg."""
    out = fg
    for _ in range(limit):
        if contrast(out, bg) >= target:
            return out
        out = shift(out, dl=-step)
    return out

def lighten_until(fg, bg, target, step=0.02, limit=60):
    out = fg
    for _ in range(limit):
        if contrast(out, bg) >= target:
            return out
        out = shift(out, dl=step)
    return out

# ---------- the ten ----------
# id, name, note, base hue colours (brand, accent, deep ink)
SCHEMES = [
 ("",          "Clinical",  "Teal · the default",      "#0A7E70", "#F0674F", "#0C2F2B"),
 ("slate",     "Slate",     "Cool, institutional",     "#2563A8", "#D9624E", "#16222E"),
 ("warm",      "Warm",      "Paper and ink",           "#8A5A2B", "#B8452F", "#2A2318"),
 ("contrast",  "Contrast",  "Maximum legibility",      "#00563F", "#B3200E", "#000000"),
 ("indigo",    "Indigo",    "Deep blue-violet",        "#4A4FB5", "#E0634B", "#1B1C38"),
 ("forest",    "Forest",    "Dark green, natural",     "#2F6B41", "#C66A2E", "#17251B"),
 ("plum",      "Plum",      "Purple, editorial",       "#6D3B8E", "#D4557A", "#241530"),
 ("crimson",   "Crimson",   "Red, high energy",        "#A8323C", "#1F6F7A", "#2B1416"),
 ("ocean",     "Ocean",     "Cyan and navy",           "#0E6E8C", "#E07A3E", "#0E2430"),
 ("graphite",  "Graphite",  "Neutral, one accent",     "#44505C", "#C9512F", "#1A1E22"),
]

AA = 4.5          # WCAG AA for normal text
AA_LARGE = 3.0    # for big display text / UI

def build_light(brand, coral, deep):
    bg    = "#FFFFFF"
    ink   = darken_until(deep, bg, 12.0)
    ink2  = darken_until(shift(deep, dl=.18), bg, 7.0)
    muted = darken_until(shift(deep, dl=.38, ds=-.18), bg, AA)
    bg2   = mix(bg, brand, .035)
    bg3   = mix(bg, brand, .085)
    line  = mix(bg, brand, .13)
    line2 = mix(bg, brand, .26)
    b     = darken_until(brand, bg, AA)              # white text sits on it
    bink  = darken_until(brand, bg, 7.0)
    bsoft = mix(bg, brand, .12)
    c     = darken_until(coral, bg, AA)
    cink  = darken_until(coral, bg, 6.0)
    csoft = mix(bg, coral, .11)
    ok    = darken_until("#1D8A5C", bg, AA)
    warn  = darken_until("#9A6714", bg, AA)
    wsoft = mix(bg, "#9A6714", .11)
    return dict(ink=ink, ink2=ink2, muted=muted, bg=bg, bg2=bg2, bg3=bg3,
                line=line, line2=line2, brand=b, brand_ink=bink, brand_soft=bsoft,
                deep=darken_until(deep, bg, 14.0), coral=c, coral_ink=cink, coral_soft=csoft,
                ok=ok, warn=warn, warn_soft=wsoft,
                on_brand="#FFFFFF", on_coral="#FFFFFF")

def build_dark(brand, coral, deep):
    bg    = shift(deep, dl=-.06, ds=.02)
    if lum(bg) > 0.05: bg = shift(bg, dl=-.10)
    bg2   = mix(bg, "#FFFFFF", .045)
    bg3   = mix(bg, "#FFFFFF", .085)
    ink   = lighten_until(shift(brand, dl=.46, ds=-.56), bg, 11.0)
    ink2  = lighten_until(shift(brand, dl=.34, ds=-.44), bg, 6.5)
    muted = lighten_until(shift(brand, dl=.22, ds=-.34), bg, AA)
    line  = mix(bg, "#FFFFFF", .10)
    line2 = mix(bg, "#FFFFFF", .19)
    b     = lighten_until(brand, bg, AA + 1.0)
    bink  = lighten_until(brand, bg, 7.5)
    bsoft = mix(bg, brand, .17)
    c     = lighten_until(coral, bg, AA + 0.6)
    cink  = lighten_until(coral, bg, 6.5)
    csoft = mix(bg, coral, .15)
    ok    = lighten_until("#1D8A5C", bg, AA)
    warn  = lighten_until("#9A6714", bg, AA)
    wsoft = mix(bg, "#9A6714", .15)
    # in dark mode the brand is a LIGHT colour, so text on it must be dark
    on_b = darken_until(bg, b, 7.0)
    on_c = darken_until(bg, c, 7.0)
    return dict(ink=ink, ink2=ink2, muted=muted, bg=bg, bg2=bg2, bg3=bg3,
                line=line, line2=line2, brand=b, brand_ink=bink, brand_soft=bsoft,
                deep=shift(bg, dl=-.03), coral=c, coral_ink=cink, coral_soft=csoft,
                ok=ok, warn=warn, warn_soft=wsoft,
                on_brand=on_b, on_coral=on_c)

KEYS = [("ink","--ink"),("ink2","--ink-2"),("muted","--muted"),
        ("bg","--bg"),("bg2","--bg-2"),("bg3","--bg-3"),
        ("line","--line"),("line2","--line-2"),
        ("brand","--brand"),("brand_ink","--brand-ink"),("brand_soft","--brand-soft"),
        ("deep","--deep"),("coral","--coral"),("coral_ink","--coral-ink"),("coral_soft","--coral-soft"),
        ("ok","--ok"),("warn","--warn"),("warn_soft","--warn-soft"),
        ("on_brand","--on-brand"),("on_coral","--on-coral")]

def block(d, indent="  "):
    return "\n".join("%s%s:%s;" % (indent, css, d[k]) for k, css in KEYS)

out = ["""
/* ============================================================
   COLOUR SCHEMES — generated, with contrast verified
   Ten palettes, each with a light and a dark variant.
   Switched by data-scheme on <html>; site.js persists it.
   Do not hand-edit: re-run scratchpad/gen_schemes.py.
   ============================================================ */"""]

report = []
for sid, name, note, brand, coral, deep in SCHEMES:
    L = build_light(brand, coral, deep)
    D = build_dark(brand, coral, deep)
    sel = ':root[data-scheme="%s"]' % sid if sid else ":root"
    if sid:
        out.append("\n/* ---- %s — %s ---- */\n%s{\n%s\n}" % (name, note, sel, block(L)))
        out.append('@media (prefers-color-scheme:dark){\n  :root[data-scheme="%s"]:not([data-theme="light"]){\n%s\n  }\n}'
                   % (sid, block(D, "    ")))
        out.append(':root[data-scheme="%s"][data-theme="dark"]{\n%s\n}' % (sid, block(D)))
    else:
        out.append("\n/* ---- %s — %s (the base) ---- */\n:root{\n%s\n}" % (name, note, block(L)))
        out.append('@media (prefers-color-scheme:dark){\n  :root:not([data-theme="light"]):not([data-scheme]){\n%s\n  }\n}'
                   % block(D, "    "))
        out.append(':root[data-theme="dark"]:not([data-scheme]){\n%s\n}' % block(D))

    for mode, d in (("light", L), ("dark", D)):
        checks = {
            "body text": contrast(d["ink"], d["bg"]),
            "secondary": contrast(d["ink2"], d["bg"]),
            "muted":     contrast(d["muted"], d["bg"]),
            "brand btn": contrast(d["on_brand"], d["brand"]),
            "coral btn": contrast(d["on_coral"], d["coral"]),
            "brand link":contrast(d["brand_ink"], d["bg"]),
            "coral":     contrast(d["coral_ink"], d["bg"]),
        }
        report.append((name, mode, checks))

io.open("/home/claude/clinipd/_build/schemes.css",
        "w", encoding="utf-8").write("\n".join(out) + "\n")

bad = 0
print("%-10s %-6s " % ("scheme", "mode") + "  ".join("%-10s" % k for k in
      ["body","second","muted","btn","cbtn","link","coral"]))
for name, mode, c in report:
    vals = [c["body text"], c["secondary"], c["muted"], c["brand btn"], c["coral btn"], c["brand link"], c["coral"]]
    flag = "" if all(v >= 4.5 for v in vals) else "  <-- CHECK"
    if flag: bad += 1
    print("%-10s %-6s " % (name, mode) + "  ".join("%-10.2f" % v for v in vals) + flag)
print("\nschemes:", len(SCHEMES), "| rows failing AA:", bad)

io.open("/home/claude/clinipd/_build/schemes.json",
        "w", encoding="utf-8").write(json.dumps(
    [{"id": s[0], "name": s[1], "note": s[2],
      "sw": [build_light(s[3], s[4], s[5])["brand"],
             build_light(s[3], s[4], s[5])["coral"],
             build_light(s[3], s[4], s[5])["deep"],
             build_light(s[3], s[4], s[5])["bg2"]]} for s in SCHEMES], indent=1))
