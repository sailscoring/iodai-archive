"""2012 IODAI events — PHASE 2 (older Sail100, best-effort). See events/y2013.py.

2012 is almost entirely missing: the site was barely archived that year and only a
single results file survives on iodai.com — **Ulster Senior** (`ulse12os.html`).
Every other 2012 region/fleet (and any results index) 404s and isn't in the
Wayback Machine, so they can't be sourced. The one surviving fleet reconstructs
exactly (27/27). Event date isn't on the page (only a Jan-2013 re-publish stamp) —
approximate. Venue blank.
"""
from .helpers import p2_main

SERIES = [
    p2_main('iodai-ulsters-2012-main-fleet', 'IODAI Ulsters 2012 — Main Fleet',
            ['2012-06-16', '2012-06-17'], 6, '2012/ulsters/ulse12os.html',
            discards=[(4, 1)]),
]
