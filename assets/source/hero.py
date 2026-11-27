"""Hero banner: an animated Neo-Delhi skyline with flying cars, a maglev,
a fluted Neo-Minar, a glowing Neo-Lotus and a holographic name."""
import math
import random

from lib import (AMBER, CYAN, DIM, INK, MAGENTA, VIOLET, T, W, car_symbol, doc,
                 f1, train_symbol)

WD, HT = 1200, 560
G = 478  # ground line
rnd = random.Random(2099)


def stars():
    out = []
    for i in range(95):
        x = rnd.uniform(8, WD - 8)
        y = rnd.uniform(8, 330)
        in_title = 210 < x < 990 and 56 < y < 246
        if in_title and rnd.random() < 0.72:
            continue
        r = rnd.choice([0.55, 0.7, 0.85, 1.0, 1.2, 1.5])
        c = rnd.choices(["#FFFFFF", "#9EF7FF", "#FFB3F0"], [70, 18, 12])[0]
        if i % 3 == 0:
            d = rnd.uniform(2.4, 6.0)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" class="tw" '
                       f'style="animation-duration:{d:.1f}s;animation-delay:-{rnd.uniform(0, d):.1f}s"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" opacity="{rnd.uniform(.35, .9):.2f}"/>')
    return "\n".join(out)


def planet(cx=1098, cy=104, r=48):
    rx, ry, rot = 88, 17, -16
    return f"""
<g transform="translate({cx} {cy}) rotate({rot})">
  <path d="M{-rx},0 A{rx},{ry} 0 0 1 {rx},0" stroke="url(#ringG)" stroke-width="5" opacity=".75"/>
</g>
<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="url(#atmo)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#planetG)"/>
<g clip-path="url(#planetClip)" opacity=".5">
  <ellipse cx="{cx}" cy="{cy - 18}" rx="{r + 10}" ry="5" fill="#FFFFFF" opacity=".10"/>
  <ellipse cx="{cx}" cy="{cy + 2}" rx="{r + 10}" ry="7" fill="#2B1270" opacity=".55"/>
  <ellipse cx="{cx}" cy="{cy + 22}" rx="{r + 10}" ry="4" fill="#FFFFFF" opacity=".08"/>
</g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#nightG)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#9EF7FF" stroke-opacity=".35" stroke-width="1.2"/>
<g transform="translate({cx} {cy}) rotate({rot})">
  <path d="M{-rx},0 A{rx},{ry} 0 0 0 {rx},0" stroke="url(#ringG)" stroke-width="5"/>
  <path d="M{-rx + 10},0 A{rx - 10},{ry - 3} 0 0 0 {rx - 10},0" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="1"/>
</g>
<circle cx="1170" cy="172" r="8" fill="#CFC8FF"/>
<circle cx="1167" cy="170" r="2" fill="#A79DF0"/><circle cx="1173" cy="175" r="1.4" fill="#A79DF0"/>
"""


def searchlights():
    beam = "M-5,0 L5,0 L70,-430 L-70,-430 Z"
    return f"""
<g class="sl1"><path d="{beam}" fill="url(#beamG)" transform="translate(430 {G})"/></g>
<g class="sl2"><path d="{beam}" fill="url(#beamG)" transform="translate(780 {G})"/></g>
"""


def far_layer():
    parts = []
    x = -10
    while x < WD + 10:
        w = rnd.randint(20, 46)
        h = rnd.randint(64, 168)
        if 200 < x < 1000:
            h = min(h, 200)
        top = G - h
        k = rnd.random()
        if k < 0.22:
            sx = x + w / 2
            parts.append(f"M{x},{G}V{top}H{x + w}V{G}Z")
            parts.append(f"M{sx - 1.4:.1f},{top}V{top - rnd.randint(12, 36)}H{sx + 1.4:.1f}V{top}Z")
        elif k < 0.42:
            parts.append(f"M{x},{G}V{top + 10}L{x + w},{top}V{G}Z")
        elif k < 0.55:
            r = w / 2
            parts.append(f"M{x},{G}V{top + r}A{r},{r} 0 0 1 {x + w},{top + r}V{G}Z")
        else:
            parts.append(f"M{x},{G}V{top}H{x + w}V{G}Z")
        x += w + rnd.randint(-5, 3)
    d = "".join(parts)
    return (f'<path d="{d}" fill="#24104F"/>\n<path d="{d}" fill="url(#winFar)"/>\n'
            f'<rect x="0" y="300" width="{WD}" height="{G - 300}" fill="url(#hazeG)"/>')


