"""One hand-drawn character per card - the easter egg.

Each suit gets nine characters from its game, one per rank. They are authored
in a unit box (-0.5..0.5) and drawn through ``deck.sketch``, so every line
carries a small deterministic wobble and reads as pen work.

Drawing order is always body, then head filled with the paper colour (so the
body line does not show through it), then features on top.
"""
from __future__ import annotations

import math

from .config import state
from .sketch import blob, ink, oval

# --- shared building blocks -------------------------------------------------


def shoulders(c, k, w=0.34, top=-0.15, seed=1):
    ink(c, [("m", -w, -0.50), ("c", -w * 0.92, -0.30, -w * 0.46, top, 0.0, top),
            ("c", w * 0.46, top, w * 0.92, -0.30, w, -0.50)], k, seed=seed)


def head(c, k, paper, cx=0.0, cy=0.15, rx=0.26, ry=0.28, seed=2):
    oval(c, cx, cy, rx, ry, k, seed=seed, fill=paper)


def eyes(c, k, y=0.15, dx=0.105, r=0.052):
    blob(c, -dx, y, r, k)
    blob(c, dx, y, r, k)


def slit_eyes(c, k, y=0.15, dx=0.115, w=0.085, seed=9):
    for sx in (-1, 1):
        ink(c, [("m", sx * dx - w / 2, y), ("l", sx * dx + w / 2, y)],
            k, width=0.075, seed=seed + sx)


def horns(c, k, paper, spread=0.56, rise=0.50, base=0.22, seed=5):
    for sx in (1, -1):
        ink(c, [("m", -0.15 * sx, base + 0.04),
                ("c", -0.30 * sx, base + 0.14, -0.44 * sx, rise - 0.10, -spread * sx, rise),
                ("c", -0.47 * sx, rise - 0.20, -0.36 * sx, base - 0.02, -0.26 * sx, base - 0.10)],
            k, seed=seed + sx, close=True, fill=k)


def smile(c, k, y=0.02, w=0.13, depth=0.07, seed=8):
    ink(c, [("m", -w, y), ("c", -w * 0.4, y - depth, w * 0.4, y - depth, w, y)], k, seed=seed)


# ===========================================================================
# Hollow Knight - spades
# ===========================================================================
def hk_knight(c, k, a, paper):
    ink(c, [("m", -0.35, -0.50), ("c", -0.31, -0.24, -0.18, -0.12, 0.0, -0.12),
            ("c", 0.18, -0.12, 0.31, -0.24, 0.35, -0.50)], k, seed=3)
    ink(c, [("m", -0.35, -0.50), ("l", 0.35, -0.50)], k, seed=4)
    horns(c, k, paper, spread=0.54, rise=0.50, base=0.22, seed=5)
    head(c, k, paper, cy=0.13, rx=0.25, ry=0.27, seed=7)
    eyes(c, k, y=0.13)


def hk_hornet(c, k, a, paper):
    shoulders(c, k, w=0.30, seed=11)
    ink(c, [("m", -0.40, 0.30), ("c", -0.20, 0.46, 0.20, 0.46, 0.40, 0.30)], k, seed=12)
    head(c, k, paper, cy=0.14, rx=0.24, ry=0.27, seed=13)
    for sx in (-1, 1):
        ink(c, [("m", 0.10 * sx, 0.36), ("l", 0.24 * sx, 0.52), ("l", 0.27 * sx, 0.31)],
            k, seed=14 + sx, close=True, fill=k)
    ink(c, [("m", 0.0, 0.38), ("l", 0.0, 0.56)], k, seed=16)
    eyes(c, k, y=0.13, dx=0.100)
    ink(c, [("m", 0.26, -0.28), ("l", 0.52, 0.22)], k, width=0.045, seed=17)


