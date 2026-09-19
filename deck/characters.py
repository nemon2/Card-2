"""One hand-drawn character per card - the easter egg.

Each suit gets nine characters from its game, one per rank. They are authored
in a unit box (-0.5..0.5) and drawn through ``deck.sketch``, so every line
carries a small deterministic wobble and reads as pen work.

Anything held or worn behind the figure is drawn first; ``bust`` and ``cloak``
fill with the paper colour and mask it, so props read as being carried.
"""
from __future__ import annotations

import math

from .config import state
from .parts import (brow, bust, cloak, collar, dot_eyes, folds, hatch, haft,
                    horn, mask_face, mouth_line, pauldrons, teeth, void_eyes)
from .sketch import blob, ink, oval


# ===========================================================================
# Hollow Knight - spades
# ===========================================================================
def hk_knight(c, k, a, paper):
    haft(c, k, 0.26, -0.46, 0.54, 0.26, width=0.030, seed=1)
    cloak(c, k, paper, w=0.40, neck_y=-0.04, seed=3)
    folds(c, k, (-0.20, 0.0, 0.20), -0.14, -0.46, seed=4)
    for sx in (1, -1):
        horn(c, k, sx, base=(0.19, 0.24), tip=(0.60, 0.54), thick=0.22, seed=5 + sx, fill=k)
    mask_face(c, k, paper, cy=0.16, rx=0.235, ry=0.265, seed=7)
    void_eyes(c, k, y=0.16, dx=0.100)


def hk_hornet(c, k, a, paper):
    haft(c, k, -0.34, -0.46, 0.44, 0.44, width=0.024, seed=11)
    cloak(c, k, paper, w=0.36, neck_y=-0.02, seed=12, scallop=0.07)
    folds(c, k, (-0.16, 0.06), -0.12, -0.46, seed=13)
    mask_face(c, k, paper, cy=0.16, rx=0.225, ry=0.250, seed=14)
    for x, h in ((-0.16, 0.50), (0.0, 0.58), (0.16, 0.50)):
        ink(c, [("m", x - 0.075, 0.33), ("l", x, h), ("l", x + 0.075, 0.33)],
            k, seed=15 + int(h * 10), close=True, fill=paper)
    void_eyes(c, k, y=0.15, dx=0.098, rx=0.052, ry=0.072)
    ink(c, [("m", -0.225, 0.10), ("c", -0.10, 0.02, 0.10, 0.02, 0.225, 0.10)],
        k, width=0.024, seed=18)


def hk_grimm(c, k, a, paper):
    cloak(c, k, paper, w=0.44, neck_y=0.02, seed=21, scallop=0.08)
    folds(c, k, (-0.24, -0.06, 0.14), -0.08, -0.46, seed=22)
    for sx in (-1, 1):   # high pointed collar
        ink(c, [("m", sx * 0.10, -0.02), ("l", sx * 0.34, 0.30), ("l", sx * 0.36, 0.00)],
            k, width=0.030, seed=23 + sx, fill=paper)
    for sx in (1, -1):
        horn(c, k, sx, base=(0.16, 0.26), tip=(0.42, 0.66), thick=0.20, seed=25 + sx, fill=k)
    mask_face(c, k, paper, cy=0.14, rx=0.215, ry=0.265, seed=27)
    for sx in (-1, 1):   # sharp slanted eyes
        ink(c, [("m", sx * 0.045, 0.24), ("l", sx * 0.175, 0.14), ("l", sx * 0.060, 0.11)],
            k, width=0.026, seed=28 + sx, fill=k)
    teeth(c, k, y=0.02, w=0.115, h=0.055, n=5, seed=30)


def hk_quirrel(c, k, a, paper):
    oval(c, 0.30, -0.24, 0.20, 0.19, k, seed=31)
    ink(c, [("m", 0.30, -0.24), ("c", 0.38, -0.20, 0.36, -0.34, 0.27, -0.32),
            ("c", 0.19, -0.30, 0.22, -0.14, 0.34, -0.14)], k, width=0.022, seed=32)
    haft(c, k, -0.24, -0.46, -0.46, 0.22, width=0.028, seed=33)
    bust(c, k, paper, w=0.32, neck_y=-0.10, seed=34)
    collar(c, k, y=-0.10, w=0.15, seed=35)
    for sx in (1, -1):
        horn(c, k, sx, base=(0.16, 0.24), tip=(0.38, 0.46), thick=0.14, seed=37 + sx, fill=k)
    mask_face(c, k, paper, cx=-0.02, cy=0.16, rx=0.235, ry=0.245, seed=36)
    void_eyes(c, k, y=0.16, dx=0.095, rx=0.050, ry=0.070)