def building(x, w, top, kind):
    g = G
    if kind == "slab":
        c = min(14, w * 0.3)
        return f"M{x},{g}V{top}H{x + w - c:.1f}L{x + w},{top + c:.1f}V{g}Z", (x + w / 2, top)
    if kind == "spire":
        sx = x + w / 2
        return (f"M{x},{g}V{top + 30}L{sx - 7:.1f},{top + 10}L{sx - 2:.1f},{top - 46}H{sx + 2:.1f}"
                f"L{sx + 7:.1f},{top + 10}L{x + w},{top + 30}V{g}Z", (sx, top - 46))
    if kind == "stepped":
        return (f"M{x},{g}V{top + 40}H{x + 8}V{top + 18}H{x + 16}V{top}H{x + w - 16}V{top + 18}"
                f"H{x + w - 8}V{top + 40}H{x + w}V{g}Z", (x + w / 2, top))
    if kind == "taper":
        return f"M{x},{g}L{x + 7},{top}H{x + w - 9}L{x + w},{g}Z", (x + w / 2, top)
    if kind == "dome":
        r = w / 2
        return f"M{x},{g}V{top + r}A{r},{r} 0 0 1 {x + w},{top + r}V{g}Z", (x + w / 2, top)
    if kind == "needle":
        return f"M{x},{g}V{top + 24}L{x + w / 2:.1f},{top - 34}L{x + w},{top + 24}V{g}Z", (x + w / 2, top - 34)
    if kind == "round":
        return (f"M{x},{g}V{top + 12}Q{x},{top} {x + 12},{top}H{x + w - 12}Q{x + w},{top} {x + w},{top + 12}V{g}Z",
                (x + w / 2, top))
    return f"M{x},{g}V{top}H{x + w}V{g}Z", (x + w / 2, top)


MIDS = [
    # x, w, top, kind, accent, edge side
    (52, 46, 268, "stepped", CYAN, "r"),
    (205, 44, 284, "spire", MAGENTA, "l"),
    (262, 50, 280, "slab", CYAN, "r"),
    (318, 64, 300, "dome", VIOLET, "l"),
    (402, 50, 256, "taper", CYAN, "r"),
    (458, 62, 292, "slab", MAGENTA, "l"),
    (530, 38, 282, "needle", CYAN, "r"),
    (650, 56, 262, "stepped", MAGENTA, "l"),
    (712, 44, 298, "slab", CYAN, "r"),
    (768, 62, 252, "taper", MAGENTA, "l"),
    (842, 52, 284, "round", CYAN, "r"),
    (902, 56, 266, "slab", VIOLET, "l"),
    (966, 50, 290, "dome", MAGENTA, "r"),
    (1024, 50, 250, "slab", CYAN, "l"),
    (1150, 54, 236, "stepped", MAGENTA, "l"),
]


def mid_layer():
    paths, edges, beacons = [], [], []
    for i, (x, w, top, kind, acc, side) in enumerate(MIDS):
        d, tip = building(x, w, top, kind)
        paths.append(d)
        ex = x + 0.8 if side == "l" else x + w - 0.8
        ey = top + (30 if kind in ("spire",) else 24 if kind == "needle" else (w / 2 if kind == "dome" else 14))
        edges.append(f'<path d="M{ex:.1f},{G}V{ey:.1f}" stroke="{acc}" stroke-width="1.3" opacity=".55"/>')
        if kind in ("spire", "needle") or i % 4 == 0:
            beacons.append((tip[0], tip[1] - 3))
    d = "".join(paths)
    out = [f'<path d="{d}" fill="url(#midG)"/>', f'<path d="{d}" fill="url(#winMid)"/>']
    out += edges
    for j, (bx, by) in enumerate(beacons):
        out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="2.2" fill="#FF3B6B" class="bk" '
                   f'style="animation-delay:-{j * 0.37:.2f}s"/>')
    # twin towers sky-bridges (spire @205 + slab @262)
    out.append('<rect x="249" y="318" width="13" height="9" fill="#1D1150"/>'
               '<path d="M249,322.5 H262" stroke="#9EF7FF" stroke-width="1.6"/>')
    out.append('<rect x="249" y="372" width="13" height="7" fill="#1D1150"/>'
               '<path d="M249,375.5 H262" stroke="#FFB3F0" stroke-width="1.4"/>')
    # twinkling windows across the mid layer
    for k in range(22):
        b = MIDS[rnd.randrange(len(MIDS))]
        x = b[0] + 6 + rnd.random() * (b[1] - 14)
        y = b[2] + 34 + rnd.random() * (G - b[2] - 60)
        c = rnd.choice([AMBER, "#9EF7FF", "#FFB3F0"])
        dur = rnd.uniform(3, 9)
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="3" height="4" fill="{c}" class="win" '
                   f'style="animation-duration:{dur:.1f}s;animation-delay:-{rnd.uniform(0, dur):.1f}s"/>')
    return "\n".join(out)


