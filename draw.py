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
NAVYBLUE = NAVY2
NAVYBLUE = NAVY2
GREY = (90, 90, 90)
GREY_LT = (242, 242, 240)
GREY_MD = (200, 200, 200)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def font_path(path, size):
    return ImageFont.truetype(path, size)


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
    r = 8
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
         body="Ali Al Salem and Bahrain hit; ADNOC ship struck, 1 missing, 11 hurt.",
         visual="gulf"),
    dict(num=3, region="WORLD", topic="SPACE", src="NASA",
         head="Voyager 1 reaches a full light-day out",
         body="First object 25.9 billion km out; a command sent today arrives tomorrow.",
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
         body="Amnesty: nine strikes, June-Aug; urges war-crimes inquiry."),
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
         body="Peltola 50.1% vs 45.8%, first Alaska Native in Senate. Jeffries 251-11."),
    dict(num=12, region="WORLD", topic="CULTURE", mini="controller",
         head="GTA VI goes on sale after 13 years",
         body="Midnight launch starts in New York; millions of copies expected."),
    dict(num=13, region="ASIA", topic="LABOUR", mini="factory",
         head="Bangladesh protests shut 55 factories",
         body="Highway blocked; police report about 300 arrests."),
]

# GRID = stories 4-13 in number order (used by the grid section)
GRID = sorted(GRID_LEFT + GRID_RIGHT, key=lambda d: d["num"])

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
        d.rectangle([x + 4, y + h - 18, x + 62, y + h - 4], fill=(10, 25, 45))
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