def hk_elderbug(c, k, a, paper):
    cloak(c, k, paper, w=0.32, neck_y=-0.04, seed=41, scallop=0.04)
    folds(c, k, (-0.12, 0.10), -0.12, -0.46, seed=42)
    mask_face(c, k, paper, cy=0.16, rx=0.235, ry=0.235, seed=43)
    ink(c, [("m", -0.16, 0.34), ("c", -0.08, 0.46, 0.08, 0.46, 0.16, 0.34)],
        k, width=0.026, seed=44)
    dot_eyes(c, k, y=0.20, dx=0.090, r=0.034)
    mouth_line(c, k, y=0.05, w=0.085, depth=0.045, seed=45)
    hatch(c, k, -0.20, 0.10, 0.045, -0.02, n=2, step=0.045, seed=46)


def hk_zote(c, k, a, paper):
    haft(c, k, 0.26, -0.46, 0.50, 0.30, width=0.044, seed=51)
    ink(c, [("m", 0.42, 0.06), ("l", 0.56, 0.10)], k, width=0.024, seed=52)
    bust(c, k, paper, w=0.36, neck_y=-0.14, seed=53)
    oval(c, 0.0, -0.30, 0.26, 0.16, k, seed=54, width=0.026)
    ink(c, [("m", -0.235, -0.06), ("l", -0.255, 0.28), ("l", 0.255, 0.28),
            ("l", 0.235, -0.06)], k, seed=55, close=True, fill=paper)
    brow(c, k, y=0.20, dx=0.105, w=0.10, drop=0.05, seed=56)
    dot_eyes(c, k, y=0.13, dx=0.100, r=0.032)
    mouth_line(c, k, y=0.01, w=0.095, seed=57)


def hk_false_knight(c, k, a, paper):
    haft(c, k, 0.30, -0.44, 0.44, 0.20, width=0.040, seed=61)
    oval(c, 0.50, 0.30, 0.14, 0.13, k, seed=62, fill=paper)
    for ang in (-0.10, 0.10):
        ink(c, [("m", 0.50 + ang, 0.42), ("l", 0.50 + ang * 1.4, 0.50)],
            k, width=0.024, seed=63)
    bust(c, k, paper, w=0.44, neck_y=-0.02, seed=64)
    pauldrons(c, k, paper, w=0.44, y=-0.22, seed=65)
    ink(c, [("m", -0.30, 0.00), ("l", -0.32, 0.28),
            ("c", -0.10, 0.44, 0.10, 0.44, 0.32, 0.28),
            ("l", 0.30, 0.00)], k, seed=66, close=True, fill=paper)
    ink(c, [("m", -0.21, 0.16), ("l", 0.21, 0.16)], k, width=0.070, seed=67)
    hatch(c, k, -0.24, 0.30, 0.03, 0.05, n=3, step=0.05, seed=68)


def hk_mantis(c, k, a, paper):
    for sx in (-1, 1):   # scythe arms
        ink(c, [("m", sx * 0.28, -0.14), ("c", sx * 0.46, 0.04, sx * 0.52, 0.24, sx * 0.44, 0.40)],
            k, width=0.030, seed=71 + sx)
        ink(c, [("m", sx * 0.44, 0.40), ("l", sx * 0.34, 0.30)], k, width=0.022, seed=73 + sx)
    bust(c, k, paper, w=0.34, neck_y=-0.12, seed=74)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.10, -0.12), ("l", sx * 0.33, -0.06), ("l", sx * 0.30, -0.24)],
            k, width=0.028, seed=75 + sx, fill=paper)
    ink(c, [("m", -0.22, 0.02), ("l", -0.26, 0.28), ("l", 0.0, 0.50), ("l", 0.26, 0.28),
            ("l", 0.22, 0.02)], k, seed=77, close=True, fill=paper)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.050, 0.24), ("l", sx * 0.180, 0.16), ("l", sx * 0.065, 0.12)],
            k, width=0.024, seed=78 + sx, fill=k)
    mouth_line(c, k, y=0.05, w=0.07, seed=80)


def hk_vessel(c, k, a, paper):
    haft(c, k, -0.26, -0.46, -0.52, 0.30, width=0.030, seed=81)
    cloak(c, k, paper, w=0.34, neck_y=-0.02, seed=82, scallop=0.05)
    folds(c, k, (-0.14, 0.06), -0.10, -0.46, seed=83)
    for sx in (1, -1):
        horn(c, k, sx, base=(0.17, 0.24), tip=(0.66, 0.62), thick=0.19, seed=84 + sx, fill=k)
    mask_face(c, k, paper, cy=0.14, rx=0.200, ry=0.280, seed=86)
    void_eyes(c, k, y=0.15, dx=0.090, rx=0.050, ry=0.082)