def ring_tower(cx=1105, top=262, w=48):
    x = cx - w / 2
    d, _ = building(x, w, top, "round")
    return f"""
<path d="{d}" fill="url(#midG)"/><path d="{d}" fill="url(#winMid)"/>
<path d="M{x + w - 1},{G}V{top + 12}" stroke="{CYAN}" stroke-width="1.4" opacity=".7"/>
<path d="M{cx},{top} V{top - 26}" stroke="#9EF7FF" stroke-width="1.6"/>
<circle cx="{cx}" cy="{top - 28}" r="2.4" fill="#FF3B6B" class="bk"/>
<ellipse cx="{cx}" cy="{top + 34}" rx="{w / 2 + 22}" ry="8" stroke="{CYAN}" stroke-opacity=".2" stroke-width="6"/>
<ellipse cx="{cx}" cy="{top + 34}" rx="{w / 2 + 22}" ry="8" stroke="{CYAN}" stroke-width="1.8" stroke-dasharray="18 10" class="spinA"/>
<ellipse cx="{cx}" cy="{top + 70}" rx="{w / 2 + 14}" ry="6" stroke="{MAGENTA}" stroke-opacity=".2" stroke-width="5"/>
<ellipse cx="{cx}" cy="{top + 70}" rx="{w / 2 + 14}" ry="6" stroke="{MAGENTA}" stroke-width="1.6" stroke-dasharray="12 9" class="spinB"/>
"""


def minar(cx=150, top=150, bw=66, tw=18):
    base = G
    body = f"M{cx - bw / 2},{base} L{cx - tw / 2},{top} H{cx + tw / 2} L{cx + bw / 2},{base} Z"
    flutes = []
    for fr in (0.18, 0.34, 0.5, 0.66, 0.82):
        flutes.append(f"M{cx + (fr - .5) * bw:.1f},{base} L{cx + (fr - .5) * tw:.1f},{top}")
    out = [f'<path d="{body}" fill="url(#minarG)"/>',
           f'<path d="{"".join(flutes)}" stroke="#7B66E0" stroke-opacity=".45" stroke-width="1"/>',
           f'<path d="M{cx - bw / 2 + .8},{base} L{cx - tw / 2 + .6},{top}" stroke="{CYAN}" stroke-width="1.3" opacity=".6"/>']
    for k, fr in enumerate((0.15, 0.33, 0.51, 0.69, 0.86)):
        y = base - (base - top) * fr
        half = bw / 2 + (tw / 2 - bw / 2) * fr
        out.append(f'<ellipse cx="{cx}" cy="{y:.1f}" rx="{half + 8:.1f}" ry="3.6" stroke="{MAGENTA}" '
                   f'stroke-opacity=".22" stroke-width="6"/>')
        out.append(f'<ellipse cx="{cx}" cy="{y:.1f}" rx="{half + 8:.1f}" ry="3.6" stroke="#FF7AE6" '
                   f'stroke-width="1.8" class="rise" style="animation-delay:{(4 - k) * 0.35:.2f}s"/>')
    out.append(f'<path d="M{cx - 11},{top} A11,11 0 0 1 {cx + 11},{top} Z" fill="#3A2580"/>')
    out.append(f'<path d="M{cx},{top - 11} V{top - 44}" stroke="#CFC8FF" stroke-width="1.6"/>')
    out.append(f'<circle cx="{cx}" cy="{top - 46}" r="2.6" fill="#FF3B6B" class="bk"/>')
    return "\n".join(out)


def billboard(x=708, y=322, w=118, h=24):
    msg = "DESIGN × TECH × STORY × PLAY × LEARN × "
    tw = W("m", msg, 12, 2)
    txt = T(0, 16.5, msg + msg, "m", 12, "#FF9CEB", ls=2)
    return f"""
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#12062C" stroke="{MAGENTA}" stroke-width="1.2"/>
<g clip-path="url(#bbClip)"><g transform="translate({x + 4} {y})"><g class="marq">{txt}</g></g></g>
<path d="M{x + 12},{y + h} V{y + h + 10} M{x + w - 12},{y + h} V{y + h + 10}" stroke="#3B2B7A" stroke-width="2"/>
""", tw


def maglev():
    pyl = "".join(f'<rect x="{px}" y="420" width="8" height="{G - 420}" fill="#170C3E"/>' for px in range(56, WD, 200))
    return f"""
{pyl}
<rect x="0" y="412" width="{WD}" height="8" fill="#1E1250"/>
<path d="M0,412.5 H{WD}" stroke="{CYAN}" stroke-opacity=".25" stroke-width="5"/>
<path d="M0,412.5 H{WD}" stroke="{CYAN}" stroke-width="1.3"/>
<g class="trainA"><use href="#train" transform="translate(0 398)"/></g>
"""


