#!/usr/bin/env python3
"""News-image entry (Python 3.13, standard library only).

The image is the entry.png beside this file; the program copies it to
/output/entry.png. Deterministic: the same bytes every run, no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

# The image itself is the entry; this program only places it at the
# path the grader reads. Nothing is drawn or fetched at run time.
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
