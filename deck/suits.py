"""Traditional suit silhouettes, drawn as vector paths.

Each shape is defined in a unit box roughly spanning -0.5..0.5 on both axes
and is drawn centred on the current origin, scaled to ``size``.
"""
from __future__ import annotations

from .config import path, state

_K = 0.5523  # circle -> bezier constant


def _circle(c, cx, cy, r):
    k = r * _K
    return path(
        c,
        ("m", cx, cy + r),
        ("c", cx + k, cy + r, cx + r, cy + k, cx + r, cy),
        ("c", cx + r, cy - k, cx + k, cy - r, cx, cy - r),
        ("c", cx - k, cy - r, cx - r, cy - k, cx - r, cy),
        ("c", cx - r, cy + k, cx - k, cy + r, cx, cy + r),
        ("z",),
    )


def _heart_path(c, flip=1.0):
    """Classic heart; flip=-1 gives the inverted lobe used by the spade."""
    f = flip
    return path(
        c,
        ("m", 0.00, -0.50 * f),
        ("c", -0.30 * 1.0, -0.22 * f, -0.56, 0.02 * f, -0.56, 0.20 * f),
        ("c", -0.56, 0.40 * f, -0.40, 0.50 * f, -0.26, 0.50 * f),
        ("c", -0.13, 0.50 * f, -0.04, 0.42 * f, 0.00, 0.33 * f),
        ("c", 0.04, 0.42 * f, 0.13, 0.50 * f, 0.26, 0.50 * f),
        ("c", 0.40, 0.50 * f, 0.56, 0.40 * f, 0.56, 0.20 * f),
        ("c", 0.56, 0.02 * f, 0.30, -0.22 * f, 0.00, -0.50 * f),
        ("z",),
    )


def _stem_path(c, top_y, bot_y, half_top, half_bot):
    """Concave flared stem shared by the spade and the club."""
    span = top_y - bot_y
    return path(
        c,
        ("m", -half_top, top_y),
        ("c", -half_top, bot_y + span * 0.45,
         -half_bot * 0.55, bot_y + span * 0.22, -half_bot, bot_y),
        ("l", half_bot, bot_y),
        ("c", half_bot * 0.55, bot_y + span * 0.22,
         half_top, bot_y + span * 0.45, half_top, top_y),
        ("z",),
    )


def _spade_body(c):
    return path(
        c,
        ("m", 0.000, 0.540),
        ("c", -0.100, 0.260, -0.580, 0.020, -0.580, -0.200),
        ("c", -0.580, -0.400, -0.420, -0.500, -0.270, -0.500),
        ("c", -0.140, -0.500, -0.040, -0.430, 0.000, -0.340),
        ("c", 0.040, -0.430, 0.140, -0.500, 0.270, -0.500),
        ("c", 0.420, -0.500, 0.580, -0.400, 0.580, -0.200),
        ("c", 0.580, 0.020, 0.100, 0.260, 0.000, 0.540),
        ("z",),
    )


def draw_heart(c, size, color):
    with state(c):
        c.scale(size, size)
        c.setFillColor(color)
        c.drawPath(_heart_path(c, 1.0), fill=1, stroke=0)


def draw_spade(c, size, color):
    with state(c):
        c.scale(size, size)
        c.setFillColor(color)
        c.drawPath(_spade_body(c), fill=1, stroke=0)
        c.drawPath(_stem_path(c, -0.240, -0.560, 0.052, 0.200), fill=1, stroke=0)


def draw_club(c, size, color):
    with state(c):
        c.scale(size, size)
        c.setFillColor(color)
        r = 0.238
        c.drawPath(_stem_path(c, 0.060, -0.545, 0.078, 0.212), fill=1, stroke=0)
        c.drawPath(_circle(c, 0.000, 0.250, r), fill=1, stroke=0)
        c.drawPath(_circle(c, -0.256, -0.112, r), fill=1, stroke=0)
        c.drawPath(_circle(c, 0.256, -0.112, r), fill=1, stroke=0)


def draw_diamond(c, size, color):
    with state(c):
        c.scale(size, size)
        c.setFillColor(color)
        p = path(
            c,
            ("m", 0.00, 0.54),
            ("c", 0.14, 0.28, 0.28, 0.14, 0.40, 0.00),
            ("c", 0.28, -0.14, 0.14, -0.28, 0.00, -0.54),
            ("c", -0.14, -0.28, -0.28, -0.14, -0.40, 0.00),
            ("c", -0.28, 0.14, -0.14, 0.28, 0.00, 0.54),
            ("z",),
        )
        c.drawPath(p, fill=1, stroke=0)


DRAWERS = {
    "spades": draw_spade,
    "hearts": draw_heart,
    "clubs": draw_club,
    "diamonds": draw_diamond,
}

GLYPHS = {"spades": "♠", "hearts": "♥", "clubs": "♣", "diamonds": "♦"}


def draw_suit(c, suit, size, color):
    DRAWERS[suit](c, size, color)
