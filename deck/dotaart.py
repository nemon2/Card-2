"""Per-card Dota artwork: orbs, ability icons, gems and the scepter.

Every piece is drawn centred on the current origin and fitted into ``size``.
"""
from __future__ import annotations

import math

from .config import hx, path, rounded_rect_path, state

WHITE = hx("#ffffff")


# --- glowing orb ------------------------------------------------------------
def orb(c, size, core, mid, rim, glow):
    r = size * 0.40
    with state(c):
        for i, a in ((3, 0.09), (2, 0.15), (1, 0.24)):
            c.setFillColor(glow)
            c.setFillAlpha(a)
            c.circle(0, 0, r * (1.0 + 0.12 * i), fill=1, stroke=0)

        with state(c):
            c.circle(0, 0, r, fill=0, stroke=0)
            disc = c.beginPath()
            disc.circle(0, 0, r)
            c.clipPath(disc, stroke=0, fill=0)
            c.radialGradient(-r * 0.22, r * 0.26, r * 1.55,
                             [core, mid, rim], [0.0, 0.45, 1.0])
            # swirl
            c.setStrokeColor(core)
            c.setStrokeAlpha(0.60)
            c.setLineWidth(r * 0.20)
            c.setLineCap(1)
            pts = []
            for i in range(34):
                t = i / 33.0
                a = t * 3.5 * math.pi
                rad = r * 0.90 * (1.0 - t) ** 0.85
                pts.append((rad * math.cos(a), rad * math.sin(a)))
            sp = path(c, ("m", pts[0][0], pts[0][1]),
                      *[("l", x, y) for x, y in pts[1:]])
            c.drawPath(sp, fill=0, stroke=1)

        c.setStrokeColor(rim)
        c.setStrokeAlpha(0.45)
        c.setLineWidth(r * 0.09)
        c.circle(0, 0, r, fill=0, stroke=1)

        c.setFillColor(WHITE)
        c.setFillAlpha(0.65)
        with state(c):
            c.translate(-r * 0.32, r * 0.36)
            c.rotate(-30)
            c.scale(1.0, 0.55)
            c.circle(0, 0, r * 0.26, fill=1, stroke=0)


ORB_COLOURS = {
    "green": ("#eaffe2", "#2fae49", "#0d5424", "#5bd873"),
    "blue": ("#e4f7ff", "#2b93d6", "#0c3a60", "#5cc0f0"),
    "purple": ("#f7e8ff", "#8f3ec0", "#3d1057", "#b96ae0"),
    "orange": ("#fff2dc", "#e07d18", "#6a2a06", "#f5b45c"),
    "white": ("#ffffff", "#b9cfe2", "#5f7488", "#e8f2fa"),
}


# --- ability icon: a bold glyph in a rounded, dark tile ---------------------
def _tile(c, size, bg, edge):
    r = size * 0.5
    p = rounded_rect_path(c, -r, -r, 2 * r, 2 * r, size * 0.17)
    c.setFillColor(bg)
    c.setStrokeColor(edge)
    c.setLineWidth(size * 0.045)
    c.drawPath(p, fill=1, stroke=1)
    return p


def _poly(c, pts, color, close=True):
    cmds = [("m", pts[0][0], pts[0][1])] + [("l", x, y) for x, y in pts[1:]]
    if close:
        cmds.append(("z",))
    c.setFillColor(color)
    c.drawPath(path(c, *cmds), fill=1, stroke=0)


def _g_bolt(c, s, fg):
    _poly(c, [(0.06, 0.34), (-0.20, 0.02), (-0.02, 0.02), (-0.08, -0.34),
              (0.20, 0.00), (0.02, 0.00)], fg)


def _g_flame(c, s, fg):
    _poly(c, [(0.00, 0.36), (0.20, 0.06), (0.16, -0.12), (0.00, -0.34),
              (-0.16, -0.12), (-0.20, 0.06)], fg)
    _poly(c, [(0.00, 0.10), (0.09, -0.08), (0.00, -0.24), (-0.09, -0.08)], hx("#ffd9a0"))


def _g_blade(c, s, fg):
    _poly(c, [(-0.28, -0.20), (0.10, 0.34), (0.28, 0.10), (0.02, -0.30)], fg)
    _poly(c, [(-0.30, -0.30), (-0.12, -0.12), (-0.22, -0.02)], hx("#b9a98f"))


