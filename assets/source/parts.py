"""Typing strip, section headers, identity terminal, career transit map,
skill matrix, project cards, comms buttons and the skyway footer."""
import random

from lib import (AMBER, BG, BG2, CYAN, DIM, INK, LIME, MAGENTA, ORANGE, SOFT,
                 VIOLET, T, W, car_symbol, doc, hex_points, wrap)

rnd = random.Random(7)


def pct(t, total):
    return f"{t / total * 100:.3f}".rstrip("0").rstrip(".")


# ======================================================================= typing
def typing():
    WD, HT = 1200, 72
    phrases = [
        "designing AI content that makes learning click",
        "turning maths lessons into playable worlds",
        "crafting 3D storybooks with games inside",
        "designs that ship as real, working code",
        "design × technology × storytelling",
    ]
    size = 22
    prompt = "aniket@neo-delhi:~$"
    pw = W("m", prompt + " ", size)
    widths = [W("m", p, size) for p in phrases]
    maxw = max(widths)
    x0 = (WD - (pw + maxw + 14)) / 2
    xp = x0 + pw
    D = 4.6
    TT = D * len(phrases)
    css = [".cr{animation:cr 1s steps(1) infinite}@keyframes cr{0%,50%{opacity:1}51%,100%{opacity:0}}",
           ".lv{animation:lv 1.4s ease-in-out infinite alternate}@keyframes lv{from{opacity:.3}to{opacity:1}}"]
    groups = []
    for i, (p, w) in enumerate(zip(phrases, widths)):
        n = len(p)
        s = i * D
        t_type = min(2.3, n * 0.055)
        p0, p1 = pct(s, TT), pct(s + t_type, TT)
        p2, p3 = pct(s + D - 0.95, TT), pct(s + D - 0.35, TT)
        pe = s + D
        if i == 0:
            vis = f"0%,{pct(pe - 0.01, TT)}%{{opacity:1}}{pct(pe, TT)}%,100%{{opacity:0}}"
        elif i == len(phrases) - 1:
            vis = f"0%,{pct(s - 0.01, TT)}%{{opacity:0}}{p0}%,99.99%{{opacity:1}}100%{{opacity:0}}"
        else:
            vis = (f"0%,{pct(s - 0.01, TT)}%{{opacity:0}}{p0}%,{pct(pe - 0.01, TT)}%{{opacity:1}}"
                   f"{pct(pe, TT)}%,100%{{opacity:0}}")
        start = "0%" if i == 0 else f"0%,{p0}%"
        css.append(f"@keyframes v{i}{{{vis}}}.v{i}{{animation:v{i} {TT}s linear infinite}}")
        css.append(f"@keyframes c{i}{{{start}{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
                   f"{p1}%,{p2}%{{transform:translateX({w:.2f}px);animation-timing-function:steps({n},end)}}"
                   f"{p3}%,100%{{transform:translateX(0)}}}}.c{i}{{animation:c{i} {TT}s linear infinite}}")
        groups.append(f'<g class="v{i}">{T(xp, 44, p, "m", size, CYAN)}'
                      f'<g class="c{i}"><rect x="{xp - 1:.1f}" y="15" width="{maxw + 70:.1f}" height="42" fill="url(#tbg)"/>'
                      f'<rect x="{xp + 1:.1f}" y="24" width="11" height="24" fill="{CYAN}" class="cr"/></g></g>')
    defs = f"""<linearGradient id="tbg" x1="0" y1="0" x2="0" y2="{HT}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#0E0B30"/><stop offset="1" stop-color="#08061C"/></linearGradient>
<linearGradient id="tst" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>"""
    body = f"""
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="14" fill="url(#tbg)"/>
<circle cx="28" cy="36" r="5" fill="{MAGENTA}"/><circle cx="46" cy="36" r="5" fill="{AMBER}"/><circle cx="64" cy="36" r="5" fill="{CYAN}"/>
{T(x0, 44, prompt, "m", size, "#FF7AE6")}
{''.join(groups)}
<circle cx="1124" cy="36" r="4.5" fill="{LIME}" class="lv"/>
{T(1136, 41, "LIVE", "m", 13, LIME, ls=2)}
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="14" stroke="url(#tst)" stroke-opacity=".7" stroke-width="1.5"/>
"""
    return doc(WD, HT, "Typing terminal",
               "A terminal line typing: " + " · ".join(phrases), ["m"], "".join(css), body, defs)


# ====================================================================== headers
SECTIONS = [
    ("01", "IDENTITY SCAN", "// about the human behind the hologram", CYAN, "identity"),
    ("02", "CAREER ROUTE", "// experience and education on one transit map", MAGENTA, "career"),
    ("03", "SKILL MATRIX", "// modules installed in this unit", VIOLET, "skills"),
    ("04", "PROJECT CITY", "// featured builds · tap a card to launch it", AMBER, "projects"),
    ("05", "ARCADE DISTRICT", "// 3D storybooks and mini learning games", LIME, "arcade"),
    ("06", "TELEMETRY", "// live signal from my github", CYAN, "telemetry"),
    ("07", "COMMS LINK", "// open a channel · let's build the future", MAGENTA, "comms"),
]


def header(num, title, sub, acc):
    WD, HT = 1200, 96
    tsize, tls = 30, 4
    tw = W("o7", title, tsize, tls)
    lx0, lx1 = 112 + tw + 30, 1010
    ticks = "".join(f"M{x},46V50" for x in range(int(lx0) + 14, lx1 - 4, 22))
    bars = []
    for i in range(7):
        d = 0.55 + rnd.random() * 0.7
        bars.append(f'<rect x="{1046 + i * 16}" y="44" width="9" height="28" rx="2" fill="{acc}" class="eq" '
                    f'style="animation-duration:{d:.2f}s;animation-delay:-{rnd.random():.2f}s"/>')
    css = (".eq{transform-box:fill-box;transform-origin:50% 100%;animation:eq .8s ease-in-out infinite alternate}"
           "@keyframes eq{from{transform:scaleY(.22)}to{transform:scaleY(1)}}"
           f".pk{{animation:pk 3.4s linear infinite}}@keyframes pk{{0%{{transform:translateX(0);opacity:0}}"
           f"8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateX({lx1 - lx0:.0f}px);opacity:0}}}}"
           ".sw{animation:sw 6s ease-in-out infinite}@keyframes sw{0%{transform:translateX(-300px)}60%,100%{transform:translateX(1500px)}}"
           ".hb{animation:hb 2.2s ease-in-out infinite alternate}@keyframes hb{from{opacity:.35}to{opacity:1}}")
    defs = f"""<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#110C38"/><stop offset=".6" stop-color="#0B0A26"/><stop offset="1" stop-color="#0A0A22"/></linearGradient>
<linearGradient id="swg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".09"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{acc}" stop-opacity=".9"/><stop offset="1" stop-color="{acc}" stop-opacity=".1"/></linearGradient>
<clipPath id="hc"><rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="16"/></clipPath>"""
    body = f"""
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="16" fill="url(#hbg)"/>
<g clip-path="url(#hc)"><g class="sw"><rect x="0" y="-10" width="170" height="120" fill="url(#swg)" transform="skewX(-22)"/></g></g>
<path d="M18,22 V74" stroke="{acc}" stroke-width="3" stroke-linecap="round"/>
<polygon points="{hex_points(66, 48, 29)}" fill="#120A35" stroke="{acc}" stroke-width="2"/>
<polygon points="{hex_points(66, 48, 22)}" stroke="{acc}" stroke-opacity=".35" stroke-width="1" class="hb"/>
{T(66, 55.5, num, "o7", 19, acc, anchor="middle")}
{T(112, 54, title, "o7", tsize, "none", ls=tls, extra=f'stroke="{acc}" stroke-opacity=".28" stroke-width="6" stroke-linejoin="round"')}
{T(112, 54, title, "o7", tsize, INK, ls=tls)}
{T(114, 79, sub, "m", 14, DIM, ls=1)}
<path d="M{lx0:.0f},43 H{lx1}" stroke="url(#ln)" stroke-width="1.5"/>
<path d="{ticks}" stroke="{acc}" stroke-opacity=".35"/>
<circle cx="{lx0:.0f}" cy="43" r="3.2" fill="{acc}" class="pk"/>
{T(1046, 34, "SIGNAL", "m", 10, DIM, ls=2)}
{''.join(bars)}
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="16" stroke="{acc}" stroke-opacity=".5" stroke-width="1.5"/>
"""
    return doc(WD, HT, f"{num} · {title.title()}", sub.lstrip("/ "), ["o7", "m"], css, body, defs)


