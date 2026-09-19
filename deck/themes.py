"""Per-suit themes.

The cards are plain white - no background art. A suit's identity comes from
its pip mark, its frame colour and its hand-drawn character.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from reportlab.lib.colors import Color
from reportlab.lib.units import mm

from . import icons
from .config import hx

PAPER = hx("#ffffff")
TRIM = hx("#c8c8c8")


@dataclass
class Theme:
    key: str
    suit: str
    game: str
    rank_font: str
    label_font: str
    ink: Color                 # character line colour
    index: Color               # rank glyph
    suit_color: Color          # corner suit symbol
    frame: Color
    draw_pip: Callable
    label_size: float = 5.4
    label_tracking: float = 1.4
    rank_scale: float = 1.0
    index_x: float = 6.9 * mm
    pip_scale: float = 1.0


# --- Hollow Knight ----------------------------------------------------------
HK_INK = hx("#1b2733")
HK_FRAME = hx("#33495f")

# --- Clash Royale -----------------------------------------------------------
CR_INK = hx("#17365c")
CR_GOLD = hx("#f0b32e")
CR_GOLD_D = hx("#6d4207")
CR_GOLD_L = hx("#ffeaa8")
CR_BLUE = hx("#2fb0e8")
CR_BLUE_D = hx("#186a96")
CR_GEM = hx("#f5c33c")

# --- Dota 2 -----------------------------------------------------------------
DT_INK = hx("#7a1518")
DT_RED = hx("#a81f1f")
DT_GOLD = hx("#d2a03c")
DT_GOLD_D = hx("#66380f")
DT_GOLD_L = hx("#ffe9a8")
DT_DARK = hx("#a52424")
DT_EMBER = hx("#d9822c")

# --- Apex Legends -----------------------------------------------------------
AP_INK = hx("#8c2a14")
AP_RED = hx("#cf3b1d")
AP_DARK = hx("#461105")


THEMES = {
    "spades": Theme(
        key="hollow-knight", suit="spades", game="HOLLOW KNIGHT",
        rank_font="Cinzel", label_font="Marcellus",
        ink=HK_INK, index=HK_INK, suit_color=HK_INK, frame=HK_FRAME,
        draw_pip=lambda c, s: icons.hollow_knight_mask(c, s, HK_INK, PAPER),
        label_size=5.0, label_tracking=1.6, pip_scale=0.80,
    ),
    "clubs": Theme(
        key="clash-royale", suit="clubs", game="CLASH ROYALE",
        rank_font="Lilita", label_font="Lilita",
        ink=CR_INK, index=CR_INK, suit_color=CR_INK, frame=CR_GOLD,
        draw_pip=lambda c, s: icons.clash_royale_crown(
            c, s, CR_GOLD, CR_GOLD_D, CR_GOLD_L, CR_BLUE, CR_BLUE_D, CR_GEM),
        label_size=5.2, label_tracking=0.9, rank_scale=0.96, pip_scale=1.00,
    ),
    "hearts": Theme(
        key="dota-2", suit="hearts", game="DOTA 2",
        rank_font="Cinzel", label_font="Marcellus",
        ink=DT_INK, index=DT_RED, suit_color=DT_RED, frame=DT_GOLD,
        draw_pip=lambda c, s: icons.dota_immortal(
            c, s, DT_GOLD, DT_GOLD_D, DT_DARK, DT_EMBER, DT_GOLD_L),
        label_size=5.2, label_tracking=2.0, pip_scale=0.90,
    ),
    "diamonds": Theme(
        key="apex-legends", suit="diamonds", game="APEX LEGENDS",
        rank_font="Saira", label_font="Saira",
        ink=AP_INK, index=AP_RED, suit_color=AP_RED, frame=AP_RED,
        draw_pip=lambda c, s: icons.apex_mark(c, s, AP_RED, AP_DARK, PAPER),
        label_size=5.4, label_tracking=1.6, rank_scale=1.06, pip_scale=0.88,
    ),
}

SUIT_ORDER = ("spades", "clubs", "hearts", "diamonds")
