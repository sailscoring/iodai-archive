"""2015 IODAI events.

Sourced via the Wayback Machine; files under iodai.com/results-files/
(<region><fleet>15os.html). All five championships ran, all Sailwave — separate
Senior/Junior Main fleets + a Regatta fleet each. Some pages use ALL-CAPS headers
and a single 'Total' (net) column (handled in engine.parse_file). Ulster and
Connacht pages carry no event date — those are approximate (rule 6).
"""
from .helpers import main_fleet, solo, HYC, BYC, LRYC, KYC, SSC

L = '2015/leinsters/'
U = '2015/ulsters/'
C = '2015/connachts/'
M = '2015/munsters/'
N = '2015/nationals/'

SERIES = [
    # --- Leinsters @ Howth YC (5–6 Sep) --------------------------------------
    main_fleet('iodai-leinsters-2015-main-fleet', 'IODAI Leinsters 2015 — Main Fleet',
               'Howth Yacht Club', ['2015-09-05', '2015-09-06'], nslots=5,
               senior=L + 'lese15os.html', junior=L + 'leju15os.html',
               discards=[(4, 1)], **HYC),
    solo('iodai-leinsters-2015-regatta', 'IODAI Leinsters 2015 — Regatta',
         'Howth Yacht Club', ['2015-09-05', '2015-09-06'], nslots=4,
         file=L + 'lere15os.html', fleet='Regatta', discards=[(4, 1)], **HYC),

    # --- Ulsters @ Ballyholme YC (approx Jun) --------------------------------
    main_fleet('iodai-ulsters-2015-main-fleet', 'IODAI Ulsters 2015 — Main Fleet',
               'Ballyholme Yacht Club', ['2015-06-06', '2015-06-07'], nslots=3,
               senior=U + 'ulse15os.html', junior=U + 'ulju15os.html',
               discards=[(4, 1)], **BYC),
    solo('iodai-ulsters-2015-regatta', 'IODAI Ulsters 2015 — Regatta',
         'Ballyholme Yacht Club', ['2015-06-06', '2015-06-07'], nslots=6,
         file=U + 'ulre15os.html', fleet='Regatta', discards=[(4, 1)], **BYC),

    # --- Connachts @ Lough Ree YC (approx Jul) -------------------------------
    main_fleet('iodai-connachts-2015-main-fleet', 'IODAI Connachts 2015 — Main Fleet',
               'Lough Ree Yacht Club', ['2015-07-11', '2015-07-12'], nslots=6,
               senior=C + 'cose15os.html', junior=C + 'coju15os.html',
               discards=[(4, 1)], **LRYC),
    solo('iodai-connachts-2015-regatta', 'IODAI Connachts 2015 — Regatta',
         'Lough Ree Yacht Club', ['2015-07-11', '2015-07-12'], nslots=4,
         file=C + 'core15os.html', fleet='Regatta', discards=[(4, 1)], **LRYC),

    # --- Munsters @ Kinsale YC (16–17 May) -----------------------------------
    main_fleet('iodai-munsters-2015-main-fleet', 'IODAI Munsters 2015 — Main Fleet',
               'Kinsale Yacht Club', ['2015-05-16', '2015-05-17'], nslots=6,
               senior=M + 'muse15os.html', junior=M + 'muju15os.html',
               discards=[(4, 1)], **KYC),
    solo('iodai-munsters-2015-regatta', 'IODAI Munsters 2015 — Regatta',
         'Kinsale Yacht Club', ['2015-05-16', '2015-05-17'], nslots=6,
         file=M + 'mure15os.html', fleet='Regatta', discards=[(4, 1)], **KYC),

    # --- Nationals @ Skerries SC (13–16 Aug) ---------------------------------
    main_fleet('iodai-nationals-2015-main-fleet', 'IODAI Nationals 2015 — Main Fleet',
               'Skerries Sailing Club',
               ['2015-08-13', '2015-08-14', '2015-08-15', '2015-08-16'], nslots=10,
               senior=N + 'nase15os.html', junior=N + 'naju15os.html',
               discards=[(4, 1), (10, 2)], **SSC),
    solo('iodai-nationals-2015-regatta', 'IODAI Nationals 2015 — Regatta',
         'Skerries Sailing Club',
         ['2015-08-13', '2015-08-14', '2015-08-15', '2015-08-16'], nslots=12,
         file=N + 'nare15os.html', fleet='Regatta', discards=[(4, 1), (10, 2)], **SSC),
]
