#!/usr/bin/env python3
"""news-image-20261118 V2.5 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 18 November 2026 world news, drawn beforehand with Pillow).
V2.5 is V2.4 made COLOURFUL (owner: "bikin warna warni"): every region has
its own colour — Americas blue, Asia red, Europe navy, Middle East green,
Africa orange, Oceania teal, World purple — used in the BY REGION bar, in
each story's kicker bar (number box black), and in the map pins (with a
coloured-dot legend). Same 40 verified stories and the same V2.4 layout and
words; only the colours changed. Palette: black + white + the 7 region
colours. Serif headlines, sans body.
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