def _g_shield(c, s, fg):
    _poly(c, [(0.00, 0.34), (0.26, 0.20), (0.24, -0.10), (0.00, -0.34),
              (-0.24, -0.10), (-0.26, 0.20)], fg)


def _g_star(c, s, fg):
    pts = []
    for i in range(10):
        a = math.radians(90 + i * 36)
        rad = 0.34 if i % 2 == 0 else 0.15
        pts.append((rad * math.cos(a), rad * math.sin(a)))
    _poly(c, pts, fg)


def _g_spiral(c, s, fg):
    c.setStrokeColor(fg)
    c.setLineWidth(0.085)
    c.setLineCap(1)
    pts = []
    for i in range(26):
        t = i / 25.0
        a = t * 3.2 * math.pi
        rad = 0.30 * (1.0 - t * 0.85)
        pts.append((rad * math.cos(a), rad * math.sin(a)))
    c.drawPath(path(c, ("m", pts[0][0], pts[0][1]),
                    *[("l", x, y) for x, y in pts[1:]]), fill=0, stroke=1)


def _g_claw(c, s, fg):
    for dx in (-0.17, 0.0, 0.17):
        _poly(c, [(dx - 0.055, 0.32), (dx + 0.055, 0.30), (dx + 0.02, -0.32)], fg)


def _g_drop(c, s, fg):
    _poly(c, [(0.00, 0.34), (0.19, 0.00), (0.13, -0.22), (0.00, -0.32),
              (-0.13, -0.22), (-0.19, 0.00)], fg)


def _g_eye(c, s, fg):
    _poly(c, [(-0.32, 0.00), (0.00, 0.22), (0.32, 0.00), (0.00, -0.22)], fg)
    c.setFillColor(hx("#16110d"))
    c.circle(0, 0, 0.105, fill=1, stroke=0)


def _g_rune(c, s, fg):
    c.setStrokeColor(fg)
    c.setLineWidth(0.085)
    c.setLineCap(0)
    c.drawPath(path(c, ("m", -0.22, -0.30), ("l", -0.22, 0.30), ("l", 0.10, -0.06),
                    ("l", 0.22, -0.06)), fill=0, stroke=1)
    c.drawPath(path(c, ("m", 0.22, 0.30), ("l", 0.22, -0.30)), fill=0, stroke=1)


GLYPHS = (_g_bolt, _g_flame, _g_blade, _g_shield, _g_star,
          _g_spiral, _g_claw, _g_drop, _g_eye, _g_rune)

TILE_BG = hx("#1d2530")
TILE_EDGE = hx("#0e1319")
GLYPH_COLOURS = ("#6fd0f5", "#f0912c", "#cfd8e2", "#e8c23a", "#b96ae0",
                 "#5bd873", "#e03a29", "#4fc3e8", "#f0d78a", "#9fb4c8")


def ability(c, size, index):
    """One ability tile; ``index`` picks the glyph and its colour."""
    with state(c):
        _tile(c, size, TILE_BG, TILE_EDGE)
        with state(c):
            c.scale(size, size)
            GLYPHS[index % len(GLYPHS)](c, 1.0, hx(GLYPH_COLOURS[index % len(GLYPH_COLOURS)]))


# --- gems ------------------------------------------------------------------
GEMS = (
    ("#b96ae0", "#7a2fa8"), ("#f0912c", "#a8560c"), ("#4f8fe0", "#1f4f9c"),
    ("#e8c23a", "#a8830c"), ("#e03a29", "#8f1a10"), ("#8d97a6", "#4a525e"),
    ("#5bd873", "#1f8c3c"), ("#3fd0e0", "#1078a0"), ("#cfd8e2", "#7d8b9b"),
)


#: outline, then the lit facet, for each silhouette
_GEM_SHAPES = (
    ([(0.00, 0.44), (0.26, 0.10), (0.17, -0.42), (-0.17, -0.42), (-0.26, 0.10)],
     [(0.00, 0.44), (0.26, 0.10), (0.04, 0.02), (-0.06, -0.42), (-0.17, -0.42),
      (-0.26, 0.10)]),
    ([(-0.06, 0.46), (0.22, 0.18), (0.30, -0.20), (0.10, -0.44), (-0.24, -0.34),
      (-0.30, 0.06)],
     [(-0.06, 0.46), (0.22, 0.18), (0.02, 0.06), (0.10, -0.44), (-0.24, -0.34),
      (-0.30, 0.06)]),
    ([(0.00, 0.40), (0.30, 0.22), (0.24, -0.16), (0.00, -0.44), (-0.24, -0.16),
      (-0.30, 0.22)],
     [(0.00, 0.40), (0.30, 0.22), (0.06, 0.04), (0.00, -0.44), (-0.24, -0.16),
      (-0.30, 0.22)]),
)


