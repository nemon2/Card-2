"""Original vector marks used in place of the suit pips.

Every mark is drawn centred on the current origin inside a unit box spanning
roughly -0.65..0.65, then scaled to ``size``. They are hand-drawn
interpretations evoking each game, not reproductions of any logo artwork.
"""
from __future__ import annotations

from .config import path, state
from .suits import _circle


def _blob(c, cx, cy, rx, ry, ang, color):
    """Filled, optionally rotated ellipse."""
    with state(c):
        c.translate(cx, cy)
        if ang:
            c.rotate(ang)
        c.scale(rx, ry)
        c.setFillColor(color)
        c.drawPath(_circle(c, 0.0, 0.0, 1.0), fill=1, stroke=0)


def _shade(c, clip_path, hl_path, color, alpha):
    """Fill ``hl_path`` clipped to ``clip_path`` so it cannot spill outside."""
    with state(c):
        c.clipPath(clip_path, stroke=0, fill=0)
        c.setFillColor(color)
        c.setFillAlpha(alpha * getattr(color, "alpha", 1.0))
        c.drawPath(hl_path, fill=1, stroke=0)


# --- Hollow Knight: the Knight's horned mask -------------------------------
def _mask_face(c):
    return path(
        c,
        ("m", 0.000, -0.520),
        ("c", -0.200, -0.500, -0.345, -0.320, -0.372, -0.070),
        ("c", -0.386, 0.090, -0.320, 0.212, -0.196, 0.254),
        ("c", -0.110, 0.282, 0.110, 0.282, 0.196, 0.254),
        ("c", 0.320, 0.212, 0.386, 0.090, 0.372, -0.070),
        ("c", 0.345, -0.320, 0.200, -0.500, 0.000, -0.520),
        ("z",),
    )


def _mask_horn(c, sx):
    """One horn: a thick wedge sweeping up and outward to a sharp tip."""
    return path(
        c,
        ("m", -0.240 * sx, 0.248),
        ("c", -0.408 * sx, 0.330, -0.578 * sx, 0.404, -0.726 * sx, 0.462),
        ("c", -0.606 * sx, 0.282, -0.502 * sx, 0.136, -0.388 * sx, 0.026),
        ("c", -0.364 * sx, 0.118, -0.312 * sx, 0.198, -0.240 * sx, 0.248),
        ("z",),
    )


def hollow_knight_mask(c, size, shell, eye, edge=None):
    with state(c):
        c.scale(size, size)
        c.setFillColor(shell)
        c.setLineJoin(1)
        for sx in (1.0, -1.0):
            c.drawPath(_mask_horn(c, sx), fill=1, stroke=0)
        c.drawPath(_mask_face(c), fill=1, stroke=0)
        _blob(c, -0.158, -0.022, 0.092, 0.140, 13, eye)
        _blob(c, 0.158, -0.022, 0.092, 0.140, -13, eye)


# --- Clash Royale: the battle crown ----------------------------------------
def clash_royale_crown(c, size, gold, gold_dark, gold_light, gem):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setLineWidth(0.032)
        c.setStrokeColor(gold_dark)

        body = path(
            c,
            ("m", -0.440, -0.210),
            ("l", -0.440, 0.140),
            ("l", -0.185, -0.045),
            ("l", 0.000, 0.260),
            ("l", 0.185, -0.045),
            ("l", 0.440, 0.140),
            ("l", 0.440, -0.210),
            ("z",),
        )
        c.setFillColor(gold)
        c.drawPath(body, fill=1, stroke=1)
        _shade(
            c, body,
            path(c, ("m", -0.520, 0.320), ("l", -0.075, 0.320),
                 ("l", -0.360, -0.300), ("l", -0.520, -0.300), ("z",)),
            gold_light, 0.40,
        )

        band = path(
            c,
            ("m", -0.470, -0.460), ("l", 0.470, -0.460),
            ("l", 0.470, -0.215), ("l", -0.470, -0.215), ("z",),
        )
        c.setFillColor(gold)
        c.drawPath(band, fill=1, stroke=1)
        _shade(
            c, band,
            path(c, ("m", -0.470, -0.215), ("l", 0.470, -0.215),
                 ("l", 0.470, -0.300), ("l", -0.470, -0.300), ("z",)),
            gold_light, 0.45,
        )

        for cx, cy, r in ((-0.440, 0.195, 0.108), (0.000, 0.325, 0.128), (0.440, 0.195, 0.108)):
            c.setFillColor(gold)
            c.drawPath(_circle(c, cx, cy, r), fill=1, stroke=1)
            _blob(c, cx - r * 0.30, cy + r * 0.34, r * 0.34, r * 0.26, 30, gold_light)

        c.setFillColor(gem)
        c.drawPath(
            path(c, ("m", 0.000, -0.238), ("l", 0.094, -0.338),
                 ("l", 0.000, -0.438), ("l", -0.094, -0.338), ("z",)),
            fill=1, stroke=1,
        )


