"""Cards built from loose artwork rather than a finished card image.

Two of the supplied frames are not cards: the scepters carry no rank or suit at
all, and the orb card was drawn landscape with a small unstyled index in the
wrong suit. Both keep their artwork untouched - it is only placed on a properly
proportioned card, and the rank and suit are drawn over it in the deck's own
style: a large Grenze Gotisch numeral and the Dota logo standing in for the
suit, matching every other card.
"""
from __future__ import annotations

import os
from functools import lru_cache

import numpy as np
from PIL import Image
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics

from .config import (CARD_H, CARD_W, INDEX_RANK_BASE, INDEX_RANK_SIZE,
                     INDEX_SUIT_SIZE, INDEX_SUIT_Y, hx, state)
from .imagecards import SRC_DIR

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "marks", "dota-logo.jpg")

RED = hx("#d6332b")
INDEX_X = 9.0 * mm
MAX_INDEX_W = 9.8 * mm

#: rank -> where its artwork lives, how much of it to use and how to sit it
#: on the card. ``crop`` drops the original corner indices where there were any.
LAYOUT = {
    "2": {
        "src": "02.png",
        "crop": (392, 73, 1019, 680),      # the scepters, clear of the margin
        "bg": "#f6f6f6",
        "art_width": 0.88,                 # fraction of the card width
        "art_cy": 0.46,                    # fraction of the card height
    },
    "3": {
        "src": "03.png",
        "crop": (145, 0, 1065, 880),       # drops the small spade indices
        "bg": "#000000",
        "art_width": 1.00,
        "art_cy": 0.50,
    },
}


@lru_cache(maxsize=8)
def logo_on(bg):
    """The supplied Dota logo, flattened onto a background colour.

    The file is red on white, so the white is turned back into coverage and
    the mark is recomposed over the card's own colour - its counters then read
    as the card showing through, the way the logo is meant to sit on a dark or
    a light field. Recomposing beats an alpha channel here because the source
    is a JPEG and its edges are already blended against white.
    """
    src = Image.open(LOGO_PATH).convert("RGB")
    a = np.asarray(src).astype(float)

    ink = np.array([240.0, 58.0, 45.0])            # the logo's red
    cover = np.clip((255.0 - a[:, :, 1]) / (255.0 - ink[1]), 0.0, 1.0)

    box = Image.fromarray((cover * 255).astype(np.uint8)).getbbox()
    cover = cover[box[1]:box[3], box[0]:box[2]]

    back = np.array([bg.red * 255.0, bg.green * 255.0, bg.blue * 255.0])
    out = ink * cover[..., None] + back * (1.0 - cover[..., None])
    return Image.fromarray(out.astype(np.uint8))


def artwork(rank):
    spec = LAYOUT[rank]
    im = Image.open(os.path.join(SRC_DIR, spec["src"])).convert("RGB")
    return im.crop(spec["crop"])


def _draw_index(c, rank, light):
    """Rank over the suit mark, in the top-left corner of the card."""
    size = INDEX_RANK_SIZE
    width = pdfmetrics.stringWidth(rank, "Grenze", size)
    if width > MAX_INDEX_W:
        size *= MAX_INDEX_W / width
    with state(c):
        c.setFont("Grenze", size)
        c.setFillColor(RED)
        c.drawCentredString(INDEX_X, INDEX_RANK_BASE, rank)
    mark = logo_on(light)
    w = INDEX_SUIT_SIZE
    h = w * mark.size[1] / mark.size[0]
    c.drawImage(ImageReader(mark), INDEX_X - w / 2, INDEX_SUIT_Y - h / 2, w, h)


def draw(c, rank):
    """Draw one composed card with its lower-left corner at the origin."""
    spec = LAYOUT[rank]
    bg = hx(spec["bg"])

    with state(c):
        c.setFillColor(bg)
        c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)

    art = artwork(rank)
    w = CARD_W * spec["art_width"]
    h = w * art.size[1] / art.size[0]
    c.drawImage(ImageReader(art), (CARD_W - w) / 2,
                CARD_H * spec["art_cy"] - h / 2, w, h)

    for flip in (False, True):
        with state(c):
            if flip:
                c.translate(CARD_W, CARD_H)
                c.rotate(180)
            _draw_index(c, rank, bg)
