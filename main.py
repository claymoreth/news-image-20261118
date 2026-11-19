#!/usr/bin/env python3
"""news-image-20261118 V2.1 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 18 November 2026 world news, drawn beforehand with Pillow).
V2.1 rebuilds the page on the architecture of the day's top entry: header
with the date dominant, a region bar (7 regions, 40 stories), a numbers bar,
three hero panels side by side (APEC / Gulf / Voyager), a 5x2 grid of ten
panels, a dot-matrix world map, a 14-40 briefs list, and a date-check box.
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
