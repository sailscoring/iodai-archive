"""2023 IODAI events.

Sources linked from the iodai.com event pages (Results index → each 2023 event),
which live at the sailwave.com/results root (pre-2024 events aren't under the
/IODAI/ subdirectory). Coverage: Leinsters (NYC), Ulsters (EABC), Connachts
(LRYC), Munsters (WHSC), Nationals (Ballyholme), Sprint did not run in 2023.

All Main fleets this year were scored as separate Senior/Junior scratch fleets
(each page's DNC = its own boat count + 1). Race dates are approximate — most
2023 pages carry no per-race dates (rule 6); a few publish timestamps anchor the
weekend. Not built: the National Training Week Crosbie Cup (combined-start
positions, see y2025.py note) and the Nationals Regatta Coached page (no results
table published).
"""
from .helpers import main_fleet, solo, NYC, LRYC, WHSC, BYC, HYC

L = '2023/leinsters/'
U = '2023/ulsters/'
C = '2023/connachts/'
M = '2023/munsters/'
N = '2023/nationals/'

SERIES = [
    # --- Leinsters @ National YC (approx 13–14 May) --------------------------
    main_fleet('iodai-leinsters-2023-main-fleet', 'IODAI Leinsters 2023 — Main Fleet',
               'National Yacht Club', ['2023-05-13', '2023-05-14'], nslots=3,
               senior=L + 'NYCMainS.htm', junior=L + 'MainJ.htm', **NYC, event_url='https://iodai.com/leinster-championships-national-yacht-club/'),
    solo('iodai-leinsters-2023-regatta-racing', 'IODAI Leinsters 2023 — Regatta Racing',
         'National Yacht Club', ['2023-05-13', '2023-05-14'], nslots=7,
         file=L + 'NYCRR23.html', fleet='Regatta Racing', **NYC, event_url='https://iodai.com/leinster-championships-national-yacht-club/'),
    solo('iodai-leinsters-2023-regatta-coached', 'IODAI Leinsters 2023 — Regatta Coached',
         'National Yacht Club', ['2023-05-13', '2023-05-14'], nslots=7,
         file=L + 'NYCRC23.html', fleet='Regatta Coached', **NYC, event_url='https://iodai.com/leinster-championships-national-yacht-club/'),

    # --- Ulsters @ East Antrim Boat Club (17–18 Jun) -------------------------
    main_fleet('iodai-ulsters-2023-main-fleet', 'IODAI Ulsters 2023 — Main Fleet',
               'East Antrim Boat Club', ['2023-06-17', '2023-06-18'], nslots=5,
               senior=U + 'EABCMainS.htm', junior=U + 'EABCMainJ.htm', event_url='https://iodai.com/ulster-championships-east-antrim-boat-club/'),
    solo('iodai-ulsters-2023-regatta-racing', 'IODAI Ulsters 2023 — Regatta Racing',
         'East Antrim Boat Club', ['2023-06-17', '2023-06-18'], nslots=6,
         file=U + 'EABCRR.htm', fleet='Regatta Racing', event_url='https://iodai.com/ulster-championships-east-antrim-boat-club/'),
    solo('iodai-ulsters-2023-regatta-coached', 'IODAI Ulsters 2023 — Regatta Coached',
         'East Antrim Boat Club', ['2023-06-17', '2023-06-18'], nslots=4,
         file=U + 'EABCRC.htm', fleet='Regatta Coached', event_url='https://iodai.com/ulster-championships-east-antrim-boat-club/'),

    # --- Connachts @ Lough Ree YC (16–17 Sep) --------------------------------
    main_fleet('iodai-connachts-2023-main-fleet', 'IODAI Connachts 2023 — Main Fleet',
               'Lough Ree Yacht Club', ['2023-09-16', '2023-09-17'], nslots=7,
               senior=C + '23LRYCMainS.htm', junior=C + '23LRYCMainJ.htm', **LRYC, event_url='https://iodai.com/connaught-championships-lough-ree-yacht-club/'),
    solo('iodai-connachts-2023-regatta-racing', 'IODAI Connachts 2023 — Regatta Racing',
         'Lough Ree Yacht Club', ['2023-09-16', '2023-09-17'], nslots=5,
         file=C + '23LRYCRR.htm', fleet='Regatta Racing', **LRYC, event_url='https://iodai.com/connaught-championships-lough-ree-yacht-club/'),
    solo('iodai-connachts-2023-regatta-coached', 'IODAI Connachts 2023 — Regatta Coached',
         'Lough Ree Yacht Club', ['2023-09-16', '2023-09-17'], nslots=5,
         file=C + '23LRYCRC.htm', fleet='Regatta Coached', **LRYC, event_url='https://iodai.com/connaught-championships-lough-ree-yacht-club/'),

    # --- Munsters @ Waterford Harbour SC (approx 3–4 Jun) --------------------
    main_fleet('iodai-munsters-2023-main-fleet', 'IODAI Munsters 2023 — Main Fleet',
               'Waterford Harbour Sailing Club', ['2023-06-03', '2023-06-04'], nslots=6,
               senior=M + '23WHSCMainS.htm', junior=M + '23WHSCMainJ.htm', **WHSC, event_url='https://iodai.com/28401-2/'),
    solo('iodai-munsters-2023-regatta-racing', 'IODAI Munsters 2023 — Regatta Racing',
         'Waterford Harbour Sailing Club', ['2023-06-03', '2023-06-04'], nslots=5,
         file=M + '23WHSCRR.htm', fleet='Regatta Racing', **WHSC, event_url='https://iodai.com/28401-2/'),
    solo('iodai-munsters-2023-regatta-coached', 'IODAI Munsters 2023 — Regatta Coached',
         'Waterford Harbour Sailing Club', ['2023-06-03', '2023-06-04'], nslots=4,
         file=M + '23WHSCRC.htm', fleet='Regatta Coached', **WHSC, event_url='https://iodai.com/28401-2/'),

    # --- Nationals @ Ballyholme YC (17–20 Aug) -------------------------------
    main_fleet('iodai-nationals-2023-main-fleet', 'IODAI Nationals 2023 — Main Fleet',
               'Ballyholme Yacht Club',
               ['2023-08-17', '2023-08-18', '2023-08-19', '2023-08-20'], nslots=9,
               senior=N + 'BYC23MainS.html', junior=N + 'BYC23MainJ.html',
               discards=[(4, 1), (9, 2)], **BYC, event_url='https://iodai.com/irish-optimist-national-championships-2023/'),
    solo('iodai-nationals-2023-regatta-racing', 'IODAI Nationals 2023 — Regatta Racing',
         'Ballyholme Yacht Club',
         ['2023-08-17', '2023-08-18', '2023-08-19', '2023-08-20'], nslots=10,
         file=N + 'BYC23RR.html', fleet='Regatta Racing',
         discards=[(4, 1), (10, 2)], **BYC, event_url='https://iodai.com/irish-optimist-national-championships-2023/'),

    # --- Irish Sailing Youth Nationals @ Howth YC (Optimist, 13–16 Apr) -------
    # Not IODAI-run; included because the same sailors appear (see y2024/y2026).
    solo('irish-sailing-youth-nationals-2023-optimist',
         'Irish Sailing Youth Nationals 2023 (Optimist)',
         'Howth Yacht Club',
         ['2023-04-13', '2023-04-14', '2023-04-15', '2023-04-16'], nslots=10,
         file='2023/youth-nationals/YNHYC2023Main.html', fleet='Optimist',
         discards=[(4, 1), (10, 2)], **HYC),
]
