"""A4 imposition: one suit per sheet, 3x3 cards, with crop marks."""
from __future__ import annotations

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .card import draw_card
from . import composed
from .imagecards import load_all
from .config import (CARD_H, CARD_W, COLS, PAGE_H, PAGE_W, RANKS, ROWS,
                     register_fonts, state)
from .themes import SUIT_ORDER, THEMES

MARK_LEN = 4.0 * mm
MARK_OFF = 1.6 * mm


def _grid_origin(gap):
    block_w = COLS * CARD_W + (COLS - 1) * gap
    block_h = ROWS * CARD_H + (ROWS - 1) * gap
    return (PAGE_W - block_w) / 2, (PAGE_H - block_h) / 2, block_w, block_h


def _crop_marks(c, gap):
    ox, oy, bw, bh = _grid_origin(gap)
    with state(c):
        c.setStrokeColorRGB(0.45, 0.45, 0.45)
        c.setLineWidth(0.3)
        xs = [ox + i * (CARD_W + gap) for i in range(COLS)] + \
             [ox + (COLS - 1) * (CARD_W + gap) + CARD_W]
        ys = [oy + i * (CARD_H + gap) for i in range(ROWS)] + \
             [oy + (ROWS - 1) * (CARD_H + gap) + CARD_H]
        for x in xs:
            c.line(x, oy - MARK_OFF, x, oy - MARK_OFF - MARK_LEN)
            c.line(x, oy + bh + MARK_OFF, x, oy + bh + MARK_OFF + MARK_LEN)
        for y in ys:
            c.line(ox - MARK_OFF, y, ox - MARK_OFF - MARK_LEN, y)
            c.line(ox + bw + MARK_OFF, y, ox + bw + MARK_OFF + MARK_LEN, y)


def _caption(c, gap, text):
    ox, oy, _, _ = _grid_origin(gap)
    with state(c):
        c.setFillColorRGB(0.42, 0.42, 0.42)
        c.setFont("Helvetica", 5.6)
        c.drawString(ox, oy - 9.0 * mm, text)


def _trim_line(c, x, y):
    with state(c):
        c.setStrokeColorRGB(0.78, 0.78, 0.78)
        c.setLineWidth(0.25)
        c.rect(x, y, CARD_W, CARD_H, fill=0, stroke=1)


def build_images(out_path, gap=0.0, marks=True, ranks=None):
    """Lay the supplied card artwork onto A4 at exact card size.

    The images go down as they are: fitted to the card slot, never stretched
    and never cropped.
    """
    register_fonts()
    cards = load_all()
    order = [r for r in (ranks or RANKS)
             if r in cards or r in composed.LAYOUT]
    del cards

    c = canvas.Canvas(out_path, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Dota 2 playing cards")
    c.setSubject("Print-and-play card sheets, poker size")

    ox, oy, _, _ = _grid_origin(gap)
    per_page = COLS * ROWS
    for start in range(0, len(order), per_page):
        chunk = order[start:start + per_page]
        for idx, rank in enumerate(chunk):
            row, col = divmod(idx, COLS)
            x = ox + col * (CARD_W + gap)
            y = oy + (ROWS - 1 - row) * (CARD_H + gap)
            with state(c):
                c.translate(x, y)
                composed.draw(c, rank)
            _trim_line(c, x, y)
        if marks:
            _crop_marks(c, gap)
            _caption(c, gap,
                     "Dota 2  -  " + ", ".join(chunk) +
                     "   card 63.5 x 88.9 mm (poker / Bicycle)"
                     "   print at 100%, no scaling")
        c.showPage()
    c.save()
    return out_path


def build_singles(out_path, suits_=SUIT_ORDER, ranks=RANKS):
    """One card per page at exact card size - handy for proofing or reprints."""
    register_fonts()
    c = canvas.Canvas(out_path, pagesize=(CARD_W, CARD_H))
    c.setTitle("Game-themed playing cards - single cards")
    for suit in suits_:
        theme = THEMES[suit]
        for rank in ranks:
            draw_card(c, theme, rank)
            c.showPage()
    c.save()
    return out_path


def build(out_path, gap=0.0, marks=True, suits_=SUIT_ORDER, ranks=RANKS):
    """Write the full A4 print sheet PDF."""
    register_fonts()
    c = canvas.Canvas(out_path, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Game-themed playing cards - suits 2 to 10")
    c.setAuthor("")
    c.setSubject("Print-and-play card sheets, poker size")

    ox, oy, _, _ = _grid_origin(gap)
    for suit in suits_:
        theme = THEMES[suit]
        for idx, rank in enumerate(ranks):
            row, col = divmod(idx, COLS)
            x = ox + col * (CARD_W + gap)
            y = oy + (ROWS - 1 - row) * (CARD_H + gap)
            with state(c):
                c.translate(x, y)
                draw_card(c, theme, rank)
        if marks:
            _crop_marks(c, gap)
            _caption(c, gap,
                     f"{theme.game.title()}  -  {theme.suit}  2-10   "
                     f"card 63.5 x 88.9 mm (poker / Bicycle)   "
                     f"print at 100%, no scaling")
        c.showPage()
    c.save()
    return out_path