def hk_grimm(c, k, a, paper):
    ink(c, [("m", -0.42, -0.50), ("c", -0.34, -0.20, -0.16, -0.10, 0.0, -0.10),
            ("c", 0.16, -0.10, 0.34, -0.20, 0.42, -0.50)], k, seed=21)
    for sx in (1, -1):
        ink(c, [("m", -0.14 * sx, 0.26), ("c", -0.32 * sx, 0.42, -0.44 * sx, 0.58, -0.46 * sx, 0.68),
                ("c", -0.52 * sx, 0.52, -0.44 * sx, 0.30, -0.26 * sx, 0.15)],
            k, seed=22 + sx, close=True, fill=k)
    head(c, k, paper, cy=0.12, rx=0.235, ry=0.28, seed=24)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.05, 0.20), ("l", sx * 0.19, 0.12)], k, width=0.07, seed=25 + sx)
    ink(c, [("m", -0.12, -0.02), ("l", 0.12, -0.02)], k, seed=27)
    for x in (-0.06, 0.0, 0.06):
        ink(c, [("m", x, -0.02), ("l", x, -0.08)], k, width=0.035, seed=28)


def hk_quirrel(c, k, a, paper):
    oval(c, 0.27, -0.26, 0.20, 0.17, k, seed=31)
    shoulders(c, k, w=0.30, seed=32)
    head(c, k, paper, cx=-0.04, cy=0.15, rx=0.25, ry=0.26, seed=33)
    for sx in (1, -1):
        ink(c, [("m", -0.12 * sx - 0.04, 0.30), ("c", -0.24 * sx - 0.04, 0.40,
                -0.30 * sx - 0.04, 0.44, -0.34 * sx - 0.04, 0.46),
                ("c", -0.30 * sx - 0.04, 0.36, -0.24 * sx - 0.04, 0.28, -0.18 * sx - 0.04, 0.24)],
            k, seed=34 + sx, close=True, fill=k)
    eyes(c, k, y=0.13, dx=0.095)


def hk_elderbug(c, k, a, paper):
    ink(c, [("m", -0.30, -0.50), ("c", -0.27, -0.22, -0.15, -0.10, 0.0, -0.10),
            ("c", 0.15, -0.10, 0.27, -0.22, 0.30, -0.50)], k, seed=41)
    ink(c, [("m", -0.30, -0.50), ("l", 0.30, -0.50)], k, seed=42)
    head(c, k, paper, cy=0.12, rx=0.25, ry=0.25, seed=43)
    eyes(c, k, y=0.14, dx=0.095, r=0.048)
    smile(c, k, y=0.00, w=0.10, depth=0.05, seed=44)


def hk_zote(c, k, a, paper):
    oval(c, 0.0, -0.20, 0.32, 0.22, k, seed=51)
    shoulders(c, k, w=0.32, seed=52)
    ink(c, [("m", -0.24, -0.06), ("l", -0.26, 0.28), ("l", 0.26, 0.28),
            ("l", 0.24, -0.06)], k, seed=53, close=True, fill=paper)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.05, 0.19), ("l", sx * 0.19, 0.24)], k, width=0.055, seed=54 + sx)
    eyes(c, k, y=0.10, dx=0.105, r=0.048)
    ink(c, [("m", -0.09, 0.01), ("l", 0.09, 0.01)], k, seed=56)


def hk_false_knight(c, k, a, paper):
    ink(c, [("m", -0.44, -0.50), ("c", -0.40, -0.18, -0.20, -0.06, 0.0, -0.06),
            ("c", 0.20, -0.06, 0.40, -0.18, 0.44, -0.50)], k, seed=61)
    ink(c, [("m", -0.30, 0.02), ("l", -0.32, 0.30), ("c", -0.10, 0.44, 0.10, 0.44, 0.32, 0.30),
            ("l", 0.30, 0.02)], k, seed=62, close=True, fill=paper)
    ink(c, [("m", -0.20, 0.16), ("l", 0.20, 0.16)], k, width=0.085, seed=63)
    ink(c, [("m", 0.30, -0.30), ("l", 0.46, 0.18)], k, width=0.05, seed=64)
    oval(c, 0.49, 0.28, 0.12, 0.12, k, seed=65, fill=paper)


def hk_mantis(c, k, a, paper):
    ink(c, [("m", -0.40, -0.50), ("l", -0.30, -0.12), ("l", 0.30, -0.12), ("l", 0.40, -0.50)],
        k, seed=71)
    for sx in (1, -1):
        ink(c, [("m", -0.30 * sx, -0.10), ("l", -0.50 * sx, 0.30), ("l", -0.40 * sx, 0.32)],
            k, width=0.045, seed=72 + sx)
    ink(c, [("m", -0.22, 0.00), ("l", -0.26, 0.26), ("l", 0.0, 0.48), ("l", 0.26, 0.26),
            ("l", 0.22, 0.00)], k, seed=74, close=True, fill=paper)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.14), ("l", sx * 0.175, 0.22)], k, width=0.065, seed=75 + sx)


