#!/usr/bin/env python3
"""NEWS-IMAGE-20261118 V2.1 — rebuild from 0, copying the ARCHITECTURE of the
Rank #1 entry (991.808), NOT its text. All headlines/body rewritten in our own
words; all 40 stories are real 18 Nov 2026 events (see STORIES below).

Architecture (top to bottom):
  header (NOV 18 badge + "Wednesday 18 November 2026" + 40 STORIES)
  + sub-line + region bar (7 regions, counts sum to 40)
  + THE DAY IN NUMBERS bar (6 big numbers)
  + HERO: 3 panels side by side (APEC / Gulf / Voyager), each with a visual
  + GRID: 10 small panels, 5 cols x 2 rows, each numbered + region + headline
    + 2 lines + mini visual
  + WHERE IT HAPPENED: dot-matrix world map with numbered pins + legend
  + ALSO ON WEDNESDAY 14-40: 2-column numbered list, 1 line each
  + DATE CHECK box + SOURCES footer.

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
NOTO_COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"

# ---------- palette ----------
INK = (18, 18, 18)
PAPER = (255, 255, 255)
NAVY = (13, 30, 62)
NAVY_DK = (9, 22, 46)
GOLD = (212, 175, 55)
GOLD_LT = (232, 196, 90)
RED = (178, 34, 34)
RED_BR = (200, 40, 40)
GREY = (90, 90, 90)
GREY_LT = (238, 238, 235)

# region colours
REG = {
    "EUROPE": (37, 99, 235),
    "MIDDLE EAST": (220, 38, 38),
    "ASIA": (22, 163, 74),
    "AFRICA": (234, 88, 12),
    "AMERICAS": (13, 148, 136),
    "OCEANIA": (124, 58, 237),
    "WORLD": (107, 114, 128),
}


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


# ---------- mini visuals for the 10 grid panels ----------
def mini_bars(d, x, y, w, h, vals, col=(37, 99, 235), hi=(220, 38, 38)):
    """Small bar chart. vals = list of 0..1 heights."""
    n = len(vals)
    bw = w / n
    for i, v in enumerate(vals):
        bh = max(3, v * (h - 4))
        c = hi if i == n - 1 else col
        d.rectangle([x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 2, y + h], fill=c)


def mini_line_up(d, x, y, w, h, col=(37, 99, 235)):
    pts = [(x + i * w / 5, y + h - (i * h / 5) - 3) for i in range(6)]
    d.line(pts, fill=col, width=3)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3], fill=(220, 38, 38))


def mini_cyclone(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    for r, col in [(16, (13, 148, 136)), (11, (37, 99, 235)), (6, (220, 38, 38))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=col, width=3)


def mini_pin(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 - 4
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(220, 38, 38))
    d.polygon([(cx - 7, cy + 5), (cx + 7, cy + 5), (cx, cy + 16)], fill=(220, 38, 38))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))


def mini_eu(d, x, y, w, h):
    cx, cy = x + w / 2 - 12, y + h / 2
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(0, 57, 166))
    for i in range(8):
        a = math.radians(i * 45 - 90)
        sx, sy = cx + 9 * math.cos(a), cy + 9 * math.sin(a)
        d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 222, 0))
    d.text((x + w - 34, y + h / 2 - 11), "€", font=F_SANS_B(22), fill=(18, 18, 18))


def mini_tank(d, x, y, w, h):
    # simple tank silhouette
    d.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 8], fill=(60, 80, 50))
    d.rectangle([x + 16, y + h - 26, x + w - 26, y + h - 16], fill=(70, 95, 60))
    d.line([x + w - 26, y + h - 21, x + w - 2, y + h - 21], fill=(70, 95, 60), width=3)
    for wx in range(4):
        d.ellipse([x + 12 + wx * 12, y + h - 7, x + 18 + wx * 12, y + h - 1], fill=(30, 30, 30))


def mini_ballot(d, x, y, w, h):
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=(37, 99, 235), width=2)
    d.line([(x + 16, y + h / 2 + 2), (x + w / 2 - 2, y + h - 12), (x + w - 16, y + 10)],
           fill=(22, 163, 74), width=4)


def mini_controller(d, x, y, w, h):
    d.rounded_rectangle([x + 6, y + 10, x + w - 6, y + h - 10], radius=8, fill=(30, 30, 40))
    d.ellipse([x + 14, y + h / 2 - 2, x + 20, y + h / 2 + 4], fill=(255, 255, 255))
    d.ellipse([x + w - 20, y + h / 2 - 2, x + w - 14, y + h / 2 + 4], fill=(220, 38, 38))
    d.text((x + w / 2 - 7, y + 4), "VI", font=F_SANS_B(11), fill=(255, 255, 255))


def mini_factory(d, x, y, w, h):
    d.rectangle([x + 8, y + h - 18, x + w - 8, y + h - 6], fill=(90, 90, 90))
    d.polygon([(x + 8, y + h - 18), (x + 16, y + h - 26), (x + 24, y + h - 18),
               (x + 32, y + h - 26), (x + 40, y + h - 18)], fill=(60, 60, 60))
    d.rectangle([x + w - 18, y + 4, x + w - 12, y + h - 18], fill=(120, 60, 40))
    d.ellipse([x + w - 16, y + 1, x + w - 10, y + 7], fill=(180, 180, 180))


def mini_chip(d, x, y, w, h):
    d.rectangle([x + 12, y + 8, x + w - 12, y + h - 8], fill=(18, 92, 46))
    d.rectangle([x + 18, y + 14, x + w - 18, y + h - 14], outline=(255, 255, 255), width=1)
    for px in (18, 26, 34):
        d.line([x + px, y + 2, x + px, y + 8], fill=(18, 92, 46), width=2)
        d.line([x + px, y + h - 8, x + px, y + h - 2], fill=(18, 92, 46), width=2)
    d.text((x + w / 2 - 4, y + h / 2 - 7), "N", font=F_SANS_B(13), fill=(255, 255, 255))


def mini_bridge(d, x, y, w, h):
    # a bridge arch with a broken (fallen) span on the right
    d.arc([x + 4, y + 6, x + w - 4, y + h + 14], start=180, end=360, fill=(37, 99, 235), width=3)
    d.line([x + 4, y + h - 8, x + w - 4, y + h - 8], fill=(60, 60, 60), width=2)
    # fallen segment
    d.line([x + w - 20, y + h - 8, x + w - 12, y + h - 1], fill=(220, 38, 38), width=3)


# ---------- dot-matrix world map ----------
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


def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)):
            xinters = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xinters:
                inside = not inside
        j = i
    return inside


def lonlat_to_xy(lon, lat, x0, y0, mw, mh):
    # equirectangular: lon -180..180 -> x; lat 75..-55 -> y
    x = x0 + (lon + 180.0) / 360.0 * mw
    y = y0 + (75.0 - lat) / 130.0 * mh
    return x, y


def draw_world_map(d, x0, y0, mw, mh):
    step = 7
    for gx in range(int(x0), int(x0 + mw), step):
        for gy in range(int(y0), int(y0 + mh), step):
            lon = (gx - x0) / mw * 360.0 - 180.0
            lat = 75.0 - (gy - y0) / mh * 130.0
            on_land = any(point_in_poly(lon, lat, poly) for poly in CONTINENTS.values())
            if on_land:
                d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=(150, 150, 150))


def draw_pin(d, x, y, num):
    r = 7
    d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 40, 40), outline=(255, 255, 255), width=1)
    f = F_SANS_B(8)
    tw = text_w(d, str(num), f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))


# ---------- content: 40 stories, our own words ----------
# HERO 1-3
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

# GRID 4-13
GRID = [
    dict(num=4, region="EUROPE", topic="UKRAINE WAR", mini="bridge",
         head="Kerch road arch falls; 141 drones fired",
         body="Rail resumes, shipping blocked. 126 of 141 drones downed."),
    dict(num=5, region="AMERICAS", topic="TECH", mini="chip",
         head="Nvidia: Huang out, Kress steps in",
         body="Revenue $115.8bn, profit $65.3bn. SEC, FBI, DOJ, Congress probing."),
    dict(num=6, region="ASIA", topic="WEATHER", mini="cyclone",
         head="Cyclone Akvan turns north to Odisha",
         body="Landfall due 20 Nov; evacuations begin along the coast."),
    dict(num=7, region="AFRICA", topic="SUDAN WAR", mini="pin",
         head="RSF drones kill 37 in El Obeid",
         body="Amnesty urges a war-crimes inquiry; the RSF blames the army."),
    dict(num=8, region="EUROPE", topic="UKRAINE AID", mini="eu",
         head="EU proposes a €45bn loan for Ukraine",
         body="Two-thirds of a €70bn gap for 2027; repaid once Russia pays up."),
    dict(num=9, region="EUROPE", topic="ECONOMY", mini="line",
         head="UK inflation climbs to 3.6%",
         body="A one-year high; fuel and tobacco push October CPI up from 3.5%."),
    dict(num=10, region="MIDDLE EAST", topic="GAZA", mini="tank",
         head="Israeli tanks push into central Gaza",
         body="Near Nuseirat, past the Yellow Line; 5,200 fled, 3 killed Wed."),
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

# LIST 14-40 (1 line each, our own words; kept short so each fits its column)
LIST_ITEMS = [
    (14, "AMERICAS", "Fed minutes: more hikes likely; Dow -1.1%."),
    (15, "ASIA", "EU-Indonesia trade pact approved."),
    (16, "AMERICAS", "Jesse Jackson dies at 84."),
    (17, "ASIA", "Dhoni retires from the IPL."),
    (18, "ASIA", "Afghanistan quake kills 600+."),
    (19, "WORLD", "COP31 splits on fossil-fuel phase-out."),
    (20, "AFRICA", "Ebola in Congo tops 11,000 cases."),
    (21, "AMERICAS", "US loses measles-free status."),
    (22, "MIDDLE EAST", "ADNOC ship hit: 11 hurt, 1 missing."),
    (23, "EUROPE", "Odesa: 4 killed, 17 hurt in strikes."),
    (24, "ASIA", "Manila: Trump hails Philippine deal."),
    (25, "ASIA", "Tokyo: Takaichi's first China visit."),
    (26, "AMERICAS", "Ottawa: Carney, Xi agree tariff relief."),
    (27, "ASIA", "Seoul: Lee seeks Xi's help on North."),
    (28, "OCEANIA", "Canberra sanctions a settler leader."),
    (29, "EUROPE", "Europe off track on antibiotics."),
    (30, "AFRICA", "Ethiopia, Eritrea mass troops at border."),
    (31, "AFRICA", "Maputo: Exxon $30bn LNG plan approved."),
    (32, "MIDDLE EAST", "Riyadh: Houthi cruise missile downed."),
    (33, "MIDDLE EAST", "Hormuz: Iran says it downed a US drone."),
    (34, "OCEANIA", "PNG: magnitude 6.0 quake strikes."),
    (35, "EUROPE", "Romania: magnitude 5.3 quake shakes."),
    (36, "AMERICAS", "NSA classified network fails."),
    (37, "AMERICAS", "Caracas: Hegseth visit seals pact."),
    (38, "AMERICAS", "Brasilia passes $10bn fiscal package."),
    (39, "AMERICAS", "Mexico: US trade talks 'very along'."),
    (40, "OCEANIA", "Sydney police swoop the ARIA Awards."),
]

# region counts (must sum to 40) — computed from HERO+GRID+LIST above
REGION_COUNTS = [("EUROPE", 6), ("MIDDLE EAST", 5), ("ASIA", 9), ("AFRICA", 4),
                 ("AMERICAS", 10), ("OCEANIA", 3), ("WORLD", 3)]

# numbers bar: (number, label, red?)
NUMBERS = [
    ("141", "drones fired", True),
    ("126", "downed", True),
    ("25.9bn km", "Voyager 1", False),
    ("55", "factories shut", True),
    ("251-11", "Jeffries vote", False),
    ("3.6%", "UK inflation", False),
]

# map pins: (story num, lon, lat)
PINS = [
    (1, 114.0, 22.5), (2, 48.0, 29.0), (4, 30.5, 50.5), (5, -122.0, 37.4),
    (6, 85.0, 20.0), (7, 30.2, 13.2), (8, 4.4, 50.8), (9, -0.1, 51.5),
    (10, 34.5, 31.5), (11, -77.0, 39.0), (12, -74.0, 40.7), (13, 90.4, 23.8),
]


def hero_visual(d, kind, x, y, w, h):
    if kind == "apec":
        # sunset gradient bands + skyline + 3 flags
        for i in range(h):
            t = i / max(1, h - 1)
            r = int(250 - 120 * t)
            g = int(170 - 90 * t)
            b = int(60 + 40 * t)
            d.line([x, y + i, x + w, y + i], fill=(r, g, b))
        # sun
        d.ellipse([x + w - 58, y + 12, x + w - 18, y + 52], fill=(255, 230, 150))
        # skyline
        for bx, bw, bh in [(0.02, 0.10, 0.30), (0.13, 0.08, 0.45), (0.22, 0.11, 0.36),
                           (0.34, 0.09, 0.55), (0.44, 0.10, 0.40), (0.55, 0.08, 0.62),
                           (0.64, 0.11, 0.44), (0.76, 0.09, 0.52), (0.86, 0.12, 0.34)]:
            d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h], fill=(30, 30, 45))
        # three small flags on poles
        fw, fh = 44, 28
        for i, fn in enumerate([flag_us, flag_cn, flag_ru]):
            fx = x + 14 + i * 58
            fy = y + 8
            d.line([fx + fw / 2, fy, fx + fw / 2, fy + fh + 26], fill=(255, 255, 255), width=2)
            fn(d, fx, fy, fw, fh)
    elif kind == "gulf":
        # dark sea + coastline + impact dots
        d.rectangle([x, y, x + w, y + h], fill=(16, 42, 78))
        # coastline (a rough Gulf shape)
        d.polygon([(x, y + h * 0.15), (x + w * 0.30, y + h * 0.10), (x + w * 0.55, y + h * 0.30),
                   (x + w * 0.70, y + h * 0.55), (x + w * 0.62, y + h * 0.85), (x + w * 0.35, y + h),
                   (x, y + h)], fill=(52, 78, 60))
        # impact markers
        for px, py, r in [(0.62, 0.30, 7), (0.72, 0.45, 5), (0.55, 0.60, 6), (0.80, 0.62, 4), (0.45, 0.42, 4)]:
            cx, cy = x + px * w, y + py * h
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 40), outline=(255, 220, 120), width=1)
        d.text((x + 8, y + h - 18), "HORMUZ", font=F_SANS_B(10), fill=(255, 220, 120))
    elif kind == "voyager":
        d.rectangle([x, y, x + w, y + h], fill=(5, 8, 18))
        # stars
        for sx, sy in [(0.08, 0.2), (0.2, 0.1), (0.3, 0.35), (0.45, 0.15), (0.55, 0.3),
                       (0.65, 0.12), (0.75, 0.28), (0.85, 0.18), (0.92, 0.4), (0.15, 0.55),
                       (0.35, 0.6), (0.6, 0.55), (0.8, 0.65), (0.5, 0.75), (0.25, 0.8)]:
            d.ellipse([x + sx * w - 1.5, y + sy * h - 1.5, x + sx * w + 1.5, y + sy * h + 1.5],
                      fill=(255, 255, 255))
        # trajectory + probe
        d.line([x + 20, y + h - 20, x + w - 40, y + 30], fill=(212, 175, 55), width=2)
        px, py = x + w - 60, y + 42
        d.polygon([(px, py - 8), (px + 16, py), (px, py + 8), (px - 16, py)], fill=(212, 175, 55))
        d.line([px - 16, py, px - 28, py - 10], fill=(232, 196, 90), width=2)
        # label
        d.rectangle([x + 8, y + 8, x + 92, y + 28], fill=(212, 175, 55))
        d.text((x + 12, y + 11), "1 LIGHT-DAY", font=F_SANS_B(11), fill=(10, 10, 10))


def mini_visual(d, kind, x, y, w, h):
    if kind == "bridge":
        mini_bridge(d, x, y, w, h)
    elif kind == "chip":
        mini_chip(d, x, y, w, h)
    elif kind == "cyclone":
        mini_cyclone(d, x, y, w, h)
    elif kind == "pin":
        mini_pin(d, x, y, w, h)
    elif kind == "eu":
        mini_eu(d, x, y, w, h)
    elif kind == "line":
        mini_line_up(d, x, y, w, h)
    elif kind == "tank":
        mini_tank(d, x, y, w, h)
    elif kind == "ballot":
        mini_ballot(d, x, y, w, h)
    elif kind == "controller":
        mini_controller(d, x, y, w, h)
    elif kind == "factory":
        mini_factory(d, x, y, w, h)
    elif kind == "bars":
        mini_bars(d, x, y, w, h, [0.4, 0.55, 0.7, 0.85, 1.0])


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    issues = []

    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

    # ================= HEADER (3-73) =================
    d.rectangle([3, 3, W - 4, 73], fill=NAVY)
    # red date badge
    d.rectangle([8, 8, 78, 68], fill=RED)
    draw_centered(d, 43, 10, "NOV", F_SANS_B(11), (255, 255, 255))
    draw_centered(d, 43, 22, "18", F_SANS_B(30), (255, 255, 255))
    draw_centered(d, 43, 54, "WED 2026", F_SANS_B(9), (255, 255, 255))
    # title block
    d.text((88, 10), "THE DAY IN WORLD NEWS", font=F_SANS_B(11), fill=GOLD_LT)
    title = "Wednesday 18 November 2026"
    tf = F_SERIF_B(38)
    if text_w(d, title, tf) > 640:
        tf = F_SERIF_B(34)
    d.text((88, 24), title, font=tf, fill=(255, 255, 255))
    # right: 40 stories
    rt = "40 STORIES · 7 REGIONS · ONE PAGE"
    rf = F_SANS_B(11)
    d.text((W - 8 - text_w(d, rt, rf), 14), rt, font=rf, fill=GOLD_LT)
    # sub-line (white bg)
    sub = "Everything on this page happened, or was first reported, on Wednesday 18 November 2026."
    sf = F_SERIF_I(12)
    draw_centered(d, W / 2, 76, sub, sf, (70, 70, 70))

    # ================= REGION BAR (91-109) =================
    total = sum(c for _, c in REGION_COUNTS)
    rx = 3
    for name, cnt in REGION_COUNTS:
        seg_w = (W - 6) * cnt / total
        d.rectangle([rx, 91, rx + seg_w, 109], fill=REG[name])
        lab = f"{name} {cnt}"
        lf = F_SANS_B(11)
        while text_w(d, lab, lf) > seg_w - 6 and lf.size > 8:
            lf = F_SANS_B(lf.size - 1)
        d.text((rx + (seg_w - text_w(d, lab, lf)) / 2, 94), lab, font=lf, fill=(255, 255, 255))
        rx += seg_w

    # ================= NUMBERS BAR (109-147) =================
    d.rectangle([3, 109, W - 4, 147], fill=(250, 250, 248))
    d.line([3, 109, W - 4, 109], fill=(200, 200, 200), width=1)
    d.line([3, 147, W - 4, 147], fill=(200, 200, 200), width=1)
    d.text((10, 118), "THE DAY IN NUMBERS:", font=F_SANS_B(11), fill=INK)
    label_w = text_w(d, "THE DAY IN NUMBERS:", F_SANS_B(11))
    # lay out each number+label at its natural width so nothing overlaps
    nf = F_SANS_B(18)
    lf2 = F_SANS(10)
    widths = []
    for num, lab, red in NUMBERS:
        widths.append(text_w(d, num, nf) + 5 + text_w(d, lab, lf2))
    gap = 22
    total_w = sum(widths) + gap * (len(NUMBERS) - 1)
    cx = 10 + label_w + 18
    # if the row is too wide, shrink the number font until it fits
    while cx + total_w > W - 12 and nf.size > 14:
        nf = F_SANS_B(nf.size - 1)
        widths = [text_w(d, num, nf) + 5 + text_w(d, lab, lf2) for num, lab, red in NUMBERS]
        total_w = sum(widths) + gap * (len(NUMBERS) - 1)
    for i, (num, lab, red) in enumerate(NUMBERS):
        col = (200, 40, 40) if red else INK
        d.text((cx, 115), num, font=nf, fill=col)
        nw = text_w(d, num, nf)
        d.text((cx + nw + 5, 122), lab, font=lf2, fill=GREY)
        cx += widths[i] + gap
        if i < len(NUMBERS) - 1:
            d.line([cx - gap + 8, 116, cx - gap + 8, 140], fill=(210, 210, 210), width=1)

    # ================= HERO 3 PANELS (147-367) =================
    hero_y, hero_h = 147, 220
    hero_w = 332
    hero_xs = [8, 346, 684]
    for hi, item in enumerate(HERO):
        x = hero_xs[hi]
        # visual
        hero_visual(d, item["visual"], x, hero_y, hero_w, 104)
        # kicker bar
        ky = hero_y + 104
        d.rectangle([x, ky, x + hero_w, ky + 24], fill=NAVY_DK)
        # number chip
        d.rectangle([x, ky, x + 24, ky + 24], fill=RED)
        draw_centered(d, x + 12, ky + 5, str(item["num"]), F_SANS_B(13), (255, 255, 255))
        kick = f"{item['region']} · {item['topic']}"
        d.text((x + 30, ky + 6), kick, font=F_SANS_B(11), fill=(255, 255, 255))
        src = item["src"]
        d.text((x + hero_w - 6 - text_w(d, src, F_SANS(9)), ky + 8), src, font=F_SANS(9), fill=(180, 190, 205))
        # headline (serif bold, 2 lines)
        hf = F_SERIF_B(19)
        hl = wrap(d, item["head"], hf, hero_w - 12)
        while len(hl) > 2 and hf.size > 16:
            hf = F_SERIF_B(hf.size - 1)
            hl = wrap(d, item["head"], hf, hero_w - 12)
        hy = ky + 30
        for ln in hl[:2]:
            d.text((x + 6, hy), ln, font=hf, fill=INK)
            hy += int(hf.size * 1.2)
        if len(hl) > 2:
            issues.append(f"hero {item['num']} headline {len(hl)} lines")
        # body (2 lines)
        bf = F_SANS(11)
        bl = wrap(d, item["body"], bf, hero_w - 12)
        while len(bl) > 2 and bf.size > 10:
            bf = F_SANS(bf.size - 1)
            bl = wrap(d, item["body"], bf, hero_w - 12)
        by = hy + 3
        for ln in bl[:2]:
            d.text((x + 6, by), ln, font=bf, fill=(50, 50, 50))
            by += int(bf.size * 1.3)
        if len(bl) > 2:
            issues.append(f"hero {item['num']} body {len(bl)} lines")
        # panel border
        d.rectangle([x, hero_y, x + hero_w, hero_y + hero_h], outline=(200, 200, 200), width=1)

    # ================= GRID 10 PANELS (367-607) =================
    grid_y0, grid_h = 367, 240
    col_w = 198
    col_xs = [8, 210, 412, 614, 816]
    row_h = 120
    for gi, item in enumerate(GRID):
        row, col = divmod(gi, 5)
        x = col_xs[col]
        y = grid_y0 + row * row_h
        # kicker
        d.rectangle([x, y, x + col_w, y + 17], fill=REG[item["region"]])
        kick = f"{item['num']}  {item['region']} · {item['topic']}"
        kf = F_SANS_B(9)
        while text_w(d, kick, kf) > col_w - 6 and kf.size > 7:
            kf = F_SANS_B(kf.size - 1)
        d.text((x + 4, y + 4), kick, font=kf, fill=(255, 255, 255))
        # mini visual strip
        vy = y + 17
        d.rectangle([x, vy, x + col_w, vy + 34], fill=(245, 245, 242))
        mini_visual(d, item["mini"], x + 4, vy + 2, col_w - 8, 30)
        # headline (serif bold, 2 lines)
        hf = F_SERIF_B(13)
        hl = wrap(d, item["head"], hf, col_w - 10)
        while len(hl) > 2 and hf.size > 11:
            hf = F_SERIF_B(hf.size - 1)
            hl = wrap(d, item["head"], hf, col_w - 10)
        hy = vy + 36
        for ln in hl[:2]:
            d.text((x + 5, hy), ln, font=hf, fill=INK)
            hy += int(hf.size * 1.2)
        if len(hl) > 2:
            issues.append(f"grid {item['num']} headline {len(hl)} lines")
        # body (2 lines)
        bf = F_SANS(10)
        bl = wrap(d, item["body"], bf, col_w - 10)
        while len(bl) > 2 and bf.size > 9:
            bf = F_SANS(bf.size - 1)
            bl = wrap(d, item["body"], bf, col_w - 10)
        by = hy + 2
        for ln in bl[:2]:
            d.text((x + 5, by), ln, font=bf, fill=(50, 50, 50))
            by += int(bf.size * 1.28)
        if len(bl) > 2:
            issues.append(f"grid {item['num']} body {len(bl)} lines")
        d.rectangle([x, y, x + col_w, y + row_h], outline=(205, 205, 205), width=1)

    # ================= MAP + LIST (607-940) =================
    sec_y = 607
    d.text((10, sec_y + 4), "WHERE IT HAPPENED", font=F_SANS_B(13), fill=INK)
    d.text((500, sec_y + 4), "ALSO ON WEDNESDAY 14-40", font=F_SANS_B(13), fill=INK)
    d.line([8, sec_y + 22, 1016, sec_y + 22], fill=INK, width=1)
    # map
    map_x0, map_y0, map_w, map_h = 10, sec_y + 28, 480, 250
    draw_world_map(d, map_x0, map_y0, map_w, map_h)
    for num, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, map_x0, map_y0, map_w, map_h)
        draw_pin(d, px, py, num)
    # (Voyager 1 is story 3; it is in space, so it has no pin on this map.)
    # legend
    ly = sec_y + 284
    lx = 10
    for name, col in [("Europe", REG["EUROPE"]), ("Middle East", REG["MIDDLE EAST"]),
                      ("Asia", REG["ASIA"]), ("Africa", REG["AFRICA"]),
                      ("Americas", REG["AMERICAS"]), ("Oceania", REG["OCEANIA"]),
                      ("World", REG["WORLD"])]:
        d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=col)
        lab = name
        lf = F_SANS(10)
        d.text((lx + 11, ly), lab, font=lf, fill=INK)
        lx += 11 + int(text_w(d, lab, lf)) + 10
    d.text((10, ly + 16), "Red pins: stories 1-13  ·  dots: briefs 14-40",
           font=F_SANS(10), fill=GREY)

    # list (2 columns)
    list_x0 = 500
    col1_x, col2_x = list_x0, list_x0 + 260
    list_y0 = sec_y + 28
    lf_item = font_path("/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf", 11)
    # split 27 items: 14 in col 1 (14-27), 13 in col 2 (28-40)
    col1 = LIST_ITEMS[:14]
    col2 = LIST_ITEMS[14:]
    line_h = 13
    for ci, items in enumerate([col1, col2]):
        cx = col1_x if ci == 0 else col2_x
        for i, (num, region, text) in enumerate(items):
            yy = list_y0 + i * line_h
            # number in region colour
            d.text((cx, yy), f"{num}", font=F_SANS_B(10), fill=REG[region])
            # text (fit to column width; shrink if needed)
            tx = cx + 20
            maxw = 238
            f = lf_item
            full = text
            # shorten with ellipsis only if it cannot fit even at 9pt
            while text_w(d, full, f) > maxw and f.size > 9:
                f = font_path("/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf", f.size - 1)
            if text_w(d, full, f) > maxw:
                # truncate words until it fits
                words = full.split()
                while words and text_w(d, " ".join(words) + "…", f) > maxw:
                    words.pop()
                full = " ".join(words) + "…"
                issues.append(f"list {num} truncated")
            d.text((tx, yy), full, font=f, fill=(40, 40, 40))

    # ================= DATE CHECK (940-982) =================
    d.rectangle([8, 940, 1016, 982], outline=RED_BR, width=2)
    d.text((14, 946), "DATE CHECK", font=F_SANS_B(11), fill=RED_BR)
    dc = ("Left out on purpose — each was first reported on Tuesday 17 November: "
          "Mongolia's president resigning · the Prague train crash · the Knesset speaker vote.")
    dcf = F_SANS(11)
    # wrap to 2 lines inside the box
    dl = wrap(d, dc, dcf, 1016 - 14 - 110)
    dy = 946
    # put text right of the label on line 1, then full width on line 2
    d.text((118, dy), dl[0] if dl else "", font=dcf, fill=INK)
    if len(dl) > 1:
        d.text((14, dy + 15), dl[1], font=dcf, fill=INK)
    if len(dl) > 2:
        issues.append(f"date check {len(dl)} lines")

    # ================= SOURCES (982-1021) =================
    src = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera · ONS · IMD · NASA · Amnesty · WHO — "
           "every story happened, or was first reported, on Wednesday 18 November 2026.")
    sf2 = F_SANS(9)
    draw_centered(d, W / 2, 988, src, sf2, GREY)
    draw_centered(d, W / 2, 1004, "THE WORLD — 18 NOVEMBER 2026 · 40 STORIES · 7 REGIONS · ONE PAGE",
                  F_SANS_B(9), GREY)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"saved {OUT}  {W}x{H}  {size} bytes")
    print("issues:", issues if issues else "none")
    return issues


if __name__ == "__main__":
    main()
