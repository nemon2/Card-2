"""The four game marks used in place of the suit pips.

Each mark is drawn centred on the current origin inside a unit box spanning
roughly -0.8..0.8, then scaled to ``size``.
"""
from __future__ import annotations

import math

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
#: five square battlements over a blue band, as the crown appears in game
_TEETH = (-0.390, -0.195, 0.000, 0.195, 0.390)
_TOOTH_HW = 0.0725
_TOOTH_TOP = 0.400
_NOTCH_Y = 0.140
_BAND_TOP = -0.060


def _crown_body(c):
    cmds = [("m", _TEETH[0] - _TOOTH_HW, _BAND_TOP),
            ("l", _TEETH[0] - _TOOTH_HW, _TOOTH_TOP)]
    for i, cx in enumerate(_TEETH):
        cmds.append(("l", cx + _TOOTH_HW, _TOOTH_TOP))
        if i < len(_TEETH) - 1:
            cmds += [("l", cx + _TOOTH_HW, _NOTCH_Y),
                     ("l", _TEETH[i + 1] - _TOOTH_HW, _NOTCH_Y),
                     ("l", _TEETH[i + 1] - _TOOTH_HW, _TOOTH_TOP)]
    cmds.append(("l", _TEETH[-1] + _TOOTH_HW, _BAND_TOP))
    cmds.append(("z",))
    return path(c, *cmds)


def clash_royale_crown(c, size, gold, gold_d, gold_l, blue, blue_d, gem):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)
        c.setLineWidth(0.042)

        c.setStrokeColor(gold_d)
        c.setFillColor(gold)
        c.drawPath(_crown_body(c), fill=1, stroke=1)

        # lit top face of every battlement, so the rim reads as having depth
        for cx in _TEETH:
            c.setFillColor(gold_l)
            c.setStrokeColor(gold_d)
            c.setLineWidth(0.030)
            c.drawPath(path(c, ("m", cx - _TOOTH_HW, _TOOTH_TOP),
                            ("l", cx + _TOOTH_HW, _TOOTH_TOP),
                            ("l", cx + _TOOTH_HW, _TOOTH_TOP - 0.052),
                            ("l", cx - _TOOTH_HW, _TOOTH_TOP - 0.052), ("z",)),
                       fill=1, stroke=1)

        # blue band, barrelled the way a cylinder reads from slightly above
        band = path(
            c,
            ("m", -0.500, -0.050),
            ("c", -0.500, -0.300, -0.480, -0.400, -0.440, -0.448),
            ("c", -0.250, -0.512, 0.250, -0.512, 0.440, -0.448),
            ("c", 0.480, -0.400, 0.500, -0.300, 0.500, -0.050),
            ("c", 0.250, -0.112, -0.250, -0.112, -0.500, -0.050),
            ("z",),
        )
        c.setFillColor(blue)
        c.setStrokeColor(blue_d)
        c.setLineWidth(0.042)
        c.drawPath(band, fill=1, stroke=1)

        c.setFillColor(gem)
        c.setStrokeColor(gold_d)
        c.setLineWidth(0.030)
        c.drawPath(path(c, ("m", 0.0, -0.148), ("l", 0.110, -0.282),
                        ("l", 0.0, -0.416), ("l", -0.110, -0.282), ("z",)),
                   fill=1, stroke=1)


# --- Dota 2: the Immortal rank medal ----------------------------------------
_FEATHERS = ((16, 0.54, 0.108), (45, 0.60, 0.102), (73, 0.47, 0.086))


def _feather(c, ln, wd):
    return path(
        c,
        ("m", 0.0, 0.0),
        ("c", ln * 0.34, wd, ln * 0.72, wd * 0.88, ln, 0.0),
        ("c", ln * 0.72, -wd * 0.88, ln * 0.34, -wd, 0.0, 0.0),
        ("z",),
    )


