"""Shared helpers for the futuristic README SVG set.

Fonts are renamed OFL subsets embedded as base64 woff2, so the SVGs render
with the intended typefaces inside GitHub's <img> sandbox (which cannot load
external resources). Every text run is checked against its font's cmap.
"""
import base64
import html
import io
import os
import re

from fontTools import subset as ftsubset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# key -> (family, file stem, css weight, fallback stack)
FONTS = {
    "o9": ("NeoOrbitBlack", "orbit900", 900, "'Arial Black',Helvetica,Arial,sans-serif"),
    "o7": ("NeoOrbit", "orbit700", 700, "'Segoe UI',Helvetica,Arial,sans-serif"),
    "m": ("NeoMono", "mono", 400, "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"),
    "s": ("NeoSans", "sans600", 600, "'Segoe UI',Helvetica,Arial,sans-serif"),
    "sb": ("NeoSansBold", "sans700", 700, "'Segoe UI',Helvetica,Arial,sans-serif"),
}

LICENSE = (
    "<!-- Typefaces: renamed subsets embedded under the SIL Open Font License 1.1 "
    "(https://openfontlicense.org). Orbitron: Copyright 2018 The Orbitron Project Authors "
    "(https://github.com/theleagueof/orbitron), Reserved Font Name \"Orbitron\". "
    "Share Tech Mono: Copyright (c) 2012 Carrois Type Design, Ralph du Carrois, "
    "Reserved Font Name \"Share\". Rajdhani: Copyright (c) 2014 Indian Type Foundry. -->"
)

# Palette
CYAN = "#00F0FF"
MAGENTA = "#FF2BD6"
VIOLET = "#8A5CFF"
AMBER = "#FFC857"
LIME = "#39FF88"
ORANGE = "#FF7A45"
INK = "#EAF6FF"
DIM = "#8FA3C7"
SOFT = "#B9C3E6"
BG = "#0A0A22"
BG2 = "#0D0B2E"


class Metric:
    def __init__(self, key):
        fam, stem, _, _ = FONTS[key]
        f = TTFont(os.path.join(FONT_DIR, stem + ".ttf"))
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        self.key = key

    def has(self, ch):
        return ord(ch) in self.cmap

    def adv(self, ch):
        g = self.cmap.get(ord(ch), ".notdef")
        return self.hmtx[g][0]

    def width(self, text, size, ls=0.0):
        """Rendered width of the ink run (letter-spacing between glyphs only)."""
        if not text:
            return 0.0
        units = sum(self.adv(c) for c in text)
        return units * size / self.upm + ls * (len(text) - 1)


METRICS = {k: Metric(k) for k in FONTS}


def check(key, text):
    m = METRICS[key]
    missing = sorted({c for c in text if not m.has(c)})
    if missing:
        raise ValueError(f"font {key} lacks {missing!r} in {text!r}")


def W(key, text, size, ls=0.0):
    return METRICS[key].width(text, size, ls)


def esc(s):
    return html.escape(s, quote=True)


_SUBSET_CACHE = {}


def subset_b64(key, chars):
    """woff2 (base64) of font `key` cut down to exactly `chars`."""
    ck = (key, "".join(sorted(chars)))
    if ck in _SUBSET_CACHE:
        return _SUBSET_CACHE[ck]
    fam, stem, _, _ = FONTS[key]
    font = TTFont(os.path.join(FONT_DIR, stem + ".ttf"), recalcTimestamp=False)  # deterministic output
    opts = ftsubset.Options()
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    opts.layout_features = ["kern", "liga"]
    opts.notdef_outline = True
    sub = ftsubset.Subsetter(opts)
    sub.populate(text="".join(chars))
    sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    _SUBSET_CACHE[ck] = b64
    return b64


def used_chars(markup):
    chars = {" "}
    for m in re.finditer(r"<text\b[^>]*>(.*?)</text>", markup, re.S):
        chars |= set(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))))
    return chars


def font_css(keys, chars):
    out = []
    for k in keys:
        fam, stem, weight, fb = FONTS[k]
        b64 = subset_b64(k, chars)
        out.append(
            f"@font-face{{font-family:'{fam}';font-weight:{weight};font-style:normal;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
        )
        out.append(f".{k}{{font-family:'{fam}',{fb};font-weight:{weight}}}")
    return "".join(out)