# ===========================================================================
# Clash Royale - clubs
# ===========================================================================
def cr_knight(c, k, a, paper):
    bust(c, k, paper, w=0.38, neck_y=-0.10, seed=101)
    pauldrons(c, k, paper, w=0.38, y=-0.26, seed=102)
    ink(c, [("m", 0.0, -0.10), ("l", 0.0, -0.48)], k, width=0.026, seed=103)
    ink(c, [("m", -0.26, -0.06), ("l", -0.27, 0.16),
            ("c", -0.27, 0.40, 0.27, 0.40, 0.27, 0.16),
            ("l", 0.26, -0.06)], k, seed=104, close=True, fill=paper)
    ink(c, [("m", -0.19, 0.12), ("l", 0.19, 0.12)], k, width=0.070, seed=105)
    ink(c, [("m", -0.26, 0.24), ("l", 0.26, 0.24)], k, width=0.026, seed=106)
    ink(c, [("m", 0.0, 0.33), ("c", 0.12, 0.50, 0.24, 0.58, 0.33, 0.59),
            ("c", 0.24, 0.46, 0.13, 0.37, 0.05, 0.30)], k, seed=107, close=True, fill=paper)


def cr_archer(c, k, a, paper):
    ink(c, [("m", 0.34, -0.44), ("c", 0.56, -0.18, 0.56, 0.24, 0.34, 0.50)],
        k, width=0.030, seed=111)
    ink(c, [("m", 0.34, -0.44), ("l", 0.34, 0.50)], k, width=0.020, seed=112)
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=113)
    collar(c, k, y=-0.12, w=0.14, seed=114)
    mask_face(c, k, paper, cy=0.12, rx=0.205, ry=0.215, seed=115)
    ink(c, [("m", -0.27, -0.04), ("c", -0.32, 0.44, 0.32, 0.44, 0.27, -0.04)],
        k, seed=116)
    ink(c, [("m", -0.27, -0.04), ("c", -0.17, 0.06, 0.17, 0.06, 0.27, -0.04)],
        k, width=0.028, seed=117)
    dot_eyes(c, k, y=0.14, dx=0.078, r=0.030)
    mouth_line(c, k, y=0.02, w=0.06, depth=0.035, seed=118)


def cr_goblin(c, k, a, paper):
    haft(c, k, 0.28, -0.40, 0.46, 0.14, width=0.028, seed=121)
    ink(c, [("m", 0.42, 0.06), ("l", 0.50, 0.26), ("l", 0.54, 0.04)],
        k, width=0.022, seed=122, fill=paper)
    bust(c, k, paper, w=0.31, neck_y=-0.14, seed=123)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.19, 0.24), ("l", sx * 0.48, 0.36), ("l", sx * 0.20, 0.06)],
            k, width=0.028, seed=124 + sx, fill=paper)
    mask_face(c, k, paper, cy=0.14, rx=0.215, ry=0.225, seed=126)
    brow(c, k, y=0.24, dx=0.090, w=0.085, drop=0.035, seed=127)
    dot_eyes(c, k, y=0.16, dx=0.085, r=0.032)
    teeth(c, k, y=0.02, w=0.085, h=0.045, n=3, seed=128)


def cr_giant(c, k, a, paper):
    bust(c, k, paper, w=0.46, neck_y=-0.04, seed=131)
    ink(c, [("m", -0.14, -0.06), ("l", -0.10, -0.46)], k, width=0.026, seed=132)
    ink(c, [("m", 0.14, -0.06), ("l", 0.10, -0.46)], k, width=0.026, seed=133)
    mask_face(c, k, paper, cy=0.20, rx=0.255, ry=0.245, seed=134)
    dot_eyes(c, k, y=0.27, dx=0.100, r=0.034)
    brow(c, k, y=0.35, dx=0.100, w=0.095, drop=0.030, seed=135)
    ink(c, [("m", -0.23, 0.14), ("c", -0.27, -0.10, -0.16, -0.26, 0.0, -0.26),
            ("c", 0.16, -0.26, 0.27, -0.10, 0.23, 0.14)], k, seed=136)
    ink(c, [("m", -0.145, 0.11), ("c", -0.07, 0.03, 0.07, 0.03, 0.145, 0.11)],
        k, width=0.042, seed=137)


def cr_wizard(c, k, a, paper):
    oval(c, 0.42, -0.14, 0.13, 0.13, k, seed=141, fill=paper)
    for d in (-0.13, 0.0, 0.13):
        ink(c, [("m", 0.42 + d * 0.7, 0.00), ("l", 0.42 + d * 1.5, 0.16)],
            k, width=0.022, seed=142)
    bust(c, k, paper, w=0.33, neck_y=-0.12, seed=143)
    collar(c, k, y=-0.12, w=0.15, seed=144)
    mask_face(c, k, paper, cy=0.08, rx=0.205, ry=0.215, seed=145)
    ink(c, [("m", -0.31, 0.22), ("l", 0.31, 0.22), ("l", 0.05, 0.62)],
        k, seed=146, close=True, fill=paper)
    ink(c, [("m", -0.31, 0.22), ("l", 0.31, 0.22)], k, width=0.026, seed=147)
    dot_eyes(c, k, y=0.10, dx=0.080, r=0.030)
    ink(c, [("m", -0.155, -0.02), ("c", -0.08, -0.20, 0.08, -0.20, 0.155, -0.02)],
        k, width=0.026, seed=148)


