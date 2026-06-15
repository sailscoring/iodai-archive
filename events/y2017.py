"""2017 IODAI events.

Sourced via the Wayback Machine; files under iodai.com/results-files/
(<region><fleet>17os.html). All five championships ran, all Sailwave — separate
Senior/Junior Main fleets + a Regatta fleet each. Discard counts were read per
fleet from the pages (2017 discarded later than recent years — nothing until ~5
races). As in 2018 the pages used non-standard tie scoring, so `tie_tolerant` is
set throughout (RRS A8.1 re-scores a few boats by ±0.5–1; ranks unchanged).
"""
from .helpers import main_fleet, solo, NYC, KYC, RIYC

L = '2017/leinsters/'
U = '2017/ulsters/'
C = '2017/connachts/'
M = '2017/munsters/'
N = '2017/nationals/'

SERIES = [
    # --- Leinsters @ National YC (9–10 Sep) ----------------------------------
    main_fleet('iodai-leinsters-2017-main-fleet', 'IODAI Leinsters 2017 — Main Fleet',
               'National Yacht Club', ['2017-09-09', '2017-09-10'], nslots=4,
               senior=L + 'lese17os.html', junior=L + 'leju17os.html',
               discards=[], tie_tolerant=True, **NYC, event_url='https://iodai.com/leinsters-2017-results-nyc/'),
    solo('iodai-leinsters-2017-regatta', 'IODAI Leinsters 2017 — Regatta',
         'National Yacht Club', ['2017-09-09', '2017-09-10'], nslots=5,
         file=L + 'lere17os.html', fleet='Regatta',
         discards=[(5, 1)], tie_tolerant=True, **NYC, event_url='https://iodai.com/leinsters-2017-results-nyc/'),

    # --- Ulsters @ Royal North of Ireland YC (10–11 May) — no logo -----------
    main_fleet('iodai-ulsters-2017-main-fleet', 'IODAI Ulsters 2017 — Main Fleet',
               'Royal North of Ireland Yacht Club', ['2017-05-10', '2017-05-11'], nslots=3,
               senior=U + 'ulse17os.html', junior=U + 'ulju17os.html',
               discards=[], tie_tolerant=True),
    solo('iodai-ulsters-2017-regatta', 'IODAI Ulsters 2017 — Regatta',
         'Royal North of Ireland Yacht Club', ['2017-05-10', '2017-05-11'], nslots=3,
         file=U + 'ulre17os.html', fleet='Regatta', discards=[], tie_tolerant=True),

    # --- Connachts @ Waterford Harbour SC (15–16 Jul) — no logo --------------
    main_fleet('iodai-connachts-2017-main-fleet', 'IODAI Connachts 2017 — Main Fleet',
               'Waterford Harbour Sailing Club', ['2017-07-15', '2017-07-16'], nslots=3,
               senior=C + 'cose17os.html', junior=C + 'coju17os.html',
               discards=[], tie_tolerant=True),
    solo('iodai-connachts-2017-regatta', 'IODAI Connachts 2017 — Regatta',
         'Waterford Harbour Sailing Club', ['2017-07-15', '2017-07-16'], nslots=5,
         file=C + 'core17os.html', fleet='Regatta', discards=[(5, 1)], tie_tolerant=True),

    # --- Munsters @ Kinsale YC (13–14 May) -----------------------------------
    main_fleet('iodai-munsters-2017-main-fleet', 'IODAI Munsters 2017 — Main Fleet',
               'Kinsale Yacht Club', ['2017-05-13', '2017-05-14'], nslots=6,
               senior=M + 'muse17os.html', junior=M + 'muju17os.html',
               discards=[(5, 1)], tie_tolerant=True, **KYC),
    solo('iodai-munsters-2017-regatta', 'IODAI Munsters 2017 — Regatta',
         'Kinsale Yacht Club', ['2017-05-13', '2017-05-14'], nslots=5,
         file=M + 'mure17os.html', fleet='Regatta', discards=[], tie_tolerant=True, **KYC),

    # --- Nationals @ Royal Irish YC (17–20 Aug) ------------------------------
    main_fleet('iodai-nationals-2017-main-fleet', 'IODAI Nationals 2017 — Main Fleet',
               'Royal Irish Yacht Club',
               ['2017-08-17', '2017-08-18', '2017-08-19', '2017-08-20'], nslots=10,
               senior=N + 'nase17os.html', junior=N + 'naju17os.html',
               discards=[(5, 1), (9, 2)], tie_tolerant=True, **RIYC, event_url='https://iodai.com/nationals-2017-results-riyc/'),
    solo('iodai-nationals-2017-regatta', 'IODAI Nationals 2017 — Regatta',
         'Royal Irish Yacht Club',
         ['2017-08-17', '2017-08-18', '2017-08-19', '2017-08-20'], nslots=8,
         file=N + 'nare17os.html', fleet='Regatta', discards=[(5, 1)],
         tie_tolerant=True, **RIYC, event_url='https://iodai.com/nationals-2017-results-riyc/'),
]