def gem(c, size, index):
    """A faceted crystal; ``index`` picks its colour pair and silhouette."""
    light, dark = (hx(v) for v in GEMS[index % len(GEMS)])
    outline, facet = _GEM_SHAPES[index % len(_GEM_SHAPES)]
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setStrokeColor(hx("#16110d"))
        c.setLineWidth(0.050)
        c.setFillColor(dark)
        c.drawPath(path(c, ("m", *outline[0]), *[("l", *q) for q in outline[1:]],
                        ("z",)), fill=1, stroke=1)
        c.setFillColor(light)
        c.drawPath(path(c, ("m", *facet[0]), *[("l", *q) for q in facet[1:]],
                        ("z",)), fill=1, stroke=1)


# --- Aghanim's scepter -----------------------------------------------------
def scepter(c, size, wood, wood_d, iris, glow):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setFillColor(glow)
        c.setFillAlpha(0.20)
        c.circle(0.0, 0.26, 0.30, fill=1, stroke=0)
        c.setFillAlpha(1.0)

        c.setStrokeColor(wood)
        c.setLineWidth(0.085)
        c.drawPath(path(c, ("m", -0.06, -0.48), ("c", 0.02, -0.24, -0.02, 0.02, 0.0, 0.10)),
                   fill=0, stroke=1)
        c.setStrokeColor(wood_d)
        c.setLineWidth(0.030)
        c.drawPath(path(c, ("m", -0.05, -0.40), ("c", 0.02, -0.20, -0.01, 0.00, 0.0, 0.06)),
                   fill=0, stroke=1)

        for sx in (-1, 1):
            c.setStrokeColor(wood)
            c.setLineWidth(0.070)
            c.drawPath(path(c, ("m", 0.02 * sx, 0.08),
                            ("c", 0.22 * sx, 0.10, 0.28 * sx, 0.34, 0.16 * sx, 0.46)),
                       fill=0, stroke=1)

        c.setFillColor(iris)
        c.setStrokeColor(wood_d)
        c.setLineWidth(0.045)
        c.circle(0.0, 0.26, 0.175, fill=1, stroke=1)
        c.setFillColor(hx("#16110d"))
        c.drawPath(path(c, ("m", 0.0, 0.40), ("c", 0.075, 0.32, 0.075, 0.20, 0.0, 0.12),
                        ("c", -0.075, 0.20, -0.075, 0.32, 0.0, 0.40), ("z",)),
                   fill=1, stroke=0)


# --- per-rank pip art -------------------------------------------------------
#: Each rank keeps its own concept, exactly as the reference cards did.
#: (kind, key-per-index, size multiplier)
_RANK_ART = {
    "2": ("scepter", lambda i: 0, 1.30),
    "3": ("orb", lambda i: "green", 1.00),
    "4": ("hero", lambda i: ("crystal_maiden", "meepo", "queen_of_pain",
                             "pudge")[i], 1.06),
    "5": ("hero", lambda i: "meepo", 1.06),
    "6": ("orb", lambda i: ("blue", "purple", "orange")[i % 3], 1.00),
    "7": ("hero", lambda i: "shadow_fiend", 1.06),
    "8": ("ability", lambda i: i, 0.96),
    "9": ("gem", lambda i: i, 1.06),
    "10": ("ability", lambda i: i, 0.96),
}


def draw_rank_pip(c, size, rank, index):
    """Draw the pip art this rank uses, centred on the current origin."""
    from .pixelart import HEROES, draw_sprite
    kind, pick, scale = _RANK_ART[rank]
    s = size * scale
    key = pick(index)
    if kind == "orb":
        orb(c, s, *[hx(v) for v in ORB_COLOURS[key]])
    elif kind == "hero":
        draw_sprite(c, HEROES[key], s)
    elif kind == "ability":
        ability(c, s, key)
    elif kind == "gem":
        gem(c, s, key)
    elif kind == "scepter":
        scepter(c, s, hx("#8a6a45"), hx("#4a3520"), hx("#3aa8e8"), hx("#5cc0f0"))
    else:  # pragma: no cover - programming error
        raise ValueError(kind)