def cr_hog_rider(c, k, a, paper):
    haft(c, k, 0.24, -0.42, 0.42, 0.16, width=0.030, seed=151)
    ink(c, [("m", 0.34, 0.14), ("l", 0.58, 0.22), ("l", 0.54, 0.40), ("l", 0.30, 0.32)],
        k, width=0.028, seed=152, close=True, fill=paper)
    bust(c, k, paper, w=0.36, neck_y=-0.10, seed=153)
    mask_face(c, k, paper, cy=0.14, rx=0.215, ry=0.230, seed=154)
    ink(c, [("m", -0.06, 0.34), ("c", -0.02, 0.52, 0.08, 0.60, 0.16, 0.62),
            ("c", 0.12, 0.46, 0.06, 0.37, 0.03, 0.32)], k, seed=155, close=True, fill=k)
    dot_eyes(c, k, y=0.17, dx=0.085, r=0.032)
    ink(c, [("m", -0.175, 0.02), ("c", -0.09, -0.10, 0.09, -0.10, 0.175, 0.02)],
        k, width=0.030, seed=156)
    hatch(c, k, -0.20, -0.06, 0.035, -0.04, n=2, step=0.045, seed=157)


def cr_pekka(c, k, a, paper):
    haft(c, k, -0.26, -0.44, -0.46, 0.34, width=0.036, seed=161)
    bust(c, k, paper, w=0.44, neck_y=-0.04, seed=162)
    pauldrons(c, k, paper, w=0.44, y=-0.22, seed=163)
    ink(c, [("m", -0.25, -0.02), ("l", -0.27, 0.22), ("l", 0.0, 0.50), ("l", 0.27, 0.22),
            ("l", 0.25, -0.02)], k, seed=164, close=True, fill=paper)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.16), ("l", sx * 0.195, 0.24), ("l", sx * 0.070, 0.10)],
            k, width=0.024, seed=165 + sx, fill=k)
        ink(c, [("m", sx * 0.27, 0.24), ("l", sx * 0.42, 0.54)], k, width=0.032, seed=167 + sx)
    ink(c, [("m", -0.13, -0.01), ("l", 0.13, -0.01)], k, width=0.026, seed=169)


def cr_skeleton(c, k, a, paper):
    ink(c, [("m", -0.22, -0.50), ("l", -0.15, -0.12), ("l", 0.15, -0.12), ("l", 0.22, -0.50)],
        k, seed=171, fill=paper)
    for y in (-0.42, -0.32, -0.22):
        ink(c, [("m", -0.175, y), ("l", 0.175, y)], k, width=0.026, seed=172, amp=0.005)
    ink(c, [("m", 0.0, -0.46), ("l", 0.0, -0.14)], k, width=0.022, seed=173)
    mask_face(c, k, paper, cy=0.16, rx=0.235, ry=0.245, seed=174)
    oval(c, -0.095, 0.21, 0.062, 0.070, k, seed=175, fill=k, width=0.016)
    oval(c, 0.095, 0.21, 0.062, 0.070, k, seed=176, fill=k, width=0.016)
    ink(c, [("m", -0.022, 0.09), ("l", 0.022, 0.09)], k, width=0.038, seed=177)
    teeth(c, k, y=0.00, w=0.115, h=0.055, n=5, seed=178)


def cr_king(c, k, a, paper):
    bust(c, k, paper, w=0.44, neck_y=-0.02, seed=181)
    pauldrons(c, k, paper, w=0.44, y=-0.24, seed=182)
    mask_face(c, k, paper, cy=0.18, rx=0.235, ry=0.230, seed=183)
    dot_eyes(c, k, y=0.24, dx=0.095, r=0.032)
    ink(c, [("m", -0.215, 0.12), ("c", -0.255, -0.12, -0.15, -0.28, 0.0, -0.28),
            ("c", 0.15, -0.28, 0.255, -0.12, 0.215, 0.12)], k, seed=184)
    ink(c, [("m", -0.135, 0.09), ("c", -0.06, 0.01, 0.06, 0.01, 0.135, 0.09)],
        k, width=0.040, seed=185)
    ink(c, [("m", -0.29, 0.34), ("l", -0.29, 0.58), ("l", -0.145, 0.44), ("l", 0.0, 0.62),
            ("l", 0.145, 0.44), ("l", 0.29, 0.58), ("l", 0.29, 0.34)],
        k, seed=186, close=True, fill=paper)
    for x in (-0.29, 0.0, 0.29):
        blob(c, x, 0.615, 0.030, k)


