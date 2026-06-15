"""2021 IODAI events (a COVID-affected season).

Sources linked from the iodai.com event pages; most 2021 result files are hosted
under iodai.com/results-files/ rather than on sailwave.com (Munsters is the
exception). Coverage: Leinsters (Howth YC), Ulsters (EABC), Connachts (Lough Ree
YC), Munsters (Monkstown Bay SC), Nationals (Lough Derg YC). Each event ran a
single combined Regatta fleet (one series), not split Regatta Racing + Coached.
Dates come from the page titles. Sprint did not run; NTW Crosbie deferred.

(Separate smaller 2021 events — a Royal St George open and a Malahide regatta —
are listed on the Results index but not built here; they aren't tracker events.)
"""
from .helpers import main_fleet, solo, HYC, LRYC, LDYC

L = '2021/leinsters/'
U = '2021/ulsters/'
C = '2021/connachts/'
M = '2021/munsters/'
N = '2021/nationals/'

SERIES = [
    # --- Leinsters @ Howth YC (3–4 Jul) --------------------------------------
    main_fleet('iodai-leinsters-2021-main-fleet', 'IODAI Leinsters 2021 — Main Fleet',
               'Howth Yacht Club', ['2021-07-03', '2021-07-04'], nslots=6,
               senior=L + 'leinster2021SF.html', junior=L + 'leinster2021JF.html', **HYC, event_url='https://iodai.com/results-leinsters-2021/'),
    solo('iodai-leinsters-2021-regatta', 'IODAI Leinsters 2021 — Regatta',
         'Howth Yacht Club', ['2021-07-03', '2021-07-04'], nslots=6,
         file=L + 'leinster2021R.html', fleet='Regatta', **HYC, event_url='https://iodai.com/results-leinsters-2021/'),

    # --- Ulsters @ East Antrim Boat Club (18–19 Sep) -------------------------
    main_fleet('iodai-ulsters-2021-main-fleet', 'IODAI Ulsters 2021 — Main Fleet',
               'East Antrim Boat Club', ['2021-09-18', '2021-09-19'], nslots=6,
               senior=U + 'EABC2021SF.html', junior=U + 'EABC2021JF.html', event_url='https://iodai.com/eabc-results-2021/'),
    solo('iodai-ulsters-2021-regatta', 'IODAI Ulsters 2021 — Regatta',
         'East Antrim Boat Club', ['2021-09-18', '2021-09-19'], nslots=7,
         file=U + 'EABC2021R.html', fleet='Regatta', discards=[(4, 1), (7, 2)], event_url='https://iodai.com/eabc-results-2021/'),

    # --- Connachts @ Lough Ree YC (17–18 Jul) --------------------------------
    # Senior 1643 sits in a tie the page scores 163.5 (A8.1 average) but that the
    # reconstruction renders 164 — a 0.5 tie-rounding difference. Suspect.
    main_fleet('iodai-connachts-2021-main-fleet', 'IODAI Connachts 2021 — Main Fleet',
               'Lough Ree Yacht Club', ['2021-07-17', '2021-07-18'], nslots=6,
               senior=C + 'Conn2021SF.html', junior=C + 'Conn2021JF.html',
               suspect=['1643'], **LRYC, event_url='https://iodai.com/results-connaughts-2021/'),
    solo('iodai-connachts-2021-regatta', 'IODAI Connachts 2021 — Regatta',
         'Lough Ree Yacht Club', ['2021-07-17', '2021-07-18'], nslots=8,
         file=C + 'Conn2021R.html', fleet='Regatta', **LRYC, event_url='https://iodai.com/results-connaughts-2021/'),

    # --- Munsters @ Monkstown Bay SC (2–3 Oct) -------------------------------
    main_fleet('iodai-munsters-2021-main-fleet', 'IODAI Munsters 2021 — Main Fleet',
               'Monkstown Bay Sailing Club', ['2021-10-02', '2021-10-03'], nslots=6,
               senior=M + 'MBSC2021SF.html', junior=M + 'MBSC2021J1.html', event_url='https://iodai.com/mbsc-results-2021/'),
    solo('iodai-munsters-2021-regatta', 'IODAI Munsters 2021 — Regatta',
         'Monkstown Bay Sailing Club', ['2021-10-02', '2021-10-03'], nslots=6,
         file=M + 'MBSC21R.html', fleet='Regatta', discards=[(4, 1), (6, 2)], event_url='https://iodai.com/mbsc-results-2021/'),

    # --- Nationals @ Lough Derg YC (19–22 Aug) -------------------------------
    main_fleet('iodai-nationals-2021-main-fleet', 'IODAI Nationals 2021 — Main Fleet',
               'Lough Derg Yacht Club',
               ['2021-08-19', '2021-08-20', '2021-08-21', '2021-08-22'], nslots=11,
               senior=N + 'Nats2021SF.html', junior=N + 'Nats2021JF.html',
               discards=[(4, 1), (11, 2)], **LDYC, event_url='https://iodai.com/iodai-nationals-2021-results/'),
    # The Regatta fleet's DNC value is 50 (49 entries) but only 48 boats appear
    # in the table — an entrant counted toward the DNC base is missing — so the
    # heavily-DNC'd bottom boats reconstruct 1 low per coded race. Suspect.
    solo('iodai-nationals-2021-regatta', 'IODAI Nationals 2021 — Regatta',
         'Lough Derg Yacht Club',
         ['2021-08-19', '2021-08-20', '2021-08-21', '2021-08-22'], nslots=7,
         file=N + 'Nats2021R.html', fleet='Regatta',
         suspect=['1464', '1214', '1351', '1270', '1234'], **LDYC, event_url='https://iodai.com/iodai-nationals-2021-results/'),
]