def hk_vessel(c, k, a, paper):
    ink(c, [("m", -0.30, -0.50), ("c", -0.26, -0.20, -0.14, -0.08, 0.0, -0.08),
            ("c", 0.14, -0.08, 0.26, -0.20, 0.30, -0.50)], k, seed=81)
    ink(c, [("m", -0.30, -0.50), ("l", 0.30, -0.50)], k, seed=82)
    horns(c, k, paper, spread=0.62, rise=0.60, base=0.20, seed=83)
    head(c, k, paper, cy=0.10, rx=0.215, ry=0.29, seed=85)
    eyes(c, k, y=0.12, dx=0.090, r=0.050)
    ink(c, [("m", -0.34, -0.32), ("l", -0.52, 0.30)], k, width=0.045, seed=86)


# ===========================================================================
# Clash Royale - clubs
# ===========================================================================
def cr_knight(c, k, a, paper):
    shoulders(c, k, w=0.36, top=-0.12, seed=101)
    ink(c, [("m", -0.26, -0.10), ("l", -0.27, 0.14), ("c", -0.27, 0.36, 0.27, 0.36, 0.27, 0.14),
            ("l", 0.26, -0.10)], k, seed=102, close=True, fill=paper)
    ink(c, [("m", -0.18, 0.08), ("l", 0.18, 0.08)], k, width=0.085, seed=103)
    ink(c, [("m", 0.0, 0.30), ("c", 0.10, 0.46, 0.20, 0.54, 0.28, 0.55),
            ("c", 0.21, 0.44, 0.12, 0.35, 0.05, 0.28)], k, seed=104, close=True, fill=paper)


def cr_archer(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=111)
    head(c, k, paper, cy=0.08, rx=0.20, ry=0.20, seed=113)
    ink(c, [("m", -0.28, -0.04), ("c", -0.32, 0.42, 0.32, 0.42, 0.28, -0.04)], k, seed=112)
    eyes(c, k, y=0.08, dx=0.080, r=0.042)
    ink(c, [("m", 0.30, -0.34), ("c", 0.52, -0.12, 0.52, 0.22, 0.30, 0.44)], k, width=0.045, seed=114)
    ink(c, [("m", 0.30, -0.34), ("l", 0.30, 0.44)], k, width=0.032, seed=115)


def cr_goblin(c, k, a, paper):
    shoulders(c, k, w=0.30, seed=121)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.20, 0.22), ("l", sx * 0.46, 0.34), ("l", sx * 0.21, 0.06)],
            k, seed=122 + sx, close=True, fill=paper)
    head(c, k, paper, cy=0.14, rx=0.23, ry=0.24, seed=124)
    eyes(c, k, y=0.18, dx=0.090, r=0.046)
    ink(c, [("m", -0.11, 0.02), ("c", -0.04, 0.10, 0.04, 0.10, 0.11, 0.02)], k, seed=125)
    ink(c, [("m", 0.30, -0.30), ("l", 0.44, 0.10)], k, width=0.045, seed=126)


def cr_giant(c, k, a, paper):
    ink(c, [("m", -0.46, -0.50), ("c", -0.42, -0.16, -0.22, -0.04, 0.0, -0.04),
            ("c", 0.22, -0.04, 0.42, -0.16, 0.46, -0.50)], k, seed=131)
    head(c, k, paper, cy=0.20, rx=0.27, ry=0.26, seed=132)
    eyes(c, k, y=0.26, dx=0.105, r=0.048)
    ink(c, [("m", -0.22, 0.14), ("c", -0.26, -0.08, -0.16, -0.24, 0.0, -0.24),
            ("c", 0.16, -0.24, 0.26, -0.08, 0.22, 0.14)], k, seed=133)
    ink(c, [("m", -0.14, 0.11), ("c", -0.07, 0.03, 0.07, 0.03, 0.14, 0.11)],
        k, width=0.05, seed=134)


