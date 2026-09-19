"""The four game marks used in place of the suit pips.

Each mark is drawn centred on the current origin inside a unit box spanning
roughly -0.8..0.8, then scaled to ``size``.
"""
from __future__ import annotations

from .config import path, state
from .suits import _circle


def _blob(c, cx, cy, rx, ry, ang, color):
    with state(c):
        c.translate(cx, cy)
        if ang:
            c.rotate(ang)
        c.scale(rx, ry)
        c.setFillColor(color)
        c.drawPath(_circle(c, 0.0, 0.0, 1.0), fill=1, stroke=0)


# --- Hollow Knight: the Knight's mask ---------------------------------------
def _mask_horn(c, sx):
    return path(
        c,
        ("m", -0.230 * sx, 0.250),
        ("c", -0.410 * sx, 0.335, -0.610 * sx, 0.428, -0.790 * sx, 0.502),
        ("c", -0.650 * sx, 0.285, -0.515 * sx, 0.105, -0.400 * sx, -0.030),
        ("c", -0.355 * sx, 0.095, -0.305 * sx, 0.195, -0.230 * sx, 0.250),
        ("z",),
    )


def _mask_face(c):
    return path(
        c,
        ("m", 0.000, -0.540),
        ("c", -0.205, -0.520, -0.352, -0.330, -0.378, -0.070),
        ("c", -0.392, 0.100, -0.325, 0.215, -0.200, 0.258),
        ("c", -0.112, 0.286, 0.112, 0.286, 0.200, 0.258),
        ("c", 0.325, 0.215, 0.392, 0.100, 0.378, -0.070),
        ("c", 0.352, -0.330, 0.205, -0.520, 0.000, -0.540),
        ("z",),
    )


def hollow_knight_mask(c, size, shell, eye):
    with state(c):
        c.scale(size, size)
        c.setFillColor(shell)
        for sx in (1.0, -1.0):
            c.drawPath(_mask_horn(c, sx), fill=1, stroke=0)
        c.drawPath(_mask_face(c), fill=1, stroke=0)
        _blob(c, -0.152, -0.030, 0.094, 0.145, 14, eye)
        _blob(c, 0.152, -0.030, 0.094, 0.145, -14, eye)


# --- Clash Royale: the battle crown -----------------------------------------
def clash_royale_crown(c, size, gold, dark, light, gem):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setStrokeColor(dark)
        c.setLineWidth(0.055)

        body = path(
            c,
            ("m", -0.450, -0.240),
            ("c", -0.450, -0.050, -0.440, 0.060, -0.430, 0.130),
            ("c", -0.360, 0.060, -0.280, -0.040, -0.185, -0.105),
            ("c", -0.105, -0.045, -0.045, 0.080, -0.018, 0.225),
            ("c", -0.006, 0.225, 0.006, 0.225, 0.018, 0.225),
            ("c", 0.045, 0.080, 0.105, -0.045, 0.185, -0.105),
            ("c", 0.280, -0.040, 0.360, 0.060, 0.430, 0.130),
            ("c", 0.440, 0.060, 0.450, -0.050, 0.450, -0.240),
            ("z",),
        )
        c.setFillColor(gold)
        c.drawPath(body, fill=1, stroke=1)

        band = path(c, ("m", -0.480, -0.470), ("l", 0.480, -0.470),
                    ("l", 0.480, -0.220), ("l", -0.480, -0.220), ("z",))
        c.setFillColor(gold)
        c.drawPath(band, fill=1, stroke=1)

        for cx, cy, r in ((-0.435, 0.205, 0.100), (0.0, 0.305, 0.115), (0.435, 0.205, 0.100)):
            c.setFillColor(gold)
            c.drawPath(_circle(c, cx, cy, r), fill=1, stroke=1)
            _blob(c, cx - r * 0.28, cy + r * 0.34, r * 0.34, r * 0.24, 30, light)

        c.setFillColor(gem)
        c.drawPath(path(c, ("m", 0.0, -0.245), ("l", 0.085, -0.345),
                        ("l", 0.0, -0.445), ("l", -0.085, -0.345), ("z",)),
                   fill=1, stroke=1)


# --- Dota 2: the Immortal rank medal ----------------------------------------
def dota_immortal(c, size, gold, dark, field, gem):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setStrokeColor(dark)
        c.setLineWidth(0.045)

        for sx in (-1.0, 1.0):
            c.setFillColor(gold)
            c.drawPath(path(c, ("m", 0.175 * sx, 0.275), ("l", 0.620 * sx, 0.620),
                            ("l", 0.600 * sx, 0.275), ("l", 0.380 * sx, 0.090),
                            ("l", 0.215 * sx, 0.055), ("z",)), fill=1, stroke=1)

        crest = path(c, ("m", 0.0, 0.620), ("l", 0.195, 0.255), ("l", 0.250, -0.130),
                     ("l", 0.0, -0.620), ("l", -0.250, -0.130), ("l", -0.195, 0.255), ("z",))
        c.setFillColor(gold)
        c.drawPath(crest, fill=1, stroke=1)

        inner = path(c, ("m", 0.0, 0.410), ("l", 0.118, 0.195), ("l", 0.155, -0.105),
                     ("l", 0.0, -0.405), ("l", -0.155, -0.105), ("l", -0.118, 0.195), ("z",))
        c.setFillColor(field)
        c.setLineWidth(0.032)
        c.drawPath(inner, fill=1, stroke=1)

        c.setFillColor(gem)
        c.drawPath(_circle(c, 0.0, 0.020, 0.105), fill=1, stroke=1)


# --- Apex Legends: the mark -------------------------------------------------
def apex_mark(c, size, main, dark, light):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(0)
        body = path(
            c,
            ("m", 0.000, 0.640),
            ("l", 0.258, -0.030),
            ("l", 0.258, -0.215),
            ("l", 0.425, -0.215),
            ("l", 0.425, -0.620),
            ("l", 0.185, -0.620),
            ("l", 0.000, -0.215),
            ("l", -0.185, -0.620),
            ("l", -0.425, -0.620),
            ("l", -0.425, -0.215),
            ("l", -0.258, -0.215),
            ("l", -0.258, -0.030),
            ("z",),
        )
        c.setFillColor(main)
        c.setStrokeColor(dark)
        c.setLineWidth(0.040)
        c.drawPath(body, fill=1, stroke=1)
