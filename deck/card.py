"""Renders a single card: frame, pips, corner indices, wordmark, character."""
from __future__ import annotations

from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics

from . import suits
from .characters import draw_character
from .config import (CARD_H, CARD_W, CHAR_CY, CHAR_SIZE, FRAME_INSET, FRAME_R,
                     INDEX_RANK_SIZE, INDEX_RANK_TOP, INDEX_SUIT_SIZE,
                     INDEX_SUIT_Y, LABEL_BASE, PIP_BOT, PIP_HALF_SPAN,
                     PIP_SIZE, PIP_TOP, TRIM_LINE, rounded_rect_path, state)
from .themes import PAPER, TRIM

L, C, R = -1.0, 0.0, 1.0

#: Standard poker pip layout. Each entry is (column, fraction-from-top-row);
#: a pip whose fraction is below the midline is rotated 180 degrees.
PIP_LAYOUTS = {
    "2": [(C, 0.0), (C, 1.0)],
    "3": [(C, 0.0), (C, 0.5), (C, 1.0)],
    "4": [(L, 0.0), (R, 0.0), (L, 1.0), (R, 1.0)],
    "5": [(L, 0.0), (R, 0.0), (C, 0.5), (L, 1.0), (R, 1.0)],
    "6": [(L, 0.0), (R, 0.0), (L, 0.5), (R, 0.5), (L, 1.0), (R, 1.0)],
    "7": [(L, 0.0), (R, 0.0), (C, 0.25), (L, 0.5), (R, 0.5), (L, 1.0), (R, 1.0)],
    "8": [(L, 0.0), (R, 0.0), (C, 0.25), (L, 0.5), (R, 0.5), (C, 0.75),
          (L, 1.0), (R, 1.0)],
    "9": [(L, 0.0), (R, 0.0), (L, 1 / 3), (R, 1 / 3), (C, 0.5),
          (L, 2 / 3), (R, 2 / 3), (L, 1.0), (R, 1.0)],
    "10": [(L, 0.0), (R, 0.0), (C, 1 / 6), (L, 1 / 3), (R, 1 / 3),
           (L, 2 / 3), (R, 2 / 3), (C, 5 / 6), (L, 1.0), (R, 1.0)],
}

MAX_INDEX_W = 9.8 * mm


def _tracked_centred(c, text, font, size, cx, y, tracking):
    """drawCentredString that accounts for letter spacing."""
    width = pdfmetrics.stringWidth(text, font, size) + tracking * (len(text) - 1)
    t = c.beginText(cx - width / 2, y)
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.textOut(text)
    c.drawText(t)


def _draw_index(c, theme, rank):
    """Rank + suit glyph in the top-left corner (origin at card lower-left)."""
    size = INDEX_RANK_SIZE * theme.rank_scale
    width = pdfmetrics.stringWidth(rank, theme.rank_font, size)
    if width > MAX_INDEX_W:
        size *= MAX_INDEX_W / width
    baseline = INDEX_RANK_TOP - pdfmetrics.getAscent(theme.rank_font, size)

    with state(c):
        c.setFont(theme.rank_font, size)
        c.setFillColor(theme.index)
        c.drawCentredString(theme.index_x, baseline, rank)
    with state(c):
        c.translate(theme.index_x, INDEX_SUIT_Y)
        suits.draw_suit(c, theme.suit, INDEX_SUIT_SIZE, theme.suit_color)


def _draw_pips(c, theme, rank):
    span = PIP_TOP - PIP_BOT
    for col, frac in PIP_LAYOUTS[rank]:
        x = CARD_W / 2 + col * PIP_HALF_SPAN
        y = PIP_TOP - frac * span
        with state(c):
            c.translate(x, y)
            if frac > 0.5:
                c.rotate(180)
            theme.draw_pip(c, PIP_SIZE * theme.pip_scale)


def _draw_frame(c, theme):
    i = FRAME_INSET
    with state(c):
        # faint cut guide printed on the trim edge itself
        c.setStrokeColor(TRIM)
        c.setLineWidth(TRIM_LINE)
        c.rect(0, 0, CARD_W, CARD_H, fill=0, stroke=1)

        c.setStrokeColor(theme.frame)
        c.setStrokeAlpha(0.85)
        c.setLineWidth(0.8)
        c.drawPath(
            rounded_rect_path(c, i, i, CARD_W - 2 * i, CARD_H - 2 * i, FRAME_R),
            fill=0, stroke=1,
        )


def draw_card(c, theme, rank):
    """Draw one card with its lower-left corner at the current origin."""
    with state(c):
        c.setFillColor(PAPER)
        c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)

    _draw_frame(c, theme)
    _draw_pips(c, theme, rank)

    for flip in (False, True):
        with state(c):
            if flip:
                c.translate(CARD_W, CARD_H)
                c.rotate(180)
            _draw_index(c, theme, rank)

    with state(c):
        c.setFillColor(theme.frame)
        _tracked_centred(c, theme.game, theme.label_font, theme.label_size,
                         CARD_W / 2, LABEL_BASE, theme.label_tracking)

    with state(c):
        c.translate(CARD_W / 2, CHAR_CY)
        draw_character(c, theme.suit, rank, CHAR_SIZE, theme.ink, theme.frame, PAPER)
