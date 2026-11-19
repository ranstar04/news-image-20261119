#!/usr/bin/env python3
"""Draw the news-image-20261119 poster (1024x1024 PNG) with Pillow.

BUILD-TIME ONLY. The grader never runs this file: it runs main.py, which is
stdlib-only and only copies the entry.png produced here. This script is
deterministic: no clock, no randomness, no network. Fonts come from the
system DejaVu set, so nothing needs to be bundled with the poster.

Poster: a newspaper front page for Thursday 19 November 2026. Six stories,
each with its own picture and a short label a reader can follow without any
outside context: GTA VI launches, the Trump-Xi-Putin summit in China,
Voyager 1 reaching one light-day, Anthropic's record IPO, a record Van Gogh
sale, and the EU's EUR 45bn loan plan for Ukraine.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (16, 30, 51)
NAVY = (13, 27, 46)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
PINK = (255, 107, 139)
ORANGE = (255, 138, 61)
PURPLE = (88, 44, 128)
TEAL = (14, 116, 110)
RED = (178, 34, 34)
MUSTARD = (232, 180, 44)


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, fill=GOLD):
    draw.text((x, y), label, font=SANS_B(17), fill=fill)
    return y + 24


def sunset(draw, box):
    x0, y0, x1, y1 = box
    bands = [(PURPLE, 0.0), ((214, 69, 120), 0.34), (ORANGE, 0.62), ((255, 196, 84), 1.0)]
    steps = 64
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        # pick the band colour by interpolating between stops
        col = bands[-1][0]
        for j in range(len(bands) - 1):
            a, b = bands[j], bands[j + 1]
            if a[1] <= t0 <= b[1]:
                f = 0 if b[1] == a[1] else (t0 - a[1]) / (b[1] - a[1])
                col = tuple(int(a[0][k] + (b[0][k] - a[0][k]) * f) for k in range(3))
                break
        draw.rectangle([x0, y0 + t0 * (y1 - y0), x1, y0 + t1 * (y1 - y0)], fill=col)
    # sun
    cx, cy, r = (x0 + x1) // 2 + 180, y0 + 118, 58
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 120))
    # skyline (tall enough to show above the text band at the bottom)
    base = y1
    heights = [120, 170, 140, 200, 160, 220, 150, 190, 130, 210, 170, 120]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        draw.rectangle([x0 + i * bw + 4, base - hh, x0 + (i + 1) * bw - 4, base],
                       fill=(30, 16, 52))
        for wy in range(base - hh + 12, base - 10, 22):
            draw.rectangle([x0 + i * bw + 12, wy, x0 + i * bw + 18, wy + 8],
                           fill=(255, 214, 120))
    # palm silhouettes (tall enough to show above the text band)
    for px, py, s in [(x0 + 52, y1 - 8, 1.0), (x1 - 64, y1 - 8, 0.85)]:
        draw.line([px, py, px + 6 * s, py - 150 * s], fill=(30, 16, 52), width=7)
        for dx, dy in [(-52, -150), (-30, -172), (4, -176), (38, -162), (56, -138)]:
            draw.line([px + 6 * s, py - 150 * s, px + dx * s, py + dy * s],
                      fill=(30, 16, 52), width=6)


def stars(draw, box, n=46):
    x0, y0, x1, y1 = box
    for i in range(n):
        x = x0 + (i * 173) % (x1 - x0 - 8) + 4
        y = y0 + (i * 97) % (y1 - y0 - 8) + 4
        r = 1 if i % 3 else 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)


def probe(draw, cx, cy):
    # Voyager: gold dish on the left, silver body, long boom to the right
    draw.polygon([(cx - 96, cy - 52), (cx - 30, cy - 18), (cx - 30, cy + 18),
                  (cx - 96, cy + 52)], fill=(212, 175, 55))
    draw.ellipse([cx - 108, cy - 52, cx - 18, cy + 52], outline=(240, 200, 90), width=3)
    draw.rectangle([cx - 30, cy - 26, cx + 42, cy + 26], fill=(200, 205, 212))
    draw.rectangle([cx + 42, cy - 4, cx + 118, cy + 4], fill=(160, 165, 175))
    draw.ellipse([cx + 112, cy - 12, cx + 136, cy + 12], fill=(212, 175, 55))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((24, 14), "THE WORLD IN ONE DAY", font=SERIF_B(52), fill=WHITE)
    d.rectangle([24, 88, 1000, 91], fill=GOLD)
    d.text((24, 96), "THURSDAY  ·  19 NOVEMBER 2026", font=SANS_B(19), fill=GOLD)
    d.text((640, 96), "SIX STORIES  ·  ONE DAY", font=SANS_B(19), fill=WHITE)

    # ---- hero: GTA VI ----
    hx0, hy0, hx1, hy1 = 24, 132, 1000, 430
    sunset(d, (hx0, hy0, hx1, hy1))
    d.rectangle([hx0, hy1 - 118, hx1, hy1], fill=(13, 27, 46))
    kicker(d, hx0 + 20, hy1 - 110, "GAMES  ·  OUT TODAY")
    d.text((hx0 + 20, hy1 - 84), "GTA VI IS OUT", font=SERIF_B(58), fill=WHITE)
    d.text((hx0 + 20, hy1 - 26), "Vice City opens after 13 years of waiting",
           font=SANS(24), fill=(255, 220, 170))

    # ---- middle row: summit + Voyager ----
    my0, my1 = 442, 700
    # summit panel
    sx0, sx1 = 24, 500
    d.rounded_rectangle([sx0, my0, sx1, my1], radius=10, fill=(122, 20, 20))
    d.rectangle([sx0, my0, sx1, my0 + 74], fill=(90, 12, 12))
    # three flag strips: US stars-and-stripes, China red, Russia white-blue-red
    for i, (fx, cols) in enumerate([
            (sx0 + 24, [(178, 34, 34), WHITE, (178, 34, 34), WHITE, (178, 34, 34)]),
            (sx0 + 132, [(222, 41, 16)] * 5),
            (sx0 + 240, [WHITE, (0, 57, 166), (213, 0, 50)])]):
        for j, c in enumerate(cols):
            d.rectangle([fx, my0 + 12 + j * 10, fx + 84, my0 + 22 + j * 10], fill=c)
    kicker(d, sx0 + 20, my0 + 72, "DIPLOMACY  ·  CHINA", fill=(255, 214, 120))
    text_block(d, (sx0 + 20, my0 + 98),
               wrap(d, "TRUMP, XI & PUTIN MEET IN CHINA", SERIF_B(30), sx1 - sx0 - 40),
               SERIF_B(30), WHITE, 36)
    text_block(d, (sx0 + 20, my0 + 178),
               wrap(d, "Xi greets Trump on the tarmac; talks set for Thursday in Shenzhen.",
                    SANS(20), sx1 - sx0 - 40),
               SANS(20), (255, 228, 210), 25)
    # Voyager panel
    vx0, vx1 = 524, 1000
    d.rounded_rectangle([vx0, my0, vx1, my1], radius=10, fill=(8, 12, 28))
    stars(d, (vx0, my0, vx1, my1 - 90))
    probe(d, vx0 + 250, my0 + 68)
    kicker(d, vx0 + 20, my0 + 126, "SPACE  ·  A FIRST", fill=(140, 200, 255))
    text_block(d, (vx0 + 20, my0 + 150),
               wrap(d, "VOYAGER 1: ONE LIGHT-DAY AWAY", SERIF_B(28), vx1 - vx0 - 40),
               SERIF_B(28), WHITE, 34)
    text_block(d, (vx0 + 20, my0 + 222),
               ["Nearly 50 years after launch."],
               SANS(19), (200, 215, 235), 25)

    # ---- bottom row: IPO + Van Gogh ----
    by0, by1 = 712, 928
    # IPO panel
    ix0, ix1 = 24, 500
    d.rounded_rectangle([ix0, by0, ix1, by1], radius=10, fill=WHITE,
                        outline=(200, 205, 210), width=2)
    d.text((ix0 + 300, by0 + 14), "$81.3BN", font=SANS_B(36), fill=TEAL)
    kicker(d, ix0 + 20, by0 + 14, "BUSINESS  ·  RECORD IPO", fill=TEAL)
    text_block(d, (ix0 + 20, by0 + 44),
               wrap(d, "ANTHROPIC IPO: LARGEST EVER", SERIF_B(26), 272),
               SERIF_B(26), INK, 32)
    text_block(d, (ix0 + 20, by0 + 112),
               wrap(d, "Debut values the AI lab above $1.4 trillion.",
                    SANS(19), ix1 - ix0 - 40),
               SANS(19), (70, 80, 95), 25)
    bars = [14, 24, 20, 32, 44]
    for i, bh in enumerate(bars):
        x = ix0 + 24 + i * 52
        d.rectangle([x, by1 - 12 - bh, x + 36, by1 - 12], fill=TEAL if i < 4 else GOLD)
    # Van Gogh panel
    gx0, gx1 = 524, 1000
    d.rounded_rectangle([gx0, by0, gx1, by1], radius=10, fill=(44, 36, 18))
    # sunflower: petals around a brown centre
    cx, cy = gx0 + 84, by0 + 80
    for ang in range(0, 360, 30):
        import math
        px = cx + int(52 * math.cos(math.radians(ang)))
        py = cy + int(52 * math.sin(math.radians(ang)))
        d.ellipse([px - 22, py - 14, px + 22, py + 14], fill=MUSTARD)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(101, 67, 33))
    for i in range(9):
        import math
        a = i * 40
        d.ellipse([cx - 26 + int(14 * math.cos(math.radians(a))),
                   cy - 26 + int(14 * math.sin(math.radians(a))),
                   cx - 16 + int(14 * math.cos(math.radians(a))),
                   cy - 16 + int(14 * math.sin(math.radians(a)))], fill=(60, 40, 20))
    d.text((gx0 + 176, by0 + 16), "$190.4M", font=SANS_B(36), fill=MUSTARD)
    kicker(d, gx0 + 176, by0 + 62, "ART  ·  RECORD SALE", fill=MUSTARD)
    text_block(d, (gx0 + 20, by0 + 128),
               ["VAN GOGH SELLS FOR A RECORD"],
               SERIF_B(22), WHITE, 30)
    text_block(d, (gx0 + 20, by0 + 164),
               wrap(d, "Portrait fetches $190.4m after its Nazi-era dispute.",
                    SANS(18), gx1 - gx0 - 40),
               SANS(18), (220, 205, 170), 23)

    # ---- footer: EU loan ----
    d.rectangle([0, 942, W, H], fill=(0, 51, 102))
    for i in range(12):
        import math
        a = math.radians(i * 30 - 90)
        sx = 52 + int(20 * math.cos(a))
        sy = 972 + int(20 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))
    d.text((92, 954), "EU proposes a €45bn loan for Ukraine — repaid once Russia pays reparations.",
           font=SANS_B(20), fill=WHITE)
    d.text((92, 980), "Sources: BBC · Al Jazeera · NYT · Reuters · FT  —  19 November 2026",
           font=SANS(15), fill=(180, 205, 230))

    img.save(HERE / "entry.png", optimize=True)
    print("wrote", HERE / "entry.png", (HERE / "entry.png").stat().st_size, "bytes")


if __name__ == "__main__":
    main()
