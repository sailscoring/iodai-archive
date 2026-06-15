"""2011 IODAI events — PHASE 2 (older Sail100, best-effort). See events/y2013.py.

Sourced via iodai.com/results-files/ (<region><fleet>11os.html). bare_dnc +
tie_tolerant; venues not on pages (blank); dates from publish timestamps
(approximate). Nationals Junior page wasn't found (Main = Senior only). Discards
[(4,1)] regional, [(4,1),(8,2)] Nationals. A couple of Nationals/Connacht senior
fleets reconstruct loosely (qualifying-style scoring) — accepted at Phase-2 bar.
"""
from .helpers import p2_main, p2_reg

L, U, C, M, N = ('2011/leinsters/', '2011/ulsters/', '2011/connachts/',
                 '2011/munsters/', '2011/nationals/')
NAT = [(4, 1), (8, 2)]

SERIES = [
    p2_main('iodai-leinsters-2011-main-fleet', 'IODAI Leinsters 2011 — Main Fleet',
            ['2011-06-15', '2011-06-16'], 4, L + 'lese11os.html', L + 'leju11os.html'),
    p2_reg('iodai-leinsters-2011-regatta', 'IODAI Leinsters 2011 — Regatta',
           ['2011-06-15', '2011-06-16'], 5, L + 'lere11os.html'),

    p2_main('iodai-ulsters-2011-main-fleet', 'IODAI Ulsters 2011 — Main Fleet',
            ['2011-06-12', '2011-06-13'], 5, U + 'ulse11os.html', U + 'ulju11os.html'),
    p2_reg('iodai-ulsters-2011-regatta', 'IODAI Ulsters 2011 — Regatta',
           ['2011-06-12', '2011-06-13'], 6, U + 'ulre11os.html'),

    p2_main('iodai-connachts-2011-main-fleet', 'IODAI Connachts 2011 — Main Fleet',
            ['2011-05-29', '2011-05-30'], 4, C + 'cose11os.html', C + 'coju11os.html'),
    p2_reg('iodai-connachts-2011-regatta', 'IODAI Connachts 2011 — Regatta',
           ['2011-05-29', '2011-05-30'], 4, C + 'core11os.html'),

    p2_main('iodai-munsters-2011-main-fleet', 'IODAI Munsters 2011 — Main Fleet',
            ['2011-06-25', '2011-06-26'], 6, M + 'muse11os.html', M + 'muju11os.html'),
    p2_reg('iodai-munsters-2011-regatta', 'IODAI Munsters 2011 — Regatta',
           ['2011-06-25', '2011-06-26'], 3, M + 'mure11os.html'),

    p2_main('iodai-nationals-2011-main-fleet', 'IODAI Nationals 2011 — Main Fleet',
            ['2011-08-17', '2011-08-18', '2011-08-19', '2011-08-20'], 12,
            N + 'nase11os.html', discards=NAT),
    p2_reg('iodai-nationals-2011-regatta', 'IODAI Nationals 2011 — Regatta',
           ['2011-08-17', '2011-08-18', '2011-08-19', '2011-08-20'], 12,
           N + 'nare11os.html', discards=NAT),
]