def T(x, y, s, f, size, fill, ls=0, anchor="start", extra="", cls=""):
    """A text element. Centered text is nudged by ls/2 to cancel the trailing
    letter-spacing browsers add after the final glyph."""
    check(f, s)
    if anchor == "middle" and ls:
        x = x + ls / 2
    if anchor == "end" and ls:
        x = x + ls
    c = f"{f} {cls}".strip()
    attrs = f'x="{x:.1f}" y="{y:.1f}" class="{c}" font-size="{size}" fill="{fill}"'
    if ls:
        attrs += f' letter-spacing="{ls}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    if "  " in s or s != s.strip():
        attrs += ' xml:space="preserve" style="white-space:pre"'
    if extra:
        attrs += " " + extra
    return f"<text {attrs}>{esc(s)}</text>"


def wrap(text, f, size, max_w, ls=0):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if W(f, trial, size, ls) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


BASE_CSS = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def doc(w, h, title, desc, fonts, css, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" fill="none">\n'
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>\n'
        f"{LICENSE}\n"
        f"<style>{font_css(fonts, used_chars(body + defs))}{BASE_CSS}{css}</style>\n"
        f"<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


def f1(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- vehicles

def car_symbol(sid="car", body_a="#F2F7FF", body_b="#8E9BD6", neon=CYAN, tail=MAGENTA):
    """A sleek hover car facing right, centred near (0,0), ~66 x 22 units."""
    return f"""
<linearGradient id="{sid}B" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{body_a}"/><stop offset="1" stop-color="{body_b}"/>
</linearGradient>
<linearGradient id="{sid}G" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#E6FDFF"/><stop offset="1" stop-color="{neon}" stop-opacity=".55"/>
</linearGradient>
<linearGradient id="{sid}T" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{tail}" stop-opacity="0"/><stop offset="1" stop-color="{tail}" stop-opacity=".85"/>
</linearGradient>
<linearGradient id="{sid}L" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
<radialGradient id="{sid}U"><stop offset="0" stop-color="{neon}" stop-opacity=".95"/><stop offset="1" stop-color="{neon}" stop-opacity="0"/></radialGradient>
<g id="{sid}">
  <path d="M-120,1.5 H-31 V5.5 H-120 Z" fill="url(#{sid}T)"/>
  <ellipse cx="-13" cy="12.5" rx="13" ry="3.6" fill="url(#{sid}U)"/>
  <ellipse cx="18" cy="12.5" rx="13" ry="3.6" fill="url(#{sid}U)"/>
  <path d="M-31,4 C-29,-3 -17,-8 -3,-8 L13,-7.5 C24,-6.5 32,-2.5 34.5,2.5 C35.5,6.5 31.5,9 26,9 L-27,9 C-31,9 -32,7 -31,4 Z" fill="url(#{sid}B)"/>
  <path d="M-9,-7.6 C-3,-13 11,-13 20,-6.6 L13,-7.1 Z" fill="url(#{sid}G)"/>
  <path d="M-25,3 H22" stroke="{neon}" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M35,2 L130,-12 L130,16 Z" fill="url(#{sid}L)" opacity=".5"/>
  <circle cx="33.6" cy="2.4" r="1.9" fill="#FFFFFF"/>
  <rect x="-32" y="1.6" width="3" height="3.6" rx="1" fill="{tail}"/>
</g>"""


def train_symbol(sid="train"):
    return f"""
<linearGradient id="{sid}B" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F5FAFF"/><stop offset="1" stop-color="#8C9CD8"/>
</linearGradient>
<linearGradient id="{sid}T" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".7"/>
</linearGradient>
<g id="{sid}">
  <rect x="-170" y="3" width="160" height="5" fill="url(#{sid}T)"/>
  <path d="M-10,0 H190 C214,0 232,6 238,14 H-10 Z" fill="url(#{sid}B)"/>
  <path d="M0,4 H186" stroke="{CYAN}" stroke-width="3.2" stroke-dasharray="14 4"/>
  <path d="M196,4 C210,4 220,7 226,11 H196 Z" fill="{CYAN}" opacity=".9"/>
  <path d="M-10,14 H238" stroke="{MAGENTA}" stroke-width="1.4"/>
  <path d="M62,0 V14 M126,0 V14" stroke="#5C6AA8" stroke-width="1"/>
</g>"""


def hex_points(cx, cy, r, rot=30):
    import math
    pts = []
    for i in range(6):
        a = math.radians(60 * i + rot)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return len(content.encode("utf-8"))
