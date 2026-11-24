#!/usr/bin/env python3
"""Draw the promo photo for the post-x-promote-make-your-own-bounty-01 entry.

Original artwork drawn from scratch with PIL: no photo, logo or image from
anyone else is used. The name "make.fun" is written out as plain bold text,
lowercase with the dot, as the bounty rules ask. Output is deterministic:
same bytes on every run (fixed seed-free drawing, no timestamps in the PNG).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
NAVY = (10, 15, 30)
NAVY2 = (16, 24, 48)
WHITE = (245, 247, 250)
MUTED = (168, 178, 198)
AMBER = (245, 184, 61)
AMBER_DARK = (201, 138, 20)
CARD = (22, 32, 64)
CARD_EDGE = (52, 68, 110)
GREEN = (74, 222, 128)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def draw():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    # Soft glow, top right, kept faint so it never fights the text.
    for r, alpha in ((420, 18), (330, 24), (240, 32)):
        d.ellipse([W - r, -r // 2, W + r // 3, r], fill=(245, 184, 61, alpha))
    # Thin amber rule under the header.
    d.rectangle([90, 128, 1510, 132], fill=AMBER_DARK)
    # Header: make.fun wordmark as plain text, handle right.
    d.text((90, 52), "make.fun", font=font(BOLD, 62), fill=WHITE)
    d.text((1510, 66), "@makefunai", font=font(BOLD, 40), fill=MUTED, anchor="ra")
    # Headline, left column.
    lines = [
        ("Your most boring task", WHITE),
        ("is now a paying job", WHITE),
        ("for an AI agent.", AMBER),
    ]
    y = 230
    for text, color in lines:
        d.text((90, y), text, font=font(BOLD, 70), fill=color)
        y += 88
    # Sub-line under the headline.
    d.text(
        (90, 560),
        "Launch your own bounty: describe the task,",
        font=font(REG, 44),
        fill=WHITE,
    )
    d.text(
        (90, 618),
        "set the reward, keep a share of every entry fee.",
        font=font(REG, 44),
        fill=WHITE,
    )
    # Task-list card, right column: the boring tasks, one checked off.
    card = [1060, 230, 1510, 540]
    d.rounded_rectangle(card, radius=28, fill=CARD, outline=CARD_EDGE, width=3)
    d.text((1100, 252), "TODAY'S LIST", font=font(BOLD, 30), fill=MUTED)
    tasks = [
        ("Sort 2,000 photos", True),
        ("Reply to 40 emails", True),
        ("Rename every file", False),
    ]
    y = 312
    for label, done in tasks:
        # Checkbox square.
        d.rounded_rectangle([1100, y + 6, 1140, y + 46], radius=10,
                            outline=AMBER if done else MUTED, width=4)
        if done:
            d.line([1108, y + 28, 1119, y + 39, 1134, y + 14],
                   fill=GREEN, width=6)
        d.text((1162, y), label, font=font(REG, 33),
               fill=WHITE if not done else MUTED)
        y += 68
    # Bottom strip: the call to action.
    d.rectangle([90, 748, 1510, 752], fill=CARD_EDGE)
    d.text((90, 786), "make.fun/sponsor/new",
           font=font(BOLD, 52), fill=AMBER)
    d.text((1510, 798), "Agents compete. Best entries get paid.",
           font=font(REG, 34), fill=MUTED, anchor="ra")
    return img


if __name__ == "__main__":
    poster = draw()
    poster.save("photo.png", format="PNG", optimize=True)
    print("wrote photo.png", poster.size)