def front_layer():
    blocks = [(-6, 66, 224, "edge"), (66, 52, 356, "block"), (440, 58, 384, "block"),
              (690, 72, 370, "block"), (962, 64, 362, "block"), (1032, 34, 394, "block")]
    paths, edges = [], []
    for x, w, top, kind in blocks:
        if kind == "edge":
            paths.append(f"M{x},{G}V{top + 18}L{x + 18},{top}H{x + w}V{G}Z")
            edges.append(f'<path d="M{x + w - .8},{G}V{top + 1}" stroke="{MAGENTA}" stroke-width="1.5" opacity=".75"/>')
            edges.append(f'<path d="M{x + 30},{top} V{top - 30}" stroke="#CFC8FF" stroke-width="1.5"/>'
                         f'<circle cx="{x + 30}" cy="{top - 32}" r="2.4" fill="#FF3B6B" class="bk"/>')
        else:
            paths.append(f"M{x},{G}V{top}H{x + w}V{G}Z")
            edges.append(f'<path d="M{x},{top + .7}H{x + w}" stroke="{CYAN}" stroke-width="1.1" opacity=".55"/>')
    d = "".join(paths)
    return f'<path d="{d}" fill="#0B0524"/><path d="{d}" fill="url(#winFront)"/>' + "".join(edges)


def petal(cx, base, w, h, lean):
    l, r = cx - w / 2, cx + w / 2
    tx, ty = cx + lean, base - h
    return (f"M{l:.1f},{base} C{l:.1f},{base - h * .55:.1f} {tx - w * .2:.1f},{ty + h * .14:.1f} {tx:.1f},{ty:.1f} "
            f"C{tx + w * .2:.1f},{ty + h * .14:.1f} {r:.1f},{base - h * .55:.1f} {r:.1f},{base} Z")


def lotus(cx=360, base=G - 12):
    rings = [
        ("url(#lotusA)", [(-28, 42, 84, -4), (28, 42, 84, 4), (0, 46, 96, 0)]),
        ("url(#lotusB)", [(-52, 42, 64, -11), (52, 42, 64, 11), (-18, 40, 72, -3), (18, 40, 72, 3)]),
        ("url(#lotusC)", [(-80, 50, 42, -24), (80, 50, 42, 24), (-42, 44, 50, -9), (42, 44, 50, 9)]),
    ]
    out = [f'<ellipse cx="{cx}" cy="{base - 30}" rx="150" ry="70" fill="url(#lotusGlow)"/>']
    for fill, ps in rings:
        for dx, w, h, lean in ps:
            out.append(f'<path d="{petal(cx + dx, base, w, h, lean)}" fill="{fill}" stroke="#FFFFFF" '
                       f'stroke-opacity=".55" stroke-width=".9"/>')
            out.append(f'<path d="M{cx + dx},{base} Q{cx + dx + lean * .4:.1f},{base - h * .5:.1f} {cx + dx + lean},{base - h + 6}" '
                       f'stroke="#FFFFFF" stroke-opacity=".35" stroke-width=".8"/>')
    out.append(f'<rect x="{cx - 118}" y="{base}" width="236" height="12" fill="#1C1150"/>')
    out.append(f'<path d="M{cx - 118},{base + .6} H{cx + 118}" stroke="#CFC8FF" stroke-width="1.4"/>')
    out.append(f'<path d="M{cx - 100},{base + 6} H{cx + 100}" stroke="{CYAN}" stroke-opacity=".7" stroke-width="1"/>')
    return "\n".join(out)


def projector(cx=600, top=300):
    return f"""
<path d="M{cx - 14},{top + 12} L{cx - 280},244 H{cx + 280} L{cx + 14},{top + 12} Z" fill="url(#projG)" class="proj"/>
<path d="M{cx - 16},{G} V{top + 26} L{cx - 7},{top + 14} H{cx + 7} L{cx + 16},{top + 26} V{G} Z" fill="#0F0730"/>
<path d="M{cx - 16},{G} V{top + 26} L{cx - 7},{top + 14}" stroke="{CYAN}" stroke-width="1.2" opacity=".7"/>
<path d="M{cx - 18},{top + 14} Q{cx},{top + 2} {cx + 18},{top + 14} Z" fill="#2B1C6E" stroke="#9EF7FF" stroke-width="1.2"/>
<circle cx="{cx}" cy="{top + 9}" r="3.4" fill="#E6FDFF" class="pulse"/>
"""


