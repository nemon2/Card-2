"""Hand-drawn ink styling for the character easter eggs.

Paths are authored in a unit box (roughly -0.5..0.5) and every coordinate is
nudged by a small deterministic amount before drawing, so the strokes read as
pen lines rather than perfect vector curves. The nudge is a pure function of
the seed, so every build produces an identical PDF.
"""
from __future__ import annotations

from .config import path, state

LW = 0.052          # default stroke weight, in unit-box terms
AMP = 0.011         # default wobble amplitude


def _noise(seed, i):
    """Deterministic pseudo-random value in [-1, 1]."""
    x = (seed * 374761393 + i * 668265263) & 0xFFFFFFFF
    x = ((x ^ (x >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((x ^ (x >> 16)) & 0xFFFF) / 32767.5 - 1.0


def wobble(cmds, amp, seed):
    out, k = [], 0
    for cmd in cmds:
        op, args = cmd[0], list(cmd[1:])
        for j in range(len(args)):
            args[j] += _noise(seed, k) * amp
            k += 1
        out.append(tuple([op] + args))
    return out


def ink(c, cmds, color, width=LW, seed=1, amp=AMP, fill=None, close=False):
    """Draw one wobbled pen stroke, optionally filled."""
    cmds = list(cmds) + ([("z",)] if close else [])
    with state(c):
        c.setLineCap(1)
        c.setLineJoin(1)
        c.setLineWidth(width)
        c.setStrokeColor(color)
        p = path(c, *wobble(cmds, amp, seed))
        if fill is not None:
            c.setFillColor(fill)
            c.drawPath(p, fill=1, stroke=1)
        else:
            c.drawPath(p, fill=0, stroke=1)


def blob(c, cx, cy, r, color, seed=1, squash=1.0):
    """Small filled dot - eyes, rivets, beads."""
    with state(c):
        c.translate(cx, cy)
        c.scale(1.0, squash)
        c.setFillColor(color)
        c.circle(0, 0, r, fill=1, stroke=0)


def oval(c, cx, cy, rx, ry, color, seed=1, width=LW, fill=None, rot=0.0):
    """Wobbled ellipse outline."""
    k = 0.5523
    cmds = [("m", cx, cy + ry),
            ("c", cx + rx * k, cy + ry, cx + rx, cy + ry * k, cx + rx, cy),
            ("c", cx + rx, cy - ry * k, cx + rx * k, cy - ry, cx, cy - ry),
            ("c", cx - rx * k, cy - ry, cx - rx, cy - ry * k, cx - rx, cy),
            ("c", cx - rx, cy + ry * k, cx - rx * k, cy + ry, cx, cy + ry),
            ("z",)]
    if rot:
        with state(c):
            c.translate(cx, cy)
            c.rotate(rot)
            c.translate(-cx, -cy)
            ink(c, cmds, color, width=width, seed=seed, fill=fill)
    else:
        ink(c, cmds, color, width=width, seed=seed, fill=fill)