def cr_wizard(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=141)
    head(c, k, paper, cy=0.06, rx=0.22, ry=0.22, seed=142)
    ink(c, [("m", -0.30, 0.20), ("l", 0.30, 0.20), ("l", 0.06, 0.60)], k, seed=143,
        close=True, fill=paper)
    eyes(c, k, y=0.06, dx=0.085, r=0.044)
    ink(c, [("m", -0.14, -0.06), ("c", -0.06, -0.18, 0.06, -0.18, 0.14, -0.06)], k, seed=144)
    oval(c, 0.38, -0.16, 0.12, 0.12, k, seed=145, fill=paper)
    for ang in (-0.14, 0.0, 0.14):
        ink(c, [("m", 0.38 + ang, -0.02), ("l", 0.38 + ang * 1.6, 0.10)], k, width=0.035, seed=146)


def cr_hog_rider(c, k, a, paper):
    shoulders(c, k, w=0.34, seed=151)
    head(c, k, paper, cy=0.12, rx=0.23, ry=0.24, seed=152)
    ink(c, [("m", -0.06, 0.34), ("c", -0.02, 0.50, 0.06, 0.56, 0.12, 0.58),
            ("c", 0.10, 0.44, 0.06, 0.36, 0.04, 0.32)], k, seed=153, close=True, fill=k)
    eyes(c, k, y=0.14, dx=0.090, r=0.046)
    ink(c, [("m", -0.10, 0.00), ("l", 0.10, 0.00)], k, seed=154)
    ink(c, [("m", 0.28, -0.32), ("l", 0.44, 0.14)], k, width=0.05, seed=155)
    ink(c, [("m", 0.34, 0.14), ("l", 0.54, 0.20), ("l", 0.50, 0.34), ("l", 0.30, 0.28)],
        k, width=0.04, seed=156, close=True, fill=paper)


def cr_pekka(c, k, a, paper):
    ink(c, [("m", -0.44, -0.50), ("l", -0.34, -0.08), ("l", 0.34, -0.08), ("l", 0.44, -0.50)],
        k, seed=161)
    ink(c, [("m", -0.25, -0.06), ("l", -0.27, 0.20), ("l", 0.0, 0.46), ("l", 0.27, 0.20),
            ("l", 0.25, -0.06)], k, seed=162, close=True, fill=paper)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.12), ("l", sx * 0.185, 0.20)], k, width=0.07, seed=163 + sx)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.26, 0.22), ("l", sx * 0.40, 0.48)], k, width=0.042, seed=165 + sx)


def cr_skeleton(c, k, a, paper):
    ink(c, [("m", -0.20, -0.50), ("l", -0.14, -0.14), ("l", 0.14, -0.14), ("l", 0.20, -0.50)],
        k, seed=171)
    for y in (-0.44, -0.34, -0.24):
        ink(c, [("m", -0.17, y), ("l", 0.17, y)], k, width=0.034, seed=172)
    head(c, k, paper, cy=0.14, rx=0.24, ry=0.25, seed=173)
    blob(c, -0.095, 0.18, 0.062, k)
    blob(c, 0.095, 0.18, 0.062, k)
    ink(c, [("m", -0.02, 0.06), ("l", 0.02, 0.06)], k, width=0.05, seed=174)
    for x in (-0.09, -0.03, 0.03, 0.09):
        ink(c, [("m", x, -0.02), ("l", x, -0.09)], k, width=0.032, seed=175)
    ink(c, [("m", -0.13, -0.02), ("l", 0.13, -0.02)], k, width=0.034, seed=176)


def cr_king(c, k, a, paper):
    ink(c, [("m", -0.44, -0.50), ("c", -0.40, -0.14, -0.20, -0.02, 0.0, -0.02),
            ("c", 0.20, -0.02, 0.40, -0.14, 0.44, -0.50)], k, seed=181)
    head(c, k, paper, cy=0.16, rx=0.25, ry=0.24, seed=182)
    eyes(c, k, y=0.22, dx=0.100, r=0.046)
    ink(c, [("m", -0.21, 0.10), ("c", -0.25, -0.10, -0.15, -0.26, 0.0, -0.26),
            ("c", 0.15, -0.26, 0.25, -0.10, 0.21, 0.10)], k, seed=183)
    ink(c, [("m", -0.13, 0.08), ("c", -0.06, 0.01, 0.06, 0.01, 0.13, 0.08)],
        k, width=0.048, seed=185)
    ink(c, [("m", -0.28, 0.34), ("l", -0.28, 0.54), ("l", -0.14, 0.42), ("l", 0.0, 0.58),
            ("l", 0.14, 0.42), ("l", 0.28, 0.54), ("l", 0.28, 0.34)],
        k, seed=184, close=True, fill=paper)


