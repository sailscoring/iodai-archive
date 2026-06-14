"""2024 IODAI events.

Sourced from the Sailwave IODAI directory, cross-referenced against the
iodai.com Results index. Coverage: Leinsters (MYC), Ulsters (EABC),
Connachts (GBSC), Munsters (RCYC), Nationals (HYC), Sprint Series, plus the
Irish Sailing Youth Nationals (Optimist, at RCYC — not IODAI-run but republished).

Notes on suspect/edge data (carried as-is, best effort):
- Nationals (HYC) Main was published as ONE combined 74-boat fleet (Gold/Silver/
  Bronze divisions), not split Senior/Junior — the MainS and MainJ pages are two
  views of the identical boat set, and the Fleet column reads "Junior" for all.
  Modelled as a single Main fleet from one page to match the published scoring.
- The Sprint Series published one combined-fleet page that splits Senior/Junior
  via the Division column (not a Fleet column); re-scored per fleet off Division.
- Ulsters (EABC) and the Sprint carry no race dates on their pages; those dates
  are approximate (rule 6).
"""
from .helpers import main_fleet, solo, combined, IODAI, MYC, GBSC, RCYC, HYC

L = '2024/leinsters/'
U = '2024/ulsters/'
C = '2024/connachts/'
M = '2024/munsters/'
N = '2024/nationals/'

