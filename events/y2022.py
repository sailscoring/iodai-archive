"""2022 IODAI events.

Sources linked from the iodai.com event pages (Results index → each 2022 event),
at the sailwave.com/results root. Coverage: Leinsters (Skerries SC), Ulsters
(Howth YC), Connachts (Galway Bay SC), Munsters (Royal Cork YC), Nationals (Royal
St George YC). Sprint did not run in 2022. Dates come from the page titles.

Structural notes (best effort):
- Ulsters @ HYC published each Main fleet over two pages — a primary page (all
  boats) and a Bronze-only re-score (…SB/…JB) covering the same boat set over
  fewer races (a qualifying/final split). We take the primary Senior/Junior page
  (which carries every boat) and skip the Bronze re-score view.
- Connachts, Leinsters and Munsters ran a single combined Regatta fleet (one 'R'
  page), not separate Regatta Racing + Regatta Coached — built as one series.
- The Gold/Silver/Bronze prize division sits in the 'Rating' column this year
  (the 'Divison' column holds Senior/Junior); the engine reads Rating for it.
"""
from .helpers import main_fleet, solo, SSC, HYC, GBSC, RCYC, RSGYC

L = '2022/leinsters/'
U = '2022/ulsters/'
C = '2022/connachts/'
M = '2022/munsters/'
N = '2022/nationals/'

SERIES = [
    # --- Leinsters @ Skerries SC (18–19 Jun) ---------------------------------
    # Seniors 1639 and 1467 tie for 17th in R1; the page scores both 17.0, but
    # the app applies RRS A8.1 tie-averaging (17.5 each) — a 0.5 difference the
    # app scores more correctly than this Sailwave page. Tolerated as suspect.
    main_fleet('iodai-leinsters-2022-main-fleet', 'IODAI Leinsters 2022 — Main Fleet',
               'Skerries Sailing Club', ['2022-06-18', '2022-06-19'], nslots=6,
               senior=L + 'SSC2022S.html', junior=L + 'SSC2022J.html',
               suspect=['1639', '1467'], **SSC),
    solo('iodai-leinsters-2022-regatta', 'IODAI Leinsters 2022 — Regatta',
         'Skerries Sailing Club', ['2022-06-18', '2022-06-19'], nslots=7,
         file=L + 'SSC2022R.html', fleet='Regatta', discards=[(4, 1), (7, 2)], **SSC),

    # --- Ulsters @ Howth YC (10–11 Sep) --------------------------------------
    main_fleet('iodai-ulsters-2022-main-fleet', 'IODAI Ulsters 2022 — Main Fleet',
               'Howth Yacht Club', ['2022-09-10', '2022-09-11'], nslots=6,
               senior=U + 'OHYC2022S.html', junior=U + 'OHYC2022J.html', **HYC),
    solo('iodai-ulsters-2022-regatta-racing', 'IODAI Ulsters 2022 — Regatta Racing',
         'Howth Yacht Club', ['2022-09-10', '2022-09-11'], nslots=8,
         file=U + 'OHYC2022RR.html', fleet='Regatta Racing',
         discards=[(4, 1), (8, 2)], **HYC),
    # Regatta Coached was a participation roster — no scores published (blank
    # Total/Nett), so it's a 0-race series that just carries the competitors.
    solo('iodai-ulsters-2022-regatta-coached', 'IODAI Ulsters 2022 — Regatta Coached',
         'Howth Yacht Club', ['2022-09-10', '2022-09-11'], nslots=0,
         file=U + 'OHYC2022RC.html', fleet='Regatta Coached', **HYC),

    # --- Connachts @ Galway Bay SC (9–10 Jul) --------------------------------
    main_fleet('iodai-connachts-2022-main-fleet', 'IODAI Connachts 2022 — Main Fleet',
               'Galway Bay Sailing Club', ['2022-07-09', '2022-07-10'], nslots=4,
               senior=C + 'G2022S.html', junior=C + 'G2022J.html', **GBSC),
    solo('iodai-connachts-2022-regatta', 'IODAI Connachts 2022 — Regatta',
         'Galway Bay Sailing Club', ['2022-07-09', '2022-07-10'], nslots=4,
         file=C + 'G2022R.html', fleet='Regatta', **GBSC),

    # --- Munsters @ Royal Cork YC (21 May) -----------------------------------
    main_fleet('iodai-munsters-2022-main-fleet', 'IODAI Munsters 2022 — Main Fleet',
               'Royal Cork Yacht Club', ['2022-05-21'], nslots=6,
               senior=M + 'RCYC2022M.html', junior=M + 'RCYC2022J.html', **RCYC),
    solo('iodai-munsters-2022-regatta', 'IODAI Munsters 2022 — Regatta',
         'Royal Cork Yacht Club', ['2022-05-21'], nslots=5,
         file=M + 'RCYC2022R.html', fleet='Regatta', **RCYC),

    # --- Nationals @ Royal St George YC (11–14 Aug) --------------------------
    # Seniors 1651 and junior 1493 carry SCP (scoring-penalty) cells whose
    # published whole-number penalty can't be reproduced from the reconstructed
    # finishing position under the app's tenth-rounded percentage. Suspect.
    main_fleet('iodai-nationals-2022-main-fleet', 'IODAI Nationals 2022 — Main Fleet',
               'Royal St George Yacht Club',
               ['2022-08-11', '2022-08-12', '2022-08-13', '2022-08-14'], nslots=7,
               senior=N + 'ONATS2022S.html', junior=N + 'ONATS2022J.html',
               suspect=['1651', '1493'], **RSGYC),
    solo('iodai-nationals-2022-regatta-racing', 'IODAI Nationals 2022 — Regatta Racing',
         'Royal St George Yacht Club',
         ['2022-08-11', '2022-08-12', '2022-08-13', '2022-08-14'], nslots=10,
         file=N + 'ONATS2022RR.html', fleet='Regatta Racing',
         discards=[(4, 1), (10, 2)], **RSGYC),
    solo('iodai-nationals-2022-regatta-coached', 'IODAI Nationals 2022 — Regatta Coached',
         'Royal St George Yacht Club',
         ['2022-08-11', '2022-08-12', '2022-08-13', '2022-08-14'], nslots=6,
         file=N + 'ONATS2022RC2.html', fleet='Regatta Coached', **RSGYC),
]
