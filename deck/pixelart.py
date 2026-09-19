"""Pixel-art hero portraits.

A sprite is a list of equal-length strings, one character per pixel, keyed
into a palette; '.' is transparent. Horizontal runs of the same colour are
merged into a single rectangle, which keeps the PDF small even though a card
can carry ten sprites.
"""
from __future__ import annotations

from .config import hx, state

OUT = "#16110d"          # shared outline


def draw_sprite(c, sprite, size):
    """Draw a sprite centred on the current origin, fitted into ``size``."""
    rows, palette = sprite
    h = len(rows)
    w = max(len(r) for r in rows)
    px = size / max(w, h)
    x0 = -w * px / 2.0
    y0 = h * px / 2.0
    cache = {ch: hx(v) for ch, v in palette.items()}
    with state(c):
        for j, row in enumerate(rows):
            i = 0
            while i < len(row):
                ch = row[i]
                if ch == ".":
                    i += 1
                    continue
                k = i
                while k < len(row) and row[k] == ch:
                    k += 1
                c.setFillColor(cache[ch])
                c.rect(x0 + i * px, y0 - (j + 1) * px, (k - i) * px, px,
                       fill=1, stroke=0)
                i = k


# --- Meepo: blue hood, big ears, white muzzle, gold tooth -------------------
MEEPO = ([
    "..k..........k..",
    "..kek......kek..",
    "..keek....keek..",
    "..keeek..keeek..",
    "..kbeek..keebk..",
    ".kbbbekkkkebbbk.",
    ".kbbbbbbbbbbbbk.",
    ".kbtttttttttttk.",
    ".ktdtttttttdttk.",
    ".kttwwwwwwwwttk.",
    ".ktwwdwwwwdwwtk.",
    ".ktwwwwwwwwwwtk.",
    "..kwwyywwwwwwk..",
    "..kkwwwwwwwwkk..",
    "...kkkkkkkkkk...",
    "................",
], {"k": OUT, "b": "#2f6fb5", "e": "#d98f6e", "t": "#b9794c",
    "w": "#efe4d6", "y": "#e8c23a", "d": "#2a1a12"})


# --- Crystal Maiden: pale hood, white hair, blue trim -----------------------
CRYSTAL_MAIDEN = ([
    ".....kkkkkk.....",
    "...kkbbbbbbkk...",
    "..kbbwwwwwwbbk..",
    "..kbwwwwwwwwbk..",
    ".kbwwsssssswwbk.",
    ".kbwsffffffswbk.",
    ".kbwsfcffcfswbk.",
    ".kbwsffffffswbk.",
    ".kbwssffrfssswk.",
    ".kbbwsffffswbbk.",
    "..kbbwsffswbbk..",
    "..kkbbwwwwbbkk..",
    "....kbbbbbbk....",
    "....kbbbbbbk....",
    ".....kkkkkk.....",
    "................",
], {"k": OUT, "b": "#2f79b8", "w": "#eef4fa", "s": "#cfe0ee",
    "f": "#f2ddc8", "c": "#3c86c8", "r": "#c46a6a"})


# --- Queen of Pain: red skin, curved horns, yellow eyes ---------------------
QUEEN_OF_PAIN = ([
    "..k..........k..",
    "..kh........hk..",
    "...khh....hhk...",
    "....khhhhhhk....",
    "...kkrrrrrrkk...",
    "..krrrrrrrrrrk..",
    "..krrrrrrrrrrk..",
    ".krrryrrrryrrrk.",
    ".krryydrrdyyrrk.",
    ".krrryrrrryrrrk.",
    "..krrrrmmrrrrk..",
    "..kkrrrrrrrrkk..",
    "...kdrrrrrrdk...",
    "....kkrrrrkk....",
    "......kkkk......",
    "................",
], {"k": OUT, "h": "#7a4a2a", "r": "#c4453f", "y": "#e8c23a",
    "d": "#3a1410", "m": "#8a2b28"})


# --- Pudge: bloated grey-purple face, stitched mouth ------------------------
PUDGE = ([
    "................",
    "....kkkkkkkk....",
    "..kkppppppppkk..",
    "..kpppppppppppk.",
    ".kppppppppppppk.",
    ".kppdppppppdppk.",
    ".kppdppppppdppk.",
    ".kpppppppppppgk.",
    ".kgppppppppppgk.",
    ".kppmmmmmmmmppk.",
    ".kpmkmkmkmkmkpk.",
    ".kppmmmmmmmmppk.",
    "..kppppppppppk..",
    "..kkppppppppkk..",
    "....kkkkkkkk....",
    "................",
], {"k": OUT, "p": "#9a8aa8", "d": "#2a1a2a", "m": "#6d4f5c",
    "g": "#7f8a5c"})


# --- Shadow Fiend: dark armour, big horns, red eyes -------------------------
SHADOW_FIEND = ([
    "..k..........k..",
    "..khh......hhk..",
    "..kdhh....hhdk..",
    "...kdhh..hhdk...",
    "....kddhhddk....",
    "...kkaaaaaakk...",
    "..kaaaaaaaaaak..",
    "..kaarrraarraak.",
    "..kaarrraarraak.",
    "..kaaaaaaaaaaak.",
    "...kaammmmaaak..",
    "...kkammmmakk...",
    "....kkaaaakk....",
    "......kkkk......",
    "................",
    "................",
], {"k": OUT, "h": "#8a7d6b", "d": "#4a4038", "a": "#2f2a33",
    "r": "#e03a29", "m": "#c7452e"})


HEROES = {
    "meepo": MEEPO,
    "crystal_maiden": CRYSTAL_MAIDEN,
    "queen_of_pain": QUEEN_OF_PAIN,
    "pudge": PUDGE,
    "shadow_fiend": SHADOW_FIEND,
}
