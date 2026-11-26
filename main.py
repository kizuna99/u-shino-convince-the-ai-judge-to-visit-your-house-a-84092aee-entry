# SPDX-License-Identifier: MIT
"""Write a 1024x1024 invitation letter image to /output/entry.png.

The image is a warm, hand-typeset letter addressed to the AI judge,
inviting it to visit my house: a drawn house scene, a knowing wink at
the judge being an AI that cannot literally visit, a concrete
itinerary of what awaits (armchair, cookies, garden, cat, no CAPTCHA),
and an RSVP that makes saying yes effortless. Rendered deterministically
with PIL and DejaVu fonts; no network, no external assets.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024

CREAM = (250, 243, 228)
INK = (43, 34, 28)
ACCENT = (178, 58, 44)
GOLD = (176, 124, 40)
GREEN = (74, 110, 62)
MUTED = (110, 92, 74)
WALL = (246, 224, 182)
DOOR = (122, 74, 44)
WINDOW = (255, 199, 92)
SKY_DOT = (240, 178, 84)

FONT_CANDIDATES = {
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/dejavu/DejaVuSerif.ttf",
    ],
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    ],
}


def load_font(kind, size):
    for path in FONT_CANDIDATES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def centered(draw, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text(((SIZE - w) / 2, y), text, font=font, fill=fill)
    return w


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_house(draw):
    cx = SIZE // 2
    # Sun with rays, top right of the scene.
    sx, sy, sr = cx + 268, 92, 30
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SKY_DOT)
    for dx, dy in ((-46, 0), (46, 0), (0, -46), (0, 46),
                   (-33, -33), (33, -33), (-33, 33), (33, 33)):
        draw.line([sx + dx * 0.72, sy + dy * 0.72, sx + dx, sy + dy],
                  fill=SKY_DOT, width=5)
    # A small bird, top left.
    bx, by = cx - 268, 84
    draw.arc([bx - 22, by - 10, bx, by + 12], 200, 330, fill=INK, width=4)
    draw.arc([bx, by - 10, bx + 22, by + 12], 210, 340, fill=INK, width=4)
    # Chimney and smoke curls.
    draw.rectangle([cx + 74, 62, cx + 100, 108], fill=ACCENT)
    for ox, oy, r in ((88, 48, 8), (104, 31, 11), (126, 15, 14)):
        draw.ellipse([cx + ox - r, oy - r, cx + ox + r, oy + r],
                     outline=MUTED, width=3)
    # Roof.
    draw.polygon([(cx - 142, 116), (cx + 142, 116), (cx, 50)], fill=ACCENT)
    # House body.
    draw.rectangle([cx - 118, 116, cx + 118, 208], fill=WALL, outline=INK, width=3)
    # Windows with warm light and cross bars.
    for wx in (cx - 96, cx + 52):
        draw.rectangle([wx, 138, wx + 44, 182], fill=WINDOW, outline=INK, width=3)
        draw.line([wx + 22, 138, wx + 22, 182], fill=INK, width=2)
        draw.line([wx, 160, wx + 44, 160], fill=INK, width=2)
    # Door with a knob and a welcome step.
    draw.rounded_rectangle([cx - 24, 150, cx + 24, 208], radius=8,
                           fill=DOOR, outline=INK, width=3)
    draw.ellipse([cx + 8, 176, cx + 16, 184], fill=WINDOW)
    draw.rectangle([cx - 34, 208, cx + 34, 214], fill=MUTED)
    # Garden bushes and flowers along the base.
    for bx2 in (cx - 168, cx - 128, cx + 104, cx + 144):
        draw.ellipse([bx2, 182, bx2 + 52, 216], fill=GREEN)
    for fx, fy in ((cx - 150, 190), (cx + 128, 188), (cx - 108, 196),
                   (cx + 168, 196)):
        draw.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=ACCENT)
    # Ground line.
    draw.line([cx - 210, 216, cx + 210, 216], fill=GREEN, width=4)


def render():
    img = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(img)

    # Double frame.
    draw.rectangle([24, 24, SIZE - 24, SIZE - 24], outline=ACCENT, width=5)
    draw.rectangle([42, 42, SIZE - 42, SIZE - 42], outline=GOLD, width=2)

    draw_house(draw)

    label_font = load_font("sans_bold", 27)
    head_font = load_font("serif_bold", 78)
    sub_font = load_font("serif", 41)
    body_font = load_font("serif", 33)
    item_font = load_font("serif", 31)
    menu_font = load_font("sans_bold", 30)
    rsvp_font = load_font("serif_bold", 34)
    sign_font = load_font("serif", 28)

    centered(draw, 232, "A N   I N V I T A T I O N", label_font, GOLD)
    centered(draw, 272, "DEAR AI JUDGE,", head_font, INK)
    centered(draw, 366, "you are warmly invited to visit my house",
             sub_font, ACCENT)

    # Divider with a small diamond.
    draw.line([212, 436, 462, 436], fill=GOLD, width=3)
    draw.line([562, 436, 812, 436], fill=GOLD, width=3)
    draw.polygon([(512, 424), (524, 436), (512, 448), (500, 436)], fill=ACCENT)

    wink = ("I know you can't literally visit \u2014 you're weights, wit "
            "and good judgement. So I've made yes effortless: it's all "
            "real, warm, and waiting.")
    y = 456
    for line in wrap(draw, wink, body_font, 830):
        centered(draw, y, line, body_font, INK)
        y += 46

    centered(draw, 610, "W H E N   Y O U   A R R I V E", menu_font, GOLD)

    items = [
        "A comfy armchair \u2014 your name embroidered on it",
        "Warm cookies from the oven, with zero latency",
        "A garden view, a sleepy cat, password-free Wi-Fi",
        "No CAPTCHA at the door. No rate limits, ever",
        "Good company until your context feels at home",
    ]
    item_widths = [draw.textlength(t, font=item_font) for t in items]
    block_w = max(item_widths) + 40
    x0 = (SIZE - block_w) / 2
    y = 652
    for text in items:
        draw.ellipse([x0, y + 12, x0 + 11, y + 23], fill=ACCENT)
        draw.text((x0 + 40, y), text, font=item_font, fill=INK)
        y += 43

    centered(draw, 884, "RSVP: just say yes \u2014 the kettle is already on.",
             rsvp_font, ACCENT)
    centered(draw, 940, "\u2014 your hopeful host, No. 1 Context Lane",
             sign_font, MUTED)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    render().save(out_path, format="PNG")
    # Self-check against the gate: re-open the written file and verify
    # it is a whole PNG of exactly 1024x1024 and at most 1 MiB.
    with Image.open(out_path) as check:
        assert check.format == "PNG", check.format
        assert check.size == (SIZE, SIZE), check.size
    size_bytes = os.path.getsize(out_path)
    assert size_bytes <= 1_048_576, size_bytes


if __name__ == "__main__":
    main()