# ===================================================================== identity
def identity():
    WD, HT = 1200, 400
    # ---- holo ID card (left)
    cx, cy = 210, 148
    card = f"""
<path d="M54,30 H390 V346 L366,370 H30 V54 Z" fill="url(#cardG)" stroke="{CYAN}" stroke-opacity=".55" stroke-width="1.5"/>
<path d="M30,54 L54,30" stroke="{CYAN}" stroke-width="2"/>
{T(52, 58, "CITIZEN ID // NEO-DELHI", "m", 11, CYAN, ls=2, extra='opacity=".8"')}
<circle cx="{cx}" cy="{cy}" r="86" stroke="{CYAN}" stroke-opacity=".5" stroke-width="1.2" stroke-dasharray="3 7" class="spin"/>
<circle cx="{cx}" cy="{cy}" r="78" stroke="{MAGENTA}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="40 14" class="spinR"/>
<polygon points="{hex_points(cx, cy, 66, 0)}" fill="url(#hexG)" stroke="url(#hexS)" stroke-width="2.2"/>
<g clip-path="url(#hexClip)">
  <path d="M{cx - 66},{cy} H{cx + 66} M{cx},{cy - 66} V{cy + 66}" stroke="{CYAN}" stroke-opacity=".08"/>
  <rect x="{cx - 70}" y="{cy - 70}" width="140" height="10" fill="url(#scanV)" class="scanY"/>
</g>
{T(cx, cy + 20, "AC", "o9", 58, "none", ls=2, anchor="middle", extra=f'stroke="{CYAN}" stroke-opacity=".3" stroke-width="7" stroke-linejoin="round"')}
{T(cx, cy + 20, "AC", "o9", 58, "url(#acG)", ls=2, anchor="middle")}
{T(cx, 266, "ANIKET CHAUHAN", "o7", 19, INK, ls=2, anchor="middle")}
{T(cx, 290, "AI CONTENT DESIGNER · UI/UX", "m", 12, CYAN, ls=2, anchor="middle")}
"""
    stats = [("2+", "YRS DESIGN"), ("17", "LIVE BUILDS"), ("25", "DESIGN STUDIES")]
    sx = [90, 210, 330]
    for (big, small), x in zip(stats, sx):
        card += T(x, 330, big, "o7", 20, MAGENTA, anchor="middle")
        card += T(x, 348, small, "m", 9.5, DIM, ls=1.5, anchor="middle")
    card += '<path d="M150,316 V350 M270,316 V350" stroke="#2A2F6A"/>'

    # ---- terminal (right)
    tx0, ty0, tx1, ty1 = 420, 30, 1170, 370
    size, lh = 15, 25
    lines = [
        ("cmd", "whoami"),
        ("out", "Aniket Chauhan — AI Content & UI/UX Designer @ ConveGenius.AI"),
        ("cmd", "cat mission.txt"),
        ("out", "Make learning more engaging through design + technology."),
        ("cmd", "ls ~/worlds"),
        ("out", "ai-content/  ui-ux/  graphics/  learning-games/  3d-storybooks/"),
        ("cmd", "cat motto.txt"),
        ("out", "\"I build digital experiences where design, technology"),
        ("out", " and storytelling become one.\""),
        ("cmd", "status --now"),
        ("live", "Building playable maths worlds for classrooms"),
    ]
    lx = tx0 + 28
    y = ty0 + 66
    TT = 26.0
    t = 0.6
    css = [".cr{animation:cr 1s steps(1) infinite}@keyframes cr{0%,50%{opacity:1}51%,100%{opacity:0}}",
           ".spin{transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite}"
           ".spinR{transform-box:fill-box;transform-origin:center;animation:spin 16s linear infinite reverse}"
           "@keyframes spin{to{transform:rotate(360deg)}}",
           ".scanY{animation:scanY 3.2s linear infinite}@keyframes scanY{from{transform:translateY(0)}to{transform:translateY(140px)}}",
           ".lv{animation:lv 1.2s ease-in-out infinite alternate}@keyframes lv{from{opacity:.35}to{opacity:1}}",
           f".tg{{animation:tg {TT}s linear infinite}}@keyframes tg{{0%,95%{{opacity:1}}97.5%,100%{{opacity:0}}}}"]
    rows, covers = [], []
    for i, (kind, txt) in enumerate(lines):
        if kind == "cmd":
            full = "$ " + txt
            rows.append(T(lx, y, "$", "m", size, "#FF7AE6") + T(lx + W("m", "$ ", size), y, txt, "m", size, INK))
            n = len(full)
            dur = n * 0.07
            tf = f"steps({n},end)"
        elif kind == "out":
            full = "  " + txt
            rows.append(T(lx, y, full, "m", size, "#9EF7FF"))
            dur = 0.45
            tf = "linear"
        else:
            full = "  ● " + txt
            dot_x = lx + W("m", "  ", size) + 5
            rows.append(f'<circle cx="{dot_x:.1f}" cy="{y - 5}" r="4.5" fill="{LIME}" class="lv"/>'
                        + T(lx + W("m", "    ", size), y, txt, "m", size, LIME))
            caret_x = lx + W("m", "    " + txt, size) + 5
            rows.append(f'<rect x="{caret_x:.1f}" y="{y - 13}" width="9" height="16" fill="{LIME}" class="cr"/>')
            dur = 0.5
            tf = "linear"
        width = (W("m", full, size) if kind != "live" else W("m", "    " + txt, size) + 18) + 10
        a, b = pct(t, TT), pct(t + dur, TT)
        css.append(f"@keyframes k{i}{{0%,{a}%{{transform:translateX(0);animation-timing-function:{tf}}}"
                   f"{b}%,100%{{transform:translateX({width:.1f}px)}}}}.k{i}{{animation:k{i} {TT}s linear infinite}}")
        covers.append(f'<rect x="{lx - 2}" y="{y - 18}" width="{tx1 - lx + 40}" height="{lh}" fill="#070A1C" class="k{i}"/>')
        t += dur + (0.35 if kind == "cmd" else 0.25)
        y += lh
    term = f"""
<rect x="{tx0}" y="{ty0}" width="{tx1 - tx0}" height="{ty1 - ty0}" rx="12" fill="#070A1C" stroke="#2A2F6A" stroke-width="1.5"/>
<path d="M{tx0 + 12},{ty0} H{tx1 - 12} A12,12 0 0 1 {tx1},{ty0 + 12} V{ty0 + 34} H{tx0} V{ty0 + 12} A12,12 0 0 1 {tx0 + 12},{ty0} Z" fill="#0E1230"/>
<circle cx="{tx0 + 22}" cy="{ty0 + 17}" r="5" fill="{MAGENTA}"/><circle cx="{tx0 + 40}" cy="{ty0 + 17}" r="5" fill="{AMBER}"/><circle cx="{tx0 + 58}" cy="{ty0 + 17}" r="5" fill="{CYAN}"/>
{T((tx0 + tx1) / 2, ty0 + 22, "aniket@neo-delhi: ~/profile", "m", 13, DIM, ls=1, anchor="middle")}
<g clip-path="url(#termClip)"><g class="tg">{''.join(rows)}{''.join(covers)}</g></g>
<rect x="{tx0}" y="{ty0}" width="{tx1 - tx0}" height="{ty1 - ty0}" rx="12" stroke="url(#termS)" stroke-width="1.5"/>
"""
    defs = f"""
<linearGradient id="cardG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#120D3A"/><stop offset="1" stop-color="#090720"/></linearGradient>
<radialGradient id="hexG" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#2A1A6E"/><stop offset="1" stop-color="#0B0828"/></radialGradient>
<linearGradient id="hexS" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
<linearGradient id="acG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#B9F6FF"/></linearGradient>
<linearGradient id="scanV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".45"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="termS" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".7"/><stop offset=".5" stop-color="{VIOLET}" stop-opacity=".4"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity=".7"/></linearGradient>
<clipPath id="hexClip"><polygon points="{hex_points(cx, cy, 64, 0)}"/></clipPath>
<clipPath id="termClip"><rect x="{tx0 + 2}" y="{ty0 + 36}" width="{tx1 - tx0 - 4}" height="{ty1 - ty0 - 38}"/></clipPath>
"""
    body = f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="{BG}"/>' \
           f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="url(#gridP)"/>{card}{term}' \
           f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" stroke="#232A5C" stroke-width="1.5"/>'
    defs += ('<pattern id="gridP" width="40" height="40" patternUnits="userSpaceOnUse">'
             '<path d="M40,0 H0 V40" stroke="#1A1F4A" stroke-opacity=".7"/></pattern>')
    return doc(WD, HT, "Identity scan — Aniket Chauhan",
               "Holographic ID card (AC monogram, AI Content Designer and UI/UX; 2+ years in design, 17 live builds, "
               "25 design studies) beside a terminal: whoami → Aniket Chauhan, AI Content & UI/UX Designer @ ConveGenius.AI; "
               "mission → make learning more engaging through design + technology; motto → I build digital "
               "experiences where design, technology and storytelling become one; status → building playable "
               "maths worlds for classrooms.",
               ["o9", "o7", "m"], "".join(css), body, defs)