def dota_immortal(c, size, gold, gold_d, dark, ember, bright):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(1)

        # feathered wings
        for sx in (-1.0, 1.0):
            for i, (ang, ln, wd) in enumerate(_FEATHERS):
                with state(c):
                    c.translate(0.095 * sx, -0.010)
                    c.rotate(ang * sx if sx > 0 else 180 - ang)
                    c.setFillColor(ember if i == 1 else dark)
                    c.setStrokeColor(gold_d)
                    c.setLineWidth(0.040)
                    c.drawPath(_feather(c, ln, wd), fill=1, stroke=1)

        # central body
        c.setFillColor(dark)
        c.setStrokeColor(gold_d)
        c.setLineWidth(0.040)
        c.drawPath(path(c, ("m", 0.0, 0.330),
                        ("c", 0.105, 0.250, 0.135, 0.020, 0.105, -0.170),
                        ("c", 0.065, -0.320, -0.065, -0.320, -0.105, -0.170),
                        ("c", -0.135, 0.020, -0.105, 0.250, 0.0, 0.330), ("z",)),
                   fill=1, stroke=1)

        # starburst over the body
        with state(c):
            c.translate(0.0, 0.045)
            c.setFillColor(bright)
            c.setStrokeColor(gold_d)
            c.setLineWidth(0.026)
            pts = []
            for k in range(16):
                a = math.radians(k * 22.5)
                r = 0.215 if k % 4 == 0 else (0.115 if k % 2 == 0 else 0.052)
                pts.append((r * math.cos(a), r * math.sin(a)))
            cmds = [("m", pts[0][0], pts[0][1])] + [("l", x, y) for x, y in pts[1:]] + [("z",)]
            c.drawPath(path(c, *cmds), fill=1, stroke=1)

        # spire with crossguard
        c.setFillColor(gold)
        c.setStrokeColor(gold_d)
        c.setLineWidth(0.030)
        c.drawPath(path(c, ("m", -0.026, 0.300), ("l", -0.026, 0.520), ("l", 0.0, 0.610),
                        ("l", 0.026, 0.520), ("l", 0.026, 0.300), ("z",)), fill=1, stroke=1)
        c.drawPath(path(c, ("m", -0.105, 0.400), ("l", 0.105, 0.400),
                        ("l", 0.105, 0.440), ("l", -0.105, 0.440), ("z",)), fill=1, stroke=1)

        # plinth
        c.setFillColor(gold)
        c.setLineWidth(0.036)
        c.drawPath(path(c, ("m", -0.205, -0.330), ("l", 0.205, -0.330),
                        ("l", 0.165, -0.520), ("l", -0.165, -0.520), ("z",)), fill=1, stroke=1)
        c.setFillColor(dark)
        c.setLineWidth(0.026)
        c.drawPath(path(c, ("m", -0.135, -0.372), ("l", 0.135, -0.372),
                        ("l", 0.112, -0.478), ("l", -0.112, -0.478), ("z",)), fill=1, stroke=1)


# --- Apex Legends: the mark -------------------------------------------------
def apex_mark(c, size, main, dark, light):
    with state(c):
        c.scale(size, size)
        c.setLineJoin(0)
        body = path(
            c,
            ("m", 0.000, 0.620),
            ("l", 0.300, -0.120),
            ("l", 0.300, -0.255),
            ("l", 0.470, -0.255),
            ("l", 0.470, -0.620),
            ("l", 0.215, -0.620),
            ("l", 0.000, -0.075),
            ("l", -0.215, -0.620),
            ("l", -0.470, -0.620),
            ("l", -0.470, -0.255),
            ("l", -0.300, -0.255),
            ("l", -0.300, -0.120),
            ("z",),
        )
        c.setFillColor(main)
        c.setStrokeColor(dark)
        c.setLineWidth(0.038)
        c.drawPath(body, fill=1, stroke=1)


# --- Dota 2: the logo mark --------------------------------------------------
#: A rough-edged square cut by two diagonal stripes. The three light shapes are
#: 180-degree rotations of each other, exactly as the real mark is built.
def _dota_plate(c):
    return path(
        c,
        ("m", -0.500, -0.455),
        ("l", -0.472, -0.020), ("l", -0.500, 0.200), ("l", -0.462, 0.500),
        ("l", -0.100, 0.470), ("l", 0.160, 0.500), ("l", 0.500, 0.458),
        ("l", 0.472, 0.100), ("l", 0.500, -0.160), ("l", 0.458, -0.500),
        ("l", 0.080, -0.470), ("l", -0.180, -0.500),
        ("z",),
    )


def dota_logo(c, size, red, light):
    """Red plate cut by two diagonal stripes into three light shapes.

    The band and the two counters are 180-degree rotations of one another,
    the way the real mark is built; red stays dominant.
    """
    with state(c):
        c.scale(size, size)
        c.setLineJoin(0)
        c.setFillColor(red)
        c.drawPath(_dota_plate(c), fill=1, stroke=0)

        c.setFillColor(light)
        c.drawPath(path(c,
                        ("m", -0.058, 0.360), ("l", 0.360, -0.271),
                        ("l", 0.360, -0.360), ("l", 0.058, -0.360),
                        ("l", -0.360, 0.271), ("l", -0.360, 0.360), ("z",)),
                   fill=1, stroke=0)
        for sx in (1.0, -1.0):
            c.drawPath(path(c,
                            ("m", 0.093 * sx, 0.360 * sx),
                            ("l", 0.360 * sx, 0.360 * sx),
                            ("l", 0.360 * sx, -0.043 * sx), ("z",)),
                       fill=1, stroke=0)
