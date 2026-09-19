"""Print-geometry checks: a mis-sized card only shows up after printing."""
from __future__ import annotations

from reportlab.lib.units import mm

from deck.card import PIP_LAYOUTS
from deck.config import (CARD_H, CARD_W, COLS, PAGE_H, PAGE_W, RANKS, ROWS,
                         PIP_BOT, PIP_HALF_SPAN, PIP_SIZE, PIP_TOP, SAFE)


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
