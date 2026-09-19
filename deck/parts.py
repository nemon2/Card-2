"""Reusable body parts for the hand-drawn characters.

Anything drawn behind a figure goes down first; ``bust`` and ``cloak`` fill
with the paper colour so they mask whatever is behind them, which is how the
weapons and capes read as being carried rather than pasted on.
"""
from __future__ import annotations

from .sketch import blob, ink, oval


def bust(c, k, paper, w=0.34, neck_y=-0.14, hem=-0.50, seed=1):
    """Neck and shoulders."""
    ink(c, [("m", -w, hem),
            ("c", -w * 0.96, -0.32, -w * 0.52, neck_y, 0.0, neck_y),
            ("c", w * 0.52, neck_y, w * 0.96, -0.32, w, hem),
            ("l", -w, hem)], k, seed=seed, fill=paper)


def cloak(c, k, paper, w=0.40, neck_y=-0.06, hem=-0.50, seed=1, scallop=0.05):
    """Shoulders as a cape with a ragged hem."""
    ink(c, [("m", -w, hem),
            ("c", -w * 0.92, -0.30, -w * 0.46, neck_y, 0.0, neck_y),
            ("c", w * 0.46, neck_y, w * 0.92, -0.30, w, hem),
            ("l", w * 0.60, hem + scallop), ("l", w * 0.30, hem),
            ("l", 0.0, hem + scallop), ("l", -w * 0.30, hem),
            ("l", -w * 0.60, hem + scallop), ("z",)], k, seed=seed, fill=paper)


def folds(c, k, xs, top, bottom, seed=1, width=0.024):
    """Vertical drape lines on a cloak or tunic."""
    for i, x in enumerate(xs):
        ink(c, [("m", x, top), ("c", x + 0.012, (top + bottom) / 2, x - 0.010, bottom + 0.05,
                                x, bottom)], k, width=width, seed=seed + i)


def pauldrons(c, k, paper, w=0.34, y=-0.26, seed=1):
    """A curved shoulder plate on each side."""
    for sx in (-1, 1):
        ink(c, [("m", sx * w * 0.42, y + 0.10),
                ("c", sx * w * 0.86, y + 0.09, sx * (w + 0.06), y - 0.02, sx * (w + 0.04), y - 0.16),
                ("c", sx * w * 0.78, y - 0.10, sx * w * 0.56, y - 0.06, sx * w * 0.40, y - 0.05),
                ("z",)], k, width=0.032, seed=seed + sx, fill=paper)


def collar(c, k, y=-0.12, w=0.16, seed=1):
    ink(c, [("m", -w, y + 0.05), ("l", 0.0, y - 0.06), ("l", w, y + 0.05)],
        k, width=0.030, seed=seed)


def hatch(c, k, x0, y0, dx, dy, n=3, step=0.055, seed=1, width=0.020):
    """Short parallel shading strokes."""
    for i in range(n):
        ink(c, [("m", x0 + i * step, y0), ("l", x0 + i * step + dx, y0 + dy)],
            k, width=width, seed=seed + i, amp=0.005)


def haft(c, k, x0, y0, x1, y1, width=0.034, seed=1):
    """A weapon shaft."""
    ink(c, [("m", x0, y0), ("l", x1, y1)], k, width=width, seed=seed)


def mask_face(c, k, paper, cx=0.0, cy=0.15, rx=0.24, ry=0.27, seed=2):
    oval(c, cx, cy, rx, ry, k, seed=seed, fill=paper)


def void_eyes(c, k, y=0.15, dx=0.105, rx=0.055, ry=0.078, tilt=12):
    """The big dark voids every Hollow Knight vessel has."""
    for sx in (-1, 1):
        oval(c, sx * dx, y, rx, ry, k, seed=40 + sx, fill=k, width=0.018, rot=-tilt * sx)


def dot_eyes(c, k, y=0.15, dx=0.095, r=0.036):
    blob(c, -dx, y, r, k)
    blob(c, dx, y, r, k)


def brow(c, k, y=0.24, dx=0.105, w=0.085, drop=0.045, seed=1):
    """Angry eyebrows."""
    for sx in (-1, 1):
        ink(c, [("m", sx * (dx - w / 2), y + drop), ("l", sx * (dx + w / 2), y - drop * 0.4)],
            k, width=0.032, seed=seed + sx)


def mouth_line(c, k, y=0.02, w=0.11, depth=0.0, seed=1, width=0.028):
    if depth:
        ink(c, [("m", -w, y), ("c", -w * 0.4, y - depth, w * 0.4, y - depth, w, y)],
            k, width=width, seed=seed)
    else:
        ink(c, [("m", -w, y), ("l", w, y)], k, width=width, seed=seed)


def teeth(c, k, y=0.04, w=0.10, h=0.06, n=4, seed=1):
    ink(c, [("m", -w, y), ("l", w, y)], k, width=0.026, seed=seed)
    for i in range(n):
        x = -w + (2 * w) * (i + 0.5) / n
        ink(c, [("m", x, y), ("l", x, y - h)], k, width=0.022, seed=seed + i, amp=0.004)


def horn(c, k, sx, base=(0.20, 0.22), tip=(0.62, 0.56), thick=0.20, seed=1, fill=None):
    """One swept horn, base on the head, tapering to a point."""
    bx, by = base
    tx, ty = tip
    mx, my = (bx + tx) / 2, (by + ty) / 2
    ink(c, [("m", sx * bx * 0.35, by + 0.05),
            ("c", sx * mx * 0.9, my + 0.12, sx * tx * 0.86, ty - 0.04, sx * tx, ty),
            ("c", sx * mx * 1.02, my - 0.06, sx * bx * 1.05, by - thick * 0.6, sx * bx, by - thick),
            ("z",)], k, seed=seed, fill=fill)
