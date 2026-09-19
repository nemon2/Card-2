"""Geometry, colour helpers and font registration for the deck."""
from __future__ import annotations

import os
from contextlib import contextmanager

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")

# --- Card geometry: standard poker size, same as a Bicycle deck ------------
CARD_W_MM, CARD_H_MM = 63.5, 88.9          # 2.5 x 3.5 inch
CARD_W, CARD_H = CARD_W_MM * mm, CARD_H_MM * mm

PAGE_W, PAGE_H = A4                         # 210 x 297 mm
COLS, ROWS = 3, 3                           # 9 cards per sheet, 1 suit per sheet

RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10")

# Nothing meaningful is drawn inside this band, so a 1-1.5 mm cutting error
# never clips artwork.
SAFE = 4.0 * mm
FRAME_INSET = 3.2 * mm
FRAME_R = 2.6 * mm

# --- Pip field -------------------------------------------------------------
PIP_TOP = CARD_H - 26.0 * mm                # centre of the top pip row
PIP_BOT = 26.0 * mm                         # centre of the bottom pip row
PIP_HALF_SPAN = 14.0 * mm                   # left/right column offset
PIP_SIZE = 9.0 * mm                        # icon bounding box

# Easter-egg character, sitting in the clear band below the bottom pip row.
CHAR_CY = 12.3 * mm
CHAR_SIZE = 15.5 * mm

# --- Corner index ----------------------------------------------------------
INDEX_X = 6.9 * mm                          # centre line of the index column
INDEX_RANK_TOP = CARD_H - 6.2 * mm          # top of the rank glyph
INDEX_RANK_SIZE = 20.5                      # points
INDEX_SUIT_SIZE = 5.0 * mm
INDEX_SUIT_Y = CARD_H - 18.2 * mm

# Game wordmark, centred just inside the top of the frame.
LABEL_BASE = CARD_H - 7.8 * mm

TRIM_LINE = 0.25            # pt - faint cut guide printed on the trim edge

_FONT_FILES = {
    "Cinzel": "Cinzel-Bold.ttf",
    "CinzelDeco": "CinzelDecorative-Bold.ttf",
    "Lilita": "LilitaOne.ttf",
    "Oswald": "Oswald-Bold.ttf",
    "Saira": "SairaCondensed-ExtraBold.ttf",
    "Russo": "RussoOne.ttf",
    "Marcellus": "MarcellusSC.ttf",
    "Bebas": "BebasNeue.ttf",
}

_registered = False


def register_fonts() -> None:
    """Register the bundled display faces with reportlab (idempotent)."""
    global _registered
    if _registered:
        return
    for name, filename in _FONT_FILES.items():
        path = os.path.join(FONT_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"missing font {path}")
        pdfmetrics.registerFont(TTFont(name, path))
    _registered = True


# --- Colour helpers --------------------------------------------------------
def hx(value: str) -> Color:
    """Hex string -> reportlab Color."""
    return HexColor(value)


@contextmanager
def state(c):
    """Save/restore the canvas graphics state around a block."""
    c.saveState()
    try:
        yield c
    finally:
        c.restoreState()


def path(c, *cmds):
    """Tiny path DSL: ('m',x,y) ('l',x,y) ('c',x1,y1,x2,y2,x3,y3) ('z',)."""
    p = c.beginPath()
    for cmd in cmds:
        op, args = cmd[0], cmd[1:]
        if op == "m":
            p.moveTo(*args)
        elif op == "l":
            p.lineTo(*args)
        elif op == "c":
            p.curveTo(*args)
        elif op == "z":
            p.close()
        else:  # pragma: no cover - programming error
            raise ValueError(f"unknown path op {op!r}")
    return p


def rounded_rect_path(c, x, y, w, h, r):
    """Rounded rectangle as a path object (reportlab has no path-level helper)."""
    k = r * 0.5523
    return path(
        c,
        ("m", x + r, y),
        ("l", x + w - r, y),
        ("c", x + w - r + k, y, x + w, y + r - k, x + w, y + r),
        ("l", x + w, y + h - r),
        ("c", x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h),
        ("l", x + r, y + h),
        ("c", x + r - k, y + h, x, y + h - r + k, x, y + h - r),
        ("l", x, y + r),
        ("c", x, y + r - k, x + r - k, y, x + r, y),
        ("z",),
    )
