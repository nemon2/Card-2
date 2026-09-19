"""Place the supplied card artwork on the sheet as-is.

The images arrive framed differently: some are full bleed, others sit on a grey
studio background, sometimes with a drop shadow or a decorative stack of cards
behind. Each one is trimmed back to the card face and letterboxed to the card's
aspect ratio in its own background colour. Nothing is stretched and nothing of
the card face is cropped away.
"""
from __future__ import annotations

import os
from collections import Counter

import numpy as np
from PIL import Image

from .config import CARD_H, CARD_W

SRC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "cards", "src")

CARD_AR = CARD_W / CARD_H      # 0.714
BG_TOL = 18                    # colour distance that still counts as background
RING = 0.03                    # fraction of the frame treated as border
MARGIN = 9                     # luminance a card must clear the border by


def _ring_pixels(a, frac=RING):
    """The outer border of the frame, where the studio background lives."""
    h, w, _ = a.shape
    by, bx = max(1, int(h * frac)), max(1, int(w * frac))
    return np.concatenate([
        a[:by].reshape(-1, 3), a[-by:].reshape(-1, 3),
        a[:, :bx].reshape(-1, 3), a[:, -bx:].reshape(-1, 3),
    ])


def _is_full_bleed(a):
    corners = np.array([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]], dtype=float)
    bg = np.median(corners, axis=0)
    return (np.abs(a - bg).max(axis=2) <= BG_TOL).mean() < 0.02


def _solidify(mask):
    """Span each row from its first hit to its last.

    Dark artwork inside a light card falls outside the luminance mask, which
    would otherwise leave the card looking like a holey blob rather than a
    rectangle.
    """
    out = np.zeros_like(mask)
    for j in range(mask.shape[0]):
        idx = np.nonzero(mask[j])[0]
        if idx.size:
            out[j, idx[0]:idx[-1] + 1] = True
    return out


def _face_mask(a):
    """The card face: whichever side of the border's luminance range it sits on.

    Thresholds come from percentiles of the border rather than a single sampled
    colour, so a background with a gradient in it does not leak into the mask.
    """
    lum = a.mean(axis=2)
    ring_lum = _ring_pixels(a).mean(axis=1)
    hi = np.percentile(ring_lum, 98) + MARGIN
    lo = np.percentile(ring_lum, 2) - MARGIN
    bright, dark = lum > hi, lum < lo
    return _solidify(bright if bright.sum() >= dark.sum() else dark)


def _pad_colour(im):
    """Most common colour a little inside the card edge."""
    a = np.asarray(im)
    h, w, _ = a.shape
    inset = max(2, int(min(w, h) * 0.05))
    ring = np.concatenate([
        a[inset, inset:w - inset], a[h - 1 - inset, inset:w - inset],
        a[inset:h - inset, inset], a[inset:h - inset, w - 1 - inset],
    ])
    return Counter(tuple((p // 8 * 8).tolist()) for p in ring).most_common(1)[0][0]


def _clean_edges(im, pad):
    """Repaint leftovers in the outer ring: rounded corners, background slivers."""
    a = np.asarray(im).astype(np.int16).copy()
    h, w, _ = a.shape
    bx, by = max(1, int(w * 0.03)), max(1, int(h * 0.03))
    ring = np.zeros((h, w), dtype=bool)
    ring[:by, :] = ring[-by:, :] = True
    ring[:, :bx] = ring[:, -bx:] = True
    far = np.abs(a - np.asarray(pad, dtype=np.int16)).max(axis=2) > 34
    a[ring & far] = np.asarray(pad, dtype=np.int16)
    return Image.fromarray(a.astype(np.uint8))


def prepare(path):
    """Trim one source image to the card face and letterbox it to card shape."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)

    if not _is_full_bleed(a):
        mask = _face_mask(a)
        ys, xs = np.nonzero(mask)
        im = im.crop((int(xs.min()), int(ys.min()),
                      int(xs.max()) + 1, int(ys.max()) + 1))
        im = _clean_edges(im, _pad_colour(im))

    pad = _pad_colour(im)
    w, h = im.size
    target = (w, round(w / CARD_AR)) if w / h > CARD_AR else (round(h * CARD_AR), h)
    out = Image.new("RGB", target, pad)
    out.paste(im, ((target[0] - w) // 2, (target[1] - h) // 2))
    return out


def load_all():
    """{rank: prepared image} for every source card present."""
    cards = {}
    for name in sorted(os.listdir(SRC_DIR)):
        if not name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        cards[str(int(os.path.splitext(name)[0]))] = prepare(
            os.path.join(SRC_DIR, name))
    return cards
