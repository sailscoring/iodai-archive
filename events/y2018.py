"""2018 IODAI events.

Sourced via the Wayback Machine (see SOURCES.md); files under iodai.com/results-files/
(<region><fleet>18os.html). All five championships ran — separate Senior/Junior
Main fleets + a single Regatta fleet each. All Sailwave this year (with assorted
header spellings the engine now handles). Nationals files are capitalised (Nase/
Naju/Nare18os).
"""
from .helpers import main_fleet, solo, HYC, MYC, LDYC, KYC, RSGYC

L = '2018/leinsters/'
U = '2018/ulsters/'
C = '2018/connachts/'
M = '2018/munsters/'
N = '2018/nationals/'

SERIES = [
    # --- Leinsters @ Howth YC (16–17 Jun) ------------------------------------
    main_fleet('iodai-leinsters-2018-main-fleet', 'IODAI Leinsters 2018 — Main Fleet',
               'Howth Yacht Club', ['2018-06-16', '2018-06-17'], nslots=6,
               senior=L + 'lese18os.html', junior=L + 'leju18os.html', tie_tolerant=True, **HYC, event_url='https://iodai.com/leinsters-2018-hyc-results/'),
    solo('iodai-leinsters-2018-regatta', 'IODAI Leinsters 2018 — Regatta',
         'Howth Yacht Club', ['2018-06-16', '2018-06-17'], nslots=6,
         file=L + 'lere18os.html', fleet='Regatta', **HYC, event_url='https://iodai.com/leinsters-2018-hyc-results/'),

    # --- Ulsters @ Malahide YC (19–20 May) -----------------------------------
    main_fleet('iodai-ulsters-2018-main-fleet', 'IODAI Ulsters 2018 — Main Fleet',
               'Malahide Yacht Club', ['2018-05-19', '2018-05-20'], nslots=6,
               senior=U + 'ulse18os.html', junior=U + 'ulju18os.html', **MYC, event_url='https://iodai.com/ulsters-2018-myc/'),
    solo('iodai-ulsters-2018-regatta', 'IODAI Ulsters 2018 — Regatta',
         'Malahide Yacht Club', ['2018-05-19', '2018-05-20'], nslots=6,
         file=U + 'ulre18os.html', fleet='Regatta', **MYC, event_url='https://iodai.com/ulsters-2018-myc/'),

    # --- Connachts @ Lough Derg YC (7–8 Jul) ---------------------------------
    main_fleet('iodai-connachts-2018-main-fleet', 'IODAI Connachts 2018 — Main Fleet',
               'Lough Derg Yacht Club', ['2018-07-07', '2018-07-08'], nslots=5,
               senior=C + 'cose18os.html', junior=C + 'coju18os.html', tie_tolerant=True, **LDYC, event_url='https://iodai.com/connaughts-2018-results-ldyc/'),
    solo('iodai-connachts-2018-regatta', 'IODAI Connachts 2018 — Regatta',
         'Lough Derg Yacht Club', ['2018-07-07', '2018-07-08'], nslots=9,
         file=C + 'core18os.html', fleet='Regatta', **LDYC, event_url='https://iodai.com/connaughts-2018-results-ldyc/'),

    # --- Munsters @ Tralee Bay SC (8–9 Sep) — no canonical venue logo --------
    main_fleet('iodai-munsters-2018-main-fleet', 'IODAI Munsters 2018 — Main Fleet',
               'Tralee Bay Sailing Club', ['2018-09-08', '2018-09-09'], nslots=6,
               senior=M + 'muse18os.html', junior=M + 'muju18os.html', tie_tolerant=True, event_url='https://iodai.com/munsters-2018-results-tbsc/'),
    solo('iodai-munsters-2018-regatta', 'IODAI Munsters 2018 — Regatta',
         'Tralee Bay Sailing Club', ['2018-09-08', '2018-09-09'], nslots=9,
         file=M + 'mure18os.html', fleet='Regatta', event_url='https://iodai.com/munsters-2018-results-tbsc/'),

    # --- Nationals @ Kinsale YC (16–19 Aug) ----------------------------------
    main_fleet('iodai-nationals-2018-main-fleet', 'IODAI Nationals 2018 — Main Fleet',
               'Kinsale Yacht Club',
               ['2018-08-16', '2018-08-17', '2018-08-18', '2018-08-19'], nslots=11,
               senior=N + 'Nase18os.html', junior=N + 'Naju18os.html',
               discards=[(4, 1), (11, 2)], tie_tolerant=True, **KYC, event_url='https://iodai.com/nationals-2018-kyc-results/'),
    solo('iodai-nationals-2018-regatta', 'IODAI Nationals 2018 — Regatta',
         'Kinsale Yacht Club',
         ['2018-08-16', '2018-08-17', '2018-08-18', '2018-08-19'], nslots=12,
         file=N + 'Nare18os.html', fleet='Regatta', discards=[(4, 1), (12, 2)], **KYC, event_url='https://iodai.com/nationals-2018-kyc-results/'),

    # --- Optimist Trials @ Royal St. George YC (5–8 Apr) -----------------------
    # IODAI's team-selection event: one combined scratch fleet (the 'Division'
    # column holds Senior/Junior; the page carries a duplicate empty 'Ranking'
    # header, handled by parse_file's first-non-empty rule). See README "Trials".
    solo('iodai-trials-2018', 'IODAI Optimist Trials 2018',
         'Royal St. George Yacht Club',
         ['2018-04-05', '2018-04-06', '2018-04-07', '2018-04-08'], nslots=10,
         file='2018/trials/trials2018.html', fleet='Trials',
         discards=[(4, 1), (10, 2)], **RSGYC),
]
