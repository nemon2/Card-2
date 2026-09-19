"""Cards assembled from the supplied artwork with the deck's own index.

Every card keeps its artwork untouched. What changes is the corner index: the
originals are small, unstyled and in assorted suits, so they are patched out
with the colour around them and redrawn in one style - a large Grenze Gotisch
numeral over the supplied Dota logo standing in for the suit.

Two frames were never cards at all. The scepters carry no rank or suit, and the
orbs were drawn landscape; both use their raw artwork placed on a card of the
right proportions.
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
from .imagecards import SRC_DIR, _face_colour, prepare

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "marks", "dota-logo.jpg")

RED = hx("#d6332b")
INDEX_X = 9.0 * mm
MAX_INDEX_W = 9.8 * mm

#: Boxes are fractions of the card, measured from the top-left, and are
#: mirrored through the centre unless the card lists all of its corners.
LAYOUT = {
    "2": {"raw": (392, 73, 1019, 680), "bg": "#f6f6f6",
          "art_width": 0.88, "art_cy": 0.46},
    "3": {"raw": (145, 0, 1065, 880), "bg": "#000000",
          "art_width": 1.00, "art_cy": 0.50},
    "4": {"patches": [(0.00, 0.05, 0.13, 0.31)], "art_width": 0.76},
    "5": {"patches": [(0.03, 0.01, 0.17, 0.25)], "art_width": 1.00},
    # the 6 sits in a gold frame, so its lower box is placed by hand rather
    # than mirrored - the mirror would have run into the frame and the orb
    # The 6 sits on a nebula, where any patch shows, so its lower box is kept
    # to the footprint of the new index that covers it.
    "6": {"patches": [(0.03, 0.00, 0.23, 0.33)],
          "clone": [((0.778, 0.772, 0.938, 0.988), -0.235, 0.0)],
          "mirror": False, "art_width": 1.00},
    # the 7 carries an index in all four corners and sits on a decorative
    # stack of cards, so each box is placed tightly by hand
    "7": {"patches": [(0.040, 0.085, 0.122, 0.250),
                      (0.796, 0.080, 0.876, 0.245),
                      (0.038, 0.785, 0.112, 0.960),
                      (0.860, 0.770, 0.965, 0.968)],
          "mirror": False, "art_width": 1.00},
    "8": {"patches": [(0.03, 0.03, 0.23, 0.35)], "art_width": 1.00},
    "9": {"patches": [(0.01, 0.03, 0.19, 0.29)], "art_width": 1.00},
    "10": {"patches": [(0.01, 0.01, 0.19, 0.31)], "art_width": 1.00},
}


@lru_cache(maxsize=8)
def logo_on(bg):
    """The supplied Dota logo, flattened onto a background colour.

    The file is red on white, so the white is turned back into coverage and the
    mark recomposed over the card's own colour - its counters then read as the
    card showing through, the way the logo sits on a dark or a light field.
    Recomposing beats an alpha channel because the source is a JPEG whose edges
    are already blended against white.
    """
    a = np.asarray(Image.open(LOGO_PATH).convert("RGB")).astype(float)
    ink = np.array([240.0, 58.0, 45.0])
    cover = np.clip((255.0 - a[:, :, 1]) / (255.0 - ink[1]), 0.0, 1.0)
    box = Image.fromarray((cover * 255).astype(np.uint8)).getbbox()
    cover = cover[box[1]:box[3], box[0]:box[2]]
    back = np.array([bg.red * 255.0, bg.green * 255.0, bg.blue * 255.0])
    return Image.fromarray(
        (ink * cover[..., None] + back * (1.0 - cover[..., None])).astype(np.uint8))


def _fill_patch(a, box, face=None):
    """Blank one index box.

    With ``face`` the box is painted flat in the card's own colour, which is
    invisible on the cards whose face is plain. Without it the box is
    interpolated inwards from the pixels just outside, which is what the 6
    needs because its background is a gradient - but interpolation drags
    neighbouring colour sideways, so it is wrong wherever an index sits next to
    something strongly coloured.
    """
    h, w = a.shape[:2]
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    x0, y0 = max(1, x0), max(1, y0)
    x1, y1 = min(w - 1, x1), min(h - 1, y1)
    bw, bh = x1 - x0, y1 - y0
    if bw <= 0 or bh <= 0:
        return
    if face is not None:
        a[y0:y1, x0:x1] = np.asarray(face, dtype=a.dtype)
        return

    top = a[y0 - 1, x0:x1].astype(float)          # (bw, 3)
    bottom = a[y1, x0:x1].astype(float)
    left = a[y0:y1, x0 - 1].astype(float)         # (bh, 3)
    right = a[y0:y1, x1].astype(float)

    fy = (np.arange(bh) + 0.5)[:, None, None] / bh
    fx = (np.arange(bw) + 0.5)[None, :, None] / bw
    vertical = top[None, :, :] * (1 - fy) + bottom[None, :, :] * fy
    horizontal = left[:, None, :] * (1 - fx) + right[:, None, :] * fx
    fill = (vertical + horizontal) / 2.0

    # Feather the rim: a hard-edged rectangle of flat colour is obvious against
    # a textured background even when its colour is right.
    mx = max(1, int(bw * 0.18))
    my = max(1, int(bh * 0.18))
    ramp_x = np.minimum(np.minimum(np.arange(bw), np.arange(bw)[::-1]) / mx, 1.0)
    ramp_y = np.minimum(np.minimum(np.arange(bh), np.arange(bh)[::-1]) / my, 1.0)
    alpha = (ramp_y[:, None] * ramp_x[None, :])[..., None]
    old = a[y0:y1, x0:x1].astype(float)
    a[y0:y1, x0:x1] = (fill * alpha + old * (1 - alpha)).astype(a.dtype)


def _clone_patch(a, box, dx, dy):
    """Cover a box with a same-sized piece of artwork from ``dx, dy`` away.

    On a painted background - a nebula, a gradient - no synthetic fill matches,
    but a clean neighbouring piece of the same painting does.
    """
    h, w = a.shape[:2]
    x0, y0, x1, y1 = (int(round(v)) for v in
                      (box[0] * w, box[1] * h, box[2] * w, box[3] * h))
    sx, sy = int(round(dx * w)), int(round(dy * h))
    bw, bh = x1 - x0, y1 - y0
    src = a[y0 + sy:y0 + sy + bh, x0 + sx:x0 + sx + bw]
    if src.shape[:2] != (bh, bw):
        return
    mx, my = max(1, int(bw * 0.16)), max(1, int(bh * 0.16))
    rx = np.minimum(np.minimum(np.arange(bw), np.arange(bw)[::-1]) / mx, 1.0)
    ry = np.minimum(np.minimum(np.arange(bh), np.arange(bh)[::-1]) / my, 1.0)
    alpha = (ry[:, None] * rx[None, :])[..., None]
    a[y0:y1, x0:x1] = (src.astype(float) * alpha
                       + a[y0:y1, x0:x1].astype(float) * (1 - alpha)).astype(a.dtype)


@lru_cache(maxsize=16)
def artwork(rank):
    """The card's artwork with its original indices removed."""
    spec = LAYOUT[rank]
    if "raw" in spec:
        src = [f for f in os.listdir(SRC_DIR) if f.startswith(rank.zfill(2))][0]
        return Image.open(os.path.join(SRC_DIR, src)).convert("RGB").crop(spec["raw"])

    im = prepare(os.path.join(SRC_DIR, f"{rank.zfill(2)}.png"))
    a = np.asarray(im).astype(np.int16).copy()
    h, w = a.shape[:2]
    boxes = list(spec["patches"])
    if spec.get("mirror", True):
        boxes += [(1 - x1, 1 - y1, 1 - x0, 1 - y0)
                  for x0, y0, x1, y1 in spec["patches"]]
    face = None if spec.get("patch_fill") == "blend" else _face_colour(a)
    for x0, y0, x1, y1 in boxes:
        _fill_patch(a, (x0 * w, y0 * h, x1 * w, y1 * h), face)
    for box, dx, dy in spec.get("clone", ()):
        _clone_patch(a, box, dx, dy)
    return Image.fromarray(a.astype(np.uint8))


def background(rank):
    spec = LAYOUT[rank]
    if "bg" in spec:
        return hx(spec["bg"])
    r, g, b = _face_colour(np.asarray(artwork(rank)).astype(np.int16))
    return hx("#%02x%02x%02x" % (r, g, b))


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
    bg = background(rank)

    with state(c):
        c.setFillColor(bg)
        c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)

    art = artwork(rank)
    w = CARD_W * spec["art_width"]
    h = w * art.size[1] / art.size[0]
    c.drawImage(ImageReader(art), (CARD_W - w) / 2,
                CARD_H * spec.get("art_cy", 0.5) - h / 2, w, h)

    for flip in (False, True):
        with state(c):
            if flip:
                c.translate(CARD_W, CARD_H)
                c.rotate(180)
            _draw_index(c, rank, bg)