# ===========================================================================
# Dota 2 - hearts
# ===========================================================================
def dt_pudge(c, k, a, paper):
    ink(c, [("m", 0.34, -0.42), ("c", 0.54, -0.18, 0.56, 0.06, 0.46, 0.18),
            ("c", 0.36, 0.28, 0.26, 0.18, 0.32, 0.08)], k, width=0.030, seed=201)
    bust(c, k, paper, w=0.48, neck_y=-0.02, seed=202)
    for y in (-0.16, -0.30):
        ink(c, [("m", -0.26, y), ("c", -0.08, y - 0.05, 0.08, y - 0.05, 0.26, y)],
            k, width=0.024, seed=203)
    mask_face(c, k, paper, cy=0.22, rx=0.255, ry=0.235, seed=204)
    dot_eyes(c, k, y=0.29, dx=0.095, r=0.030)
    ink(c, [("m", -0.155, 0.10), ("l", 0.155, 0.10)], k, width=0.028, seed=205)
    for x in (-0.10, -0.03, 0.04, 0.11):
        ink(c, [("m", x, 0.145), ("l", x + 0.025, 0.055)], k, width=0.020, seed=206, amp=0.004)
    hatch(c, k, -0.22, 0.30, 0.03, 0.045, n=2, step=0.05, seed=207)


def dt_juggernaut(c, k, a, paper):
    haft(c, k, -0.28, -0.44, -0.50, 0.32, width=0.030, seed=211)
    bust(c, k, paper, w=0.34, neck_y=-0.12, seed=212)
    collar(c, k, y=-0.12, w=0.15, seed=213)
    mask_face(c, k, paper, cy=0.16, rx=0.225, ry=0.260, seed=214)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.050, 0.24), ("l", sx * 0.175, 0.24)], k, width=0.055, seed=215 + sx)
    teeth(c, k, y=0.06, w=0.125, h=0.065, n=5, seed=217)
    ink(c, [("m", 0.0, 0.42), ("c", 0.08, 0.56, 0.18, 0.60, 0.26, 0.60)],
        k, width=0.038, seed=218)
    ink(c, [("m", -0.225, 0.14), ("l", 0.225, 0.14)], k, width=0.022, seed=219)


def dt_crystal_maiden(c, k, a, paper):
    for i in range(3):
        a = math.radians(i * 60)
        dx, dy = 0.115 * math.cos(a), 0.115 * math.sin(a)
        ink(c, [("m", 0.42 - dx, -0.16 - dy), ("l", 0.42 + dx, -0.16 + dy)],
            k, width=0.022, seed=221 + i)
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=222)
    mask_face(c, k, paper, cy=0.12, rx=0.200, ry=0.215, seed=223)
    ink(c, [("m", -0.31, -0.10), ("c", -0.38, 0.52, 0.38, 0.52, 0.31, -0.10)], k, seed=224)
    ink(c, [("m", -0.29, -0.06), ("c", -0.18, 0.06, 0.18, 0.06, 0.29, -0.06)],
        k, width=0.030, seed=225)
    for sx in (-1, 1):   # tiara points
        ink(c, [("m", sx * 0.07, 0.35), ("l", sx * 0.13, 0.46)], k, width=0.022, seed=226 + sx)
    dot_eyes(c, k, y=0.15, dx=0.075, r=0.028)
    mouth_line(c, k, y=0.02, w=0.055, depth=0.03, seed=228)


def dt_axe(c, k, a, paper):
    haft(c, k, 0.24, -0.44, 0.40, 0.12, width=0.032, seed=231)
    ink(c, [("m", 0.36, 0.10), ("c", 0.54, 0.16, 0.55, 0.36, 0.42, 0.44),
            ("l", 0.35, 0.24)], k, width=0.026, seed=232, close=True, fill=paper)
    bust(c, k, paper, w=0.42, neck_y=-0.04, seed=233)
    pauldrons(c, k, paper, w=0.42, y=-0.24, seed=234)
    mask_face(c, k, paper, cy=0.18, rx=0.225, ry=0.235, seed=235)
    for sx in (1, -1):
        horn(c, k, sx, base=(0.15, 0.32), tip=(0.32, 0.50), thick=0.11, seed=236 + sx, fill=paper)
    brow(c, k, y=0.26, dx=0.095, w=0.09, drop=0.045, seed=238)
    dot_eyes(c, k, y=0.17, dx=0.090, r=0.030)
    teeth(c, k, y=0.03, w=0.105, h=0.050, n=4, seed=239)


def dt_invoker(c, k, a, paper):
    for cx, cy in ((-0.42, 0.34), (-0.46, 0.08), (0.44, 0.26)):
        oval(c, cx, cy, 0.085, 0.085, k, seed=241, fill=paper)
        blob(c, cx, cy, 0.024, k)
    bust(c, k, paper, w=0.31, neck_y=-0.10, seed=242)
    mask_face(c, k, paper, cy=0.22, rx=0.205, ry=0.205, seed=243)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.26), ("l", sx * 0.170, 0.26)], k, width=0.045, seed=244 + sx)
    ink(c, [("m", -0.17, 0.14), ("c", -0.14, -0.22, 0.14, -0.22, 0.17, 0.14)],
        k, seed=246)
    ink(c, [("m", -0.115, 0.12), ("c", -0.05, 0.05, 0.05, 0.05, 0.115, 0.12)],
        k, width=0.026, seed=247)
    for x in (-0.07, 0.0, 0.07):
        ink(c, [("m", x, -0.02), ("l", x + 0.012, -0.19)], k, width=0.020, seed=248, amp=0.004)
    ink(c, [("m", -0.21, 0.36), ("c", -0.10, 0.46, 0.10, 0.46, 0.21, 0.36)],
        k, width=0.026, seed=248)


