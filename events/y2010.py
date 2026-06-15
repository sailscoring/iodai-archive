"""2010 IODAI events — PHASE 2 (older Sail100, best-effort). See events/y2013.py.

Sourced via iodai.com/results-files/ (<region><fleet>10os.html). bare_dnc +
tie_tolerant; venues blank; dates from publish timestamps (approximate). Several
Junior Main pages weren't found (Leinster/Ulster/Connacht/Nationals → Main =
Senior only). Discards [(4,1)] except Nationals Senior [(4,1),(8,2)].
"""
from .helpers import p2_main, p2_reg

L, U, C, M, N = ('2010/leinsters/', '2010/ulsters/', '2010/connachts/',
                 '2010/munsters/', '2010/nationals/')
NAT = [(4, 1), (8, 2)]

SERIES = [
    p2_main('iodai-leinsters-2010-main-fleet', 'IODAI Leinsters 2010 — Main Fleet',
            ['2010-06-12', '2010-06-13'], 5, L + 'lese10os.html'),
    p2_reg('iodai-leinsters-2010-regatta', 'IODAI Leinsters 2010 — Regatta',
           ['2010-06-12', '2010-06-13'], 2, L + 'lere10os.html'),

    p2_main('iodai-ulsters-2010-main-fleet', 'IODAI Ulsters 2010 — Main Fleet',
            ['2010-06-26', '2010-06-27'], 5, U + 'ulse10os.html'),
    p2_reg('iodai-ulsters-2010-regatta', 'IODAI Ulsters 2010 — Regatta',
           ['2010-06-26', '2010-06-27'], 6, U + 'ulre10os.html'),

    p2_main('iodai-connachts-2010-main-fleet', 'IODAI Connachts 2010 — Main Fleet',
            ['2010-05-29', '2010-05-30'], 5, C + 'cose10os.html'),
    p2_reg('iodai-connachts-2010-regatta', 'IODAI Connachts 2010 — Regatta',
           ['2010-05-29', '2010-05-30'], 4, C + 'core10os.html'),

    p2_main('iodai-munsters-2010-main-fleet', 'IODAI Munsters 2010 — Main Fleet',
            ['2010-05-15', '2010-05-16'], 6, M + 'muse10os.html', M + 'muju10os.html'),
    p2_reg('iodai-munsters-2010-regatta', 'IODAI Munsters 2010 — Regatta',
           ['2010-05-15', '2010-05-16'], 3, M + 'mure10os.html'),

    p2_main('iodai-nationals-2010-main-fleet', 'IODAI Nationals 2010 — Main Fleet',
            ['2010-08-18', '2010-08-19', '2010-08-20', '2010-08-21'], 11,
            N + 'nase10os.html', discards=NAT),
    p2_reg('iodai-nationals-2010-regatta', 'IODAI Nationals 2010 — Regatta',
           ['2010-08-18', '2010-08-19', '2010-08-20', '2010-08-21'], 9,
           N + 'nare10os.html'),
]
