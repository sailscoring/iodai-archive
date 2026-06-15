"""2014 IODAI events.

Sourced via the Wayback Machine; files under iodai.com/results-files/
(<region><fleet>14os.html). All five championships ran, all Sailwave — separate
Senior/Junior Main fleets + a Regatta fleet each. Discards read per fleet;
tie_tolerant set throughout (non-standard tie scoring on some pages). One page
labels its net column 'Total Points' (handled in the engine).
"""
from .helpers import main_fleet, solo, RIYC, SSC, GBSC, RCYC

L = '2014/leinsters/'
U = '2014/ulsters/'
C = '2014/connachts/'
M = '2014/munsters/'
N = '2014/nationals/'

SERIES = [
    # --- Leinsters @ Royal Irish YC (5–6 Jul) --------------------------------
    main_fleet('iodai-leinsters-2014-main-fleet', 'IODAI Leinsters 2014 — Main Fleet',
               'Royal Irish Yacht Club', ['2014-07-05', '2014-07-06'], nslots=4,
               senior=L + 'lese14os.html', junior=L + 'leju14os.html',
               discards=[(4, 1)], tie_tolerant=True, **RIYC),
    solo('iodai-leinsters-2014-regatta', 'IODAI Leinsters 2014 — Regatta',
         'Royal Irish Yacht Club', ['2014-07-05', '2014-07-06'], nslots=6,
         file=L + 'lere14os.html', fleet='Regatta', discards=[(4, 1)], tie_tolerant=True, **RIYC),

    # --- Ulsters @ Skerries SC (14–15 Jun) -----------------------------------
    main_fleet('iodai-ulsters-2014-main-fleet', 'IODAI Ulsters 2014 — Main Fleet',
               'Skerries Sailing Club', ['2014-06-14', '2014-06-15'], nslots=3,
               senior=U + 'ulse14os.html', junior=U + 'ulju14os.html',
               discards=[(4, 1)], tie_tolerant=True, **SSC),
    solo('iodai-ulsters-2014-regatta', 'IODAI Ulsters 2014 — Regatta',
         'Skerries Sailing Club', ['2014-06-14', '2014-06-15'], nslots=4,
         file=U + 'ulre14os.html', fleet='Regatta', discards=[(5, 1)], tie_tolerant=True, **SSC),

    # --- Connachts @ Galway Bay SC (17–18 May) -------------------------------
    main_fleet('iodai-connachts-2014-main-fleet', 'IODAI Connachts 2014 — Main Fleet',
               'Galway Bay Sailing Club', ['2014-05-17', '2014-05-18'], nslots=5,
               senior=C + 'cose14os.html', junior=C + 'coju14os.html',
               discards=[(4, 1)], tie_tolerant=True, **GBSC),
    solo('iodai-connachts-2014-regatta', 'IODAI Connachts 2014 — Regatta',
         'Galway Bay Sailing Club', ['2014-05-17', '2014-05-18'], nslots=7,
         file=C + 'core14os.html', fleet='Regatta', discards=[(4, 1)], tie_tolerant=True, **GBSC),

    # --- Munsters @ Tralee Bay SC (6–7 Sep) — no logo ------------------------
    main_fleet('iodai-munsters-2014-main-fleet', 'IODAI Munsters 2014 — Main Fleet',
               'Tralee Bay Sailing Club', ['2014-09-06', '2014-09-07'], nslots=6,
               senior=M + 'muse14os.html', junior=M + 'muju14os.html',
               discards=[(4, 1)], tie_tolerant=True),
    solo('iodai-munsters-2014-regatta', 'IODAI Munsters 2014 — Regatta',
         'Tralee Bay Sailing Club', ['2014-09-06', '2014-09-07'], nslots=8,
         file=M + 'mure14os.html', fleet='Regatta', discards=[(4, 1)], tie_tolerant=True),

    # --- Nationals @ Royal Cork YC (14–17 Aug) -------------------------------
    main_fleet('iodai-nationals-2014-main-fleet', 'IODAI Nationals 2014 — Main Fleet',
               'Royal Cork Yacht Club',
               ['2014-08-14', '2014-08-15', '2014-08-16', '2014-08-17'], nslots=10,
               senior=N + 'nase14os.html', junior=N + 'naju14os.html',
               discards=[(4, 1), (10, 2)], tie_tolerant=True, **RCYC),
    solo('iodai-nationals-2014-regatta', 'IODAI Nationals 2014 — Regatta',
         'Royal Cork Yacht Club',
         ['2014-08-14', '2014-08-15', '2014-08-16', '2014-08-17'], nslots=7,
         file=N + 'nare14os.html', fleet='Regatta', discards=[(4, 1)], tie_tolerant=True, **RCYC),
]
