"""2016 IODAI events.

Sourced via the Wayback Machine; files under iodai.com/results-files/
(<region><fleet>16os.html). All five championships ran, all Sailwave — separate
Senior/Junior Main fleets + a Regatta fleet (the Nationals Regatta page,
nare16os, has no results table, so it isn't built). These pages put the Net/Total
columns *before* the race columns (handled in engine.parse_file) and use
non-standard tie scoring (`tie_tolerant`). Discards read per fleet.
"""
from .helpers import main_fleet, solo, RSGYC, LDYC, HYC

L = '2016/leinsters/'
U = '2016/ulsters/'
C = '2016/connachts/'
M = '2016/munsters/'
N = '2016/nationals/'

SERIES = [
    # --- Leinsters @ Royal St George YC (14–15 May) --------------------------
    main_fleet('iodai-leinsters-2016-main-fleet', 'IODAI Leinsters 2016 — Main Fleet',
               'Royal St George Yacht Club', ['2016-05-14', '2016-05-15'], nslots=6,
               senior=L + 'lese16os.html', junior=L + 'leju16os.html',
               discards=[(4, 1)], tie_tolerant=True, suspect=['511'], **RSGYC),
    solo('iodai-leinsters-2016-regatta', 'IODAI Leinsters 2016 — Regatta',
         'Royal St George Yacht Club', ['2016-05-14', '2016-05-15'], nslots=9,
         file=L + 'lere16os.html', fleet='Regatta', discards=[(4, 1), (8, 2)], tie_tolerant=True, **RSGYC),

    # --- Ulsters @ Malahide SC (2–3 Jul) — no logo ---------------------------
    main_fleet('iodai-ulsters-2016-main-fleet', 'IODAI Ulsters 2016 — Main Fleet',
               'Malahide Sailing Club', ['2016-07-02', '2016-07-03'], nslots=6,
               senior=U + 'ulse16os.html', junior=U + 'ulju16os.html',
               discards=[(4, 1)], tie_tolerant=True, suspect=['1439']),
    solo('iodai-ulsters-2016-regatta', 'IODAI Ulsters 2016 — Regatta',
         'Malahide Sailing Club', ['2016-07-02', '2016-07-03'], nslots=5,
         file=U + 'ulre16os.html', fleet='Regatta', discards=[(4, 1)], tie_tolerant=True),

    # --- Connachts @ Foynes SC (11–12 Jun) — no logo -------------------------
    main_fleet('iodai-connachts-2016-main-fleet', 'IODAI Connachts 2016 — Main Fleet',
               'Foynes Yacht Club', ['2016-06-11', '2016-06-12'], nslots=3,
               senior=C + 'cose16os.html', junior=C + 'coju16os.html',
               discards=[(4, 1)], tie_tolerant=True),
    solo('iodai-connachts-2016-regatta', 'IODAI Connachts 2016 — Regatta',
         'Foynes Yacht Club', ['2016-06-11', '2016-06-12'], nslots=9,
         file=C + 'core16os.html', fleet='Regatta', discards=[(4, 1), (8, 2)], tie_tolerant=True),

    # --- Munsters @ Cobh/CRYC (10–11 Sep) — no logo --------------------------
    main_fleet('iodai-munsters-2016-main-fleet', 'IODAI Munsters 2016 — Main Fleet',
               'CRYC', ['2016-09-10', '2016-09-11'], nslots=3,
               senior=M + 'muse16os.html', junior=M + 'muju16os.html',
               discards=[(4, 1)], tie_tolerant=True, event_url='https://iodai.com/munsters-2016-results-rcyc/'),
    solo('iodai-munsters-2016-regatta', 'IODAI Munsters 2016 — Regatta',
         'CRYC', ['2016-09-10', '2016-09-11'], nslots=3,
         file=M + 'mure16os.html', fleet='Regatta', discards=[(4, 1)], tie_tolerant=True, event_url='https://iodai.com/munsters-2016-results-rcyc/'),

    # --- Nationals @ Lough Derg YC (15–19 Aug) — Regatta page has no results --
    main_fleet('iodai-nationals-2016-main-fleet', 'IODAI Nationals 2016 — Main Fleet',
               'Lough Derg Yacht Club',
               ['2016-08-15', '2016-08-16', '2016-08-17', '2016-08-18'], nslots=10,
               senior=N + 'nase16os.html', junior=N + 'naju16os.html',
               discards=[(4, 1), (8, 2)], tie_tolerant=True, **LDYC, event_url='https://iodai.com/nationals-2016-results-ldyc/'),

    # --- Optimist Trials @ Howth YC (31 Mar – 3 Apr) ---------------------------
    # IODAI's team-selection event: one combined scratch fleet (the 'Class'
    # column holds Senior/Junior, informational only). See README "Trials".
    solo('iodai-trials-2016', 'IODAI Optimist Trials 2016',
         'Howth Yacht Club',
         ['2016-03-31', '2016-04-01', '2016-04-02', '2016-04-03'], nslots=11,
         file='2016/trials/trials2016.html', fleet='Trials',
         discards=[(4, 1), (11, 2)], **HYC),
]