# ===========================================================================
# Dota 2 - hearts
# ===========================================================================
def dt_pudge(c, k, a, paper):
    ink(c, [("m", -0.46, -0.50), ("c", -0.44, -0.14, -0.24, 0.0, 0.0, 0.0),
            ("c", 0.24, 0.0, 0.44, -0.14, 0.46, -0.50)], k, seed=201)
    head(c, k, paper, cy=0.22, rx=0.26, ry=0.24, seed=202)
    eyes(c, k, y=0.28, dx=0.100, r=0.046)
    ink(c, [("m", -0.14, 0.10), ("l", 0.14, 0.10)], k, seed=203)
    for x in (-0.09, -0.01, 0.07):
        ink(c, [("m", x, 0.14), ("l", x + 0.03, 0.06)], k, width=0.032, seed=204)
    ink(c, [("m", 0.34, -0.34), ("l", 0.50, 0.08), ("c", 0.54, 0.22, 0.40, 0.26, 0.36, 0.14)],
        k, width=0.045, seed=205)


def dt_juggernaut(c, k, a, paper):
    shoulders(c, k, w=0.33, seed=211)
    head(c, k, paper, cy=0.14, rx=0.24, ry=0.27, seed=212)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.20), ("l", sx * 0.175, 0.20)], k, width=0.07, seed=213 + sx)
    for x in (-0.10, 0.0, 0.10):
        ink(c, [("m", x, 0.04), ("l", x, -0.06)], k, width=0.034, seed=215)
    ink(c, [("m", -0.13, 0.04), ("l", 0.13, 0.04)], k, width=0.036, seed=216)
    ink(c, [("m", 0.0, 0.41), ("c", 0.06, 0.52, 0.14, 0.56, 0.20, 0.56)], k, width=0.05, seed=217)
    ink(c, [("m", -0.30, -0.30), ("l", -0.50, 0.24)], k, width=0.045, seed=218)


def dt_crystal_maiden(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=221)
    head(c, k, paper, cy=0.06, rx=0.20, ry=0.20, seed=223)
    ink(c, [("m", -0.29, -0.06), ("c", -0.34, 0.44, 0.34, 0.44, 0.29, -0.06)], k, seed=222)
    ink(c, [("m", -0.29, -0.06), ("c", -0.18, 0.06, 0.18, 0.06, 0.29, -0.06)],
        k, width=0.042, seed=226)
    eyes(c, k, y=0.06, dx=0.080, r=0.042)
    for ang in range(6):
        t = math.radians(ang * 60)
        ink(c, [("m", 0.40 + 0.0, -0.22), ("l", 0.40 + 0.11 * math.cos(t), -0.22 + 0.11 * math.sin(t))],
            k, width=0.032, seed=224 + ang)


def dt_axe(c, k, a, paper):
    ink(c, [("m", -0.44, -0.50), ("c", -0.40, -0.16, -0.20, -0.04, 0.0, -0.04),
            ("c", 0.20, -0.04, 0.40, -0.16, 0.44, -0.50)], k, seed=231)
    head(c, k, paper, cy=0.16, rx=0.24, ry=0.24, seed=232)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.18, 0.30), ("l", sx * 0.40, 0.50), ("l", sx * 0.22, 0.20)],
            k, seed=233 + sx, close=True, fill=paper)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.24), ("l", sx * 0.175, 0.16)], k, width=0.065, seed=235 + sx)
    ink(c, [("m", -0.14, 0.02), ("l", 0.14, 0.02)], k, seed=237)
    for x in (-0.07, 0.0, 0.07):
        ink(c, [("m", x, 0.02), ("l", x, -0.06)], k, width=0.032, seed=238)


def dt_invoker(c, k, a, paper):
    shoulders(c, k, w=0.30, seed=241)
    head(c, k, paper, cy=0.20, rx=0.22, ry=0.22, seed=242)
    slit_eyes(c, k, y=0.24, dx=0.095, w=0.075, seed=243)
    ink(c, [("m", -0.16, 0.10), ("c", -0.12, -0.24, 0.12, -0.24, 0.16, 0.10)],
        k, seed=244, close=True, fill=paper)
    for cx, cy in ((-0.40, 0.30), (-0.44, 0.06), (0.42, 0.22)):
        oval(c, cx, cy, 0.085, 0.085, k, seed=245, fill=paper)


