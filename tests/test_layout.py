"""Print-geometry checks: a mis-sized card only shows up after printing."""
from __future__ import annotations

from reportlab.lib.units import mm

from deck.card import PIP_LAYOUTS
from deck.characters import CHARACTERS
from deck.config import (CARD_H, CARD_W, CHAR_CY, CHAR_SIZE, COLS, PAGE_H,
                         PAGE_W, RANKS, ROWS, PIP_BOT, PIP_HALF_SPAN, PIP_SIZE,
                         PIP_TOP, SAFE)
from deck.themes import SUIT_ORDER


def test_card_is_standard_poker_size():
    assert round(CARD_W / mm, 2) == 63.50
    assert round(CARD_H / mm, 2) == 88.90


def test_every_rank_has_matching_pip_count():
    assert set(PIP_LAYOUTS) == set(RANKS)
    for rank, pips in PIP_LAYOUTS.items():
        assert len(pips) == int(rank), f"{rank} has {len(pips)} pips"


def test_pip_layout_is_180_degree_symmetric():
    """Rotating a card must map its pip set onto itself.

    The 7 is the one standard exception: its odd seventh pip sits in the upper
    half, between the top and middle rows, exactly as on a real deck.
    """
    for rank, pips in PIP_LAYOUTS.items():
        rotated = sorted((round(-col, 6), round(1.0 - frac, 6)) for col, frac in pips)
        same = sorted((round(col, 6), round(frac, 6)) for col, frac in pips)
        if rank == "7":
            assert rotated != same
            assert (0.0, 0.25) in same and (0.0, 0.75) not in same
        else:
            assert rotated == same, rank


def test_grid_fits_on_a4_with_room_for_crop_marks():
    assert COLS * CARD_W <= PAGE_W
    assert ROWS * CARD_H <= PAGE_H
    assert (PAGE_W - COLS * CARD_W) / 2 >= 6 * mm     # side margin
    assert (PAGE_H - ROWS * CARD_H) / 2 >= 10 * mm    # top/bottom margin


def test_pips_stay_inside_the_safe_area():
    half = PIP_SIZE / 2
    assert CARD_W / 2 - PIP_HALF_SPAN - half >= SAFE
    assert PIP_BOT - half >= SAFE
    assert PIP_TOP + half <= CARD_H - SAFE


def test_every_card_has_its_own_character():
    for suit in SUIT_ORDER:
        assert set(CHARACTERS[suit]) == set(RANKS), suit
    names = [n for suit in CHARACTERS.values() for n, _ in suit.values()]
    assert len(names) == 36
    assert len(set(names)) == 36, "character names must be unique"


def test_character_band_is_clear_of_pips_and_trim():
    """Checked against the default pip field, which the mascot suits use.

    Dota overrides the field on its theme because it carries no character.
    """
    top = CHAR_CY + CHAR_SIZE / 2
    bottom = CHAR_CY - CHAR_SIZE / 2
    assert bottom >= SAFE, "character would sit in the cutting margin"
    assert top <= PIP_BOT - PIP_SIZE / 2, "character would collide with the bottom pip row"