SERIES = [
    # --- Leinsters @ Malahide YC (7–8 Sep) -----------------------------------
    main_fleet('iodai-leinsters-2024-main-fleet', 'IODAI Leinsters 2024 — Main Fleet',
               'Malahide Yacht Club', ['2024-09-07', '2024-09-08'], nslots=6,
               senior=L + '2024MYCMainS.htm', junior=L + '2024MYCMainJ.htm', **MYC),
    solo('iodai-leinsters-2024-regatta-racing', 'IODAI Leinsters 2024 — Regatta Racing',
         'Malahide Yacht Club', ['2024-09-07', '2024-09-08'], nslots=6,
         file=L + '2024MYCRR.htm', fleet='Regatta Racing', **MYC),
    solo('iodai-leinsters-2024-regatta-coached', 'IODAI Leinsters 2024 — Regatta Coached',
         'Malahide Yacht Club', ['2024-09-07', '2024-09-08'], nslots=6,
         file=L + '2024MYCRC.htm', fleet='Regatta Coached', **MYC),

    # --- Ulsters @ East Antrim Boat Club, Larne (approx 15–16 Jun) ------------
    # Main was scored as ONE combined senior+junior start (DNC = 69 over 68
    # boats), published split across the two view pages — load both into one fleet.
    combined('iodai-ulsters-2024-main-fleet', 'IODAI Ulsters 2024 — Main Fleet',
             'East Antrim Boat Club', ['2024-06-15', '2024-06-16'], nslots=6,
             files=[U + '2024EABCMainS.htm', U + '2024EABCMainJ.htm']),
    solo('iodai-ulsters-2024-regatta-racing', 'IODAI Ulsters 2024 — Regatta Racing',
         'East Antrim Boat Club', ['2024-06-15', '2024-06-16'], nslots=9,
         file=U + '2024EABCRR.htm', fleet='Regatta Racing'),
    solo('iodai-ulsters-2024-regatta-coached', 'IODAI Ulsters 2024 — Regatta Coached',
         'East Antrim Boat Club', ['2024-06-15', '2024-06-16'], nslots=9,
         file=U + '2024EABCRC.htm', fleet='Regatta Coached'),

    # --- Connachts @ Galway Bay SC (20–21 Jul) -------------------------------
    main_fleet('iodai-connachts-2024-main-fleet', 'IODAI Connachts 2024 — Main Fleet',
               'Galway Bay Sailing Club', ['2024-07-20', '2024-07-21'], nslots=6,
               senior=C + '2024GBSCMainS.htm', junior=C + '2024GBSCMainJ.htm', **GBSC),
    solo('iodai-connachts-2024-regatta-racing', 'IODAI Connachts 2024 — Regatta Racing',
         'Galway Bay Sailing Club', ['2024-07-20', '2024-07-21'], nslots=7,
         file=C + '2024GBSCRR.htm', fleet='Regatta Racing', **GBSC),
    solo('iodai-connachts-2024-regatta-coached', 'IODAI Connachts 2024 — Regatta Coached',
         'Galway Bay Sailing Club', ['2024-07-20', '2024-07-21'], nslots=5,
         file=C + '2024GBSCRC.htm', fleet='Regatta Coached', **GBSC),

    # --- Munsters @ Royal Cork YC (approx 15–16 Jun) -------------------------
    # Junior boat 1391 (Oscar Rowan) carries a ZFP cell published as 21.0 that is
    # inconsistent with his forced finishing position (10th — the only gap in
    # R2), so no standard 20% penalty reproduces it. Tolerated as suspect.
    main_fleet('iodai-munsters-2024-main-fleet', 'IODAI Munsters 2024 — Main Fleet',
               'Royal Cork Yacht Club', ['2024-06-15', '2024-06-16'], nslots=3,
               senior=M + '2024RCYCMainS.htm', junior=M + '2024RCYCMainJ.htm',
               suspect=['1391'], **RCYC),
    solo('iodai-munsters-2024-regatta-racing', 'IODAI Munsters 2024 — Regatta Racing',
         'Royal Cork Yacht Club', ['2024-06-15', '2024-06-16'], nslots=5,
         file=M + '2024RCYCRR.htm', fleet='Regatta Racing', **RCYC),
    solo('iodai-munsters-2024-regatta-coached', 'IODAI Munsters 2024 — Regatta Coached',
         'Royal Cork Yacht Club', ['2024-06-15', '2024-06-16'], nslots=5,
         file=M + '2024RCYCRC.htm', fleet='Regatta Coached', **RCYC),

    # --- Nationals @ Howth YC (15–18 Aug) — Main is one combined fleet --------
    solo('iodai-nationals-2024-main-fleet', 'IODAI Nationals 2024 — Main Fleet',
         'Howth Yacht Club', ['2024-08-15', '2024-08-16', '2024-08-17', '2024-08-18'],
         nslots=11, file=N + '2024HYCMainS.htm', fleet='Main', subdivision=True,
         discards=[(4, 1), (11, 2)], **HYC),
    solo('iodai-nationals-2024-regatta-racing', 'IODAI Nationals 2024 — Regatta Racing',
         'Howth Yacht Club', ['2024-08-15', '2024-08-16', '2024-08-17', '2024-08-18'],
         nslots=10, file=N + '2024HYCRR.htm', fleet='Regatta Racing',
         discards=[(4, 1), (10, 2)], **HYC),
    solo('iodai-nationals-2024-regatta-coached', 'IODAI Nationals 2024 — Regatta Coached',
         'Howth Yacht Club', ['2024-08-15', '2024-08-16', '2024-08-17'],
         nslots=6, file=N + '2024HYCRC.htm', fleet='Regatta Coached', **HYC),

    # --- Sprint Series (RCYC / NYC / LDYC) — combined page, split via Division -
    dict(
        out='iodai-sprint-series-2024', name='IODAI Sprint Series 2024',
        venue='RCYC / NYC / LDYC', start='2024-03-02', end='2024-03-02',
        **IODAI, subdivision=False, boat_class=False, primary='helm',
        discards=[(4, 1)], nslots=4, validate_combined=True,
        sources=[dict(file='2024/sprint/2024SprintSeriesALL.htm',
                      fleet_from_col=True, fleet_col='Division', slot0=0)],
        fleet_order=['Senior', 'Junior'],
        date=lambda i: '2024-03-02',
    ),

    # --- Irish Sailing Youth Nationals @ Royal Cork YC (Optimist, 4 Apr) ------
    solo('irish-sailing-youth-nationals-2024-optimist',
         'Irish Sailing Youth Nationals 2024 (Optimist)',
         'Royal Cork Yacht Club', ['2024-04-04'], nslots=4,
         file='2024/youth-nationals/2024YNOptimist.htm', fleet='Optimist',
         discards=[], **RCYC),
]