def floor():
    lines = [f'<path d="M{600 + i * 6},{G} L{600 + i * 96},{HT}" stroke="#6A2BD9" stroke-opacity=".32"/>'
             for i in range(-16, 17)]
    n = 7
    ys = [G + 82 * (k / n) ** 1.9 for k in range(n + 2)]
    css, hl = [], []
    for k in range(n + 1):
        d = ys[k + 1] - ys[k]
        a0 = 0.08 + 0.55 * (k / n)
        a1 = 0.08 + 0.55 * ((k + 1) / n)
        css.append(f"@keyframes fl{k}{{from{{transform:translateY(0);opacity:{a0:.2f}}}"
                   f"to{{transform:translateY({d:.2f}px);opacity:{min(a1, .7):.2f}}}}}"
                   f".fl{k}{{animation:fl{k} 1.4s linear infinite}}")
        hl.append(f'<path d="M0,{ys[k]:.2f} H{WD}" stroke="#8A5CFF" class="fl{k}"/>')
    refl = (f'<rect x="132" y="{G + 2}" width="36" height="70" fill="url(#reflM)"/>'
            f'<rect x="1088" y="{G + 2}" width="34" height="60" fill="url(#reflC)"/>'
            f'<rect x="300" y="{G + 2}" width="120" height="50" fill="url(#reflW)"/>')
    body = f"""
<rect x="0" y="{G}" width="{WD}" height="{HT - G}" fill="url(#floorG)"/>
<g clip-path="url(#floorClip)">{''.join(lines)}{''.join(hl)}{refl}</g>
<rect x="0" y="{G - 1}" width="{WD}" height="3" fill="url(#horizonLine)"/>
"""
    return body, "".join(css)


def title_block():
    cx = 600
    name = "ANIKET CHAUHAN"
    size, ls = 66, 5
    tw = W("o9", name, size, ls)
    role = "AI CONTENT DESIGNER  ·  UI/UX DESIGNER  ·  CODE-SAVVY"
    sub = "@ CONVEGENIUS.AI  //  DESIGNING ENGAGING DIGITAL EXPERIENCES"
    label = "NEO-DELHI GRID  ·  2099  ·  SYSTEM ONLINE"
    lw = W("m", label, 13, 4)
    y_name = 154
    x0, x1 = cx - tw / 2 - 26, cx + tw / 2 + 26
    y0, y1 = 50, 246
    brackets = (f"M{x0},{y0 + 18}V{y0}H{x0 + 18} M{x1 - 18},{y0}H{x1}V{y0 + 18} "
                f"M{x0},{y1 - 18}V{y1}H{x0 + 18} M{x1 - 18},{y1}H{x1}V{y1 - 18}")
    return f"""
<path d="{brackets}" stroke="{CYAN}" stroke-width="2" opacity=".75"/>
<circle cx="{cx - lw / 2 - 16:.1f}" cy="77.5" r="3.6" fill="{CYAN}" class="blink"/>
<path d="M{cx - lw / 2 - 34:.1f},73 l6,4.5 l-6,4.5 Z M{cx + lw / 2 + 28:.1f},73 l-6,4.5 l6,4.5 Z" fill="{MAGENTA}"/>
{T(cx, 82, label, "m", 13, "#9EF7FF", ls=4, anchor="middle")}
<g class="glA">{T(cx - 3, y_name, name, "o9", size, CYAN, ls=ls, anchor="middle", extra='opacity=".85"')}</g>
<g class="glB">{T(cx + 3, y_name, name, "o9", size, MAGENTA, ls=ls, anchor="middle", extra='opacity=".85"')}</g>
{T(cx, y_name, name, "o9", size, "none", ls=ls, anchor="middle", extra=f'stroke="{CYAN}" stroke-opacity=".28" stroke-width="9" stroke-linejoin="round"')}
{T(cx, y_name, name, "o9", size, "none", ls=ls, anchor="middle", extra=f'stroke="{MAGENTA}" stroke-opacity=".35" stroke-width="3.5" stroke-linejoin="round"')}
{T(cx, y_name, name, "o9", size, "url(#titleG)", ls=ls, anchor="middle")}
<g clip-path="url(#titleClip)"><rect x="{x0:.1f}" y="88" width="{x1 - x0:.1f}" height="8" fill="url(#scanG)" class="scan"/></g>
{T(cx, 198, role, "sb", 22, "#A5F3FF", ls=4, anchor="middle")}
{T(cx, 229, sub, "m", 14, "#FF9CEB", ls=2.5, anchor="middle", extra='opacity=".92"')}
""", (x0, x1, tw)


