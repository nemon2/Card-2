"""Place the supplied card artwork on the sheet as-is.

The images arrive framed differently: some are full bleed, others sit on a grey
studio background, sometimes with a drop shadow or a decorative stack of cards
behind. Each one is trimmed back to the card face and letterboxed to the card's
aspect ratio in its own background colour. Nothing is stretched and nothing of
the card face is cropped away.
"""
from __future__ import annotations

import os

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


def _on_studio_background(a):
    """True when the card sits on a flat background rather than filling the frame.

    Measured against the corner colour: a studio shot leaves a wide margin of
    it, while a full-bleed card matches it only in the slivers outside its own
    rounded corners.
    """
    corners = np.array([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]], dtype=float)
    bg = np.median(corners, axis=0)
    return (np.abs(a - bg).max(axis=2) <= BG_TOL).mean() >= 0.02


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


def _face_colour(a):
    """The card's own background - the colour that dominates the whole face."""
    quant = (a.astype(np.int32) // 8 * 8).reshape(-1, 3)
    keys, counts = np.unique(quant, axis=0, return_counts=True)
    return tuple(int(v) for v in keys[counts.argmax()])


def _trim_to_face(im, tol=18, keep=0.5):
    """Shave edge lines that are not mostly the card's own background.

    The luminance mask can run a little past the card where the studio
    background carries a gradient; this pulls the crop back to the face.
    """
    a = np.asarray(im).astype(np.int16)
    face = np.asarray(_face_colour(a), dtype=np.int16)
    near = np.abs(a - face).max(axis=2) <= tol
    h, w = near.shape
    top, bottom, left, right = 0, h - 1, 0, w - 1
    while top < bottom and near[top, left:right + 1].mean() < keep:
        top += 1
    while bottom > top and near[bottom, left:right + 1].mean() < keep:
        bottom -= 1
    while left < right and near[top:bottom + 1, left].mean() < keep:
        left += 1
    while right > left and near[top:bottom + 1, right].mean() < keep:
        right -= 1
    return im.crop((left, top, right + 1, bottom + 1))


def _pad_colour(im):
    """The card's own background, used to extend it to the card's shape.

    Taken over the whole face rather than a ring just inside the edge: a ring
    can land on a vignette or a frame and then the added band reads as a
    different shade from the card it is extending.
    """
    return _face_colour(np.asarray(im).astype(np.int16))


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


def prepare(path, report=None):
    """Trim one source image to the card face and letterbox it to card shape."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)

    if _on_studio_background(a):
        ys, xs = np.nonzero(_face_mask(a))
        box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        # crop to the card, then pull the crop back to the face in case the
        # background carried a gradient the luminance mask ran past
        im = _trim_to_face(im.crop(box))
    pad = _pad_colour(im)
    im = _clean_edges(im, pad)

    w, h = im.size
    target = (w, round(w / CARD_AR)) if w / h > CARD_AR else (round(h * CARD_AR), h)
    out = Image.new("RGB", target, pad)
    out.paste(im, ((target[0] - w) // 2, (target[1] - h) // 2))
    if report is not None:
        grew = max(target[0] / w, target[1] / h) - 1.0
        report[os.path.basename(path)] = (w, h, w / h, grew)
    return out


def load_all(report=None):
    """{rank: prepared image} for every source card present."""
    cards = {}
    for name in sorted(os.listdir(SRC_DIR)):
        if not name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        cards[str(int(os.path.splitext(name)[0]))] = prepare(
            os.path.join(SRC_DIR, name), report)
    return cards