def dt_sniper(c, k, a, paper):
    shoulders(c, k, w=0.30, seed=251)
    head(c, k, paper, cy=0.10, rx=0.22, ry=0.21, seed=252)
    ink(c, [("m", -0.34, 0.26), ("l", 0.34, 0.26)], k, seed=253)
    ink(c, [("m", -0.20, 0.26), ("c", -0.22, 0.50, 0.22, 0.50, 0.20, 0.26)],
        k, seed=254, close=True, fill=paper)
    for sx in (-1, 1):
        oval(c, sx * 0.105, 0.10, 0.075, 0.075, k, seed=255 + sx, fill=paper)
    ink(c, [("m", -0.03, 0.10), ("l", 0.03, 0.10)], k, width=0.034, seed=257)
    ink(c, [("m", -0.40, -0.10), ("l", 0.34, -0.34)], k, width=0.05, seed=258)


def dt_lina(c, k, a, paper):
    shoulders(c, k, w=0.30, seed=261)
    head(c, k, paper, cy=0.08, rx=0.21, ry=0.22, seed=262)
    for x0, tipx, h in ((-0.15, -0.26, 0.48), (0.0, 0.03, 0.62), (0.15, 0.26, 0.50)):
        ink(c, [("m", x0 - 0.07, 0.26),
                ("c", x0 - 0.05, 0.38, tipx - 0.02, h - 0.10, tipx, h),
                ("c", tipx + 0.02, h - 0.16, x0 + 0.09, 0.38, x0 + 0.07, 0.26)],
            k, seed=263 + int(h * 100), close=True, fill=paper)
    eyes(c, k, y=0.10, dx=0.082, r=0.042)
    smile(c, k, y=-0.02, w=0.10, depth=0.055, seed=266)


def dt_antimage(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=271)
    head(c, k, paper, cy=0.14, rx=0.23, ry=0.25, seed=272)
    slit_eyes(c, k, y=0.18, dx=0.105, w=0.085, seed=273)
    ink(c, [("m", 0.0, 0.39), ("l", 0.0, 0.56)], k, width=0.045, seed=274)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.30, -0.34), ("c", sx * 0.52, -0.12, sx * 0.50, 0.20, sx * 0.34, 0.34)],
            k, width=0.045, seed=275 + sx)


def dt_phantom(c, k, a, paper):
    shoulders(c, k, w=0.31, seed=281)
    head(c, k, paper, cy=0.08, rx=0.20, ry=0.21, seed=283)
    ink(c, [("m", -0.29, -0.04), ("c", -0.34, 0.46, 0.34, 0.46, 0.29, -0.04)], k, seed=282)
    ink(c, [("m", -0.13, 0.12), ("l", 0.13, 0.12)], k, width=0.075, seed=284)
    ink(c, [("m", 0.28, -0.32), ("l", 0.46, 0.06)], k, width=0.045, seed=285)
    ink(c, [("m", 0.34, -0.14), ("l", 0.44, -0.20)], k, width=0.034, seed=286)


# ===========================================================================
# Apex Legends - diamonds
# ===========================================================================
def ap_wraith(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=301)
    head(c, k, paper, cy=0.06, rx=0.19, ry=0.19, seed=303)
    ink(c, [("m", -0.29, -0.06), ("c", -0.34, 0.46, 0.34, 0.46, 0.29, -0.06)], k, seed=302)
    slit_eyes(c, k, y=0.06, dx=0.085, w=0.070, seed=304)
    ink(c, [("m", 0.46, -0.30), ("c", 0.28, -0.22, 0.30, -0.02, 0.44, -0.04),
            ("c", 0.52, -0.06, 0.50, -0.18, 0.40, -0.18)], k, width=0.04, seed=305)