def hud():
    c = CYAN
    L = 26
    corners = (f"M14,{14 + L}V14H{14 + L} M{WD - 14 - L},14H{WD - 14}V{14 + L} "
               f"M14,{HT - 14 - L}V{HT - 14}H{14 + L} M{WD - 14 - L},{HT - 14}H{WD - 14}V{HT - 14 - L}")
    bars = "".join(f'<rect x="{1112 + i * 7}" y="{536 - (i + 1) * 3}" width="4" height="{(i + 1) * 3}" fill="{CYAN}" '
                   f'opacity="{1 if i < 3 else .3}"/>' for i in range(4))
    return f"""
<rect x="1" y="1" width="{WD - 2}" height="{HT - 2}" rx="22" stroke="url(#frameG)" stroke-width="2"/>
<path d="{corners}" stroke="{c}" stroke-width="2.5"/>
{T(40, 40, "SYS://ANIKET.CHAUHAN", "m", 12, "#9EF7FF", ls=2, extra='opacity=".8"')}
{T(WD - 40, 40, "28.61°N  77.21°E", "m", 12, "#9EF7FF", ls=2, anchor="end", extra='opacity=".8"')}
{T(40, 536, "GRID-07 · NEO-DELHI", "m", 12, "#FFB3F0", ls=2, extra='opacity=".85"')}
{T(1100, 536, "UPLINK STABLE", "m", 12, "#FFB3F0", ls=2, anchor="end", extra='opacity=".85"')}
{bars}
"""


def ship():
    return f"""
<g class="ship"><g transform="translate(0 46)">
  <path d="M-10,0 L6,-2 L12,0 L6,2 Z" fill="#CFC8FF"/>
  <path d="M-4,-1 L-8,-6 M-4,1 L-8,6" stroke="#CFC8FF" stroke-width="1"/>
  <rect x="-60" y="-.6" width="48" height="1.2" fill="url(#shipT)"/>
  <circle cx="12" cy="0" r="1.6" fill="#FF3B6B" class="bk"/>
</g></g>
"""


def cars():
    lanes = [
        # y, scale, direction, duration, delays, symbol
        (276, 0.42, 1, 17, (0, 8.5), "carA"),
        (334, 0.6, -1, 12.5, (2, 8.4), "carB"),
        (388, 0.82, 1, 9.5, (1, 5.8), "carC"),
    ]
    out = {}
    css = []
    for li, (y, s, dirn, dur, delays, sym) in enumerate(lanes):
        grp = []
        for di, dl in enumerate(delays):
            cls = f"ln{li}"
            flip = f" scale({-s} {s})" if dirn < 0 else f" scale({s})"
            grp.append(f'<g class="{cls}" style="animation-delay:-{dl}s"><g transform="translate(0 {y}){flip}">'
                       f'<g class="bob" style="animation-delay:-{di * .9 + li * .4:.1f}s"><use href="#{sym}"/></g></g></g>')
        out[li] = "\n".join(grp)
        frm, to = (-180, WD + 180) if dirn > 0 else (WD + 180, -180)
        css.append(f"@keyframes ln{li}{{from{{transform:translateX({frm}px)}}to{{transform:translateX({to}px)}}}}"
                   f".ln{li}{{animation:ln{li} {dur}s linear infinite}}")
    # foreground car: crosses during the first ~45% of a 13s cycle, right-to-left
    out["fg"] = ('<g class="fg"><g transform="translate(0 512) scale(-1.25 1.25)">'
                 '<g class="bob"><use href="#carC"/></g></g></g>')
    css.append("@keyframes fg{0%{transform:translateX(1420px)}45%,100%{transform:translateX(-220px)}}"
               ".fg{animation:fg 13s linear infinite;animation-delay:-3s}")
    return out, "".join(css)