# ======================================================================= career
def career():
    WD, HT = 1200, 470
    LY, EY = 152, 374
    stations = [
        dict(x=200, date="JUN 2024 — APR 2025", role="GRAPHIC DESIGNER", org="CCIE HUB · DELHI",
             desc=["Social posts, stories & promos,", "content scheduling + tracking"]),
        dict(x=580, date="MAY 2025 — NOV 2025", role="GRAPHIC DESIGNER", org="CONVEGENIUS.AI · NOIDA",
             desc=["Social creatives, UI/UX designs", "and campaign graphics"]),
        dict(x=960, date="NOV 2025 — PRESENT", role="AI CONTENT DESIGNER", org="CONVEGENIUS.AI · NOIDA",
             desc=["UI/UX design + AI-powered content", "for engaging learning experiences"], now=True),
    ]
    out = []
    # lines
    out.append(f'<path d="M60,{LY} H1040" stroke="{CYAN}" stroke-opacity=".18" stroke-width="12" stroke-linecap="round"/>')
    out.append(f'<path d="M60,{LY} H1040" stroke="{CYAN}" stroke-width="4" stroke-linecap="round"/>')
    out.append(f'<path d="M1052,{LY} H1140" stroke="{CYAN}" stroke-width="3" stroke-dasharray="6 8" class="flow"/>')
    out.append(f'<path d="M1140,{LY - 8} L1152,{LY} L1140,{LY + 8} Z" fill="{CYAN}"/>')
    out.append(T(1150, LY - 18, "NEXT STOP: THE FUTURE", "m", 11, CYAN, ls=1.5, anchor="end", extra='opacity=".85"'))
    out.append(f'<path d="M60,{EY} H1140" stroke="{MAGENTA}" stroke-opacity=".16" stroke-width="10" stroke-linecap="round"/>')
    out.append(f'<path d="M60,{EY} H1140" stroke="{MAGENTA}" stroke-width="3" stroke-linecap="round"/>')
    # interchange connector from station 1 to the knowledge line
    out.append(f'<path d="M200,{LY + 20} V{EY - 6}" stroke="#3B3F7A" stroke-width="2" stroke-dasharray="3 6"/>')
    out.append(f'<circle cx="200" cy="{EY}" r="6" fill="#0B0B2A" stroke="{MAGENTA}" stroke-width="2"/>')
    out.append(T(212, EY + 24, "INTERCHANGE", "m", 10, DIM, ls=2))
    for st in stations:
        x = st["x"]
        acc = LIME if st.get("now") else CYAN
        dw = W("m", st["date"], 13, 1.5) + 26
        out.append(f'<rect x="{x - dw / 2:.1f}" y="{LY - 62}" width="{dw:.1f}" height="26" rx="13" fill="#0F1236" '
                   f'stroke="{acc}" stroke-opacity=".7"/>')
        out.append(T(x, LY - 44.5, st["date"], "m", 13, acc, ls=1.5, anchor="middle"))
        if st.get("now"):
            out.append(T(x, LY - 76, "YOU ARE HERE", "m", 11, LIME, ls=2, anchor="middle", cls="blink"))
            out.append(f'<circle cx="{x}" cy="{LY}" r="26" stroke="{LIME}" stroke-width="1.2" stroke-dasharray="4 5" class="spin"/>')
        out.append(f'<circle cx="{x}" cy="{LY}" r="16" stroke="{acc}" stroke-width="2" class="ping"/>')
        out.append(f'<circle cx="{x}" cy="{LY}" r="15" fill="#0B0B2A" stroke="{acc}" stroke-width="3"/>')
        out.append(f'<circle cx="{x}" cy="{LY}" r="6" fill="{acc}"/>')
        out.append(T(x, LY + 50, st["role"], "o7", 18, INK, ls=2, anchor="middle"))
        out.append(T(x, LY + 75, st["org"], "sb", 17, acc, ls=1.5, anchor="middle"))
        for k, dl in enumerate(st["desc"]):
            out.append(T(x, LY + 102 + k * 22, dl, "s", 16.5, SOFT, anchor="middle"))
    # knowledge station
    ex = 600
    out.append(f'<circle cx="{ex}" cy="{EY}" r="16" stroke="{MAGENTA}" stroke-width="2" class="ping"/>')
    out.append(f'<circle cx="{ex}" cy="{EY}" r="14" fill="#0B0B2A" stroke="{MAGENTA}" stroke-width="3"/>')
    out.append(f'<path d="M{ex - 7},{EY - 1} L{ex},{EY - 5} L{ex + 7},{EY - 1} L{ex},{EY + 3} Z M{ex - 4},{EY + 1} V{EY + 5} '
               f'Q{ex},{EY + 8} {ex + 4},{EY + 5} V{EY + 1}" fill="{MAGENTA}"/>')
    edw = W("m", "AUG 2023 — SEP 2026", 13, 1.5) + 26
    out.append(f'<rect x="{ex - edw / 2:.1f}" y="{EY - 60}" width="{edw:.1f}" height="26" rx="13" fill="#1A0E30" '
               f'stroke="{MAGENTA}" stroke-opacity=".7"/>')
    out.append(T(ex, EY - 42.5, "AUG 2023 — SEP 2026", "m", 13, "#FF9CEB", ls=1.5, anchor="middle"))
    out.append(T(ex, EY + 44, "BA • ENGLISH LANGUAGE & LITERATURE", "o7", 16, INK, ls=1.5, anchor="middle"))
    out.append(T(ex, EY + 68, "DELHI UNIVERSITY", "sb", 17, "#FF9CEB", ls=2, anchor="middle"))
    # legend + status
    out.append(f'<path d="M40,36 H70" stroke="{CYAN}" stroke-width="4" stroke-linecap="round"/>')
    out.append(T(80, 40.5, "CAREER LINE", "m", 12, DIM, ls=2))
    out.append(f'<path d="M210,36 H240" stroke="{MAGENTA}" stroke-width="3" stroke-linecap="round"/>')
    out.append(T(250, 40.5, "KNOWLEDGE LINE", "m", 12, DIM, ls=2))
    out.append(f'<circle cx="{1160 - W("m", "LINE STATUS: RUNNING", 12, 1.5) - 14:.1f}" cy="36" r="4" fill="{LIME}" class="blink"/>')
    out.append(T(1160, 40.5, "LINE STATUS: RUNNING", "m", 12, DIM, ls=1.5, anchor="end"))
    # pods
    pod = (f'<g class="podA"><g transform="translate(60 {LY})"><rect x="-60" y="-2.5" width="44" height="5" fill="url(#podT)"/>'
           f'<rect x="-18" y="-7" width="34" height="14" rx="7" fill="#E6FDFF" stroke="{CYAN}" stroke-width="1.5"/>'
           f'<rect x="-10" y="-3" width="18" height="4" rx="2" fill="{CYAN}"/></g></g>')
    pod2 = (f'<g class="podB"><g transform="translate(60 {EY})"><rect x="-50" y="-2" width="36" height="4" fill="url(#podT2)"/>'
            f'<rect x="-14" y="-6" width="28" height="12" rx="6" fill="#FFE3F8" stroke="{MAGENTA}" stroke-width="1.4"/></g></g>')
    css = (".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}"
           "@keyframes ping{from{transform:scale(1);opacity:.9}to{transform:scale(2.3);opacity:0}}"
           ".spin{transform-box:fill-box;transform-origin:center;animation:spin 10s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
           ".blink{animation:blink 1.2s steps(1) infinite}@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.2}}"
           ".flow{animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-14}}"
           ".podA{animation:podA 12s ease-in-out infinite}"
           "@keyframes podA{0%{transform:translateX(0)}12%,22%{transform:translateX(140px)}45%,55%{transform:translateX(520px)}"
           "78%,96%{transform:translateX(900px)}100%{transform:translateX(980px);opacity:0}}"
           ".podB{animation:podB 16s linear infinite}@keyframes podB{from{transform:translateX(-80px)}to{transform:translateX(1180px)}}")
    defs = f"""<pattern id="gridP" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0 H0 V40" stroke="#1A1F4A" stroke-opacity=".7"/></pattern>
<linearGradient id="podT" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".8"/></linearGradient>
<linearGradient id="podT2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MAGENTA}" stop-opacity="0"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity=".8"/></linearGradient>"""
    body = (f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="{BG}"/>'
            f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="url(#gridP)"/>'
            + "\n".join(out) + pod + pod2 +
            f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" stroke="#232A5C" stroke-width="1.5"/>')
    return doc(WD, HT, "Career route — transit map",
               "Career line: Graphic Designer at CCIE Hub, Delhi (Jun 2024 – Apr 2025); Graphic Designer at "
               "ConveGenius.AI, Noida (May 2025 – Nov 2025); AI Content Designer (UI/UX) at ConveGenius.AI, Noida "
               "(Nov 2025 – present). Knowledge line: BA English Language & Literature, Delhi University "
               "(Aug 2023 – Sep 2026).",
               ["o7", "m", "s", "sb"], css, body, defs)


# ======================================================================= skills
def icon(kind, acc):
    if kind == "pen":
        return (f'<path d="M0,-15 L10,3 L0,15 L-10,3 Z" stroke="{acc}" stroke-width="2" stroke-linejoin="round"/>'
                f'<circle cx="0" cy="2" r="3" fill="{acc}"/><path d="M0,-15 V-1" stroke="{acc}" stroke-width="1.5"/>')
    if kind == "spark":
        return (f'<path d="M0,-15 Q2.5,-2.5 15,0 Q2.5,2.5 0,15 Q-2.5,2.5 -15,0 Q-2.5,-2.5 0,-15 Z" stroke="{acc}" '
                f'stroke-width="2" stroke-linejoin="round"/><circle cx="10" cy="-10" r="2" fill="{acc}"/>')
    if kind == "code":
        return (f'<path d="M-6,-10 L-15,0 L-6,10 M6,-10 L15,0 L6,10 M3,-13 L-3,13" stroke="{acc}" stroke-width="2.4" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<rect x="-16" y="-9" width="32" height="18" rx="9" stroke="{acc}" stroke-width="2"/>'
            f'<path d="M-9,0 H-3 M-6,-3 V3" stroke="{acc}" stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="6" cy="-1.5" r="2" fill="{acc}"/><circle cx="10" cy="2.5" r="2" fill="{acc}"/>')


def skills():
    WD, HT = 1200, 496
    mods = [
        ("MOD-01", "DESIGN", CYAN, "pen",
         ["UI/UX Design", "Graphic Design", "Design Thinking", "Visual Storytelling", "Brand Communication"]),
        ("MOD-02", "AI CONTENT", MAGENTA, "spark",
         ["AI Content Design", "AI-assisted Visuals", "Social Media Creatives", "Campaign Graphics", "Content Creation"]),
        ("MOD-03", "CODE", VIOLET, "code",
         ["Web Development", "HTML · CSS · JavaScript", "TypeScript & React", "HTML Game Creation", "Real-time 3D on the Web"]),
        ("MOD-04", "AI & GAMES", AMBER, "pad",
         ["AI Game Development", "Game Development", "Learning Game Design", "Voice-over & Localisation"]),
    ]
    out = []
    mw, gap, x0, y0, mh = 270, 20, 30, 34, 322
    css = [".seg{animation:seg 2.8s steps(1) infinite}@keyframes seg{0%{opacity:.18}10%,100%{opacity:1}}",
           ".hb{animation:hb 2.4s ease-in-out infinite alternate}@keyframes hb{from{opacity:.4}to{opacity:1}}",
           ".sw{animation:sw 7s ease-in-out infinite}@keyframes sw{0%{transform:translateX(-300px)}55%,100%{transform:translateX(1500px)}}"]
    for i, (code, title, acc, ic, items) in enumerate(mods):
        x = x0 + i * (mw + gap)
        y = y0
        c = 18
        out.append(f'<path d="M{x + c},{y} H{x + mw} V{y + mh - c} L{x + mw - c},{y + mh} H{x} V{y + c} Z" '
                   f'fill="url(#modG)" stroke="{acc}" stroke-opacity=".6" stroke-width="1.5"/>')
        out.append(f'<path d="M{x},{y + c} L{x + c},{y}" stroke="{acc}" stroke-width="2.2"/>')
        out.append(f'<polygon points="{hex_points(x + 44, y + 50, 25)}" fill="#120A35" stroke="{acc}" stroke-width="1.8"/>')
        out.append(f'<g transform="translate({x + 44} {y + 50})" class="hb">{icon(ic, acc)}</g>')
        out.append(T(x + 80, y + 40, code, "m", 11, acc, ls=2))
        out.append(T(x + 80, y + 64, title, "o7", 19, INK, ls=2))
        out.append(f'<path d="M{x + 20},{y + 92} H{x + mw - 20}" stroke="url(#div{i})" stroke-width="1.5"/>')
        for k, it in enumerate(items):
            yy = y + 126 + k * 33
            out.append(f'<path d="M{x + 24},{yy - 10} l7,4.5 l-7,4.5 Z" fill="{acc}"/>')
            out.append(T(x + 40, yy, it, "s", 18, "#D6DEFF"))
        # power meter
        for s in range(10):
            sx = x + 22 + s * 17
            out.append(f'<rect x="{sx}" y="{y + mh - 38}" width="13" height="8" rx="1.5" fill="{acc}" class="seg" '
                       f'style="animation-delay:{s * 0.12 + i * 0.3:.2f}s"/>')
        out.append(T(x + mw - 22, y + mh - 30, "ONLINE", "m", 11, acc, ls=2, anchor="end"))
    # toolchain chips
    tools = ["THREE.JS", "REACT THREE FIBER", "GSAP", "FRAMER MOTION", "LENIS", "CANVAS", "SVG", "CSS 3D",
             "WEB AUDIO", "PWA", "PLAYWRIGHT", "VITEST", "FASTIFY", "FFMPEG", "CLAUDE CODE", "CLAUDE API", "CHATGPT"]
    cols = [CYAN, MAGENTA, VIOLET, AMBER, LIME]
    ty = y0 + mh + 32
    out.append(T(x0, ty + 18, "TOOLCHAIN", "o7", 15, INK, ls=3))
    out.append(T(x0, ty + 40, "// also in the kit", "m", 11, DIM, ls=1))
    cx, cy = 200, ty
    for j, tl in enumerate(tools):
        w = W("m", tl, 12.5, 1.5) + 26
        if cx + w > WD - 30:
            cx, cy = 200, cy + 40
        col = cols[j % len(cols)]
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="28" rx="14" fill="#0F1236" stroke="{col}" stroke-opacity=".55"/>')
        out.append(T(cx + 13, cy + 18.5, tl, "m", 12.5, "#D6DEFF", ls=1.5))
        cx += w + 10
    defs = (f'<pattern id="gridP" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0 H0 V40" stroke="#1A1F4A" stroke-opacity=".7"/></pattern>'
            f'<linearGradient id="modG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140E40"/><stop offset="1" stop-color="#0A0824"/></linearGradient>'
            f'<linearGradient id="swg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".06"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="pc"><rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20"/></clipPath>')
    for i, m in enumerate(mods):
        defs += (f'<linearGradient id="div{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{m[2]}"/>'
                 f'<stop offset="1" stop-color="{m[2]}" stop-opacity="0"/></linearGradient>')
    body = (f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="{BG}"/>'
            f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="url(#gridP)"/>'
            + "\n".join(out) +
            f'<g clip-path="url(#pc)"><g class="sw"><rect x="0" y="-20" width="220" height="540" fill="url(#swg)" transform="skewX(-18)"/></g></g>'
            f'<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" stroke="#232A5C" stroke-width="1.5"/>')
    alt = "; ".join(f"{m[1].title()}: {', '.join(m[4])}" for m in mods) + ". Toolchain: " + ", ".join(tools) + "."
    return doc(WD, HT, "Skill matrix", alt, ["o7", "m", "s"], "".join(css), body, defs)


# ======================================================================== cards
def ill_crown(a):
    return f"""
<path d="M0,64 V-26" stroke="#CFC8FF" stroke-width="3"/>
<path d="M-26,72 H26 L15,62 H-15 Z" fill="{a}" fill-opacity=".25" stroke="{a}" stroke-width="1.5"/>
<g class="tilt" style="transform-origin:0px -28px">
  <path d="M-74,-28 H74" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
  <circle cx="0" cy="-28" r="5.5" fill="{a}"/>
  <path d="M-74,-28 L-94,12 M-74,-28 L-54,12 M74,-28 L54,12 M74,-28 L94,12" stroke="{a}" stroke-opacity=".75" stroke-width="1.3"/>
  <path d="M-98,12 Q-74,30 -50,12 Z M50,12 Q74,30 98,12 Z" fill="{a}" fill-opacity=".2" stroke="{a}" stroke-width="1.6"/>
  <path d="M-88,8 V-8 L-81,0 L-74,-13 L-67,0 L-60,-8 V8 Z" fill="{a}" stroke="#FFF7DD" stroke-width="1"/>
  <circle cx="-74" cy="-16" r="2.2" fill="{MAGENTA}"/>
  <path d="M57,8 L61,0 H87 L91,8 Z M61,0 L65,-8 H83 L87,0 Z" fill="{a}" stroke="#FFF7DD" stroke-width="1"/>
</g>
"""


def ill_cannon(a):
    return f"""
<rect x="44" y="-84" width="40" height="40" rx="4" stroke="{AMBER}" stroke-width="1.8" fill="{AMBER}" fill-opacity=".08"/>
<path d="M54,-84 V-44 M64,-84 V-44 M74,-84 V-44" stroke="{AMBER}" stroke-width="1.6"/>
<text x="64" y="-58" class="o7" font-size="15" fill="{INK}" text-anchor="middle" opacity=".9">x</text>
<g transform="translate(-34 34) rotate(-34)">
  <rect x="-12" y="-12" width="84" height="24" rx="9" fill="#2A1B5E" stroke="{a}" stroke-width="2"/>
  <rect x="64" y="-15" width="11" height="30" rx="3" fill="{a}" fill-opacity=".35" stroke="{a}" stroke-width="2"/>
  <path d="M6,-12 V12 M30,-12 V12" stroke="{a}" stroke-opacity=".5" stroke-width="1.5"/>
</g>
<circle cx="-34" cy="48" r="22" fill="#140C3A" stroke="{INK}" stroke-width="2.5"/>
<g class="spinS" style="transform-origin:-34px 48px"><path d="M-34,28 V68 M-54,48 H-14 M-48,34 L-20,62 M-48,62 L-20,34" stroke="{a}" stroke-opacity=".6" stroke-width="1.6"/></g>
<circle cx="-34" cy="48" r="5" fill="{a}"/>
<path d="M-70,72 H40" stroke="#3B3F7A" stroke-width="2"/>
<g class="orb"><circle cx="0" cy="0" r="11" fill="url(#orbG)" stroke="#FFFFFF" stroke-width="1.2"/>
<text x="0" y="4.5" class="o7" font-size="12" fill="#1A0B3A" text-anchor="middle">+3</text></g>
<g class="flash"><path d="M30,-28 l6,-12 l2,10 l12,-4 l-9,9 l10,7 l-13,-1 Z" fill="{AMBER}"/></g>
"""


def ill_bike(a):
    return f"""
<path d="M-96,6 L-64,-38 L-46,-18 L-22,-58 L4,-22 L26,-44 L52,-12 L72,-30 L98,6" stroke="{a}" stroke-opacity=".55" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M-28,-50 L-22,-58 L-15,-48 Z M20,-38 L26,-44 L32,-36 Z" fill="#E6FDFF" opacity=".8"/>
<path d="M-96,74 C-40,60 10,52 30,30 C42,16 70,12 96,10" stroke="#CFC8FF" stroke-opacity=".35" stroke-width="10" stroke-linecap="round"/>
<path d="M-96,74 C-40,60 10,52 30,30 C42,16 70,12 96,10" stroke="{INK}" stroke-opacity=".7" stroke-width="1.6" stroke-dasharray="8 8" class="road"/>
<g transform="translate(-4 34)" class="ride">
  <path d="M-62,-14 H-38 M-70,-4 H-44 M-58,6 H-40" stroke="{a}" stroke-width="2" stroke-linecap="round" class="speed"/>
  <circle cx="-26" cy="0" r="14" stroke="{INK}" stroke-width="3"/><circle cx="-26" cy="0" r="4" fill="{a}"/>
  <circle cx="32" cy="0" r="14" stroke="{INK}" stroke-width="3"/><circle cx="32" cy="0" r="4" fill="{a}"/>
  <path d="M-26,0 L-6,-14 L22,-14 L32,0" stroke="#9AA6D8" stroke-width="2"/>
  <path d="M-30,-6 L-12,-24 L12,-26 L28,-18 L40,-6 L33,-2 L6,-4 L-12,-8 Z" fill="{a}" fill-opacity=".85" stroke="#E6FDFF" stroke-width="1.2"/>
  <path d="M-30,-6 L-42,-18 L-22,-16" stroke="#E6FDFF" stroke-width="1.6" stroke-linejoin="round"/>
  <circle cx="10" cy="-38" r="7.5" fill="{MAGENTA}" stroke="#FFFFFF" stroke-width="1"/>
  <path d="M4,-32 L-10,-24 L-2,-14" stroke="#E6FDFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</g>
"""


def ill_books(a):
    chips = []
    for k, code in enumerate(["EN", "HI", "MR", "TE", "GU", "OD"]):
        import math
        ang = math.radians(-90 + k * 60)
        x, y = 78 * math.cos(ang), 62 * math.sin(ang) - 6
        chips.append(f'<g class="lang" style="animation-delay:{k * 0.45:.2f}s"><rect x="{x - 15:.1f}" y="{y - 10:.1f}" width="30" height="20" rx="10" '
                     f'fill="#120A35" stroke="{a}" stroke-width="1.2"/>'
                     f'<text x="{x:.1f}" y="{y + 4.5:.1f}" class="m" font-size="11" fill="{INK}" text-anchor="middle">{code}</text></g>')
    return f"""
<ellipse cx="0" cy="-6" rx="78" ry="62" stroke="{a}" stroke-opacity=".25" stroke-dasharray="3 6"/>
<rect x="-42" y="26" width="84" height="16" rx="2" fill="{VIOLET}" fill-opacity=".55" stroke="#E6DDFF" stroke-width="1.2"/>
<rect x="-36" y="10" width="76" height="16" rx="2" fill="{a}" fill-opacity=".5" stroke="#FFE3F8" stroke-width="1.2"/>
<rect x="-46" y="42" width="92" height="16" rx="2" fill="{CYAN}" fill-opacity=".35" stroke="#E6FDFF" stroke-width="1.2"/>
<path d="M-30,10 V26 M-36,26 V42 M-38,42 V58" stroke="#FFFFFF" stroke-opacity=".5"/>
<g class="swing" style="transform-origin:0px -46px">
  <path d="M0,-46 V-36" stroke="#CFC8FF" stroke-width="1.2"/>
  <path d="M-22,-36 H22 L30,-18 L22,0 H-22 Z" fill="#1A0B3A" stroke="{a}" stroke-width="2"/>
  <circle cx="-14" cy="-18" r="3" stroke="{a}" stroke-width="1.4"/>
  <text x="6" y="-11" class="o7" font-size="20" fill="{INK}" text-anchor="middle">%</text>
</g>
{''.join(chips)}
"""


def ill_construct(a):
    floors = []
    for k in range(6):
        y = 64 - (k + 1) * 15
        floors.append(f'<g class="fl" style="animation-delay:{k * 0.45:.2f}s"><rect x="8" y="{y}" width="70" height="13" fill="#1B1250" stroke="{a}" stroke-width="1.2"/>'
                      f'<path d="M18,{y + 4} h8 M34,{y + 4} h8 M50,{y + 4} h8 M66,{y + 4} h6" stroke="{AMBER}" stroke-width="3"/></g>')
    lattice = "".join(f"M-62,{y} L-50,{y - 12} M-50,{y} L-62,{y - 12} " for y in range(64, -60, -12))
    return f"""
<path d="M-90,66 H96" stroke="#3B3F7A" stroke-width="2"/>
{''.join(floors)}
<path d="M-62,64 V-74 M-50,64 V-74" stroke="{INK}" stroke-width="2"/>
<path d="{lattice}" stroke="{a}" stroke-opacity=".6" stroke-width="1"/>
<path d="M-74,-74 H92 M-74,-74 L-56,-92 L92,-74 M-56,-92 V-74" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>
<rect x="-82" y="-80" width="12" height="12" fill="{a}" fill-opacity=".5" stroke="{a}"/>
<circle cx="-56" cy="-95" r="2.6" fill="#FF3B6B" class="bk"/>
<g class="trolley"><rect x="-6" y="-78" width="16" height="7" fill="{a}"/>
  <path d="M2,-71 V-30" stroke="#CFC8FF" stroke-width="1.2"/>
  <rect x="-10" y="-30" width="24" height="12" fill="{AMBER}" fill-opacity=".85" stroke="#FFF7DD"/></g>
"""


def ill_studio(a):
    return f"""
<rect x="-96" y="-44" width="72" height="54" rx="5" fill="#120A35" stroke="#E6DDFF" stroke-width="1.6"/>
<rect x="-96" y="-44" width="72" height="12" rx="5" fill="{a}" fill-opacity=".55"/>
<path d="M-86,-20 H-40 M-86,-10 H-52 M-86,0 H-46" stroke="#CFC8FF" stroke-opacity=".7" stroke-width="2.5" stroke-linecap="round"/>
<text x="-60" y="30" class="m" font-size="11" fill="{DIM}" text-anchor="middle" letter-spacing="2">PPTX</text>
<path d="M-16,-17 H18" stroke="{a}" stroke-width="2" stroke-dasharray="5 6" class="flow"/>
<path d="M16,-23 L26,-17 L16,-11 Z" fill="{a}"/>
<rect x="32" y="-38" width="64" height="40" rx="20" fill="#120A35" stroke="{INK}" stroke-width="1.8"/>
<path d="M44,-18 H58 M51,-25 V-11" stroke="{a}" stroke-width="2.6" stroke-linecap="round"/>
<circle cx="76" cy="-22" r="3.4" fill="{MAGENTA}"/><circle cx="85" cy="-14" r="3.4" fill="{CYAN}"/>
<text x="64" y="30" class="m" font-size="11" fill="{DIM}" text-anchor="middle" letter-spacing="2">GAME</text>
<g class="twk" style="transform-origin:0px -70px"><path d="M0,-86 Q3,-73 16,-70 Q3,-67 0,-54 Q-3,-67 -16,-70 Q-3,-73 0,-86 Z" fill="{AMBER}"/></g>
<text x="0" y="-38" class="m" font-size="10" fill="{AMBER}" text-anchor="middle" letter-spacing="2">AI</text>
<rect x="-70" y="50" width="140" height="22" rx="11" fill="#0F1236" stroke="{LIME}" stroke-opacity=".6"/>
<text x="0" y="65" class="m" font-size="10.5" fill="{LIME}" text-anchor="middle" letter-spacing="1.5">HUMAN APPROVES</text>
"""


def ill_distance(a):
    grid = "".join(f"M{x},-70 V70 " for x in range(-90, 91, 20)) + "".join(f"M-90,{y} H90 " for y in range(-70, 71, 20))
    return f"""
<path d="{grid}" stroke="#2A2F6A" stroke-width="1"/>
<path d="M-90,50 H90 M-70,70 V-70" stroke="#5C66A8" stroke-width="1.6"/>
<path d="M-50,30 H50 V-50" stroke="{AMBER}" stroke-width="2" stroke-dasharray="5 5"/>
<path d="M-50,30 L50,-50" stroke="{a}" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="130" class="draw"/>
<circle cx="-50" cy="30" r="6" fill="{CYAN}" stroke="#FFFFFF" stroke-width="1.4"/>
<circle cx="50" cy="-50" r="6" fill="{MAGENTA}" stroke="#FFFFFF" stroke-width="1.4"/>
<text x="-62" y="48" class="o7" font-size="14" fill="{INK}">A</text>
<text x="58" y="-56" class="o7" font-size="14" fill="{INK}">B</text>
<text x="-14" y="-16" class="o7" font-size="20" fill="{a}">d</text>
<text x="0" y="46" class="m" font-size="12" fill="{AMBER}" text-anchor="middle">x</text>
<text x="62" y="-6" class="m" font-size="12" fill="{AMBER}">y</text>
<path d="M50,30 h-9 v-9 h9" stroke="{AMBER}" stroke-width="1.2"/>
"""


def ill_orbit(a):
    return f"""
<ellipse cx="0" cy="0" rx="88" ry="26" stroke="{a}" stroke-opacity=".75" stroke-width="1.6" transform="rotate(-16)"/>
<ellipse cx="0" cy="0" rx="70" ry="54" stroke="{MAGENTA}" stroke-opacity=".45" stroke-width="1.2" transform="rotate(28)" stroke-dasharray="4 6"/>
<circle cx="0" cy="0" r="40" fill="url(#plG)" stroke="#E6FDFF" stroke-width="1.6"/>
<ellipse cx="0" cy="0" rx="16" ry="40" stroke="#E6FDFF" stroke-opacity=".45"/>
<ellipse cx="0" cy="0" rx="30" ry="40" stroke="#E6FDFF" stroke-opacity=".3"/>
<ellipse cx="0" cy="0" rx="40" ry="11" stroke="#E6FDFF" stroke-opacity=".45"/>
<path d="M-36,-18 Q0,-12 36,-18 M-36,18 Q0,24 36,18" stroke="#E6FDFF" stroke-opacity=".3"/>
<circle r="6" fill="{AMBER}"><animateMotion dur="7s" repeatCount="indefinite" path="M88,0 A88,26 0 1 1 -88,0 A88,26 0 1 1 88,0" rotate="0"/></circle>
<circle r="4.5" fill="{CYAN}"><animateMotion dur="11s" repeatCount="indefinite" path="M-70,0 A70,54 0 1 1 70,0 A70,54 0 1 1 -70,0"/></circle>
"""


CARDS = [
    dict(slug="crown-quest", title="ZIPPY'S CROWN QUEST", sector="SECTOR 01 // MATH QUEST", acc=AMBER, ill=ill_crown,
         desc="Class 8 linear equations as a 25-minute voiced adventure: Zippy the monkey swaps crowns for gold bars on a balance. Tip it and Grumble wakes up.",
         chips=["JAVASCRIPT", "WEB AUDIO", "PWA"], live=True, url="https://crown-quest-ten.vercel.app"),
    dict(slug="cannon-quest", title="CANNON QUEST", sector="SECTOR 02 // ALGEBRA ARCADE", acc=ORANGE, ill=ill_cannon,
         desc="Load operation orbs into the cannon, fire, and free x from its cage. A drag-to-load 2D algebra game with a guided tutorial and full localisation.",
         chips=["JAVASCRIPT", "GSAP", "I18N"], live=True, url="https://cannon-quest.vercel.app"),
    dict(slug="uttarakhand-riders", title="UTTARAKHAND RIDERS", sector="SECTOR 03 // 3D RACING", acc=CYAN, ill=ill_bike,
         desc="A 3D superbike race through the hills: from Ramnagar past Corbett and the Kosi river up to Ranikhet. Three riders, phone controls and voice chat.",
         chips=["THREE.JS", "NODE.JS", "PWA"], live=True, url="https://bike-game-gamma.vercel.app"),
    dict(slug="bookstore-journey", title="BOOKSTORE JOURNEY", sector="SECTOR 04 // PROFIT & DISCOUNT", acc=MAGENTA, ill=ill_books,
         desc="A voiced story game about profit and discount, set in a bookstore and playable in six languages: English, Hindi, Marathi, Telugu, Gujarati and Odia.",
         chips=["JAVASCRIPT", "I18N", "VOICE-OVER"], live=True, url="https://profit-and-discount-game.vercel.app"),
    dict(slug="irha-construction", title="IRHA CONSTRUCTION", sector="SECTOR 05 // 3D WEB", acc=AMBER, ill=ill_construct,
         desc="A scroll-driven website where a 3D excavator drives you through a live construction site: the gate, the cranes, the material yard and a finished tower.",
         chips=["REACT", "THREE.JS", "GSAP", "FRAMER"], live=True, url="https://ira-rahman-construction.vercel.app"),
    dict(slug="nexus-play-studio", title="NEXUS PLAY STUDIO", sector="SECTOR 06 // AI TOOLING", acc=VIOLET, ill=ill_studio,
         desc="Turns a PowerPoint lesson into a playable learning game. Claude drafts the learning map and blueprint, a human approves, and trusted templates build it.",
         chips=["TYPESCRIPT", "REACT", "FASTIFY", "CLAUDE"], live=False, url="https://github.com/aniketchauhan-star/game-dev"),
    dict(slug="distance-formula", title="DISTANCE FORMULA", sector="SECTOR 07 // GEOMETRY", acc=LIME, ill=ill_distance,
         desc="A whole maths lesson as one game, led by Swifty the voiced bird: plot the points, find the gaps, close the right triangle and let Pythagoras finish it.",
         chips=["JAVASCRIPT", "SVG", "WEB AUDIO"], live=True, url="https://distance-formula.vercel.app"),
    dict(slug="portfolio-3d", title="3D PORTFOLIO", sector="SECTOR 08 // PERSONAL SITE", acc=CYAN, ill=ill_orbit,
         desc="My personal site: a real-time 3D scene, orbiting skill planets, playable game builds and 25 design case studies across UI, brand and packaging.",
         chips=["NEXT.JS", "R3F", "GSAP", "TAILWIND"], live=True, url="https://portfolio-aniket-five.vercel.app"),
]


def card(c):
    WD, HT = 600, 340
    a = c["acc"]
    tsize, tls = 25, 1.5
    tlines = wrap(c["title"], "o7", tsize, 330, tls)
    out = []
    out.append(f'<path d="M24,2 H598 V316 L574,338 H2 V26 Z" fill="url(#cg)"/>')
    out.append(f'<path d="M24,2 H598 V316 L574,338 H2 V26 Z" fill="url(#gridC)"/>')
    # hologram pedestal + beam
    ix, iy = 470, 158
    out.append(f'<path d="M{ix - 62},262 L{ix - 92},64 H{ix + 92} L{ix + 62},262 Z" fill="url(#beamC)" class="flick"/>')
    out.append(f'<ellipse cx="{ix}" cy="264" rx="78" ry="13" fill="#140C3A" stroke="{a}" stroke-width="1.6"/>')
    out.append(f'<ellipse cx="{ix}" cy="264" rx="56" ry="8" stroke="{a}" stroke-opacity=".5" stroke-dasharray="6 6" class="dash"/>')
    out.append(f'<g transform="translate({ix} {iy})"><g class="float">{c["ill"](a)}</g></g>')
    out.append(f'<g clip-path="url(#illClip)"><rect x="{ix - 110}" y="50" width="220" height="8" fill="url(#scanC)" class="scanC"/></g>')
    # text block
    out.append(T(30, 38, c["sector"], "m", 12, a, ls=2))
    y = 82
    for ln in tlines:
        out.append(T(30, y, ln, "o7", tsize, INK, ls=tls))
        y += 32
    y += 4
    for ln in wrap(c["desc"], "s", 17, 338)[:5]:
        out.append(T(30, y, ln, "s", 17, SOFT))
        y += 22
    assert y < 286, (c["slug"], y)
    cx = 30
    for ch in c["chips"]:
        w = W("m", ch, 11, 1.2) + 20
        out.append(f'<rect x="{cx:.1f}" y="290" width="{w:.1f}" height="24" rx="12" fill="#0F1236" stroke="{a}" stroke-opacity=".6"/>')
        out.append(T(cx + 10, 306, ch, "m", 11, "#D6DEFF", ls=1.2))
        cx += w + 8
    # status chip
    if c["live"]:
        lab, col = "LIVE", LIME
    else:
        lab, col = "SOURCE", AMBER
    sw_ = W("m", lab, 11, 2) + 34
    out.append(f'<rect x="{576 - sw_:.1f}" y="20" width="{sw_:.1f}" height="24" rx="12" fill="#0F1236" stroke="{col}" stroke-opacity=".8"/>')
    out.append(f'<circle cx="{576 - sw_ + 14:.1f}" cy="32" r="4" fill="{col}" class="pulse"/>')
    out.append(T(576 - sw_ + 24, 36.5, lab, "m", 11, col, ls=2))
    # CTA
    cta = "LAUNCH" if c["live"] else "VIEW CODE"
    cw = W("m", cta, 12, 2.5)
    out.append(T(556, 307, cta, "m", 12, a, ls=2.5, anchor="end"))
    if c["live"]:
        out.append(f'<path d="M562,297 l9,5.5 l-9,5.5 Z" fill="{a}" class="nudge"/>')
    else:
        out.append(f'<path d="M565,297 l-4,5.5 l4,5.5 M570,297 l4,5.5 l-4,5.5" stroke="{a}" stroke-width="1.6" class="nudge"/>')
    out.append(f'<path d="M24,2 H598 V316 L574,338 H2 V26 Z" stroke="{a}" stroke-opacity=".75" stroke-width="1.6"/>')
    out.append(f'<path d="M2,26 L24,2 M574,338 L598,316" stroke="{a}" stroke-width="3"/>')
    css = (".float{animation:float 4s ease-in-out infinite alternate}@keyframes float{from{transform:translateY(-4px)}to{transform:translateY(4px)}}"
           ".flick{animation:flick 5s steps(1) infinite}@keyframes flick{0%,86%,90%,100%{opacity:1}88%{opacity:.35}}"
           ".scanC{animation:scanC 3.4s linear infinite}@keyframes scanC{from{transform:translateY(0)}to{transform:translateY(210px)}}"
           ".dash{animation:dash 3s linear infinite}@keyframes dash{to{stroke-dashoffset:-48}}"
           ".pulse{animation:pulse 1.3s ease-in-out infinite alternate}@keyframes pulse{from{opacity:.3}to{opacity:1}}"
           ".nudge{animation:nudge 1.6s ease-in-out infinite}@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}"
           ".tilt{animation:tilt 3.2s ease-in-out infinite alternate}@keyframes tilt{from{transform:rotate(-5deg)}to{transform:rotate(5deg)}}"
           ".spinS{animation:spinS 6s linear infinite}@keyframes spinS{to{transform:rotate(360deg)}}"
           ".orb{animation:orb 2.6s ease-in infinite}@keyframes orb{0%{transform:translate(20px,-8px);opacity:0}8%{opacity:1}"
           "55%{transform:translate(48px,-74px)}80%{transform:translate(64px,-66px);opacity:1}88%,100%{transform:translate(64px,-66px);opacity:0}}"
           ".flash{animation:flash 2.6s steps(1) infinite}@keyframes flash{0%,10%{opacity:1}11%,100%{opacity:0}}"
           ".road{animation:road 1s linear infinite}@keyframes road{to{stroke-dashoffset:16}}"
           ".speed{animation:speed .6s linear infinite}@keyframes speed{from{transform:translateX(6px);opacity:1}to{transform:translateX(-10px);opacity:.2}}"
           ".ride{animation:ride .9s ease-in-out infinite alternate}@keyframes ride{from{transform:translate(-4px,34px)}to{transform:translate(-4px,32px)}}"
           ".lang{animation:lang 2.7s ease-in-out infinite}@keyframes lang{0%,100%{opacity:.45}25%{opacity:1}}"
           ".swing{animation:swing 3s ease-in-out infinite alternate}@keyframes swing{from{transform:rotate(-8deg)}to{transform:rotate(8deg)}}"
           ".fl{animation:fl 6s linear infinite}@keyframes fl{0%{opacity:0}6%,85%{opacity:1}92%,100%{opacity:0}}"
           ".trolley{animation:trolley 5s ease-in-out infinite alternate}@keyframes trolley{from{transform:translateX(-20px)}to{transform:translateX(64px)}}"
           ".bk{animation:bk 1.6s steps(1) infinite}@keyframes bk{0%,60%{opacity:1}61%,100%{opacity:.15}}"
           ".flow{animation:flow .8s linear infinite}@keyframes flow{to{stroke-dashoffset:-11}}"
           ".twk{animation:twk 2s ease-in-out infinite alternate}@keyframes twk{from{transform:scale(.7);opacity:.6}to{transform:scale(1.1);opacity:1}}"
           ".draw{animation:draw 3.2s ease-in-out infinite}@keyframes draw{0%{stroke-dashoffset:130}45%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-130}}")
    defs = f"""
<linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#110C38"/><stop offset="1" stop-color="#08071E"/></linearGradient>
<pattern id="gridC" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24,0 H0 V24" stroke="#1A1F4A" stroke-opacity=".55"/></pattern>
<linearGradient id="beamC" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{a}" stop-opacity=".2"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
<linearGradient id="scanC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}" stop-opacity=".25"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
<radialGradient id="orbG" cx=".35" cy=".35"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{AMBER}"/></radialGradient>
<radialGradient id="plG" cx=".35" cy=".3"><stop offset="0" stop-color="#4B6BFF" stop-opacity=".9"/><stop offset="1" stop-color="#120A35"/></radialGradient>
<clipPath id="illClip"><rect x="360" y="56" width="220" height="210"/></clipPath>
"""
    title = c["title"].title().replace("'S", "'s")
    status = "Live demo" if c["live"] else "Source code"
    return doc(WD, HT, f"{title} — project card", f'{c["desc"]} Built with {", ".join(c["chips"]).title()}. {status}.',
               ["o7", "m", "s"], css, "\n".join(out), defs)


# ====================================================================== buttons
BUTTONS = [
    ("btn-linkedin", "LINKEDIN", "CONNECT // NETWORK", CYAN, "in"),
    ("btn-portfolio", "PORTFOLIO", "EXPLORE // 3D SITE", MAGENTA, "planet"),
    ("btn-email", "EMAIL", "TRANSMIT // HELLO", AMBER, "mail"),
]


def button(slug, label, sub, acc, ic):
    WD, HT = 286, 64
    if ic == "in":
        glyph = (f'<rect x="-13" y="-13" width="26" height="26" rx="6" stroke="{acc}" stroke-width="2"/>'
                 + T(0, 6.5, "in", "sb", 19, acc, anchor="middle"))
    elif ic == "planet":
        glyph = (f'<circle r="9" stroke="{acc}" stroke-width="2"/><ellipse rx="16" ry="5" stroke="{acc}" stroke-width="1.6" '
                 f'transform="rotate(-20)"/><circle cx="7" cy="-11" r="2" fill="{acc}"/>')
    else:
        glyph = (f'<rect x="-13" y="-9" width="26" height="18" rx="3" stroke="{acc}" stroke-width="2"/>'
                 f'<path d="M-12,-7 L0,2 L12,-7" stroke="{acc}" stroke-width="2" stroke-linejoin="round"/>')
    body = f"""
<path d="M14,2 H284 V50 L272,62 H2 V14 Z" fill="url(#bg)"/>
<g clip-path="url(#bc)"><g class="sh"><rect x="0" y="-10" width="70" height="90" fill="url(#shg)" transform="skewX(-22)"/></g></g>
<path d="M14,2 H284 V50 L272,62 H2 V14 Z" stroke="{acc}" stroke-opacity=".85" stroke-width="1.6"/>
<path d="M2,14 L14,2 M272,62 L284,50" stroke="{acc}" stroke-width="3"/>
<g transform="translate(34 32)" class="pu">{glyph}</g>
<path d="M60,14 V50" stroke="{acc}" stroke-opacity=".3"/>
{T(74, 32, label, "o7", 17, INK, ls=3)}
{T(75, 49, sub, "m", 10, DIM, ls=1.5)}
<path d="M258,26 l8,6 l-8,6" stroke="{acc}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="nd"/>
"""
    css = (".sh{animation:sh 4.5s ease-in-out infinite}@keyframes sh{0%{transform:translateX(-120px)}50%,100%{transform:translateX(420px)}}"
           ".pu{animation:pu 2.2s ease-in-out infinite alternate}@keyframes pu{from{opacity:.65}to{opacity:1}}"
           ".nd{animation:nd 1.4s ease-in-out infinite}@keyframes nd{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}")
    defs = f"""<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14104A"/><stop offset="1" stop-color="#0A0824"/></linearGradient>
<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".16"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<clipPath id="bc"><path d="M14,2 H284 V50 L272,62 H2 V14 Z"/></clipPath>"""
    keys = ["o7", "m"] + (["sb"] if ic == "in" else [])
    return doc(WD, HT, f"{label.title()} button", f"{label.title()} — {sub.title()}", keys, css, body, defs)


# ======================================================================= footer
def footer():
    WD, HT = 1200, 250
    r2 = random.Random(77)
    stars = "".join(f'<circle cx="{r2.uniform(10, 1190):.0f}" cy="{r2.uniform(8, 120):.0f}" r="{r2.choice([.6, .8, 1.1])}" '
                    f'fill="#FFFFFF" opacity="{r2.uniform(.25, .8):.2f}"/>' for _ in range(60))
    # skyline silhouette
    parts, x = [], -6
    while x < WD + 6:
        w = r2.randint(18, 44)
        h = r2.randint(26, 96)
        top = 196 - h
        if r2.random() < .2:
            parts.append(f"M{x},196V{top}H{x + w}V196Z M{x + w / 2 - 1.2:.1f},{top}V{top - r2.randint(10, 26)}H{x + w / 2 + 1.2:.1f}V{top}Z")
        else:
            parts.append(f"M{x},196V{top}H{x + w}V196Z")
        x += w + r2.randint(-4, 3)
    d = "".join(parts)
    tile = "".join(f'<rect x="{cx_ * 9 + 3}" y="{cy * 11 + 3}" width="3" height="4" fill="{r2.choice([AMBER, "#9EF7FF", "#FFB3F0"])}" opacity=".75"/>'
                   for cy in range(4) for cx_ in range(5) if r2.random() < .28)
    lanes = [(184, .55, 1, 7.5, (0, 3.7)), (226, .9, -1, 6, (1.2, 4.2))]
    cars, css = [], []
    for li, (y, s, dirn, dur, delays) in enumerate(lanes):
        for dl in delays:
            sc = f"scale({s})" if dirn > 0 else f"scale({-s} {s})"
            cars.append(f'<g class="fl{li}" style="animation-delay:-{dl}s"><g transform="translate(0 {y}) {sc}"><use href="#{"fcA" if li == 0 else "fcB"}"/></g></g>')
        frm, to = (-200, WD + 200) if dirn > 0 else (WD + 200, -200)
        css.append(f"@keyframes fl{li}{{from{{transform:translateX({frm}px)}}to{{transform:translateX({to}px)}}}}.fl{li}{{animation:fl{li} {dur}s linear infinite}}")
    streaks = "".join(
        f'<rect x="0" y="{y}" width="{ln}" height="1.6" rx=".8" fill="url(#stk{i % 2})" class="st" '
        f'style="animation-duration:{du:.1f}s;animation-delay:-{dl:.1f}s"/>'
        for i, (y, ln, du, dl) in enumerate([(206, 140, 1.8, 0), (212, 90, 1.4, .7), (240, 200, 2.2, 1.1), (246, 120, 1.6, .3)]))
    css.append(".st{animation:st 2s linear infinite}@keyframes st{from{transform:translateX(-260px)}to{transform:translateX(1460px)}}"
               ".gl{animation:gl 3s ease-in-out infinite alternate}@keyframes gl{from{opacity:.75}to{opacity:1}}")
    body = f"""
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" fill="url(#fbg)"/>
<g clip-path="url(#fc)">
{stars}
<ellipse cx="600" cy="196" rx="640" ry="70" fill="url(#fglow)"/>
<path d="{d}" fill="#1A0D44"/><path d="{d}" fill="url(#fwin)"/>
<rect x="0" y="196" width="{WD}" height="10" fill="#1E1250"/>
<path d="M0,196.5 H{WD}" stroke="{CYAN}" stroke-width="1.4"/>
<path d="M0,205.5 H{WD}" stroke="{MAGENTA}" stroke-opacity=".7" stroke-width="1"/>
{''.join(f'<rect x="{px}" y="206" width="8" height="44" fill="#140A36"/>' for px in range(70, WD, 160))}
{streaks}
{''.join(cars)}
</g>
{T(600, 62, "END OF TRANSMISSION", "o7", 26, "none", ls=7, anchor="middle", extra=f'stroke="{CYAN}" stroke-opacity=".3" stroke-width="7" stroke-linejoin="round"')}
{T(600, 62, "END OF TRANSMISSION", "o7", 26, INK, ls=7, anchor="middle", cls="gl")}
{T(600, 92, "DESIGNED × DEVELOPED WITH CURIOSITY  ·  NEO-DELHI GRID", "m", 13, "#FF9CEB", ls=2.5, anchor="middle")}
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20" stroke="url(#ffr)" stroke-width="1.6"/>
"""
    defs = f"""<linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05010E"/><stop offset=".6" stop-color="#1A0640"/><stop offset="1" stop-color="#070214"/></linearGradient>
<radialGradient id="fglow"><stop offset="0" stop-color="{MAGENTA}" stop-opacity=".35"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></radialGradient>
<pattern id="fwin" width="45" height="44" patternUnits="userSpaceOnUse">{tile}</pattern>
<linearGradient id="stk0" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="stk1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MAGENTA}" stop-opacity="0"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
<linearGradient id="ffr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity=".7"/><stop offset=".5" stop-color="{VIOLET}" stop-opacity=".5"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity=".7"/></linearGradient>
<clipPath id="fc"><rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="20"/></clipPath>
""" + car_symbol("fcA", neon=CYAN, tail=MAGENTA) + car_symbol("fcB", body_a="#FFE3F8", body_b="#B060B8", neon=MAGENTA, tail="#FF3B6B")
    return doc(WD, HT, "End of transmission",
               "Footer: a neon skyway at night with hover cars and light trails beneath the words "
               "End of Transmission — designed × developed with curiosity.",
               ["o7", "m"], "".join(css), body, defs)
