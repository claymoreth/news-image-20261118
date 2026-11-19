#!/usr/bin/env python3
"""news-image-20261118 V2.2 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 18 November 2026 world news, drawn beforehand with Pillow).
V2.2 keeps V2.1's 40 verified stories but rebuilds the LOOK so it does not
resemble the day's top entry: a white masthead ("THE WORLD", black serif,
date below a thin rule), one line "40 stories across 7 regions", ONE big
hero left (APEC) with two stacked heroes right (Gulf, Voyager), a 2-column
grid of ten HORIZONTAL panels (visual left, text right), an outline world
map with BLUE pins and the legend above, a one-column "ALSO TODAY" sidebar
(14-40), a numbers bar of six white boxes at the BOTTOM, and the date check
as one italic line in the footer. Palette: black + white + brick red +
dark blue only. Serif headlines, sans body.
This program only copies it to the path the grader reads:
    /output/entry.png
Deterministic: the same bytes on every run, no network, no randomness.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