def dt_sniper(c, k, a, paper):
    ink(c, [("m", -0.46, -0.06), ("l", 0.40, -0.34)], k, width=0.040, seed=251)
    ink(c, [("m", -0.30, -0.11), ("l", -0.24, 0.02)], k, width=0.024, seed=252)
    bust(c, k, paper, w=0.31, neck_y=-0.14, seed=253)
    mask_face(c, k, paper, cy=0.12, rx=0.205, ry=0.200, seed=254)
    ink(c, [("m", -0.36, 0.26), ("l", 0.36, 0.26)], k, width=0.030, seed=255)
    ink(c, [("m", -0.21, 0.26), ("c", -0.23, 0.52, 0.23, 0.52, 0.21, 0.26)],
        k, seed=256, close=True, fill=paper)
    for sx in (-1, 1):
        oval(c, sx * 0.105, 0.13, 0.078, 0.078, k, seed=257 + sx, fill=paper)
        blob(c, sx * 0.105, 0.13, 0.026, k)
    ink(c, [("m", -0.027, 0.13), ("l", 0.027, 0.13)], k, width=0.026, seed=259)
    ink(c, [("m", -0.10, -0.02), ("c", -0.04, -0.09, 0.04, -0.09, 0.10, -0.02)],
        k, width=0.024, seed=260)


def dt_lina(c, k, a, paper):
    bust(c, k, paper, w=0.31, neck_y=-0.12, seed=261)
    collar(c, k, y=-0.12, w=0.14, seed=262)
    mask_face(c, k, paper, cy=0.10, rx=0.195, ry=0.215, seed=263)
    for x0, tipx, h in ((-0.17, -0.34, 0.46), (-0.07, -0.13, 0.58),
                        (0.07, 0.15, 0.60), (0.17, 0.34, 0.44)):
        ink(c, [("m", x0 - 0.075, 0.26),
                ("c", x0 - 0.05, 0.40, tipx - 0.03, h - 0.12, tipx, h),
                ("c", tipx + 0.02, h - 0.18, x0 + 0.095, 0.40, x0 + 0.075, 0.26)],
            k, seed=264 + int(h * 100), close=True, fill=paper)
    dot_eyes(c, k, y=0.13, dx=0.075, r=0.028)
    mouth_line(c, k, y=0.00, w=0.055, depth=0.03, seed=268)
    hatch(c, k, 0.10, -0.02, 0.03, -0.05, n=2, step=0.04, seed=269)


def dt_antimage(c, k, a, paper):
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.27, -0.42), ("c", sx * 0.46, -0.18, sx * 0.44, 0.16, sx * 0.31, 0.36)],
            k, width=0.026, seed=271 + sx)
        ink(c, [("m", sx * 0.31, 0.36), ("l", sx * 0.23, 0.26)], k, width=0.018, seed=273 + sx)
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=274)
    mask_face(c, k, paper, cy=0.16, rx=0.215, ry=0.250, seed=275)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.050, 0.22), ("l", sx * 0.175, 0.22)], k, width=0.050, seed=276 + sx)
    ink(c, [("m", 0.0, 0.41), ("l", 0.0, 0.58)], k, width=0.030, seed=278)
    blob(c, 0.0, 0.60, 0.032, k)
    ink(c, [("m", -0.12, 0.02), ("l", 0.12, 0.02)], k, width=0.024, seed=279)


def dt_phantom(c, k, a, paper):
    haft(c, k, 0.26, -0.42, 0.46, 0.06, width=0.028, seed=281)
    ink(c, [("m", 0.42, 0.00), ("l", 0.54, 0.24), ("l", 0.50, -0.02)],
        k, width=0.020, seed=282, fill=paper)
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=283)
    mask_face(c, k, paper, cy=0.12, rx=0.200, ry=0.220, seed=284)
    ink(c, [("m", -0.29, -0.04), ("c", -0.35, 0.48, 0.35, 0.48, 0.29, -0.04)], k, seed=285)
    ink(c, [("m", -0.135, 0.16), ("l", 0.135, 0.16)], k, width=0.055, seed=286)
    ink(c, [("m", -0.20, 0.02), ("c", -0.10, -0.04, 0.10, -0.04, 0.20, 0.02)],
        k, width=0.024, seed=287)