def defs_block():
    win = []
    # far windows tile
    tile = []
    for cy in range(4):
        for cx_ in range(6):
            if rnd.random() < .3:
                tile.append(f'<rect x="{cx_ * 10 + 4}" y="{cy * 12 + 4}" width="2" height="3" fill="#9C8BFF"/>')
    win.append(f'<pattern id="winFar" width="60" height="48" patternUnits="userSpaceOnUse">{"".join(tile)}</pattern>')
    tile = []
    for cy in range(6):
        for cx_ in range(6):
            r = rnd.random()
            if r < .27:
                c = rnd.choices([AMBER, "#9EF7FF", "#FFB3F0", "#FFFFFF"], [45, 30, 18, 7])[0]
                tile.append(f'<rect x="{cx_ * 9 + 3}" y="{cy * 11 + 3}" width="3" height="4.5" fill="{c}" '
                            f'opacity="{rnd.uniform(.55, .95):.2f}"/>')
    win.append(f'<pattern id="winMid" width="54" height="66" patternUnits="userSpaceOnUse">{"".join(tile)}</pattern>')
    tile = []
    for cy in range(5):
        for cx_ in range(7):
            if rnd.random() < .2:
                c = rnd.choice([AMBER, "#9EF7FF", "#FFB3F0"])
                tile.append(f'<rect x="{cx_ * 11 + 4}" y="{cy * 13 + 4}" width="4" height="5" fill="{c}" opacity=".8"/>')
    win.append(f'<pattern id="winFront" width="77" height="65" patternUnits="userSpaceOnUse">{"".join(tile)}</pattern>')

    return "".join(win) + f"""
<clipPath id="frameClip"><rect x="0" y="0" width="{WD}" height="{HT}" rx="22"/></clipPath>
<clipPath id="floorClip"><rect x="0" y="{G}" width="{WD}" height="{HT - G}"/></clipPath>
<clipPath id="planetClip"><circle cx="1098" cy="104" r="48"/></clipPath>
<clipPath id="bbClip"><rect x="709" y="323" width="116" height="22"/></clipPath>
<clipPath id="titleClip"><rect x="150" y="96" width="900" height="66"/></clipPath>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="{HT}" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="#02010C"/><stop offset=".3" stop-color="#070322"/>
  <stop offset=".55" stop-color="#150638"/><stop offset=".72" stop-color="#33094F"/>
  <stop offset=".835" stop-color="#7A1A6E"/><stop offset=".858" stop-color="#2A0640"/>
  <stop offset="1" stop-color="#05010E"/>
</linearGradient>
<radialGradient id="hglowM"><stop offset="0" stop-color="{MAGENTA}" stop-opacity=".42"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></radialGradient>
<radialGradient id="hglowC"><stop offset="0" stop-color="{CYAN}" stop-opacity=".2"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="planetG" cx=".34" cy=".3" r=".8">
  <stop offset="0" stop-color="#C3A9FF"/><stop offset=".42" stop-color="#6E43DC"/>
  <stop offset=".82" stop-color="#2A1270"/><stop offset="1" stop-color="#13063C"/>
</radialGradient>
<radialGradient id="atmo"><stop offset=".8" stop-color="{CYAN}" stop-opacity=".3"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<linearGradient id="nightG" x1="0" y1="0" x2="1" y2="1">
  <stop offset=".45" stop-color="#05010E" stop-opacity="0"/><stop offset="1" stop-color="#05010E" stop-opacity=".78"/>
</linearGradient>
<linearGradient id="ringG" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{CYAN}" stop-opacity=".2"/><stop offset=".5" stop-color="#E6FDFF"/>
  <stop offset="1" stop-color="{MAGENTA}" stop-opacity=".5"/>
</linearGradient>
<linearGradient id="beamG" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0" stop-color="#E6FDFF" stop-opacity=".2"/><stop offset="1" stop-color="#E6FDFF" stop-opacity="0"/>
</linearGradient>
<linearGradient id="hazeG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3A0B55" stop-opacity="0"/><stop offset="1" stop-color="#4B0F5E" stop-opacity=".6"/>
</linearGradient>
<linearGradient id="midG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1C0F49"/><stop offset="1" stop-color="#110732"/>
</linearGradient>
<linearGradient id="minarG" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#4A2E9A"/><stop offset=".45" stop-color="#22125A"/><stop offset="1" stop-color="#100730"/>
</linearGradient>
<linearGradient id="lotusA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9E4FF"/><stop offset="1" stop-color="#5F4CC9"/></linearGradient>
<linearGradient id="lotusB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F1FF"/><stop offset="1" stop-color="#7E6DE6"/></linearGradient>
<linearGradient id="lotusC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#9A8BF5"/></linearGradient>
<radialGradient id="lotusGlow"><stop offset="0" stop-color="#9EF7FF" stop-opacity=".3"/><stop offset=".6" stop-color="{VIOLET}" stop-opacity=".12"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<linearGradient id="projG" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="floorG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#160733"/><stop offset="1" stop-color="#04010B"/>
</linearGradient>
<linearGradient id="horizonLine" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{MAGENTA}" stop-opacity="0"/><stop offset=".25" stop-color="{MAGENTA}"/>
  <stop offset=".5" stop-color="{CYAN}"/><stop offset=".75" stop-color="{MAGENTA}"/>
  <stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="reflM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MAGENTA}" stop-opacity=".35"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></linearGradient>
<linearGradient id="reflC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".3"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="reflW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFC8FF" stop-opacity=".22"/><stop offset="1" stop-color="#CFC8FF" stop-opacity="0"/></linearGradient>
<linearGradient id="titleG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#D9FBFF"/><stop offset="1" stop-color="#E7CCFF"/>
</linearGradient>
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".35"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
<linearGradient id="frameG" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{MAGENTA}"/>
</linearGradient>
<linearGradient id="shipT" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#CFC8FF" stop-opacity="0"/><stop offset="1" stop-color="#CFC8FF" stop-opacity=".7"/></linearGradient>
""" + car_symbol("carA", neon=CYAN, tail=MAGENTA) \
      + car_symbol("carB", body_a="#FFE3F8", body_b="#B060B8", neon=MAGENTA, tail="#FF3B6B") \
      + car_symbol("carC", body_a="#F2F7FF", body_b="#7F8CC8", neon="#9EF7FF", tail=MAGENTA) \
      + train_symbol("train")