def ap_bloodhound(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=311)
    head(c, k, paper, cy=0.16, rx=0.24, ry=0.25, seed=312)
    for sx in (-1, 1):
        oval(c, sx * 0.105, 0.22, 0.072, 0.072, k, seed=313 + sx, fill=paper)
        blob(c, sx * 0.105, 0.22, 0.030, k)
    ink(c, [("m", -0.09, 0.06), ("l", 0.0, -0.14), ("l", 0.09, 0.06)], k, seed=315,
        close=True, fill=paper)
    ink(c, [("m", -0.22, 0.38), ("c", -0.10, 0.50, 0.10, 0.50, 0.22, 0.38)], k, seed=316)


def ap_pathfinder(c, k, a, paper):
    shoulders(c, k, w=0.30, seed=321)
    head(c, k, paper, cy=0.14, rx=0.26, ry=0.26, seed=322)
    slit_eyes(c, k, y=0.22, dx=0.110, w=0.080, seed=323)
    smile(c, k, y=0.04, w=0.12, depth=0.075, seed=324)
    ink(c, [("m", 0.19, 0.34), ("c", 0.27, 0.44, 0.30, 0.50, 0.30, 0.56)], k, width=0.04, seed=325)
    blob(c, 0.30, 0.58, 0.045, k)


def ap_octane(c, k, a, paper):
    shoulders(c, k, w=0.31, seed=331)
    head(c, k, paper, cy=0.14, rx=0.23, ry=0.24, seed=332)
    for sx in (-1, 1):
        oval(c, sx * 0.105, 0.22, 0.068, 0.058, k, seed=333 + sx, fill=paper)
    ink(c, [("m", -0.16, 0.04), ("l", 0.16, 0.04), ("l", 0.12, -0.10), ("l", -0.12, -0.10)],
        k, seed=335, close=True, fill=paper)
    for x in (-0.05, 0.05):
        ink(c, [("m", x, 0.02), ("l", x, -0.08)], k, width=0.030, seed=336)
    for sx, h in ((-1, 0.50), (1, 0.52)):
        ink(c, [("m", sx * 0.06, 0.36), ("l", sx * 0.20, h)], k, width=0.042, seed=337 + sx)


def ap_lifeline(c, k, a, paper):
    shoulders(c, k, w=0.31, seed=341)
    head(c, k, paper, cy=0.12, rx=0.22, ry=0.23, seed=342)
    for sx in (-1, 1):
        for dy in (0.0, 0.10):
            ink(c, [("m", sx * 0.20, 0.22 - dy), ("c", sx * 0.34, 0.16 - dy,
                    sx * 0.36, 0.00 - dy, sx * 0.30, -0.12 - dy)], k, width=0.04, seed=343 + sx)
    eyes(c, k, y=0.16, dx=0.085, r=0.044)
    smile(c, k, y=0.02, w=0.10, depth=0.055, seed=345)
    oval(c, 0.40, 0.42, 0.10, 0.08, k, seed=346, fill=paper)
    ink(c, [("m", 0.40, 0.34), ("l", 0.40, 0.26)], k, width=0.030, seed=347)


def ap_bangalore(c, k, a, paper):
    shoulders(c, k, w=0.34, seed=351)
    ink(c, [("m", -0.26, -0.08), ("l", -0.27, 0.16), ("c", -0.27, 0.40, 0.27, 0.40, 0.27, 0.16),
            ("l", 0.26, -0.08)], k, seed=352, close=True, fill=paper)
    ink(c, [("m", -0.20, 0.12), ("l", 0.20, 0.12)], k, width=0.085, seed=353)
    ink(c, [("m", -0.27, 0.22), ("l", 0.27, 0.22)], k, width=0.036, seed=354)


def ap_caustic(c, k, a, paper):
    ink(c, [("m", -0.44, -0.50), ("c", -0.40, -0.16, -0.20, -0.04, 0.0, -0.04),
            ("c", 0.20, -0.04, 0.40, -0.16, 0.44, -0.50)], k, seed=361)
    head(c, k, paper, cy=0.18, rx=0.25, ry=0.25, seed=362)
    for sx in (-1, 1):
        oval(c, sx * 0.110, 0.26, 0.070, 0.070, k, seed=363 + sx, fill=paper)
    oval(c, 0.0, 0.03, 0.115, 0.095, k, seed=365, fill=paper)
    ink(c, [("m", 0.0, -0.07), ("l", 0.0, -0.18)], k, width=0.036, seed=366)
    ink(c, [("m", 0.30, -0.36), ("l", 0.44, -0.12), ("l", 0.32, -0.06)], k, width=0.04, seed=367)


