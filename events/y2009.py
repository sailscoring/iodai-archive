"""2009 IODAI events — PHASE 2 (older Sail100, best-effort). See events/y2013.py.

Sourced via iodai.com/results-files/ (<region><fleet>09os.html). bare_dnc +
tie_tolerant; venues blank; dates from publish timestamps (approximate). All five
events, Main + Regatta. Discards [(4,1)] regional, [(4,1),(8,2)] Nationals. A few
senior/regatta fleets reconstruct loosely (qualifying-style scoring) — accepted
at the Phase-2 bar.
"""
from .helpers import p2_main, p2_reg

L, U, C, M, N = ('2009/leinsters/', '2009/ulsters/', '2009/connachts/',
                 '2009/munsters/', '2009/nationals/')
NAT = [(4, 1), (8, 2)]

SERIES = [
    p2_main('iodai-leinsters-2009-main-fleet', 'IODAI Leinsters 2009 — Main Fleet',
            ['2009-09-05', '2009-09-06'], 6, L + 'lese09os.html', L + 'leju09os.html'),
    p2_reg('iodai-leinsters-2009-regatta', 'IODAI Leinsters 2009 — Regatta',
           ['2009-09-05', '2009-09-06'], 6, L + 'lere09os.html'),

    p2_main('iodai-ulsters-2009-main-fleet', 'IODAI Ulsters 2009 — Main Fleet',
            ['2009-06-25', '2009-06-26'], 4, U + 'ulse09os.html', U + 'ulju09os.html'),
    p2_reg('iodai-ulsters-2009-regatta', 'IODAI Ulsters 2009 — Regatta',
           ['2009-06-25', '2009-06-26'], 6, U + 'ulre09os.html'),

    p2_main('iodai-connachts-2009-main-fleet', 'IODAI Connachts 2009 — Main Fleet',
            ['2009-07-19', '2009-07-20'], 5, C + 'cose09os.html', C + 'coju09os.html'),
    p2_reg('iodai-connachts-2009-regatta', 'IODAI Connachts 2009 — Regatta',
           ['2009-07-19', '2009-07-20'], 5, C + 'core09os.html'),

    p2_main('iodai-munsters-2009-main-fleet', 'IODAI Munsters 2009 — Main Fleet',
            ['2009-06-25', '2009-06-26'], 4, M + 'muse09os.html', M + 'muju09os.html'),
    p2_reg('iodai-munsters-2009-regatta', 'IODAI Munsters 2009 — Regatta',
           ['2009-06-25', '2009-06-26'], 6, M + 'mure09os.html'),

    p2_main('iodai-nationals-2009-main-fleet', 'IODAI Nationals 2009 — Main Fleet',
            ['2009-09-05', '2009-09-06', '2009-09-07', '2009-09-08'], 12,
            N + 'nase09os.html', N + 'naju09os.html', discards=NAT),
    p2_reg('iodai-nationals-2009-regatta', 'IODAI Nationals 2009 — Regatta',
           ['2009-09-05', '2009-09-06', '2009-09-07', '2009-09-08'], 9,
           N + 'nare09os.html', discards=NAT),
]
