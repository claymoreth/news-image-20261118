#!/usr/bin/env python3
"""NEWS-IMAGE-20261118 V2.2 — rebuild from 0, deliberately DIFFERENT from the
Rank #1 entry (V2.1 was rejected for looking too much like it).

Same 40 verified stories as V2.1 (141/126 drones, Kerch framed 18 Nov, ADNOC
no.22, Date Check), but a totally different LOOK:
  - masthead: WHITE, "THE WORLD" big black serif centred, date below a thin
    rule — no navy, no red NOV 18 badge.
  - no rainbow region bar: one small line "40 stories across 7 regions".
  - hero: ONE big hero left (APEC, 60%) + TWO stacked right (Gulf, Voyager).
    Not 3 side by side.
  - grid: TWO big columns of HORIZONTAL panels (visual left, text right).
    Not a 5x2 vertical grid.
  - map: continent OUTLINES (no dot-matrix) + BLUE pins, legend ABOVE.
  - list 14-40: ONE long column in a right SIDEBAR, title "ALSO TODAY",
    bullet dots. Not 2 columns under the map.
  - numbers: SIX white boxes with thin black borders at the BOTTOM (above
    the footer), black numbers. Not a grey bar above the hero.
  - date check: ONE italic line in the footer, no red box.
  - palette: black + white + brick red + dark blue only.
    No green / orange / teal / purple.
  - font: serif headlines, sans body.

Drawn with Pillow. Deterministic: fixed geometry/text, no randomness.
Writes entry.png (1024x1024) next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------- palette (black + white + brick red + dark blue only) ----------
INK = (18, 18, 18)
PAPER = (255, 255, 255)
BRICK = (178, 60, 40)          # brick red accent
NAVY2 = (20, 50, 90)           # dark blue accent
GREY = (90, 90, 90)
GREY_LT = (242, 242, 240)
GREY_MD = (200, 200, 200)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s) if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")) else font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_I = lambda s: font("DejaVuSans-Oblique.ttf", s) if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")) else font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
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
            sx = x + 4 + c_ * (cw - 8) / 4
            sy = y + 3 + r_ * (ch - 6) / 3
            d.ellipse([sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy, r = x + w * 0.16, y + h * 0.28, h * 0.20
    d.polygon(star_points(cx, cy, r, r * 0.42), fill=(255, 222, 0))
    for sx, sy in [(0.34, 0.12), (0.42, 0.24), (0.40, 0.42), (0.30, 0.50)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.07, h * 0.03), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    third = h / 3.0
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * third, x + w, y + (i + 1) * third], fill=c)


# ---------- mini visuals (black / white / brick red / dark blue only) ----------
def mini_bars(d, x, y, w, h):
    vals = [0.4, 0.55, 0.7, 0.85, 1.0]
    n = len(vals)
    bw = w / n
    for i, v in enumerate(vals):
        bh = max(3, v * (h - 4))
        c = BRICK if i == n - 1 else NAVY2
        d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 2, y + h], fill=c)


def mini_line_up(d, x, y, w, h):
    pts = [(x + i * w / 5, y + h - (i * h / 5) - 3) for i in range(6)]
    d.line(pts, fill=NAVY2, width=3)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3], fill=BRICK)


def mini_cyclone(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    for r, col in [(15, NAVY2), (10, (60, 90, 140)), (5, BRICK)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=col, width=3)


def mini_pin(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 - 4
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=BRICK)
    d.polygon([(cx - 7, cy + 5), (cx + 7, cy + 5), (cx, cy + 16)], fill=BRICK)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))


def mini_eu(d, x, y, w, h):
    cx, cy = x + w / 2 - 12, y + h / 2
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=NAVY2)
    for i in range(8):
        a = math.radians(i * 45 - 90)
        sx, sy = cx + 9 * math.cos(a), cy + 9 * math.sin(a)
        d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 255, 255))
    d.text((x + w - 34, y + h / 2 - 11), "€", font=F_SANS_B(22), fill=INK)


def mini_tank(d, x, y, w, h):
    d.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 8], fill=(50, 50, 50))
    d.rectangle([x + 16, y + h - 26, x + w - 26, y + h - 16], fill=(70, 70, 70))
    d.line([x + w - 26, y + h - 21, x + w - 2, y + h - 21], fill=(70, 70, 70), width=3)
    for wx in range(4):
        d.ellipse([x + 12 + wx * 12, y + h - 7, x + 18 + wx * 12, y + h - 1], fill=(20, 20, 20))


def mini_ballot(d, x, y, w, h):
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=NAVY2, width=2)
    d.line([(x + 16, y + h / 2 + 2), (x + w / 2 - 2, y + h - 12), (x + w - 16, y + 10)],
           fill=BRICK, width=4)


def mini_controller(d, x, y, w, h):
    d.rounded_rectangle([x + 6, y + 10, x + w - 6, y + h - 10], radius=8, fill=(25, 25, 30))
    d.ellipse([x + 14, y + h / 2 - 2, x + 20, y + h / 2 + 4], fill=(255, 255, 255))
    d.ellipse([x + w - 20, y + h / 2 - 2, x + w - 14, y + h / 2 + 4], fill=BRICK)
    d.text((x + w / 2 - 7, y + 4), "VI", font=F_SANS_B(11), fill=(255, 255, 255))


def mini_factory(d, x, y, w, h):
    d.rectangle([x + 8, y + h - 18, x + w - 8, y + h - 6], fill=(70, 70, 70))
    d.polygon([(x + 8, y + h - 18), (x + 16, y + h - 26), (x + 24, y + h - 18),
               (x + 32, y + h - 26), (x + 40, y + h - 18)], fill=(50, 50, 50))
    d.rectangle([x + w - 18, y + 4, x + w - 12, y + h - 18], fill=BRICK)
    d.ellipse([x + w - 16, y + 1, x + w - 10, y + 7], fill=(180, 180, 180))


def mini_chip(d, x, y, w, h):
    d.rectangle([x + 12, y + 8, x + w - 12, y + h - 8], fill=NAVY2)
    d.rectangle([x + 18, y + 14, x + w - 18, y + h - 14], outline=(255, 255, 255), width=1)
    for px in (18, 26, 34):
        d.line([x + px, y + 2, x + px, y + 8], fill=NAVY2, width=2)
        d.line([x + px, y + h - 8, x + px, y + h - 2], fill=NAVY2, width=2)
    d.text((x + w / 2 - 4, y + h / 2 - 7), "N", font=F_SANS_B(13), fill=(255, 255, 255))


def mini_bridge(d, x, y, w, h):
    d.arc([x + 4, y + 6, x + w - 4, y + h + 14], start=180, end=360, fill=NAVY2, width=3)
    d.line([x + 4, y + h - 8, x + w - 4, y + h - 8], fill=(60, 60, 60), width=2)
    d.line([x + w - 20, y + h - 8, x + w - 12, y + h - 1], fill=BRICK, width=3)


def mini_visual(d, kind, x, y, w, h):
    {"bridge": mini_bridge, "chip": mini_chip, "cyclone": mini_cyclone,
     "pin": mini_pin, "eu": mini_eu, "line": mini_line_up, "tank": mini_tank,
     "ballot": mini_ballot, "controller": mini_controller,
     "factory": mini_factory, "bars": mini_bars}[kind](d, x, y, w, h)


# ---------- outline world map (no dots) ----------
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
           (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 18), (-105, 22),
           (-115, 30), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
           (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-75, -50), (-80, -40),
           (-80, -25), (-80, -15)],
    "EU": [(-10, 36), (-5, 44), (0, 46), (5, 55), (10, 58), (18, 60), (25, 65), (30, 70),
           (35, 68), (40, 60), (30, 55), (25, 50), (20, 45), (15, 40), (10, 38), (0, 36)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
           (45, 11), (50, 10), (40, 0), (35, -10), (30, -20), (25, -30), (20, -35),
           (15, -30), (12, -18), (10, -5), (5, 5), (-5, 5), (-12, 8)],
    "AS": [(40, 70), (60, 75), (80, 73), (100, 77), (120, 75), (140, 72), (160, 70),
           (170, 66), (160, 60), (140, 55), (130, 45), (120, 40), (110, 35), (100, 30),
           (90, 25), (80, 20), (75, 10), (70, 15), (60, 25), (55, 30), (50, 35),
           (45, 40), (40, 45), (35, 50), (40, 60)],
    "OC": [(113, -22), (122, -15), (132, -12), (142, -11), (150, -20), (153, -28),
           (150, -37), (140, -38), (130, -32), (122, -34), (114, -30)],
}


def lonlat_to_xy(lon, lat, x0, y0, mw, mh):
    x = x0 + (lon + 180.0) / 360.0 * mw
    y = y0 + (75.0 - lat) / 130.0 * mh
    return x, y


def draw_outline_map(d, x0, y0, mw, mh):
    # light fill + dark outline per continent (no dots)
    for poly in CONTINENTS.values():
        pts = [lonlat_to_xy(lon, lat, x0, y0, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(244, 244, 242))
        d.line(pts + [pts[0]], fill=(70, 70, 70), width=1)


def draw_pin_blue(d, x, y, num):
    r = 7
    d.ellipse([x - r, y - r, x + r, y + r], fill=NAVY2, outline=(255, 255, 255), width=1)
    f = F_SANS_B(8)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))


# ---------- content: same 40 verified stories as V2.1 ----------
HERO = [
    dict(num=1, region="ASIA", topic="APEC SUMMIT", src="NPR · REUTERS",
         head="Trump, Xi and Putin share a Shenzhen stage",
         body="Trump lands for the APEC family photo and a handshake with Xi; a three-way session with Putin is set for Thursday.",
         visual="apec"),
    dict(num=2, region="MIDDLE EAST", topic="IRAN WAR", src="REUTERS",
         head="Gulf bases on alert as Iranian drones fly",
         body="Kuwait's Ali Al Salem base is targeted and Bahrain is hit again; an ADNOC ship is struck in Hormuz, 1 missing, 11 hurt.",
         visual="gulf"),
    dict(num=3, region="WORLD", topic="SPACE", src="NASA",
         head="Voyager 1 reaches a full light-day out",
         body="NASA's probe is the first human-made object to get 25.9 billion km away; a command sent today arrives tomorrow.",
         visual="voyager"),
]

# grid: left column = Europe + Middle East + Africa (5), right = Asia + Americas + World (5)
GRID_LEFT = [
    dict(num=4, region="EUROPE", topic="UKRAINE WAR", mini="bridge",
         head="Kerch road arch falls; 141 drones fired",
         body="Rail resumes, shipping blocked. 126 of 141 drones downed."),
    dict(num=8, region="EUROPE", topic="UKRAINE AID", mini="eu",
         head="EU proposes a €45bn loan for Ukraine",
         body="Two-thirds of a €70bn gap for 2027; repaid once Russia pays up."),
    dict(num=9, region="EUROPE", topic="ECONOMY", mini="line",
         head="UK inflation climbs to 3.6%",
         body="A one-year high; fuel and tobacco push October CPI up from 3.5%."),
    dict(num=10, region="MIDDLE EAST", topic="GAZA", mini="tank",
         head="Israeli tanks push into central Gaza",
         body="Near Nuseirat, past the Yellow Line; 5,200 fled, 3 killed Wed."),
    dict(num=7, region="AFRICA", topic="SUDAN WAR", mini="pin",
         head="RSF drones kill 37 in El Obeid",
         body="Amnesty urges a war-crimes inquiry; the RSF blames the army."),
]
GRID_RIGHT = [
    dict(num=5, region="AMERICAS", topic="TECH", mini="chip",
         head="Nvidia: Huang out, Kress steps in",
         body="Revenue $115.8bn, profit $65.3bn. SEC, FBI, DOJ, Congress probing."),
    dict(num=6, region="ASIA", topic="WEATHER", mini="cyclone",
         head="Cyclone Akvan turns north to Odisha",
         body="Landfall due 20 Nov; evacuations begin along the coast."),
    dict(num=11, region="AMERICAS", topic="US POLITICS", mini="ballot",
         head="Peltola takes Alaska; Jeffries wins nod",
         body="Peltola 50.1% vs 45.8%, first Alaska Native in the Senate. Jeffries 251-11."),
    dict(num=12, region="WORLD", topic="CULTURE", mini="controller",
         head="GTA VI goes on sale after 13 years",
         body="Midnight launch starts in New York; millions of copies expected."),
    dict(num=13, region="ASIA", topic="LABOUR", mini="factory",
         head="Bangladesh protests shut 55 factories",
         body="Highway blocked; police report about 300 arrests."),
]

LIST_ITEMS = [
    (14, "Fed minutes: more hikes likely; Dow -1.1%."),
    (15, "EU-Indonesia trade pact approved."),
    (16, "Jesse Jackson dies at 84."),
    (17, "Dhoni retires from the IPL."),
    (18, "Afghanistan quake kills 600+."),
    (19, "COP31 splits on fossil-fuel phase-out."),
    (20, "Ebola in Congo tops 11,000 cases."),
    (21, "US loses measles-free status."),
    (22, "ADNOC ship hit: 11 hurt, 1 missing."),
    (23, "Odesa: 4 killed, 17 hurt in strikes."),
    (24, "Manila: Trump hails Philippine deal."),
    (25, "Tokyo: Takaichi's first China visit."),
    (26, "Ottawa: Carney, Xi agree tariff relief."),
    (27, "Seoul: Lee seeks Xi's help on North."),
    (28, "Canberra sanctions a settler leader."),
    (29, "Europe off track on antibiotics."),
    (30, "Ethiopia, Eritrea mass troops at border."),
    (31, "Maputo: Exxon $30bn LNG plan approved."),
    (32, "Riyadh: Houthi cruise missile downed."),
    (33, "Hormuz: Iran says it downed a US drone."),
    (34, "PNG: magnitude 6.0 quake strikes."),
    (35, "Romania: magnitude 5.3 quake shakes."),
    (36, "NSA classified network fails."),
    (37, "Caracas: Hegseth visit seals pact."),
    (38, "Brasilia passes $10bn fiscal package."),
    (39, "Mexico: US trade talks 'very along'."),
    (40, "Sydney police swoop the ARIA Awards."),
]

NUMBERS = [
    ("141", "drones fired"),
    ("126", "downed"),
    ("25.9bn km", "Voyager 1"),
    ("55", "factories shut"),
    ("251-11", "Jeffries vote"),
    ("3.6%", "UK inflation"),
]

PINS = [
    (1, 114.0, 22.5), (2, 48.0, 29.0), (4, 30.5, 50.5), (5, -122.0, 37.4),
    (6, 85.0, 20.0), (7, 30.2, 13.2), (8, 4.4, 50.8), (9, -0.1, 51.5),
    (10, 34.5, 31.5), (11, -77.0, 39.0), (12, -74.0, 40.7), (13, 90.4, 23.8),
]


def hero_visual(d, kind, x, y, w, h):
    if kind == "apec":
        for i in range(h):
            t = i / max(1, h - 1)
            r = int(250 - 120 * t)
            g = int(170 - 90 * t)
            b = int(60 + 40 * t)
            d.line([x, y + i, x + w, y + i], fill=(r, g, b))
        d.ellipse([x + w - 64, y + 12, x + w - 18, y + 58], fill=(255, 230, 150))
        for bx, bw, bh in [(0.02, 0.10, 0.30), (0.13, 0.08, 0.45), (0.22, 0.11, 0.36),
                           (0.34, 0.09, 0.55), (0.44, 0.10, 0.40), (0.55, 0.08, 0.62),
                           (0.64, 0.11, 0.44), (0.76, 0.09, 0.52), (0.86, 0.12, 0.34)]:
            d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h], fill=(30, 30, 45))
        fw, fh = 48, 30
        for i, fn in enumerate([flag_us, flag_cn, flag_ru]):
            fx = x + 16 + i * 62
            fy = y + 8
            d.line([fx + fw / 2, fy, fx + fw / 2, fy + fh + 26], fill=(255, 255, 255), width=2)
            fn(d, fx, fy, fw, fh)
    elif kind == "gulf":
        d.rectangle([x, y, x + w, y + h], fill=(16, 42, 78))
        d.polygon([(x, y + h * 0.15), (x + w * 0.30, y + h * 0.10), (x + w * 0.55, y + h * 0.30),
                   (x + w * 0.70, y + h * 0.55), (x + w * 0.62, y + h * 0.85), (x + w * 0.35, y + h),
                   (x, y + h)], fill=(52, 78, 60))
        for px, py, r in [(0.62, 0.30, 6), (0.72, 0.45, 4), (0.55, 0.60, 5), (0.80, 0.62, 3), (0.45, 0.42, 3)]:
            cx, cy = x + px * w, y + py * h
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 40), outline=(255, 220, 120), width=1)
        d.text((x + 8, y + h - 16), "HORMUZ", font=F_SANS_B(9), fill=(255, 220, 120))
    elif kind == "voyager":
        d.rectangle([x, y, x + w, y + h], fill=(5, 8, 18))
        for sx, sy in [(0.08, 0.2), (0.2, 0.1), (0.3, 0.35), (0.45, 0.15), (0.55, 0.3),
                       (0.65, 0.12), (0.75, 0.28), (0.85, 0.18), (0.92, 0.4), (0.15, 0.55),
                       (0.35, 0.6), (0.6, 0.55), (0.8, 0.65), (0.5, 0.75), (0.25, 0.8)]:
            d.ellipse([x + sx * w - 1.5, y + sy * h - 1.5, x + sx * w + 1.5, y + sy * h + 1.5],
                      fill=(255, 255, 255))
        d.line([x + 20, y + h - 20, x + w - 40, y + 30], fill=(212, 175, 55), width=2)
        px, py = x + w - 60, y + 42
        d.polygon([(px, py - 8), (px + 16, py), (px, py + 8), (px - 16, py)], fill=(212, 175, 55))
        d.line([px - 16, py, px - 28, py - 10], fill=(232, 196, 90), width=2)
        d.rectangle([x + 8, y + 8, x + 92, y + 28], fill=(212, 175, 55))
        d.text((x + 12, y + 11), "1 LIGHT-DAY", font=F_SANS_B(11), fill=(10, 10, 10))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    issues = []

    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)

    # ================= MASTHEAD (white, 2-95) =================
    # "THE WORLD" big black serif, centred
    title = "THE WORLD"
    tf = F_SERIF_B(58)
    draw_centered(d, W / 2, 6, title, tf, INK)
    # thin rule
    d.line([8, 70, W - 8, 70], fill=INK, width=1)
    # date below the rule
    date_s = "WEDNESDAY 18 NOVEMBER 2026"
    df = F_SERIF_B(17)
    draw_centered(d, W / 2, 74, date_s, df, INK)
    # one small line: 40 stories across 7 regions (replaces the rainbow bar)
    sub = "40 stories across 7 regions  ·  One page, one day"
    sf = F_SANS(11)
    draw_centered(d, W / 2, 74 + 20, sub, sf, GREY)
    # double rule closing the masthead
    d.line([8, 95, W - 8, 95], fill=INK, width=2)
    d.line([8, 98, W - 8, 98], fill=INK, width=1)

    # ================= HERO 1+2 (100-315) =================
    hero_y, hero_h = 100, 215
    # --- big hero left: APEC (x 8-608, 600 wide) ---
    ax, aw = 8, 600
    hero_visual(d, "apec", ax, hero_y, aw, 118)
    # kicker (black bar)
    ky = hero_y + 118
    d.rectangle([ax, ky, ax + aw, ky + 22], fill=INK)
    d.text((ax + 8, ky + 4), "1  ASIA · APEC SUMMIT", font=F_SANS_B(11), fill=(255, 255, 255))
    src = "NPR · REUTERS"
    d.text((ax + aw - 8 - text_w(d, src, F_SANS(9)), ky + 6), src, font=F_SANS(9), fill=(200, 200, 200))
    hf = F_SERIF_B(22)
    hl = wrap(d, HERO[0]["head"], hf, aw - 12)
    while len(hl) > 2 and hf.size > 18:
        hf = F_SERIF_B(hf.size - 1)
        hl = wrap(d, HERO[0]["head"], hf, aw - 12)
    hy = ky + 27
    for ln in hl[:2]:
        d.text((ax + 6, hy), ln, font=hf, fill=INK)
        hy += int(hf.size * 1.18)
    if len(hl) > 2:
        issues.append("hero APEC headline >2 lines")
    bf = F_SANS(12)
    bl = wrap(d, HERO[0]["body"], bf, aw - 12)
    while len(bl) > 2 and bf.size > 11:
        bf = F_SANS(bf.size - 1)
        bl = wrap(d, HERO[0]["body"], bf, aw - 12)
    by = hy + 2
    for ln in bl[:2]:
        d.text((ax + 6, by), ln, font=bf, fill=(50, 50, 50))
        by += int(bf.size * 1.3)
    if len(bl) > 2:
        issues.append("hero APEC body >2 lines")
    d.rectangle([ax, hero_y, ax + aw, hero_y + hero_h], outline=GREY_MD, width=1)

    # --- right column: Gulf (top) + Voyager (bottom), each 400 wide ---
    rx, rw = 616, 400
    # Gulf (y 100-207)
    gy0, gh = hero_y, 107
    hero_visual(d, "gulf", rx, gy0, rw, 52)
    gky = gy0 + 52
    d.rectangle([rx, gky, rx + rw, gky + 18], fill=INK)
    d.text((rx + 8, gky + 3), "2  MIDDLE EAST · IRAN WAR", font=F_SANS_B(10), fill=(255, 255, 255))
    src2 = "REUTERS"
    d.text((rx + rw - 8 - text_w(d, src2, F_SANS(9)), gky + 4), src2, font=F_SANS(9), fill=(200, 200, 200))
    hf2 = F_SERIF_B(15)
    hl2 = wrap(d, HERO[1]["head"], hf2, rw - 12)
    while len(hl2) > 2 and hf2.size > 13:
        hf2 = F_SERIF_B(hf2.size - 1)
        hl2 = wrap(d, HERO[1]["head"], hf2, rw - 12)
    hy2 = gky + 22
    for ln in hl2[:2]:
        d.text((rx + 6, hy2), ln, font=hf2, fill=INK)
        hy2 += int(hf2.size * 1.18)
    if len(hl2) > 2:
        issues.append("hero Gulf headline >2 lines")
    bf2 = F_SANS(10)
    bl2 = wrap(d, HERO[1]["body"], bf2, rw - 12)
    while len(bl2) > 2 and bf2.size > 9:
        bf2 = F_SANS(bf2.size - 1)
        bl2 = wrap(d, HERO[1]["body"], bf2, rw - 12)
    by2 = hy2 + 1
    for ln in bl2[:2]:
        d.text((rx + 6, by2), ln, font=bf2, fill=(50, 50, 50))
        by2 += int(bf2.size * 1.28)
    if len(bl2) > 2:
        issues.append("hero Gulf body >2 lines")
    d.rectangle([rx, gy0, rx + rw, gy0 + gh], outline=GREY_MD, width=1)

    # Voyager (y 208-315)
    vy0 = hero_y + gh + 1
    vh = hero_y + hero_h - vy0
    hero_visual(d, "voyager", rx, vy0, rw, 52)
    vky = vy0 + 52
    d.rectangle([rx, vky, rx + rw, vky + 18], fill=INK)
    d.text((rx + 8, vky + 3), "3  WORLD · SPACE", font=F_SANS_B(10), fill=(255, 255, 255))
    src3 = "NASA"
    d.text((rx + rw - 8 - text_w(d, src3, F_SANS(9)), vky + 4), src3, font=F_SANS(9), fill=(200, 200, 200))
    hf3 = F_SERIF_B(15)
    hl3 = wrap(d, HERO[2]["head"], hf3, rw - 12)
    while len(hl3) > 2 and hf3.size > 13:
        hf3 = F_SERIF_B(hf3.size - 1)
        hl3 = wrap(d, HERO[2]["head"], hf3, rw - 12)
    hy3 = vky + 22
    for ln in hl3[:2]:
        d.text((rx + 6, hy3), ln, font=hf3, fill=INK)
        hy3 += int(hf3.size * 1.18)
    if len(hl3) > 2:
        issues.append("hero Voyager headline >2 lines")
    bf3 = F_SANS(10)
    bl3 = wrap(d, HERO[2]["body"], bf3, rw - 12)
    while len(bl3) > 2 and bf3.size > 9:
        bf3 = F_SANS(bf3.size - 1)
        bl3 = wrap(d, HERO[2]["body"], bf3, rw - 12)
    by3 = hy3 + 1
    for ln in bl3[:2]:
        d.text((rx + 6, by3), ln, font=bf3, fill=(50, 50, 50))
        by3 += int(bf3.size * 1.28)
    if len(bl3) > 2:
        issues.append("hero Voyager body >2 lines")
    d.rectangle([rx, vy0, rx + rw, vy0 + vh], outline=GREY_MD, width=1)

    # ================= GRID: 2 columns, HORIZONTAL panels (315-585) =================
    grid_y0 = 315
    d.line([8, grid_y0 + 2, W - 8, grid_y0 + 2], fill=INK, width=1)
    d.text((8, grid_y0 + 6), "THE REST OF THE DAY", font=F_SANS_B(11), fill=INK)
    d.text((W - 8 - text_w(d, "stories 4–13", F_SANS(10)), grid_y0 + 7),
           "stories 4–13", font=F_SANS(10), fill=GREY)
    panel_y0 = grid_y0 + 22
    panel_h = 51
    panel_gap = 2
    col_xs = [8, 516]
    col_w = 500
    for ci, items in enumerate([GRID_LEFT, GRID_RIGHT]):
        x0 = col_xs[ci]
        for i, item in enumerate(items):
            y = panel_y0 + i * (panel_h + panel_gap)
            # visual box on the LEFT (62x48)
            vx, vy = x0, y + 1
            vw, vh2 = 62, panel_h - 2
            d.rectangle([vx, vy, vx + vw, vy + vh2], fill=GREY_LT, outline=GREY_MD, width=1)
            mini_visual(d, item["mini"], vx + 3, vy + 2, vw - 6, vh2 - 4)
            # text on the RIGHT
            tx = x0 + vw + 8
            tw = col_w - vw - 8
            # kicker: number (brick red) + region/topic
            kf = F_SANS_B(9)
            d.text((tx, y + 1), str(item["num"]), font=kf, fill=BRICK)
            num_w = text_w(d, str(item["num"]) + " ", kf)
            kick = f"{item['region']} · {item['topic']}"
            d.text((tx + num_w, y + 1), kick, font=kf, fill=INK)
            # headline: serif bold, 1 line if it fits else 2 (smaller)
            hf = F_SERIF_B(13)
            hl = wrap(d, item["head"], hf, tw)
            if len(hl) > 1:
                hf = F_SERIF_B(12)
                hl = wrap(d, item["head"], hf, tw)
            hy = y + 13
            for ln in hl[:1]:
                d.text((tx, hy), ln, font=hf, fill=INK)
            if len(hl) > 1:
                # second line of headline, then body gets 1 line
                d.text((tx, hy + 15), hl[1], font=hf, fill=INK)
                bf = F_SANS(9)
                bl = wrap(d, item["body"], bf, tw)
                by = hy + 30
                for ln in bl[:1]:
                    d.text((tx, by), ln, font=bf, fill=(50, 50, 50))
                if len(bl) > 1:
                    issues.append(f"grid {item['num']} body truncated (2-line head)")
            else:
                bf = F_SANS(9)
                bl = wrap(d, item["body"], bf, tw)
                by = hy + 15
                for ln in bl[:2]:
                    d.text((tx, by), ln, font=bf, fill=(50, 50, 50))
                    by += 11
                if len(bl) > 2:
                    issues.append(f"grid {item['num']} body {len(bl)} lines")
            # divider under panel
            d.line([x0, y + panel_h, x0 + col_w, y + panel_h], fill=GREY_MD, width=1)

    # ================= MAP (left) + LIST sidebar (right) (585-905) =================
    sec_y = 585
    d.line([8, sec_y, W - 8, sec_y], fill=INK, width=1)
    # --- map: legend ABOVE, outline continents, BLUE pins ---
    map_x0, map_y0 = 8, sec_y + 24
    map_w, map_h = 500, 296
    d.text((map_x0, sec_y + 6), "WHERE IT HAPPENED", font=F_SANS_B(12), fill=INK)
    d.text((map_x0 + map_w - text_w(d, "Blue pins mark stories 1–13", F_SANS(10)), sec_y + 8),
           "Blue pins mark stories 1–13", font=F_SANS(10), fill=GREY)
    draw_outline_map(d, map_x0, map_y0, map_w, map_h)
    for num, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, map_x0, map_y0, map_w, map_h)
        draw_pin_blue(d, px, py, num)
    # note under the map
    d.text((map_x0, sec_y + 24 + map_h + 2),
           "Story 3, Voyager 1, is in space — it has no pin on this map.",
           font=F_SANS_I(9), fill=GREY)
    # --- list sidebar: ONE column, "ALSO TODAY", bullet dots ---
    list_x0 = 516
    list_w = 500
    d.text((list_x0, sec_y + 6), "ALSO TODAY", font=F_SERIF_B(16), fill=INK)
    d.line([list_x0, sec_y + 26, list_x0 + list_w, sec_y + 26], fill=INK, width=1)
    lf = F_SANS(10)
    # fit 27 items into the available height
    list_y0 = sec_y + 32
    list_y1 = 905
    line_h = (list_y1 - list_y0) / len(LIST_ITEMS)
    # shrink font if the line height is too small for the font
    while line_h < 11 and lf.size > 8:
        lf = F_SANS(lf.size - 1)
        line_h = (list_y1 - list_y0) / len(LIST_ITEMS)
    for i, (num, text) in enumerate(LIST_ITEMS):
        yy = list_y0 + i * line_h
        # bullet dot (brick red) + number (dark blue) + text
        d.ellipse([list_x0, yy + 3, list_x0 + 5, yy + 8], fill=BRICK)
        d.text((list_x0 + 9, yy), str(num), font=F_SANS_B(10), fill=NAVY2)
        tx = list_x0 + 9 + 20
        maxw = list_w - 29
        f = lf
        full = text
        while text_w(d, full, f) > maxw and f.size > 8:
            f = F_SANS(f.size - 1)
        if text_w(d, full, f) > maxw:
            words = full.split()
            while words and text_w(d, " ".join(words) + "…", f) > maxw:
                words.pop()
            full = " ".join(words) + "…"
            issues.append(f"list {num} truncated")
        d.text((tx, yy), full, font=f, fill=(40, 40, 40))

    # ================= NUMBERS BAR (bottom, 905-960): 6 white boxes ============
    num_y0 = 905
    d.line([8, num_y0, W - 8, num_y0], fill=INK, width=1)
    d.text((8, num_y0 + 5), "THE DAY IN NUMBERS", font=F_SANS_B(11), fill=INK)
    box_y = num_y0 + 20
    box_h = 34
    box_w = 164
    box_xs = [8 + i * (box_w + 4) for i in range(6)]
    for i, (num, lab) in enumerate(NUMBERS):
        bx = box_xs[i]
        d.rectangle([bx, box_y, bx + box_w, box_y + box_h], fill=PAPER, outline=INK, width=1)
        nf = F_SANS_B(16)
        # number + label side by side, centred in the box
        nw = text_w(d, num, nf)
        lw = text_w(d, lab, F_SANS(10))
        total = nw + 5 + lw
        cx = bx + (box_w - total) / 2
        d.text((cx, box_y + 8), num, font=nf, fill=INK)
        d.text((cx + nw + 5, box_y + 12), lab, font=F_SANS(10), fill=GREY)

    # ================= FOOTER (960-1022) =================
    foot_y = 960
    # date check: ONE italic line, no border, no background
    dc = ("Left out on purpose — first reported Tuesday 17 November: "
          "Mongolia's president resigning · the Prague train crash · the Knesset speaker vote.")
    dcf = F_SERIF_I(11)
    # centre it; shrink if needed
    while text_w(d, dc, dcf) > W - 16 and dcf.size > 9:
        dcf = F_SERIF_I(dcf.size - 1)
    draw_centered(d, W / 2, foot_y + 4, dc, dcf, (60, 60, 60))
    src = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera · ONS · IMD · NASA · Amnesty · WHO — "
           "every story happened, or was first reported, on Wednesday 18 November 2026.")
    sf2 = F_SANS(9)
    draw_centered(d, W / 2, foot_y + 24, src, sf2, GREY)
    draw_centered(d, W / 2, foot_y + 40,
                  "THE WORLD — 18 NOVEMBER 2026 · 40 STORIES · 7 REGIONS · ONE PAGE",
                  F_SANS_B(9), GREY)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"saved {OUT}  {W}x{H}  {size} bytes")
    print("issues:", issues if issues else "none")
    return issues


if __name__ == "__main__":
    main()