# ===========================================================================
# Apex Legends - diamonds
# ===========================================================================
def ap_wraith(c, k, a, paper):
    ink(c, [("m", 0.50, -0.30), ("c", 0.28, -0.24, 0.28, 0.02, 0.46, 0.00),
            ("c", 0.58, -0.02, 0.54, -0.20, 0.40, -0.18)], k, width=0.026, seed=301)
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=302)
    mask_face(c, k, paper, cy=0.12, rx=0.195, ry=0.205, seed=303)
    ink(c, [("m", -0.29, -0.06), ("c", -0.35, 0.48, 0.35, 0.48, 0.29, -0.06)], k, seed=304)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.045, 0.15), ("l", sx * 0.155, 0.15)], k, width=0.045, seed=305 + sx)
    ink(c, [("m", -0.12, 0.30), ("l", 0.12, 0.30)], k, width=0.022, seed=307)


def ap_bloodhound(c, k, a, paper):
    bust(c, k, paper, w=0.34, neck_y=-0.10, seed=311)
    pauldrons(c, k, paper, w=0.34, y=-0.26, seed=312)
    mask_face(c, k, paper, cy=0.18, rx=0.225, ry=0.245, seed=313)
    for sx in (-1, 1):
        oval(c, sx * 0.105, 0.25, 0.078, 0.078, k, seed=314 + sx, fill=paper)
        blob(c, sx * 0.105, 0.25, 0.030, k)
    ink(c, [("m", -0.095, 0.10), ("l", 0.0, -0.14), ("l", 0.095, 0.10)],
        k, seed=316, close=True, fill=paper)
    ink(c, [("m", -0.05, -0.02), ("l", 0.05, -0.02)], k, width=0.020, seed=317)
    ink(c, [("m", -0.23, 0.40), ("c", -0.10, 0.52, 0.10, 0.52, 0.23, 0.40)], k, seed=318)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.16, 0.44), ("l", sx * 0.26, 0.58)], k, width=0.022, seed=319 + sx)


def ap_pathfinder(c, k, a, paper):
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=321)
    for y in (-0.22, -0.32):
        ink(c, [("m", -0.20, y), ("c", -0.07, y - 0.04, 0.07, y - 0.04, 0.20, y)],
            k, width=0.022, seed=322)
    ink(c, [("m", -0.07, -0.12), ("l", -0.07, -0.20)], k, width=0.022, seed=323)
    ink(c, [("m", 0.07, -0.12), ("l", 0.07, -0.20)], k, width=0.022, seed=324)
    mask_face(c, k, paper, cy=0.16, rx=0.255, ry=0.255, seed=325)
    oval(c, 0.0, 0.16, 0.185, 0.185, k, seed=326, width=0.022)
    for sx in (-1, 1):
        ink(c, [("m", sx * 0.055, 0.24), ("l", sx * 0.135, 0.24)], k, width=0.048, seed=327 + sx)
    ink(c, [("m", -0.105, 0.06), ("c", -0.04, -0.03, 0.04, -0.03, 0.105, 0.06)],
        k, width=0.032, seed=329)
    ink(c, [("m", 0.19, 0.36), ("c", 0.27, 0.46, 0.30, 0.54, 0.30, 0.60)],
        k, width=0.026, seed=330)
    blob(c, 0.30, 0.62, 0.038, k)


def ap_octane(c, k, a, paper):
    bust(c, k, paper, w=0.33, neck_y=-0.12, seed=331)
    mask_face(c, k, paper, cy=0.16, rx=0.220, ry=0.235, seed=332)
    for sx in (-1, 1):
        oval(c, sx * 0.108, 0.25, 0.072, 0.060, k, seed=333 + sx, fill=paper)
        blob(c, sx * 0.108, 0.25, 0.024, k)
    ink(c, [("m", -0.225, 0.32), ("l", 0.225, 0.32)], k, width=0.022, seed=335)
    ink(c, [("m", -0.165, 0.08), ("l", 0.165, 0.08), ("l", 0.125, -0.10), ("l", -0.125, -0.10)],
        k, seed=336, close=True, fill=paper)
    for x in (-0.06, 0.0, 0.06):
        ink(c, [("m", x, 0.06), ("l", x, -0.08)], k, width=0.018, seed=337, amp=0.004)
    for sx, h in ((-1, 0.52), (1, 0.55)):
        ink(c, [("m", sx * 0.07, 0.38), ("l", sx * 0.22, h)], k, width=0.030, seed=338 + sx)


def ap_lifeline(c, k, a, paper):
    oval(c, 0.42, 0.42, 0.115, 0.090, k, seed=341, fill=paper)
    ink(c, [("m", 0.42, 0.33), ("l", 0.42, 0.22)], k, width=0.020, seed=342)
    blob(c, 0.42, 0.42, 0.026, k)
    bust(c, k, paper, w=0.32, neck_y=-0.12, seed=343)
    mask_face(c, k, paper, cy=0.14, rx=0.205, ry=0.220, seed=344)
    for sx in (-1, 1):
        for i, dy in enumerate((0.02, -0.08, -0.18)):
            ink(c, [("m", sx * 0.19, 0.24 + dy),
                    ("c", sx * 0.33, 0.18 + dy, sx * 0.35, 0.02 + dy, sx * 0.29, -0.10 + dy)],
                k, width=0.026, seed=345 + sx + i)
    dot_eyes(c, k, y=0.18, dx=0.080, r=0.028)
    mouth_line(c, k, y=0.04, w=0.075, depth=0.04, seed=347)
    ink(c, [("m", -0.16, 0.34), ("c", -0.07, 0.42, 0.07, 0.42, 0.16, 0.34)],
        k, width=0.024, seed=348)


