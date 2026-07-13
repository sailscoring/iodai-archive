"""2012 IODAI events — PHASE 2 (older Sail100, best-effort). See events/y2013.py.

2012 is almost entirely missing: the site was barely archived that year and only
two events could be sourced. **Ulster Senior** (`ulse12os.html`) is the one
results file surviving on iodai.com; it reconstructs exactly (27/27). The
**Nationals** survive only as PDF exports (naju2012os.pdf / nase2012os.pdf,
surfaced by Alex Walsh — see #2), transcribed to the pipeline's HTML shape by
`sources/2012/nationals/transcribe.py`. Every other 2012 region/fleet (and any
results index) 404s and isn't in the Wayback Machine.

Event dates aren't on the pages (Ulsters: only a Jan-2013 re-publish stamp;
Nationals: a 'Sat 04 Aug 12' print timestamp anchoring the final day) —
approximate. Venues blank (not recorded in this era's exports).
"""
from .helpers import p2_main

SERIES = [
    p2_main('iodai-ulsters-2012-main-fleet', 'IODAI Ulsters 2012 — Main Fleet',
            ['2012-06-16', '2012-06-17'], 6, '2012/ulsters/ulse12os.html',
            discards=[(4, 1)]),

    # --- Nationals (venue not recorded; results printed Sat 4 Aug) -----------
    # Senior and Junior scored as separate scratch fleets (each PDF's
    # DNC-equivalent = its own entry count + 1: 48 / 97).
    p2_main('iodai-nationals-2012-main-fleet', 'IODAI Nationals 2012 — Main Fleet',
            ['2012-08-01', '2012-08-02', '2012-08-03', '2012-08-04'], 10,
            senior='2012/nationals/nase2012os.html',
            junior='2012/nationals/naju2012os.html',
            discards=[(4, 1), (10, 2)]),
]
