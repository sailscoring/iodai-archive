"""2025 IODAI events.

Sourced from the official iodai.com event pages (the canonical record of which
Sailwave files are real results) and the Sailwave IODAI directory. Each dict is
one Sail Scoring series (one group sharing a finish line). See README.md for the
per-event process and the year×event status tracker; see events/helpers.py for
the `main_fleet`/`solo` factories and the standard `DISCARDS` scheme.

Coverage: Leinsters (NYC), Ulsters (EABC), Connachts (LDYC), Munsters (KYC),
Nationals (LRYC), Sprint Series, and the National Training Week Crosbie Cup.

Notes on suspect/edge data (carried as-is, best effort):
- Munsters Regatta Coached published with zero races scored — a participation
  roster (all boats nett 0). Kept as a 0-race series.
- The Sprint published per-fleet Overall pages (OverallS/OverallJ) in 2025, so
  each fleet validates against its own page (unlike 2026's combined page).
"""
from .helpers import main_fleet, solo, combined, NYC, LDYC, KYC, LRYC, RSGYC

L = '2025/leinsters/'
U = '2025/ulsters/'
C = '2025/connachts/'
M = '2025/munsters/'
N = '2025/nationals/'
S = '2025/sprint/'

SERIES = [
    # --- Leinsters @ National YC (17–18 May) ---------------------------------
    main_fleet('iodai-leinsters-2025-main-fleet', 'IODAI Leinsters 2025 — Main Fleet',
               'National Yacht Club', ['2025-05-17', '2025-05-18'], nslots=8,
               senior=L + '2025LeinstersNYCS.htm', junior=L + '2025LeinstersNYC.htm', **NYC, event_url='https://iodai.com/2025-leinster-championships/'),
    solo('iodai-leinsters-2025-regatta-racing', 'IODAI Leinsters 2025 — Regatta Racing',
         'National Yacht Club', ['2025-05-17', '2025-05-18'], nslots=10,
         file=L + '2025LeinstersRR.htm', fleet='Regatta Racing', **NYC, event_url='https://iodai.com/2025-leinster-championships/'),
    solo('iodai-leinsters-2025-regatta-coached', 'IODAI Leinsters 2025 — Regatta Coached',
         'National Yacht Club', ['2025-05-17', '2025-05-18'], nslots=10,
         file=L + '2025LeinstersRC.htm', fleet='Regatta Coached', **NYC, event_url='https://iodai.com/2025-leinster-championships/'),

    # --- Ulsters @ East Antrim Boat Club (14–15 Jun) -------------------------
    main_fleet('iodai-ulsters-2025-main-fleet', 'IODAI Ulsters 2025 — Main Fleet',
               'East Antrim Boat Club', ['2025-06-14', '2025-06-15'], nslots=5,
               senior=U + '2025UlstersEABCS.htm', junior=U + '2025UlstersEABCJ.htm', event_url='https://iodai.com/2025-ulster-championships/'),
    solo('iodai-ulsters-2025-regatta-racing', 'IODAI Ulsters 2025 — Regatta Racing',
         'East Antrim Boat Club', ['2025-06-14', '2025-06-15'], nslots=8,
         file=U + '2025UlstersEABCRR.htm', fleet='Regatta Racing', event_url='https://iodai.com/2025-ulster-championships/'),
    solo('iodai-ulsters-2025-regatta-coached', 'IODAI Ulsters 2025 — Regatta Coached',
         'East Antrim Boat Club', ['2025-06-14', '2025-06-15'], nslots=8,
         file=U + '2025UlstersEABCRC.htm', fleet='Regatta Coached', event_url='https://iodai.com/2025-ulster-championships/'),

    # --- Connachts @ Lough Derg YC (19–20 Jul) -------------------------------
    main_fleet('iodai-connachts-2025-main-fleet', 'IODAI Connachts 2025 — Main Fleet',
               'Lough Derg Yacht Club', ['2025-07-19', '2025-07-20'], nslots=7,
               senior=C + '2025ConnachtsLDYCSM.htm', junior=C + '2025ConnachtsLDYCJM.htm', **LDYC, event_url='https://iodai.com/2025-connacht-championships/'),
    solo('iodai-connachts-2025-regatta-racing', 'IODAI Connachts 2025 — Regatta Racing',
         'Lough Derg Yacht Club', ['2025-07-19', '2025-07-20'], nslots=7,
         file=C + '2025ConnachtsLDYCRR.htm', fleet='Regatta Racing', **LDYC, event_url='https://iodai.com/2025-connacht-championships/'),
    solo('iodai-connachts-2025-regatta-coached', 'IODAI Connachts 2025 — Regatta Coached',
         'Lough Derg Yacht Club', ['2025-07-19', '2025-07-20'], nslots=8,
         file=C + '2025ConnachtsLDYCRC.htm', fleet='Regatta Coached', **LDYC, event_url='https://iodai.com/2025-connacht-championships/'),

    # --- Munsters @ Kinsale YC (13–14 Sep) -----------------------------------
    main_fleet('iodai-munsters-2025-main-fleet', 'IODAI Munsters 2025 — Main Fleet',
               'Kinsale Yacht Club', ['2025-09-13', '2025-09-14'], nslots=4,
               senior=M + '2025MunstersKYCSM.htm', junior=M + '2025MunstersKYCJM.htm', **KYC, event_url='https://iodai.com/2025-munster-championships/'),
    solo('iodai-munsters-2025-regatta-racing', 'IODAI Munsters 2025 — Regatta Racing',
         'Kinsale Yacht Club', ['2025-09-13', '2025-09-14'], nslots=4,
         file=M + '2025MunstersKYCRR.htm', fleet='Regatta Racing', **KYC, event_url='https://iodai.com/2025-munster-championships/'),
    solo('iodai-munsters-2025-regatta-coached', 'IODAI Munsters 2025 — Regatta Coached',
         'Kinsale Yacht Club', ['2025-09-13', '2025-09-14'], nslots=0,
         file=M + '2025MunstersKYCRC.htm', fleet='Regatta Coached', **KYC, event_url='https://iodai.com/2025-munster-championships/'),

    # --- Nationals @ Lough Ree YC (14–17 Aug) --------------------------------
    main_fleet('iodai-nationals-2025-main-fleet', 'IODAI Nationals 2025 — Main Fleet',
               'Lough Ree Yacht Club',
               ['2025-08-14', '2025-08-15', '2025-08-16', '2025-08-17'], nslots=8,
               senior=N + '2025NationalsLRYCSM.htm', junior=N + '2025NationalsLRYCJM.htm', **LRYC, event_url='https://iodai.com/2025-irish-optimist-national-championships/'),
    solo('iodai-nationals-2025-regatta-racing', 'IODAI Nationals 2025 — Regatta Racing',
         'Lough Ree Yacht Club',
         ['2025-08-14', '2025-08-15', '2025-08-16', '2025-08-17'], nslots=10,
         file=N + '2025NationalsLRYCRR.htm', fleet='Regatta Racing',
         discards=[(4, 1), (10, 2)], **LRYC, event_url='https://iodai.com/2025-irish-optimist-national-championships/'),
    solo('iodai-nationals-2025-regatta-coached', 'IODAI Nationals 2025 — Regatta Coached',
         'Lough Ree Yacht Club',
         ['2025-08-14', '2025-08-15', '2025-08-16', '2025-08-17'], nslots=12,
         file=N + '2025NationalsLRYCRC.htm', fleet='Regatta Coached',
         discards=[(4, 1), (12, 2)], **LRYC, event_url='https://iodai.com/2025-irish-optimist-national-championships/'),

    # --- Sprint Series (RCYC → MYC → WHSC), per-fleet Overall pages -----------
    # 14 races, 3 discards (matching the published parentheses).
    main_fleet('iodai-sprint-series-2025', 'IODAI Sprint Series 2025',
               'RCYC / MYC / WHSC', ['2025-03-01', '2025-03-22', '2025-04-13'], nslots=14,
               senior=S + '2025SprintOverallS.htm', junior=S + '2025SprintOverallJ.htm',
               discards=[(4, 1), (8, 2), (12, 3)], event_url='https://iodai.com/iodai-sprint-series-2025/'),

    # --- Irish Sailing Youth Nationals @ Royal St. George YC (Optimist) -------
    # Not IODAI-run; included because the same sailors appear (see y2024/y2026).
    # Race titles carry exact dates: R1–3 on 24 Apr, R4–5 on 25, R6–8 on 26,
    # R9–10 on 27 — encoded per-slot below rather than the two-per-day default.
    dict(
        solo('irish-sailing-youth-nationals-2025-optimist',
             'Irish Sailing Youth Nationals 2025 (Optimist)',
             'Royal St. George Yacht Club',
             ['2025-04-24', '2025-04-25', '2025-04-26', '2025-04-27'], nslots=10,
             file='2025/youth-nationals/YouthNationals.htm', fleet='Optimist',
             discards=[(4, 1), (10, 2)], **RSGYC,
             event_url='https://iodai.com/2025-irish-sailing-youth-national-championships/'),
        date=lambda i: (['2025-04-24'] * 3 + ['2025-04-25'] * 2 +
                        ['2025-04-26'] * 3 + ['2025-04-27'] * 2)[i],
    ),

    # --- National Training Week @ Lough Derg YC (1 Nov) ------------------------
    # One combined Halloween-regatta start (DNC = 84 = 83+1 on the HalloweenCup
    # page); the Halloween Cup and Crosbie Cup are prizes decided within it.
    # The published SM/JM pages are re-scores of subsets, and the Crosbie page
    # carries the combined-start positions (which is exactly why it can't be —
    # and needn't be — rebuilt as its own series). See README "National
    # Training Week".
    combined('iodai-ntw-2025-halloween-regatta',
             'IODAI National Training Week 2025 — Halloween Regatta & Crosbie Cup',
             'Lough Derg Yacht Club', ['2025-11-01'], nslots=4,
             files=['2025/ntw/2025NTWLDYCHalloweenCup.htm'], fleet='Combined',
             **LDYC, event_url='https://iodai.com/ntw-2025-halloween-regatta-crosbie-cup/'),
    solo('iodai-ntw-2025-regatta-racing',
         'IODAI National Training Week 2025 — Regatta Racing',
         'Lough Derg Yacht Club', ['2025-11-01'], nslots=4,
         file='2025/ntw/2025HalloweenRegattaLDYCRR.htm', fleet='Regatta Racing',
         **LDYC, event_url='https://iodai.com/ntw-2025-halloween-regatta-crosbie-cup/'),
    solo('iodai-ntw-2025-regatta-coached',
         'IODAI National Training Week 2025 — Regatta Coached',
         'Lough Derg Yacht Club', ['2025-11-01'], nslots=0,
         file='2025/ntw/2025HalloweenRegattaLDYCRC.htm', fleet='Regatta Coached',
         **LDYC, event_url='https://iodai.com/ntw-2025-halloween-regatta-crosbie-cup/'),
]