# --- Dota 2: the Aegis -----------------------------------------------------
def _shield_path(c, s=1.0):
    return path(
        c,
        ("m", 0.000 * s, 0.500 * s),
        ("l", -0.320 * s, 0.360 * s),
        ("c", -0.360 * s, 0.120 * s, -0.340 * s, -0.140 * s, -0.220 * s, -0.340 * s),
        ("c", -0.140 * s, -0.460 * s, -0.060 * s, -0.505 * s, 0.000 * s, -0.530 * s),
        ("c", 0.060 * s, -0.505 * s, 0.140 * s, -0.460 * s, 0.220 * s, -0.340 * s),
        ("c", 0.340 * s, -0.140 * s, 0.360 * s, 0.120 * s, 0.320 * s, 0.360 * s),
        ("z",),
    )


def dota_aegis(c, size, gold, gold_dark, inner, gem):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setLineWidth(0.030)
        c.setStrokeColor(gold_dark)

        for sx in (-1.0, 1.0):
            wing = path(
                c,
                ("m", 0.296 * sx, 0.352),
                ("l", 0.690 * sx, 0.428),
                ("l", 0.628 * sx, 0.268),
                ("l", 0.452 * sx, 0.206),
                ("l", 0.322 * sx, 0.152),
                ("z",),
            )
            c.setFillColor(gold)
            c.drawPath(wing, fill=1, stroke=1)

        outer = _shield_path(c, 1.0)
        c.setFillColor(gold)
        c.drawPath(outer, fill=1, stroke=1)
        _shade(
            c, outer,
            path(c, ("m", -0.400, 0.560), ("l", -0.060, 0.560),
                 ("l", -0.260, -0.600), ("l", -0.400, -0.600), ("z",)),
            gem, 0.30,
        )

        c.setFillColor(inner)
        c.setLineWidth(0.022)
        c.drawPath(_shield_path(c, 0.74), fill=1, stroke=1)

        c.setFillColor(gem)
        c.drawPath(_circle(c, 0.000, 0.010, 0.125), fill=1, stroke=1)


# --- Apex Legends: the angular chevron -------------------------------------
def _chevron_path(c, s=1.0):
    return path(
        c,
        ("m", 0.000 * s, 0.540 * s),
        ("l", 0.470 * s, -0.300 * s),
        ("l", 0.470 * s, -0.540 * s),
        ("l", 0.235 * s, -0.540 * s),
        ("l", 0.000 * s, -0.060 * s),
        ("l", -0.235 * s, -0.540 * s),
        ("l", -0.470 * s, -0.540 * s),
        ("l", -0.470 * s, -0.300 * s),
        ("z",),
    )


def apex_mark(c, size, main, dark, light):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(0)
        body = _chevron_path(c, 1.0)
        c.setFillColor(main)
        c.setStrokeColor(dark)
        c.setLineWidth(0.034)
        c.drawPath(body, fill=1, stroke=1)
        _shade(
            c, body,
            path(c, ("m", -0.060, 0.620), ("l", 0.060, 0.620),
                 ("l", -0.300, -0.620), ("l", -0.560, -0.620), ("z",)),
            light, 0.34,
        )
