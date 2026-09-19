#!/usr/bin/env python3
"""Build the printable A4 sheets for the game-themed deck."""
from __future__ import annotations

import argparse
import os

from reportlab.lib.units import mm

from deck.config import RANKS
from deck.sheet import build, build_images, build_singles
from deck.themes import SUIT_ORDER

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--out", default=os.path.join(ROOT, "out", "game-cards-a4.pdf"))
    ap.add_argument("--gap", type=float, default=0.0,
                    help="gap between cards in mm (default 0: shared cut lines)")
    ap.add_argument("--no-marks", action="store_true", help="omit crop marks and caption")
    ap.add_argument("--vector", action="store_true",
                    help="build the drawn deck instead of the supplied artwork")
    ap.add_argument("--singles", action="store_true",
                    help="one card per page at card size instead of A4 sheets")
    ap.add_argument("--suits", nargs="*", default=list(SUIT_ORDER))
    ap.add_argument("--ranks", nargs="*", default=list(RANKS))
    args = ap.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    if args.singles:
        path = build_singles(args.out, suits_=args.suits, ranks=args.ranks)
    elif args.vector:
        path = build(args.out, gap=args.gap * mm, marks=not args.no_marks,
                     suits_=args.suits, ranks=args.ranks)
    else:
        path = build_images(args.out, gap=args.gap * mm,
                            marks=not args.no_marks, ranks=args.ranks)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
