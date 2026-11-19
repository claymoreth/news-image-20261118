#!/usr/bin/env python3
"""news-image-20261118 V2.7 — entry program (Python 3.13, standard library only).

The entry is the image entry.png beside this file (a 1024x1024 PNG front page
summing up 18 November 2026 world news, drawn beforehand with Pillow).
V2.7 is V2.6 with upgraded ART only (same 40 verified stories, same order,
same words, same cream paper, same layout geometry): richer map/scene-like
hero visuals (APEC tarmac + plane, labelled Gulf map, Voyager with Earth,
labelled Kerch map), a navy dot-matrix world map (Rank 1/3 style) replacing
the outline map, and a HOW SURE legend. Palette: cream paper + black +
white + the 7 region colours. Serif headlines, sans body.
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