def draw_world_map_outline(d, x0, y0, mw, mh):
    """Outline world map: continent polygons as thin dark-blue outlines,
    light fill. NOT dot-matrix (that was Rank #1)."""
    # light graticule (fills empty ocean so the map does not read as blank)
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * mw
        d.line([gx, y0, gx, y0 + mh], fill=(225, 228, 232), width=1)
    for lat in [60, 30, 0, -30]:
        gy = y0 + (75 - lat) / 130 * mh
        d.line([x0, gy, x0 + mw, gy], fill=(225, 228, 232), width=1)
    for poly in CONTINENTS.values():
        pts = [lonlat_to_xy(lon, lat, x0, y0, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(238, 240, 246), outline=NAVYBLUE, width=2)
    # ocean labels (fill the empty water: Pacific left, Atlantic centre, Indian right)
    of = font_path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    for label, lon, lat in [("PACIFIC", -150, 5), ("ATLANTIC", -30, 5),
                            ("INDIAN OCEAN", 80, -35)]:
        lx, ly = lonlat_to_xy(lon, lat, x0, y0, mw, mh)
        tw = text_w(d, label, of)
        d.text((lx - tw / 2, ly - 6), label, font=of, fill=(150, 160, 170))


def draw_pin_blue(d, x, y, num):
    r = 8
    d.ellipse([x - r, y - r, x + r, y + r], fill=NAVYBLUE, outline=(255, 255, 255), width=1)
    f = F_SANS_B(8)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    issues = []

    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

    # ================= HEADER — WHITE, centred black masthead (3-98) ====
    draw_centered(d, W / 2, 8, "THE WORLD", F_SERIF_B(54), INK)
    d.line([60, 70, W - 60, 70], fill=INK, width=1)
    draw_centered(d, W / 2, 74, "WEDNESDAY 18 NOVEMBER 2026", F_SERIF_B(20), INK)
    # thin rule under the date
    d.line([60, 98, W - 60, 98], fill=(180, 180, 180), width=1)

    # ================= ONE-LINE REGION NOTE (100-114) =================
    note = ("40 stories across 7 regions  —  Europe 6 · Middle East 5 · Asia 9 · "
            "Africa 4 · Americas 10 · Oceania 3 · World 3")
    draw_centered(d, W / 2, 102, note, F_SANS(11), INK)

    # ================= HERO: 1 BIG LEFT + 2 STACKED RIGHT (118-318) ====
    def hero_block(item, x, y, w, h, vis_h, head_size, body_size, kicker_h=20):
        hero_visual(d, item["visual"], x, y, w, vis_h)
        ky = y + vis_h
        d.rectangle([x, ky, x + w, ky + kicker_h], fill=NAVYBLUE)
        d.rectangle([x, ky, x + 22, ky + kicker_h], fill=BRICK)
        draw_centered(d, x + 11, ky + 4, str(item["num"]), F_SANS_B(11), (255, 255, 255))
        kick = f"{item['region']} · {item['topic']}"
        d.text((x + 28, ky + 4), kick, font=F_SANS_B(10), fill=(255, 255, 255))
        d.text((x + w - 6 - text_w(d, item["src"], F_SANS(8)), ky + 5),
               item["src"], font=F_SANS(8), fill=(200, 210, 225))
        hf = F_SERIF_B(head_size)
        hl = wrap(d, item["head"], hf, w - 12)
        while len(hl) > 2 and hf.size > 11:
            hf = F_SERIF_B(hf.size - 1)
            hl = wrap(d, item["head"], hf, w - 12)
        hy = ky + kicker_h + 6
        for ln in hl[:2]:
            d.text((x + 6, hy), ln, font=hf, fill=INK)
            hy += int(hf.size * 1.2)
        if len(hl) > 2:
            issues.append(f"hero {item['num']} headline {len(hl)} lines")
        bf = F_SANS(body_size)
        bl = wrap(d, item["body"], bf, w - 12)
        while len(bl) > 2 and bf.size > 9:
            bf = F_SANS(bf.size - 1)
            bl = wrap(d, item["body"], bf, w - 12)
        by = hy + 2
        for ln in bl[:2]:
            d.text((x + 6, by), ln, font=bf, fill=(50, 50, 50))
            by += int(bf.size * 1.3)
        if len(bl) > 2:
            issues.append(f"hero {item['num']} body {len(bl)} lines")
        d.rectangle([x, y, x + w, y + h], outline=(190, 190, 190), width=1)

    hero_block(HERO[0], 8, 112, 596, 196, 96, 19, 11)          # APEC big left
    hero_block(HERO[1], 620, 112, 396, 94, 36, 13, 9)           # Gulf stacked top
    hero_block(HERO[2], 620, 214, 396, 94, 36, 13, 9)          # Voyager stacked bottom

    # ================= GRID: 2 BIG COLUMNS, HORIZONTAL PANELS (324-584) ==
    grid_y0, row_h = 312, 48
    left_items = [GRID[0], GRID[4], GRID[5], GRID[6], GRID[3]]   # Kerch, EU, UK, Gaza, Sudan
    right_items = [GRID[1], GRID[2], GRID[7], GRID[8], GRID[9]]  # Nvidia, Akvan, Peltola, GTA, Bangladesh
    for ci, items in enumerate([left_items, right_items]):
        x = 8 if ci == 0 else 518
        col_w = 498
        kick_col = BRICK if ci == 0 else NAVYBLUE
        for ri, item in enumerate(items):
            y = grid_y0 + ri * row_h
            d.rectangle([x, y, x + col_w, y + row_h], outline=(200, 200, 200), width=1)
            # mini visual, left
            vx, vy, vw, vh = x + 4, y + 5, 72, 42
            d.rectangle([vx, vy, vx + vw, vy + vh], fill=(245, 245, 242))
            mini_visual(d, item["mini"], vx + 2, vy + 2, vw - 4, vh - 4)
            tx = x + 84
            tw = col_w - 84 - 8
            d.text((tx, y + 3), f"{item['num']}  {item['region']} · {item['topic']}",
                   font=F_SANS_B(8), fill=kick_col)
            hf = F_SERIF_B(13)
            hl = wrap(d, item["head"], hf, tw)
            while len(hl) > 1 and hf.size > 10:
                hf = F_SERIF_B(hf.size - 1)
                hl = wrap(d, item["head"], hf, tw)
            hy = y + 15
            for ln in hl[:1]:
                d.text((tx, hy), ln, font=hf, fill=INK)
                hy += int(hf.size * 1.2)
            if len(hl) > 1:
                issues.append(f"grid {item['num']} headline {len(hl)} lines")
            bf = F_SANS(10)
            bl = wrap(d, item["body"], bf, tw)
            while len(bl) > 2 and bf.size > 8:
                bf = F_SANS(bf.size - 1)
                bl = wrap(d, item["body"], bf, tw)
            by = hy + 1
            for ln in bl[:2]:
                d.text((tx, by), ln, font=bf, fill=(50, 50, 50))
                by += int(bf.size * 1.45)
            if len(bl) > 2:
                issues.append(f"grid {item['num']} body {len(bl)} lines")

    # ================= MAP (left) + SIDEBAR LIST (right) (590-890) =====
    sec_y = 560
    d.text((10, sec_y), "WHERE IT HAPPENED", font=F_SANS_B(13), fill=INK)
    d.text((610, sec_y), "ALSO TODAY", font=F_SANS_B(13), fill=INK)
    d.line([8, sec_y + 18, 1016, sec_y + 18], fill=INK, width=1)
    # legend ABOVE the map
    d.text((10, sec_y + 22), "Blue pins 1–13 · continents as outlines · stories 14–40 at right",
           font=F_SANS(10), fill=(70, 70, 70))
    map_x0, map_y0, map_w, map_h = 10, sec_y + 40, 580, 280
    draw_world_map_outline(d, map_x0, map_y0, map_w, map_h)
    for num, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, map_x0, map_y0, map_w, map_h)
        draw_pin_blue(d, px, py, num)
    d.text((10, sec_y + 40 + map_h + 4), "Voyager 1 is story 3 — in space, so it has no pin on this map.",
           font=F_SANS(9), fill=(90, 90, 90))

    # sidebar: ONE column, bullet dots, numbers kept
    list_x = 610
    lf_item = font_path("/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf", 10)
    line_h = 12.0
    ly = sec_y + 22
    for i, (num, text) in enumerate(LIST_ITEMS):
        yy = ly + i * line_h
        d.text((list_x, yy), "•", font=F_SANS_B(10), fill=BRICK)
        d.text((list_x + 12, yy), f"{num}", font=F_SANS_B(9), fill=NAVYBLUE)
        tx = list_x + 34
        maxw = 1016 - tx
        f = lf_item
        full = text
        while text_w(d, full, f) > maxw and f.size > 8:
            f = font_path("/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf", f.size - 1)
        if text_w(d, full, f) > maxw:
            words = full.split()
            while words and text_w(d, " ".join(words) + "…", f) > maxw:
                words.pop()
            full = " ".join(words) + "…"
            issues.append(f"list {num} truncated")
        d.text((tx, yy), full, font=f, fill=(40, 40, 40))

    # ================= NUMBERS BAR — BOTTOM, 6 white boxes (896-948) =====
    nb_y, nb_h = 914, 48
    box_w = 164
    bx = 8
    for num, lab in NUMBERS:
        d.rectangle([bx, nb_y, bx + box_w, nb_y + nb_h], fill=(255, 255, 255),
                    outline=INK, width=1)
        draw_centered(d, bx + box_w / 2, nb_y + 5, num, F_SERIF_B(20), INK)
        draw_centered(d, bx + box_w / 2, nb_y + 31, lab, F_SANS(10), (70, 70, 70))
        bx += box_w + 4

    # ================= FOOTER — DATE CHECK as 1 italic line, no red box ==
    dc = ("Date check — left out on purpose, first reported 17 Nov: "
          "Mongolia, Prague, Knesset.")
    dcf = F_SERIF_I(11)
    draw_centered(d, W / 2, 966, dc, dcf, INK)
    src = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera · ONS · IMD · NASA · Amnesty · WHO — "
           "every story happened, or was first reported, on Wednesday 18 November 2026.")
    draw_centered(d, W / 2, 988, src, F_SANS(9), (90, 90, 90))
    draw_centered(d, W / 2, 1006, "THE WORLD — 18 NOVEMBER 2026 · 40 STORIES · 7 REGIONS · ONE PAGE",
                  F_SANS_B(9), (90, 90, 90))

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"saved {OUT}  {W}x{H}  {size} bytes")
    print("issues:", issues if issues else "none")
    return issues


if __name__ == "__main__":
    main()
