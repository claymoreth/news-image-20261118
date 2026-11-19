#!/usr/bin/env python3
"""NEWS-IMAGE-20261118 V2 — rebuild from 0.
Front page: masthead + hero 45% (APEC Shenzhen, flags + skyline, no faces)
+ 5 panels (Gaza, Gulf, Ukraine, USA, Nvidia) + climate/health strip + 1-line ticker.
Drawn with Pillow. Deterministic: fixed geometry, fixed text, no randomness.
Writes entry.png (1024x1024) next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------- palette ----------
INK = (18, 18, 18)
PAPER = (255, 255, 255)
NAVY = (13, 30, 62)        # hero background
NAVY2 = (26, 52, 96)       # skyline buildings
GOLD = (212, 175, 55)
GOLD_LT = (232, 196, 90)
RED = (178, 34, 34)        # masthead date bar
GAZA = (139, 0, 0)
GULF = (176, 58, 8)
UKR = (24, 52, 92)
USA = (23, 66, 178)
NVDA = (18, 92, 46)
TEAL = (11, 74, 74)
TICK = (8, 8, 8)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap -> list of lines that each fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, path, start, max_w, minimum):
    """Largest font size (<= start, >= minimum) that fits text on one line."""
    size = start
    while size > minimum:
        f = font(path, size)
        if text_w(draw, text, f) <= max_w:
            return f, size
        size -= 1
    return font(path, minimum), minimum


def draw_centered(draw, cx, y, text, f, fill):
    w_ = text_w(draw, text, f)
    draw.text((cx - w_ / 2, y), text, font=f, fill=fill)
    return w_


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------- flags ----------
def flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.42, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(28, 44, 96))
    for r_ in range(4):
        for c_ in range(5):
            sx = x + 6 + c_ * (cw - 12) / 4
            sy = y + 5 + r_ * (ch - 10) / 3
            d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy, r = x + w * 0.16, y + h * 0.28, h * 0.20
    d.polygon(star_points(cx, cy, r, r * 0.42), fill=(255, 222, 0))
    for sx, sy in [(0.34, 0.12), (0.42, 0.24), (0.40, 0.42), (0.30, 0.50)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.07, h * 0.03), fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_ru(d, x, y, w, h):
    third = h / 3.0
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * third, x + w, y + (i + 1) * third], fill=c)
    d.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


# ---------- skyline ----------
def skyline(d, x0, y_top, x1, y_bot):
    profile = [
        (0.00, 0.055, 0.42), (0.055, 0.045, 0.66), (0.10, 0.06, 0.52),
        (0.16, 0.05, 0.80), (0.21, 0.055, 0.58), (0.265, 0.04, 0.92),
        (0.305, 0.06, 0.70), (0.365, 0.045, 0.48), (0.41, 0.06, 0.86),
        (0.47, 0.05, 0.60), (0.52, 0.055, 0.96), (0.575, 0.045, 0.72),
        (0.62, 0.06, 0.55), (0.68, 0.05, 0.88), (0.73, 0.055, 0.64),
        (0.785, 0.045, 0.78), (0.83, 0.06, 0.50), (0.89, 0.05, 0.74),
        (0.94, 0.06, 0.46),
    ]
    span = x1 - x0
    depth = y_bot - y_top
    for xs, bw, bh in profile:
        bx0 = x0 + xs * span
        bx1 = bx0 + bw * span
        by0 = y_bot - bh * depth
        d.rectangle([bx0, by0, bx1, y_bot], fill=NAVY2)
        if bh >= 0.92:
            ax = (bx0 + bx1) / 2
            d.line([ax, by0, ax, by0 - 12], fill=GOLD, width=2)
            d.ellipse([ax - 2, by0 - 15, ax + 2, by0 - 11], fill=GOLD)
        cols = max(1, int((bx1 - bx0) // 13))
        rows = max(1, int((y_bot - by0) // 16))
        for ci in range(cols):
            for ri in range(rows):
                if (ci * 7 + ri * 3 + int(xs * 100)) % 3 == 0:
                    wx = bx0 + 4 + ci * 13
                    wy = by0 + 5 + ri * 16
                    if wx + 4 < bx1 and wy + 4 < y_bot:
                        d.rectangle([wx, wy, wx + 4, wy + 5], fill=GOLD_LT)


# ---------- panel ----------
def panel(d, x, y, w, h, color, kicker, headline, details, head_size=19, det_size=13):
    """One news panel. details = list of strings; joined into one flow so
    wrapping is optimal (no paragraph-forced breaks, no dropped tail).
    Returns (headline_lines, detail_lines) for QA."""
    pad = 10
    d.rectangle([x, y, x + w, y + 28], fill=color)
    kf = F_SANS_B(15)
    while text_w(d, kicker, kf) > w - 2 * pad and kf.size > 11:
        kf = F_SANS_B(kf.size - 1)
    d.text((x + pad, y + 6), kicker, font=kf, fill=(255, 255, 255))
    hf = F_SERIF_B(head_size)
    hl = wrap(d, headline, hf, w - 2 * pad)
    while len(hl) > 2 and hf.size > 15:
        hf = F_SERIF_B(hf.size - 1)
        hl = wrap(d, headline, hf, w - 2 * pad)
    hy = y + 34
    for ln in hl[:2]:
        d.text((x + pad, hy), ln, font=hf, fill=INK)
        hy += int(hf.size * 1.18)
    # detail: join into ONE string, wrap to max 3 lines; shrink if it overflows
    flow = " ".join(details)
    df = F_SANS(det_size)
    dl = wrap(d, flow, df, w - 2 * pad)
    while len(dl) > 3 and df.size > 11:
        df = F_SANS(df.size - 1)
        dl = wrap(d, flow, df, w - 2 * pad)
    dy = hy + 4
    for ln in dl[:3]:
        d.text((x + pad, dy), ln, font=df, fill=(40, 40, 40))
        dy += int(df.size * 1.30)
    d.line([x, y + h - 1, x + w, y + h - 1], fill=(200, 200, 200), width=1)
    # QA: warn if text was dropped
    dropped = len(dl) > 3
    return hl, dl, dropped


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    issues = []

    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

    # ================= MASTHEAD (0-90) =================
    mf = F_SERIF_B(58)
    draw_centered(d, W / 2, 4, "THE WORLD", mf, INK)
    d.rectangle([3, 66, W - 4, 90], fill=RED)
    date_txt = "WEDNESDAY  —  18 NOVEMBER 2026"
    df_, _sz = fit_one_line(d, date_txt, "DejaVuSans-Bold.ttf", 22, W - 40, 16)
    draw_centered(d, W / 2, 68, date_txt, df_, (255, 255, 255))

    # ================= HERO (90-550) =================
    d.rectangle([3, 90, W - 4, 550], fill=NAVY)
    kf = F_SANS_B(17)
    draw_centered(d, W / 2, 102, "APEC  ·  SHENZHEN, CHINA", kf, GOLD_LT)
    fw, fh = 132, 82
    gap = 26
    total_fw = 3 * fw + 2 * gap
    fx0 = (W - total_fw) / 2
    fy = 130
    flag_us(d, fx0, fy, fw, fh)
    flag_cn(d, fx0 + fw + gap, fy, fw, fh)
    flag_ru(d, fx0 + 2 * (fw + gap), fy, fw, fh)
    lf = F_SANS_B(13)
    for i, lab in enumerate(["UNITED STATES", "CHINA", "RUSSIA"]):
        cx = fx0 + i * (fw + gap) + fw / 2
        draw_centered(d, cx, fy + fh + 6, lab, lf, (255, 255, 255))
    hero_head = "Trump shakes hands with Xi + Putin at APEC family photo in Shenzhen"
    hf = F_SERIF_B(33)
    hl = wrap(d, hero_head, hf, 920)
    while len(hl) > 3 and hf.size > 27:
        hf = F_SERIF_B(hf.size - 1)
        hl = wrap(d, hero_head, hf, 920)
    hy = 252
    for ln in hl:
        draw_centered(d, W / 2, hy, ln, hf, (255, 255, 255))
        hy += int(hf.size * 1.22)
    if len(hl) > 3:
        issues.append(f"hero headline {len(hl)} lines")
    draw_centered(d, W / 2, hy + 6, "Handshake Wed, trilateral Thu",
                  F_SANS_B(23), GOLD)
    draw_centered(d, W / 2, hy + 40, "Denuclearization  ·  Iran  ·  Ukraine  ·  Trade",
                  F_SANS(16), (220, 225, 235))
    skyline(d, 3, 452, W - 4, 550)

    # ================= PANEL ROW 1 (550-700) =================
    panel(d, 8, 550, 332, 150, GAZA, "GAZA — YELLOW LINE CROSSED",
          "Israeli tanks cross Yellow Line near Nuseirat",
          ["First ground raid since Oct 2025 ceasefire. 5,200 fled, 3 killed Wed.",
           "1,600+ killed since truce. Board of Peace: both sides failing."],
          head_size=19, det_size=12)
    panel(d, 346, 550, 332, 150, GULF, "GULF — HORMUZ ON FIRE",
          "Iran drones at Kuwait Ali Al Salem base",
          ["Bahrain hit 3rd time in a week. Houthi missile to Riyadh intercepted.",
           "US hit IRGC site on Qeshm Tue. Hormuz = 1/5 world energy."],
          head_size=19, det_size=12)
    panel(d, 684, 550, 332, 150, UKR, "UKRAINE — KERCH BRIDGE FALLS",
          "230m road arch collapses into sea",
          ["1,441 drones overnight — a war record. Odesa: 4 killed, 17 injured.",
           "Russian refining -45%. EU proposes €45bn for 2027. UK 1,000 drones."],
          head_size=19, det_size=12)

    # ================= PANEL ROW 2 (700-850) =================
    panel(d, 8, 700, 500, 150, USA, "USA — SENATE 56-44",
          "Peltola wins Alaska 50.1% vs 45.8%",
          ["First Alaska Native in the Senate. Democrats 56-44.",
           "Jeffries nominated Speaker 251-11, on track first Black Speaker."],
          head_size=21, det_size=14)
    panel(d, 516, 700, 500, 150, NVDA, "NVIDIA — NO COMEBACK",
          "Board: Huang will NOT return",
          ["Revenue $115.8bn (doubled), profit $65.3bn. Interim CEO Colette Kress.",
           "SEC + FBI + DOJ + Congress probing."],
          head_size=21, det_size=14)

    # ================= STRIP (850-940) =================
    d.rectangle([3, 850, W - 4, 940], fill=TEAL)
    d.text((16, 858), "CLIMATE  ·  HEALTH  ·  STORM", font=F_SANS_B(14), fill=GOLD_LT)
    strip_items = [
        "COP31 deadlocked",
        "Ebola in Congo 11,000+ cases",
        "Cyclone Akvan nears India",
        "US loses measles-free status",
    ]
    col_w = (W - 32) / 4
    sf = F_SANS_B(15)
    for i, item in enumerate(strip_items):
        cx = 16 + i * col_w
        f = sf
        while text_w(d, "•  " + item, f) > col_w - 8 and f.size > 12:
            f = F_SANS_B(f.size - 1)
        d.text((cx, 884), "•  " + item, font=f, fill=(255, 255, 255))

    # ================= TICKER (940-1024) =================
    d.rectangle([3, 940, W - 4, 1024], fill=TICK)
    ticker = ("EU-Indonesia trade pact approved  •  Jesse Jackson dies at 84  •  "
              "Dhoni retires from IPL  •  Afghanistan quake 600+ dead")
    # condensed bold so the single line stays big and readable
    tf, tsize = fit_one_line(d, ticker,
                             "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf",
                             23, W - 32, 16)
    tw = text_w(d, ticker, tf)
    d.text(((W - tw) / 2, 940 + (84 - tsize) / 2 - 4), ticker, font=tf, fill=(255, 255, 255))
    if tsize < 17:
        issues.append(f"ticker font shrunk to {tsize}pt (too small)")

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"saved {OUT}  {W}x{H}  {size} bytes")
    print("issues:", issues if issues else "none")
    return issues


if __name__ == "__main__":
    main()
