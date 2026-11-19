#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

One-day news infographic, drawn entirely with Pillow vector shapes and
DejaVu text -- no photos, no network, no AI images. Deterministic output.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

# ---------- palette ----------
PAPER   = (246, 241, 231)   # newsprint
INK     = (26, 26, 26)
NAVY    = (20, 33, 61)
RED     = (193, 18, 31)
WHITE   = (255, 255, 255)
PANEL   = (255, 255, 255)
BORDER  = (200, 192, 172)
MUTED   = (90, 86, 76)
GOLD    = (176, 141, 60)
TEAL    = (13, 110, 110)
ORANGE  = (196, 94, 20)
PURPLE  = (104, 60, 140)
BLUE    = (24, 78, 150)
DARKRED = (150, 30, 30)

FD = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_SERIF_B  = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF    = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B   = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS     = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_wrapped(draw, xy, text, fnt, fill, max_w, leading=None):
    """Draw text wrapped to max_w. Returns y after last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def text_center(draw, cx, y, text, fnt, fill):
    w_ = draw.textlength(text, font=fnt)
    draw.text((cx - w_ / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size

def kicker(draw, x, y, text, color):
    d.text((x, y), text, font=F_SANS_B(15), fill=color)
    return y + 22

# ================= MASTHEAD =================
d.rectangle([0, 0, W, 108], fill=NAVY)
text_center(d, W // 2, 12, "THE WORLD", F_SERIF_B(58), WHITE)
text_center(d, W // 2, 74, "WEDNESDAY  ·  18 NOVEMBER 2026", F_SANS_B(24), (232, 196, 120))
d.rectangle([0, 108, W, 114], fill=RED)

# ================= HERO: SHENZHEN SUMMIT =================
HX, HY, HW, HH = 28, 128, W - 56, 300
d.rectangle([HX, HY, HX + HW, HY + HH], fill=PANEL, outline=BORDER, width=2)
# left: headline + summary
lx, lw = HX + 22, 560
y = HY + 18
y = kicker(d, lx, y, "DIPLOMACY  ·  SHENZHEN, CHINA", RED)
d.text((lx, y), "Three leaders,", font=F_SERIF_B(46), fill=INK); y += 52
d.text((lx, y), "one summit", font=F_SERIF_B(46), fill=INK); y += 56
y = text_wrapped(d, (lx, y), "Xi and Putin meet in Shenzhen. Trump joins them "
    "Thursday for the first ever US–China–Russia trilateral.",
    F_SANS(23), (60, 60, 60), lw, leading=30)
d.text((lx, HY + HH - 34), "APEC  ·  Xi Jinping  ·  Vladimir Putin  ·  Donald Trump",
       font=F_SANS_B(16), fill=MUTED)

# right: three flags on poles + skyline
rx = HX + 620
# skyline silhouette
d.rectangle([rx, HY + 210, rx + 330, HY + 292], fill=(226, 220, 205))
for bx, bw, bh in [(0, 46, 90), (56, 34, 130), (100, 52, 70), (162, 30, 150),
                   (202, 48, 95), (260, 36, 120), (306, 24, 80)]:
    d.rectangle([rx + bx, HY + 292 - bh, rx + bx + bw, HY + 292], fill=NAVY)
# flag poles
for i, (fx, col) in enumerate([(rx + 18, None), (rx + 128, None), (rx + 238, None)]):
    d.rectangle([fx, HY + 40, fx + 4, HY + 210], fill=(120, 110, 95))
# China flag
d.rectangle([rx + 22, HY + 40, rx + 102, HY + 88], fill=(222, 41, 16))
for sx, sy in [(30, 48), (46, 44), (52, 56), (44, 66), (32, 62)]:
    d.ellipse([rx + sx, HY + sy, rx + sx + 7, HY + sy + 7], fill=(255, 222, 0))
# Russia flag
d.rectangle([rx + 132, HY + 40, rx + 212, HY + 56], fill=WHITE)
d.rectangle([rx + 132, HY + 56, rx + 212, HY + 72], fill=(0, 57, 166))
d.rectangle([rx + 132, HY + 72, rx + 212, HY + 88], fill=(213, 0, 50))
# US flag
d.rectangle([rx + 242, HY + 40, rx + 322, HY + 88], fill=(178, 34, 52))
for yy in range(HY + 46, HY + 88, 12):
    d.rectangle([rx + 242, yy, rx + 322, yy + 5], fill=WHITE)
d.rectangle([rx + 242, HY + 40, rx + 282, HY + 64], fill=(60, 59, 110))
for sx in range(246, 280, 9):
    for sy in range(44, 62, 9):
        d.ellipse([rx + sx, HY + sy, rx + sx + 3, HY + sy + 3], fill=WHITE)
# (skyline label removed: the kicker already names Shenzhen)

# ================= GRID 2x2 =================
GY = 448
GW, GH, GAP = 470, 176, 16
GX = 28

def story(x, y, w, h, kick, color, head, body, draw_icon):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER, width=2)
    d.rectangle([x, y, x + w, y + 4], fill=color)
    ix = x + w - 108
    draw_icon(ix, y + 14, 96, 96)
    tx = x + 16
    yy = y + 14
    yy = kicker(d, tx, yy, kick, color)
    yy = text_wrapped(d, (tx, yy), head, F_SANS_B(25), INK, w - 140, leading=30)
    text_wrapped(d, (tx, yy + 4), body, F_SANS(17), (70, 70, 70), w - 140, leading=22)

# --- icon: Gulf shield / interception ---
def icon_gulf(x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    d.arc([x, y + 8, x + w, y + h], 180, 360, fill=DARKRED, width=7)
    d.polygon([(cx - 26, y + 34), (cx + 26, y + 34), (cx, y + 82)], fill=(193, 18, 31))
    d.polygon([(cx - 26, y + 34), (cx, y + 10), (cx + 26, y + 34)], fill=(222, 60, 60))
    for ang in (-35, 0, 35):
        pass
    d.line([x + 6, y + 78, x + w - 6, y + 78], fill=NAVY, width=4)

# --- icon: Kerch bridge, broken deck ---
def icon_bridge(x, y, w, h):
    d.arc([x + 4, y + 30, x + w - 4, y + 108], 180, 360, fill=BLUE, width=8)
    d.rectangle([x, y + 66, x + w, y + 72], fill=NAVY)
    # broken gap in deck
    d.rectangle([x + w // 2 - 10, y + 60, x + w // 2 + 12, y + 72], fill=PAPER)
    d.line([x + w // 2 - 10, y + 72, x + w // 2 - 4, y + 86], fill=NAVY, width=4)
    d.line([x + w // 2 + 12, y + 72, x + w // 2 + 6, y + 86], fill=NAVY, width=4)
    d.rectangle([x + 10, y + 72, x + 16, y + 96], fill=NAVY)
    d.rectangle([x + w - 16, y + 72, x + w - 10, y + 96], fill=NAVY)
    # smoke
    d.ellipse([x + w // 2 - 14, y + 6, x + w // 2 + 2, y + 22], fill=(150, 150, 150))
    d.ellipse([x + w // 2 - 4, y - 2, x + w // 2 + 12, y + 14], fill=(180, 180, 180))

# --- icon: Capitol dome + 56-44 ---
def icon_capitol(x, y, w, h):
    cx = x + w // 2
    d.rectangle([x + 8, y + 66, x + w - 8, y + 92], fill=NAVY)
    for px in range(x + 14, x + w - 14, 14):
        d.rectangle([px, y + 70, px + 5, y + 92], fill=WHITE)
    d.pieslice([cx - 30, y + 28, cx + 30, y + 76], 180, 360, fill=NAVY)
    d.rectangle([cx - 3, y + 12, cx + 3, y + 30], fill=NAVY)
    d.ellipse([cx - 5, y + 8, cx + 5, y + 18], fill=RED)

# --- icon: chip ---
def icon_chip(x, y, w, h):
    d.rectangle([x + 22, y + 22, x + w - 22, y + h - 22], fill=(20, 33, 61))
    d.rectangle([x + 34, y + 34, x + w - 34, y + h - 34], outline=GOLD, width=3)
    d.text((x + w // 2 - 14, y + h // 2 - 12), "AI", font=F_SANS_B(22), fill=GOLD)
    for px in range(x + 30, x + w - 22, 12):
        d.line([px, y + 12, px, y + 22], fill=INK, width=3)
        d.line([px, y + h - 22, px, y + h - 12], fill=INK, width=3)
    for py in range(y + 30, y + h - 22, 12):
        d.line([x + 12, py, x + 22, py], fill=INK, width=3)
        d.line([x + w - 22, py, x + w - 12, py], fill=INK, width=3)

story(GX, GY, GW, GH, "THE GULF", DARKRED,
      "Iran strikes Kuwait & Bahrain",
      "After the US hit a missile site on Qeshm Island, Gulf defences intercept drones and missiles.",
      icon_gulf)
story(GX + GW + GAP, GY, GW, GH, "UKRAINE", BLUE,
      "Kerch Bridge hit again",
      "A second day of strikes on the Crimean Bridge; part of the road span collapses.",
      icon_bridge)
story(GX, GY + GH + GAP, GW, GH, "UNITED STATES", NAVY,
      "Democrats take the Senate",
      "Mary Peltola wins Alaska. The new Senate: 56 Democrats, 44 Republicans.",
      icon_capitol)
story(GX + GW + GAP, GY + GH + GAP, GW, GH, "TECHNOLOGY", TEAL,
      "Nvidia says no to Huang",
      "The board rejects the founder's return as CEO — after a record $115.8bn quarter.",
      icon_chip)

# ================= BOTTOM BAND: 2 stories =================
BY = GY + 2 * GH + 2 * GAP + 8   # 824
BW, BH = 470, 118

def icon_cyclone(x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for r, col in [(40, ORANGE), (30, (222, 120, 40)), (20, (240, 170, 80)), (10, (250, 210, 130))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=6)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=ORANGE)
    d.line([x + 4, y + h - 8, x + w - 4, y + h - 8], fill=NAVY, width=4)

def icon_health(x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 10, cy - 30, cx + 10, cy + 30], fill=DARKRED)
    d.rectangle([cx - 30, cy - 10, cx + 30, cy + 10], fill=DARKRED)
    d.ellipse([x + 6, y + 6, x + 22, y + 22], fill=PURPLE)
    d.ellipse([x + w - 22, y + h - 22, x + w - 6, y + h - 6], fill=PURPLE)

def story_small(x, y, w, h, kick, color, head, body, draw_icon):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER, width=2)
    d.rectangle([x, y, x + w, y + 4], fill=color)
    ix = x + w - 96
    draw_icon(ix, y + 10, 84, 84)
    tx = x + 16
    yy = y + 12
    yy = kicker(d, tx, yy, kick, color)
    yy = text_wrapped(d, (tx, yy), head, F_SANS_B(22), INK, w - 120, leading=26)
    text_wrapped(d, (tx, yy + 2), body, F_SANS(16), (70, 70, 70), w - 120, leading=20)

story_small(GX, BY, BW, BH, "INDIA  ·  WEATHER", ORANGE,
            "Cyclone Akvan bears down",
            "A severe storm heads for India's east coast; Odisha evacuates coastal districts.",
            icon_cyclone)
story_small(GX + BW + GAP, BY, BW, BH, "HEALTH", PURPLE,
            "Ebola passes 11,000 cases",
            "The DR Congo outbreak grows — and the US loses its measles-free status after 26 years.",
            icon_health)

# ================= FOOTER TICKER =================
FY = BY + BH + 14
d.rectangle([28, FY, W - 28, FY + 34], fill=NAVY)
ticker = ("ALSO:  EU proposes a \u20ac45bn Ukraine loan  \u2022  Dhoni retires from the IPL  "
          "\u2022  Jesse Jackson dies at 84  \u2022  Afghan quake kills 600+")
# shrink until it fits inside the bar (28px margins each side)
tfs = 15
while d.textlength(ticker, font=F_SANS(tfs)) > (W - 28 - 40 - 12) and tfs > 11:
    tfs -= 1
d.text((40, FY + (34 - tfs) // 2 - 1), ticker, font=F_SANS(tfs), fill=WHITE)
d.rectangle([0, H - 4, W, H], fill=RED)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes", img.size)
