"""2026 IODAI events.

Each dict is one Sail Scoring series (one group sharing a finish line). `out` is
the file slug and the stable key the deterministic ids derive from — never
rename it once a series has been imported (the seriesId would change). `sources`
files are paths under `sources/`. See README.md for the per-event process and
the year×event status tracker.

Sourced so far in 2026: Ulsters, Munsters, Sprint Series, plus the Irish Sailing
Youth Nationals (an Irish Sailing event, not IODAI-run, whose Optimist results
IODAI republishes — kept here as found). Still to source: Leinsters, Connachts,
Nationals, and the National Training Week final day (Crosbie Cup).
"""
from .helpers import two_per_day, IODAI, WHSC

SERIES = [
    # --- Sprint Series (NYC → MYC → MBSC), 12 races, Senior + Junior ----------
    # Published combined-fleet (all boats scored together); we re-score Senior
    # and Junior as separate fleets, matching 2025's correct scoring.
    dict(
        out='iodai-sprint-series-2026',
        name='IODAI Sprint Series 2026',
        venue='NYC / MYC / MBSC', start='2026-02-07', end='2026-03-28',
        **IODAI,
        subdivision=True, boat_class=False, primary='helm',
        discards=[(4, 1), (8, 2), (12, 3)],
        nslots=12,
        validate_combined=True,  # 2026 publishes ONE combined-fleet page
        sources=[dict(file='2026/sprint-series/2026Sprint SeriesOverall.htm',
                      fleet_from_col=True, slot0=0)],
        fleet_order=['Senior', 'Junior'],
        date=lambda i: (['2026-02-07'] * 4 + ['2026-03-22'] * 4 + ['2026-03-28'] * 4)[i],
    ),

    # --- Ulsters @ Strangford Lough YC (17–18 May) — 3 series -----------------
    dict(
        out='iodai-ulsters-2026-main-fleet',
        name='IODAI Ulsters 2026 — Main Fleet',
        venue='Strangford Lough Yacht Club', start='2026-05-17', end='2026-05-18',
        **IODAI,
        subdivision=True, boat_class=False, primary='helm',
        discards=[(4, 1)],
        nslots=6,
        sources=[dict(file='2026/ulsters/2026ULSTERSSLYCSM.htm', fleet='Senior', slot0=0),
                 dict(file='2026/ulsters/2026ULSTERSSLYCJM.htm', fleet='Junior', slot0=0)],
        fleet_order=['Senior', 'Junior'],
        date=lambda i: two_per_day(i, ['2026-05-17', '2026-05-18', '2026-05-18']),
    ),
    dict(
        out='iodai-ulsters-2026-regatta-racing',
        name='IODAI Ulsters 2026 — Regatta Racing',
        venue='Strangford Lough Yacht Club', start='2026-05-17', end='2026-05-18',
        **IODAI,
        subdivision=False, boat_class=False, primary='helm',
        discards=[(4, 1)],
        nslots=6,
        sources=[dict(file='2026/ulsters/2026ULSTERSRR.htm', fleet='Regatta Racing', slot0=0)],
        fleet_order=['Regatta Racing'],
        date=lambda i: two_per_day(i, ['2026-05-17', '2026-05-18', '2026-05-18']),
    ),
    dict(
        out='iodai-ulsters-2026-regatta-coached',
        name='IODAI Ulsters 2026 — Regatta Coached',
        venue='Strangford Lough Yacht Club', start='2026-05-17', end='2026-05-18',
        **IODAI,
        subdivision=False, boat_class=False, primary='helm',
        discards=[(4, 1)],
        nslots=6,
        sources=[dict(file='2026/ulsters/2026ULSTERSRC.htm', fleet='Regatta Coached', slot0=0)],
        fleet_order=['Regatta Coached'],
        date=lambda i: two_per_day(i, ['2026-05-17', '2026-05-18', '2026-05-18']),
    ),

    # --- Munsters @ Waterford Harbour SC (13–14 June) — 3 series --------------
    dict(
        out='iodai-munsters-2026-main-fleet',
        name='IODAI Munsters 2026 — Main Fleet',
        venue='Waterford Harbour Sailing Club', start='2026-06-13', end='2026-06-14',
        **WHSC, **IODAI,
        subdivision=True, boat_class=False, primary='helm',
        discards=[(4, 1)],
        nslots=6,
        sources=[dict(file='2026/munsters/2026MUNSTERSWHSCSM.htm', fleet='Senior', slot0=0),
                 dict(file='2026/munsters/2026MUNSTERSWHSCJM.htm', fleet='Junior', slot0=0)],
        fleet_order=['Senior', 'Junior'],
        date=lambda i: two_per_day(i, ['2026-06-13', '2026-06-14']),
    ),
    dict(
        out='iodai-munsters-2026-regatta-racing',
        name='IODAI Munsters 2026 — Regatta Racing',
        venue='Waterford Harbour Sailing Club', start='2026-06-13', end='2026-06-14',
        **WHSC, **IODAI,
        subdivision=False, boat_class=False, primary='helm',
        discards=[(4, 1)],
        nslots=6,
        sources=[dict(file='2026/munsters/2026MunstersWHSCRR.htm', fleet='Regatta Racing', slot0=0)],
        fleet_order=['Regatta Racing'],
        date=lambda i: two_per_day(i, ['2026-06-13', '2026-06-14']),
    ),
    dict(
        out='iodai-munsters-2026-regatta-coached',
        name='IODAI Munsters 2026 — Regatta Coached',
        venue='Waterford Harbour Sailing Club', start='2026-06-13', end='2026-06-14',
        **WHSC, **IODAI,
        subdivision=False, boat_class=False, primary='helm',
        discards=[(4, 1)],
        nslots=8,
        sources=[dict(file='2026/munsters/2026MunstersWHSCRC.htm', fleet='Regatta Coached', slot0=0)],
        fleet_order=['Regatta Coached'],
        date=lambda i: two_per_day(i, ['2026-06-13', '2026-06-14']),
    ),

    # --- Irish Sailing Youth Nationals @ Ballyholme YC (Optimist) ------------
    # Not IODAI-run; included because IODAI republishes its Optimist results and
    # the same sailors appear, which the cross-series identity work will want.
    dict(
        out='irish-sailing-youth-nationals-2026-optimist',
        name='Irish Sailing Youth Nationals 2026 (Optimist)',
        venue='Ballyholme Yacht Club', start='2026-04-11', end='2026-04-13',
        subdivision=False, boat_class=True, primary='helm',
        discards=[(4, 1)],
        nslots=6,
        sources=[dict(file='2026/youth-nationals/YNBYC2026.htm', fleet='Optimist', slot0=0)],
        fleet_order=['Optimist'],
        date=lambda i: two_per_day(i, ['2026-04-11', '2026-04-12', '2026-04-13']),
    ),
]
