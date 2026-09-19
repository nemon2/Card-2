"""Checks on the supplied artwork: a stretched or low-res card only shows up
after it has been printed."""
from __future__ import annotations

import os

from reportlab.lib.units import mm

from deck.config import CARD_W
from deck.imagecards import CARD_AR, SRC_DIR, load_all

MIN_DPI = 250


def test_source_artwork_is_present():
    files = [f for f in os.listdir(SRC_DIR) if f.lower().endswith(".png")]
    assert files, "no source card artwork in assets/cards/src"


def test_every_card_matches_the_card_shape():
    for rank, im in load_all().items():
        w, h = im.size
        assert abs(w / h - CARD_AR) < 0.005, f"{rank} is {w}x{h}, not card-shaped"


def test_every_card_has_enough_resolution_to_print():
    inches = CARD_W / mm / 25.4
    for rank, im in load_all().items():
        dpi = im.size[0] / inches
        assert dpi >= MIN_DPI, f"{rank} would print at {dpi:.0f} dpi"
