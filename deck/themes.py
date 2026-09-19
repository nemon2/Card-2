"""Per-suit visual themes: palette, background art, frame and pip mark."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from reportlab.lib.colors import Color
from reportlab.lib.units import mm

from . import icons
from .config import FRAME_INSET, fade, hx, path, state


# --- shared pattern helpers ------------------------------------------------
def _card_clip(c, w, h):
    c.clipPath(path(c, ("m", 0, 0), ("l", w, 0), ("l", w, h), ("l", 0, h), ("z",)),
               stroke=0, fill=0)


def _specks(c, w, h, color, seed, n=54, alpha=0.5):
    """Deterministic scatter of tiny dots (dust, sparks, embers)."""
    rnd = _Rnd(seed)
    with state(c):
        c.setFillColor(color)
        for _ in range(n):
            x, y = rnd.f() * w, rnd.f() * h
            r = (0.16 + rnd.f() * 0.42) * mm
            c.setFillAlpha(alpha * (0.25 + rnd.f() * 0.75))
            c.circle(x, y, r, fill=1, stroke=0)


def _diagonals(c, w, h, color, alpha, step, width, ang=58.0):
    """Repeating diagonal bars across the card."""
    with state(c):
        c.setStrokeColor(color)
        c.setStrokeAlpha(alpha)
        c.setLineWidth(width)
        c.translate(w / 2, h / 2)
        c.rotate(ang)
        span = (w + h)
        n = int(span / step) + 2
        for i in range(-n, n + 1):
            x = i * step
            c.line(x, -span / 2, x, span / 2)


class _Rnd:
    """Tiny deterministic LCG so every build produces an identical PDF."""

    def __init__(self, seed):
        self.s = seed & 0x7FFFFFFF or 1

    def f(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


@dataclass
class Theme:
    key: str
    suit: str
    game: str
    rank_font: str
    label_font: str
    index: Color
    suit_color: Color
    frame: Color
    paint_background: Callable
    draw_pip: Callable
    corner: Callable = None
    label_size: float = 5.6
    label_tracking: float = 0.9
    rank_scale: float = 1.0
    index_x: float = 6.9 * mm
    pip_scale: float = 1.0


# ===========================================================================
# Hollow Knight  -  spades
# ===========================================================================
HK_DEEP = hx("#05080e")
HK_MID = hx("#24374f")
HK_PALE = hx("#e6edf6")
HK_BLUE = hx("#7f9fc4")


def _hk_background(c, w, h):
    with state(c):
        _card_clip(c, w, h)
        # One opaque radial does base + vignette: reportlab shadings ignore
        # per-stop alpha, so a translucent overlay would flatten the texture.
        c.radialGradient(w * 0.5, h * 0.62, h * 0.86, [HK_MID, HK_DEEP], [0.0, 1.0])

        # Hallownest arches
        with state(c):
            c.setStrokeColor(HK_BLUE)
            c.setLineWidth(0.5)
            for i, r in enumerate((15, 21, 27, 33)):
                c.setStrokeAlpha(0.26 - i * 0.045)
                c.arc(w / 2 - r * mm, h * 0.60 - r * mm,
                      w / 2 + r * mm, h * 0.60 + r * mm, 200, 140)

        with state(c):
            c.translate(w / 2, h * 0.50)
            icons.hollow_knight_mask(c, 27 * mm, fade(HK_PALE, 0.048),
                                     fade(HK_DEEP, 0.09))

        _specks(c, w, h, HK_PALE, seed=17, n=58, alpha=0.40)

def _hk_corner(c, w, h):
    """Small horn flourish at the top-left and bottom-right of the frame."""
    i = FRAME_INSET
    with state(c):
        c.setStrokeColor(HK_BLUE)
        c.setStrokeAlpha(0.75)
        c.setLineWidth(0.8)
        c.setLineCap(1)
        for (ox, oy, sx, sy) in ((i, h - i, 1, -1), (w - i, i, -1, 1)):
            with state(c):
                c.translate(ox, oy)
                c.scale(sx, sy)
                p = path(c, ("m", 0, -8 * mm), ("c", 0, -3 * mm, 3 * mm, 0, 8 * mm, 0))
                c.drawPath(p, fill=0, stroke=1)


# ===========================================================================
# Clash Royale  -  clubs
# ===========================================================================
CR_DEEP = hx("#0b2650")
CR_MID = hx("#2464ab")
CR_GOLD = hx("#f2bd3f")
CR_GOLD_D = hx("#7d4f0c")
CR_GOLD_L = hx("#fff0bc")
CR_ELIX = hx("#c94fd6")


def _cr_background(c, w, h):
    with state(c):
        _card_clip(c, w, h)
        c.radialGradient(w * 0.5, h * 0.60, h * 0.92, [CR_MID, CR_DEEP], [0.0, 1.0])
        _diagonals(c, w, h, CR_GOLD_L, 0.060, 8.5 * mm, 2.6 * mm, ang=58)

        rnd = _Rnd(91)
        for _ in range(13):
            x, y, sz = rnd.f() * w, rnd.f() * h, (1.7 + rnd.f() * 1.5) * mm
            with state(c):
                c.translate(x, y)
                c.rotate(rnd.f() * 360)
                c.setFillColor(fade(CR_ELIX, 0.16))
                drop = path(c, ("m", 0, sz * 1.5),
                            ("c", sz * 1.15, sz * 0.2, sz, -sz, 0, -sz),
                            ("c", -sz, -sz, -sz * 1.15, sz * 0.2, 0, sz * 1.5), ("z",))
                c.drawPath(drop, fill=1, stroke=0)

        with state(c):
            c.translate(w / 2, h * 0.50)
            icons.clash_royale_crown(c, 30 * mm, fade(CR_GOLD_L, 0.035),
                                     fade(CR_DEEP, 0.07), fade(CR_GOLD_L, 0.02),
                                     fade(CR_GOLD_L, 0.035))

def _cr_corner(c, w, h):
    """Gold rivets at the frame corners."""
    i = FRAME_INSET + 2.2 * mm
    with state(c):
        c.setFillColor(CR_GOLD)
        c.setStrokeColor(CR_GOLD_D)
        c.setLineWidth(0.4)
        for x in (i, w - i):
            for y in (i, h - i):
                c.circle(x, y, 0.85 * mm, fill=1, stroke=1)


# ===========================================================================
# Dota 2  -  hearts
# ===========================================================================
DT_DEEP = hx("#0e0506")
DT_MID = hx("#430f12")
DT_RED = hx("#c2312b")
DT_GOLD = hx("#d9a94a")
DT_GOLD_D = hx("#5e3410")
DT_GOLD_L = hx("#ffe6a6")


def _dt_background(c, w, h):
    with state(c):
        _card_clip(c, w, h)
        c.radialGradient(w * 0.5, h * 0.56, h * 0.86, [DT_MID, DT_DEEP], [0.0, 1.0])
        _diagonals(c, w, h, DT_RED, 0.050, 7.5 * mm, 1.2 * mm, ang=-58)

        # rune ring behind the pips
        with state(c):
            c.setStrokeColor(DT_GOLD)
            c.setLineWidth(0.6)
            c.setStrokeAlpha(0.24)
            c.circle(w / 2, h * 0.53, 24 * mm, fill=0, stroke=1)
            c.setStrokeAlpha(0.15)
            c.circle(w / 2, h * 0.53, 27.5 * mm, fill=0, stroke=1)
            c.setStrokeAlpha(0.32)
            for k in range(12):
                a = math.radians(k * 30 + 15)
                r0, r1 = 24 * mm, 27.5 * mm
                c.line(w / 2 + math.cos(a) * r0, h * 0.53 + math.sin(a) * r0,
                       w / 2 + math.cos(a) * r1, h * 0.53 + math.sin(a) * r1)

        with state(c):
            c.translate(w / 2, h * 0.50)
            icons.dota_aegis(c, 29 * mm, fade(DT_GOLD_L, 0.045),
                             fade(DT_MID, 0.08), fade(DT_MID, 0.11),
                             fade(DT_GOLD_L, 0.045))

        _specks(c, w, h, DT_GOLD_L, seed=53, n=40, alpha=0.30)

def _dt_corner(c, w, h):
    """Ornate gold brackets at all four frame corners."""
    i = FRAME_INSET
    L = 9.5 * mm
    with state(c):
        c.setStrokeColor(DT_GOLD)
        c.setStrokeAlpha(0.85)
        c.setLineWidth(1.0)
        c.setLineCap(1)
        for (ox, oy, sx, sy) in ((i, i, 1, 1), (w - i, i, -1, 1),
                                 (i, h - i, 1, -1), (w - i, h - i, -1, -1)):
            with state(c):
                c.translate(ox, oy)
                c.scale(sx, sy)
                c.translate(1.6 * mm, 1.6 * mm)
                c.drawPath(path(c, ("m", 0, L), ("l", 0, 0), ("l", L, 0)), fill=0, stroke=1)
                c.setFillColor(DT_GOLD)
                c.circle(0, 0, 0.7 * mm, fill=1, stroke=0)


# ===========================================================================
# Apex Legends  -  diamonds
# ===========================================================================
AP_DEEP = hx("#0b0d11")
AP_MID = hx("#333942")
AP_RED = hx("#d33f24")
AP_ORANGE = hx("#f0762c")
AP_LIGHT = hx("#e7ecf2")
AP_DARK = hx("#3a0f06")


def _ap_background(c, w, h):
    with state(c):
        _card_clip(c, w, h)
        c.radialGradient(w * 0.38, h * 0.66, h * 0.98, [AP_MID, AP_DEEP], [0.0, 1.0])

        # hex tech grid
        with state(c):
            c.setStrokeColor(AP_LIGHT)
            c.setStrokeAlpha(0.065)
            c.setLineWidth(0.45)
            r = 4.4 * mm
            dx, dy = r * 1.5, r * math.sqrt(3)
            for row in range(-1, int(h / dy) + 2):
                for col in range(-1, int(w / dx) + 2):
                    cx = col * dx
                    cy = row * dy + (dy / 2 if col % 2 else 0)
                    pth = c.beginPath()
                    for k in range(6):
                        a = math.radians(60 * k)
                        (pth.moveTo if k == 0 else pth.lineTo)(
                            cx + r * math.cos(a), cy + r * math.sin(a))
                    pth.close()
                    c.drawPath(pth, fill=0, stroke=1)

        # angled accent bands
        with state(c):
            c.translate(w / 2, h / 2)
            c.rotate(-28)
            for (off, hgt, col) in ((-27 * mm, 2.4 * mm, fade(AP_RED, 0.40)),
                                    (-22.5 * mm, 0.9 * mm, fade(AP_ORANGE, 0.34)),
                                    (28 * mm, 1.6 * mm, fade(AP_RED, 0.28))):
                c.setFillColor(col)
                c.rect(-w, off, 2 * w, hgt, fill=1, stroke=0)

        with state(c):
            c.translate(w / 2, h * 0.50)
            icons.apex_mark(c, 30 * mm, fade(AP_LIGHT, 0.050),
                            fade(AP_MID, 0.10), fade(AP_LIGHT, 0.03))

def _ap_corner(c, w, h):
    """Clipped-corner tech brackets."""
    i = FRAME_INSET
    L = 8.0 * mm
    with state(c):
        c.setStrokeColor(AP_ORANGE)
        c.setLineWidth(1.3)
        c.setLineCap(0)
        for (ox, oy, sx, sy) in ((i, i, 1, 1), (w - i, h - i, -1, -1)):
            with state(c):
                c.translate(ox, oy)
                c.scale(sx, sy)
                c.drawPath(path(c, ("m", 0, L), ("l", 0, 2.6 * mm),
                                ("l", 2.6 * mm, 0), ("l", L, 0)), fill=0, stroke=1)


# ===========================================================================
THEMES = {
    "spades": Theme(
        key="hollow-knight", suit="spades", game="HOLLOW KNIGHT",
        rank_font="Cinzel", label_font="Marcellus",
        index=HK_PALE, suit_color=HK_PALE, frame=HK_BLUE,
        paint_background=_hk_background, corner=_hk_corner,
        draw_pip=lambda c, s: icons.hollow_knight_mask(c, s, HK_PALE, HK_DEEP),
        label_size=5.2, label_tracking=1.5, pip_scale=0.74,
    ),
    "clubs": Theme(
        key="clash-royale", suit="clubs", game="CLASH ROYALE",
        rank_font="Lilita", label_font="Lilita",
        index=CR_GOLD_L, suit_color=CR_GOLD, frame=CR_GOLD,
        paint_background=_cr_background, corner=_cr_corner,
        draw_pip=lambda c, s: icons.clash_royale_crown(
            c, s, CR_GOLD, CR_GOLD_D, CR_GOLD_L, hx("#3fb7e8")),
        label_size=5.4, label_tracking=0.8, rank_scale=0.96, pip_scale=1.02,
    ),
    "hearts": Theme(
        key="dota-2", suit="hearts", game="DOTA 2",
        rank_font="Cinzel", label_font="Marcellus",
        index=DT_GOLD_L, suit_color=DT_RED, frame=DT_GOLD,
        paint_background=_dt_background, corner=_dt_corner,
        draw_pip=lambda c, s: icons.dota_aegis(
            c, s, DT_GOLD, DT_GOLD_D, hx("#8f1d1d"), DT_GOLD_L),
        label_size=5.4, label_tracking=2.0, pip_scale=0.80,
    ),
    "diamonds": Theme(
        key="apex-legends", suit="diamonds", game="APEX LEGENDS",
        rank_font="Saira", label_font="Saira",
        index=AP_LIGHT, suit_color=AP_ORANGE, frame=AP_ORANGE,
        paint_background=_ap_background, corner=_ap_corner,
        draw_pip=lambda c, s: icons.apex_mark(c, s, AP_RED, AP_DARK, hx("#ffd0a0")),
        label_size=5.6, label_tracking=1.6, rank_scale=1.06, pip_scale=1.00,
    ),
}

SUIT_ORDER = ("spades", "clubs", "hearts", "diamonds")