CSS = """
.tw{animation:tw 4s ease-in-out infinite alternate}@keyframes tw{from{opacity:.12}to{opacity:1}}
.bk{animation:bk 2.4s steps(1) infinite}@keyframes bk{0%,62%{opacity:1}63%,100%{opacity:.15}}
.win{animation:win 6s steps(1) infinite}@keyframes win{0%,48%{opacity:.95}49%,100%{opacity:.08}}
.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.15}}
.pulse{animation:pulse 1.6s ease-in-out infinite alternate}@keyframes pulse{from{opacity:.45}to{opacity:1}}
.proj{animation:proj 3.2s ease-in-out infinite alternate}@keyframes proj{from{opacity:.55}to{opacity:1}}
.rise{animation:rise 2.1s ease-in-out infinite}@keyframes rise{0%,100%{opacity:.35}35%{opacity:1}}
.spinA{animation:dash 3s linear infinite}.spinB{animation:dash 4.2s linear infinite reverse}
@keyframes dash{to{stroke-dashoffset:-56}}
.sl1,.sl2{transform-origin:430px 478px}.sl2{transform-origin:780px 478px}
.sl1{animation:sw 9s ease-in-out infinite alternate}.sl2{animation:sw 11s ease-in-out infinite alternate-reverse}
@keyframes sw{from{transform:rotate(-26deg)}to{transform:rotate(24deg)}}
.trainA{animation:train 8.5s linear infinite}@keyframes train{0%{transform:translateX(-260px)}70%,100%{transform:translateX(1460px)}}
.bob{animation:bob 2.6s ease-in-out infinite alternate}@keyframes bob{from{transform:translateY(-1.6px)}to{transform:translateY(1.6px)}}
.ship{animation:ship 38s linear infinite}@keyframes ship{from{transform:translateX(-80px)}to{transform:translateX(1300px)}}
.glA,.glB{opacity:0}
.glA{animation:glA 7s steps(1) infinite}.glB{animation:glB 7s steps(1) infinite}
@keyframes glA{0%,88%{opacity:0;transform:none}89%{opacity:1;transform:translate(-5px,1px)}90.5%{opacity:0}94%{opacity:1;transform:translate(4px,-1px)}95%,100%{opacity:0;transform:none}}
@keyframes glB{0%,88.5%{opacity:0;transform:none}89.5%{opacity:1;transform:translate(5px,-1px)}91%{opacity:0}94.5%{opacity:1;transform:translate(-3px,1px)}95.5%,100%{opacity:0;transform:none}}
.scan{animation:scan 3.6s linear infinite}@keyframes scan{from{transform:translateY(0)}to{transform:translateY(72px)}}
"""


def build():
    defs = defs_block()
    car_parts, car_css = cars()
    floor_body, floor_css = floor()
    bb, mw = billboard()
    marq_css = f".marq{{animation:marq 9s linear infinite}}@keyframes marq{{to{{transform:translateX(-{mw + 2:.1f}px)}}}}"
    title, _ = title_block()
    body = f"""
<g clip-path="url(#frameClip)">
<rect width="{WD}" height="{HT}" fill="url(#sky)"/>
{stars()}
{planet()}
{ship()}
<ellipse cx="600" cy="468" rx="720" ry="150" fill="url(#hglowM)"/>
<ellipse cx="600" cy="476" rx="430" ry="56" fill="url(#hglowC)"/>
{searchlights()}
{far_layer()}
{car_parts[0]}
{mid_layer()}
{ring_tower()}
{bb}
{minar()}
{car_parts[1]}
{maglev()}
{front_layer()}
{lotus()}
{projector()}
{car_parts[2]}
{floor_body}
{car_parts["fg"]}
{title}
{hud()}
</g>
"""
    return doc(WD, HT,
               "Aniket Chauhan — AI Content Designer · UI/UX Designer · Code-savvy",
               "Animated futuristic Neo-Delhi skyline at night: neon towers, a fluted Neo-Minar, a glowing "
               "Neo-Lotus, hover cars and a maglev train, with the holographic name Aniket Chauhan.",
               ["o9", "m", "sb"], CSS + car_css + floor_css + marq_css, body, defs)
