"""2013 IODAI events — PHASE 2 (older Sail100, best-effort).

Different output-quality expectations from 2014+. These pages were produced by an
older Sail100 that prints final points (positions *and* DNC-type penalties) as
bare numbers with no result codes, so non-finishers can't be told apart from real
places with certainty. The engine's `bare_dnc` rule treats any plain score above
the fleet size as a DNC-equivalent, which in practice reconstructs nearly every
boat exactly and the **top-half ranking of each fleet reliably** — the agreed bar
for this phase. A few deep-fleet boats may be a place out; that's accepted here.

Sourced via iodai.com/results-files/ (<region><fleet>13os.html). All five events,
separate Senior/Junior Main + Regatta. The pages record entries/races/discards
but **not the venue** (left blank — editable after import) and only a publish
timestamp; dates are approximate (rule 6). Discards: [(5, 1)] regionals (no
discard until 5 races that year), [(5, 1), (10, 2)] Nationals.
"""
from .helpers import main_fleet, solo

L = '2013/leinsters/'
U = '2013/ulsters/'
C = '2013/connachts/'
M = '2013/munsters/'
N = '2013/nationals/'
REG = [(5, 1)]
NAT = [(5, 1), (10, 2)]


def _main(out, name, days, nslots, se, ju, discards=REG, suspect=()):
    return main_fleet(out, name, '', days, nslots, senior=se, junior=ju,
                      discards=discards, tie_tolerant=True, bare_dnc=True, suspect=suspect)


def _reg(out, name, days, nslots, f, discards=REG):
    return solo(out, name, '', days, nslots, file=f, fleet='Regatta',
                discards=discards, tie_tolerant=True, bare_dnc=True)


SERIES = [
    # --- Leinsters (8 Sep) ---------------------------------------------------
    _main('iodai-leinsters-2013-main-fleet', 'IODAI Leinsters 2013 — Main Fleet',
          ['2013-09-07', '2013-09-08'], 6, L + 'lese13os.html', L + 'leju13os.html',
          suspect=['1087']),  # deep junior, ZFP-style .4 penalty
    _reg('iodai-leinsters-2013-regatta', 'IODAI Leinsters 2013 — Regatta',
         ['2013-09-07', '2013-09-08'], 4, L + 'lere13os.html', discards=[]),

    # --- Ulsters (26 May) ----------------------------------------------------
    _main('iodai-ulsters-2013-main-fleet', 'IODAI Ulsters 2013 — Main Fleet',
          ['2013-05-25', '2013-05-26'], 5, U + 'ulse13os.html', U + 'ulju13os.html'),
    _reg('iodai-ulsters-2013-regatta', 'IODAI Ulsters 2013 — Regatta',
         ['2013-05-25', '2013-05-26'], 5, U + 'ulre13os.html'),

    # --- Connachts (5–6 Oct) -------------------------------------------------
    _main('iodai-connachts-2013-main-fleet', 'IODAI Connachts 2013 — Main Fleet',
          ['2013-10-05', '2013-10-06'], 6, C + 'cose13os.html', C + 'coju13os.html'),
    _reg('iodai-connachts-2013-regatta', 'IODAI Connachts 2013 — Regatta',
         ['2013-10-05', '2013-10-06'], 7, C + 'core13os.html'),

    # --- Munsters (approx May) -----------------------------------------------
    _main('iodai-munsters-2013-main-fleet', 'IODAI Munsters 2013 — Main Fleet',
          ['2013-05-18', '2013-05-19'], 6, M + 'muse13os.html', M + 'muju13os.html'),
    _reg('iodai-munsters-2013-regatta', 'IODAI Munsters 2013 — Regatta',
         ['2013-05-18', '2013-05-19'], 7, M + 'mure13os.html'),

    # --- Nationals (15–18 Aug) -----------------------------------------------
    _main('iodai-nationals-2013-main-fleet', 'IODAI Nationals 2013 — Main Fleet',
          ['2013-08-15', '2013-08-16', '2013-08-17', '2013-08-18'], 10,
          N + 'nase13os.html', N + 'naju13os.html', discards=NAT),
    _reg('iodai-nationals-2013-regatta', 'IODAI Nationals 2013 — Regatta',
         ['2013-08-15', '2013-08-16', '2013-08-17', '2013-08-18'], 10,
         N + 'nare13os.html', discards=NAT),
]