def ap_bangalore(c, k, a, paper):
    bust(c, k, paper, w=0.36, neck_y=-0.08, seed=351)
    pauldrons(c, k, paper, w=0.36, y=-0.26, seed=352)
    ink(c, [("m", -0.26, -0.04), ("l", -0.27, 0.18),
            ("c", -0.27, 0.42, 0.27, 0.42, 0.27, 0.18),
            ("l", 0.26, -0.04)], k, seed=353, close=True, fill=paper)
    ink(c, [("m", -0.20, 0.14), ("l", 0.20, 0.14)], k, width=0.070, seed=354)
    ink(c, [("m", -0.27, 0.26), ("l", 0.27, 0.26)], k, width=0.024, seed=355)
    ink(c, [("m", -0.13, 0.00), ("l", 0.13, 0.00)], k, width=0.022, seed=356)
    hatch(c, k, 0.30, -0.16, 0.04, 0.05, n=2, step=0.05, seed=357)


def ap_caustic(c, k, a, paper):
    ink(c, [("m", 0.30, -0.40), ("l", 0.46, -0.10), ("l", 0.32, -0.02)],
        k, width=0.028, seed=361)
    bust(c, k, paper, w=0.44, neck_y=-0.04, seed=362)
    pauldrons(c, k, paper, w=0.44, y=-0.24, seed=363)
    mask_face(c, k, paper, cy=0.20, rx=0.245, ry=0.250, seed=364)
    for sx in (-1, 1):
        oval(c, sx * 0.112, 0.28, 0.074, 0.074, k, seed=365 + sx, fill=paper)
        blob(c, sx * 0.112, 0.28, 0.026, k)
    oval(c, 0.0, 0.04, 0.120, 0.098, k, seed=367, fill=paper)
    for x in (-0.05, 0.05):
        ink(c, [("m", x, 0.10), ("l", x, -0.02)], k, width=0.020, seed=368, amp=0.004)
    ink(c, [("m", 0.0, -0.06), ("l", 0.0, -0.18)], k, width=0.026, seed=369)
    ink(c, [("m", -0.24, 0.40), ("c", -0.10, 0.50, 0.10, 0.50, 0.24, 0.40)], k, width=0.024, seed=370)


def ap_gibraltar(c, k, a, paper):
    ink(c, [("m", -0.52, -0.34), ("c", -0.56, -0.10, -0.50, 0.12, -0.36, 0.22),
            ("l", -0.32, -0.32)], k, width=0.028, seed=371, close=True, fill=paper)
    bust(c, k, paper, w=0.48, neck_y=-0.02, seed=372)
    mask_face(c, k, paper, cy=0.24, rx=0.245, ry=0.225, seed=373)
    dot_eyes(c, k, y=0.30, dx=0.095, r=0.032)
    brow(c, k, y=0.38, dx=0.095, w=0.09, drop=0.028, seed=374)
    ink(c, [("m", -0.165, 0.16), ("c", -0.10, 0.04, 0.10, 0.04, 0.165, 0.16)],
        k, width=0.050, seed=375)
    ink(c, [("m", -0.12, 0.05), ("c", -0.05, -0.02, 0.05, -0.02, 0.12, 0.05)],
        k, width=0.024, seed=376)
    ink(c, [("m", -0.28, 0.42), ("c", -0.12, 0.52, 0.12, 0.52, 0.28, 0.42)], k, seed=377)


def ap_mirage(c, k, a, paper):
    ink(c, [("m", 0.34, -0.42), ("c", 0.38, -0.16, 0.46, -0.06, 0.54, -0.06)],
        k, width=0.022, seed=381)
    oval(c, 0.46, 0.14, 0.125, 0.140, k, seed=382, width=0.022)
    bust(c, k, paper, w=0.34, neck_y=-0.12, seed=383)
    collar(c, k, y=-0.12, w=0.15, seed=384)
    mask_face(c, k, paper, cy=0.16, rx=0.210, ry=0.225, seed=385)
    ink(c, [("m", -0.225, 0.28), ("c", -0.14, 0.48, 0.14, 0.48, 0.225, 0.28),
            ("c", 0.10, 0.36, -0.10, 0.36, -0.225, 0.28)], k, seed=386, close=True, fill=k)
    dot_eyes(c, k, y=0.19, dx=0.080, r=0.028)
    mouth_line(c, k, y=0.05, w=0.085, depth=0.05, seed=387)
    ink(c, [("m", -0.10, -0.02), ("c", -0.05, -0.09, 0.05, -0.09, 0.10, -0.02)],
        k, width=0.022, seed=388)


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
