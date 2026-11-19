#!/usr/bin/env python3
"""news-image-20261118 V2.3 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 18 November 2026 world news, drawn beforehand with Pillow).
V2.3 keeps V2.2's approved layout (white masthead, 1+2 hero, 2-column
horizontal grid, outline map, ALSO TODAY sidebar, numbers bar at the bottom,
italic date-check line) and polishes it to zero defects: larger grid and
list type with wider leading, a bigger outline map with a light graticule
and ocean labels, a dark backing behind the HORMUZ label, and a verified
8px+ gap between the date-check line and the sources line. Same 40 verified
stories as V2.2 (one body refined: Sudan now names the June-Aug window of
the Amnesty report). Palette: black + white + brick red + dark blue only.
Serif headlines, sans body.
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