def ap_gibraltar(c, k, a, paper):
    ink(c, [("m", -0.48, -0.50), ("c", -0.44, -0.12, -0.24, 0.0, 0.0, 0.0),
            ("c", 0.24, 0.0, 0.44, -0.12, 0.48, -0.50)], k, seed=371)
    head(c, k, paper, cy=0.22, rx=0.25, ry=0.23, seed=372)
    eyes(c, k, y=0.28, dx=0.100, r=0.046)
    ink(c, [("m", -0.16, 0.14), ("c", -0.10, 0.04, 0.10, 0.04, 0.16, 0.14)], k, width=0.055, seed=373)
    ink(c, [("m", -0.28, 0.40), ("c", -0.12, 0.48, 0.12, 0.48, 0.28, 0.40)], k, seed=374)
    ink(c, [("m", -0.50, -0.34), ("l", -0.50, -0.06), ("l", -0.34, 0.02)], k, width=0.04, seed=375)


def ap_mirage(c, k, a, paper):
    shoulders(c, k, w=0.32, seed=381)
    head(c, k, paper, cy=0.14, rx=0.22, ry=0.23, seed=382)
    ink(c, [("m", -0.22, 0.26), ("c", -0.14, 0.44, 0.14, 0.44, 0.22, 0.26),
            ("c", 0.10, 0.34, -0.10, 0.34, -0.22, 0.26)], k, seed=383, close=True, fill=k)
    eyes(c, k, y=0.16, dx=0.085, r=0.044)
    smile(c, k, y=0.03, w=0.11, depth=0.065, seed=384)
    ink(c, [("m", -0.16, -0.08), ("l", 0.16, -0.08)], k, width=0.030, seed=385)
    # decoy hologram: a faint second silhouette stepping away to one side
    ink(c, [("m", 0.30, -0.42), ("c", 0.34, -0.22, 0.42, -0.14, 0.50, -0.14)],
        k, width=0.028, seed=386)
    oval(c, 0.44, 0.06, 0.12, 0.13, k, seed=387, width=0.028)


CHARACTERS = {
    "spades": {
        "2": ("The Knight", hk_knight), "3": ("Hornet", hk_hornet),
        "4": ("Grimm", hk_grimm), "5": ("Quirrel", hk_quirrel),
        "6": ("Elderbug", hk_elderbug), "7": ("Zote", hk_zote),
        "8": ("False Knight", hk_false_knight), "9": ("Mantis Lord", hk_mantis),
        "10": ("Hollow Knight", hk_vessel),
    },
    "clubs": {
        "2": ("Knight", cr_knight), "3": ("Archer", cr_archer),
        "4": ("Goblin", cr_goblin), "5": ("Giant", cr_giant),
        "6": ("Wizard", cr_wizard), "7": ("Hog Rider", cr_hog_rider),
        "8": ("P.E.K.K.A", cr_pekka), "9": ("Skeleton", cr_skeleton),
        "10": ("King", cr_king),
    },
    "hearts": {
        "2": ("Pudge", dt_pudge), "3": ("Juggernaut", dt_juggernaut),
        "4": ("Crystal Maiden", dt_crystal_maiden), "5": ("Axe", dt_axe),
        "6": ("Invoker", dt_invoker), "7": ("Sniper", dt_sniper),
        "8": ("Lina", dt_lina), "9": ("Anti-Mage", dt_antimage),
        "10": ("Phantom Assassin", dt_phantom),
    },
    "diamonds": {
        "2": ("Wraith", ap_wraith), "3": ("Bloodhound", ap_bloodhound),
        "4": ("Pathfinder", ap_pathfinder), "5": ("Octane", ap_octane),
        "6": ("Lifeline", ap_lifeline), "7": ("Bangalore", ap_bangalore),
        "8": ("Caustic", ap_caustic), "9": ("Gibraltar", ap_gibraltar),
        "10": ("Mirage", ap_mirage),
    },
}


def draw_character(c, suit, rank, size, ink_color, accent, paper):
    """Draw the easter-egg character centred on the current origin."""
    _, fn = CHARACTERS[suit][rank]
    with state(c):
        c.scale(size, size)
        fn(c, ink_color, accent, paper)


def character_name(suit, rank):
    return CHARACTERS[suit][rank][0]
