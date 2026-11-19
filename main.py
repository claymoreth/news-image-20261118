#!/usr/bin/env python3
"""news-image-20261118 V2.4 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 18 November 2026 world news, drawn beforehand with Pillow).
V2.4 rebuilds the page from scratch, guided by a second owner-supplied
reference front page: a white "THE WORLD" masthead, a BY REGION bar, a
"Wednesday, hour by hour" timeline (only times we can stand behind), 4 large
stories + 6 + 6 medium stories (16 visual stories, each with its own drawn
visual), an outline world map with small blue pins, the remaining 24 stories
in two columns, a numbers bar of six white boxes at the bottom, and the date
check as one italic line. Same 40 verified stories as V2.3; all words are
ours — no headline, label or sentence is copied from either reference.
Palette: black + white + greys + brick red + dark blue only.
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
