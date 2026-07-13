"""2024 IODAI events.

Sourced from the official iodai.com event pages (each links its canonical
Sailwave files): Leinsters (MYC), Ulsters (EABC/Larne), Connachts (GBSC),
Munsters (RCYC), Nationals (HYC), Sprint Series, plus the Irish Sailing Youth
Nationals (Optimist, at RCYC — not IODAI-run but republished). See SOURCES.md
for the page→file mapping.

(An earlier pass mistakenly used same-year files from the Sailwave /IODAI/
directory index that turned out to be superseded/test exports — the Ulster Main
and Nationals Main were combined-fleet artifacts, and a Munster Junior copy was a
race short. Re-sourced from the iodai.com pages, where Ulster and Nationals Main
are normal separate Senior/Junior fleets.)

Notes (best effort):
- The Sprint Series published one combined-fleet page that splits Senior/Junior
  via the Division column (not a Fleet column); re-scored per fleet off Division.
- Ulster, Munster and the Sprint carry no race dates on their pages; those dates
  are approximate (rule 6).
"""
from .helpers import main_fleet, solo, combined, IODAI, MYC, GBSC, RCYC, HYC, RSGYC

L = '2024/leinsters/'
U = '2024/ulsters/'
C = '2024/connachts/'
M = '2024/munsters/'
N = '2024/nationals/'

SERIES = [
    # --- Leinsters @ Malahide YC (7–8 Sep) -----------------------------------
    main_fleet('iodai-leinsters-2024-main-fleet', 'IODAI Leinsters 2024 — Main Fleet',
               'Malahide Yacht Club', ['2024-09-07', '2024-09-08'], nslots=6,
               senior=L + '2024MYCMainS.htm', junior=L + '2024MYCMainJ.htm', **MYC, event_url='https://iodai.com/2024-leinster-championships/'),
    solo('iodai-leinsters-2024-regatta-racing', 'IODAI Leinsters 2024 — Regatta Racing',
         'Malahide Yacht Club', ['2024-09-07', '2024-09-08'], nslots=6,
         file=L + '2024MYCRR.htm', fleet='Regatta Racing', **MYC, event_url='https://iodai.com/2024-leinster-championships/'),
    solo('iodai-leinsters-2024-regatta-coached', 'IODAI Leinsters 2024 — Regatta Coached',
         'Malahide Yacht Club', ['2024-09-07', '2024-09-08'], nslots=6,
         file=L + '2024MYCRC.htm', fleet='Regatta Coached', **MYC, event_url='https://iodai.com/2024-leinster-championships/'),

    # --- Ulsters @ East Antrim Boat Club, Larne (approx 15–16 Jun) -----------
    main_fleet('iodai-ulsters-2024-main-fleet', 'IODAI Ulsters 2024 — Main Fleet',
               'East Antrim Boat Club', ['2024-06-15', '2024-06-16'], nslots=6,
               senior=U + '2024UlstersMainS.htm', junior=U + '2024UlstersMainJ.htm', event_url='https://iodai.com/2024-ulster-championships/'),
    solo('iodai-ulsters-2024-regatta-racing', 'IODAI Ulsters 2024 — Regatta Racing',
         'East Antrim Boat Club', ['2024-06-15', '2024-06-16'], nslots=8,
         file=U + '2024UlstersRR.htm', fleet='Regatta Racing', event_url='https://iodai.com/2024-ulster-championships/'),
    solo('iodai-ulsters-2024-regatta-coached', 'IODAI Ulsters 2024 — Regatta Coached',
         'East Antrim Boat Club', ['2024-06-15', '2024-06-16'], nslots=8,
         file=U + '2024UlstersRC.htm', fleet='Regatta Coached', event_url='https://iodai.com/2024-ulster-championships/'),

    # --- Connachts @ Galway Bay SC (20–21 Jul) -------------------------------
    main_fleet('iodai-connachts-2024-main-fleet', 'IODAI Connachts 2024 — Main Fleet',
               'Galway Bay Sailing Club', ['2024-07-20', '2024-07-21'], nslots=6,
               senior=C + '2024GBSCMainS.htm', junior=C + '2024GBSCMainJ.htm', **GBSC, event_url='https://iodai.com/2024-connaught-championships/'),
    solo('iodai-connachts-2024-regatta-racing', 'IODAI Connachts 2024 — Regatta Racing',
         'Galway Bay Sailing Club', ['2024-07-20', '2024-07-21'], nslots=7,
         file=C + '2024GBSCRR.htm', fleet='Regatta Racing', **GBSC, event_url='https://iodai.com/2024-connaught-championships/'),
    solo('iodai-connachts-2024-regatta-coached', 'IODAI Connachts 2024 — Regatta Coached',
         'Galway Bay Sailing Club', ['2024-07-20', '2024-07-21'], nslots=5,
         file=C + '2024GBSCRC.htm', fleet='Regatta Coached', **GBSC, event_url='https://iodai.com/2024-connaught-championships/'),

    # --- Munsters @ Royal Cork YC (approx 15–16 Jun) -------------------------
    # Junior 1391 (Oscar Rowan) has a ZFP cell (21.0) whose published whole-number
    # penalty can't be reproduced from his reconstructed position. Suspect.
    main_fleet('iodai-munsters-2024-main-fleet', 'IODAI Munsters 2024 — Main Fleet',
               'Royal Cork Yacht Club', ['2024-06-15', '2024-06-16'], nslots=3,
               senior=M + 'RCYC24MainS.htm', junior=M + 'RCYC24MainJ.htm',
               suspect=['1391'], **RCYC, event_url='https://iodai.com/2024-munster-championships/'),
    solo('iodai-munsters-2024-regatta-racing', 'IODAI Munsters 2024 — Regatta Racing',
         'Royal Cork Yacht Club', ['2024-06-15', '2024-06-16'], nslots=5,
         file=M + 'RCYC24RR.htm', fleet='Regatta Racing', **RCYC, event_url='https://iodai.com/2024-munster-championships/'),
    solo('iodai-munsters-2024-regatta-coached', 'IODAI Munsters 2024 — Regatta Coached',
         'Royal Cork Yacht Club', ['2024-06-15', '2024-06-16'], nslots=5,
         file=M + 'RCYC24RC.htm', fleet='Regatta Coached', **RCYC, event_url='https://iodai.com/2024-munster-championships/'),

    # --- Nationals @ Howth YC (15–18 Aug) — separate Senior/Junior fleets -----
    # Senior 1673 has a ZFP cell (46.0) whose published whole-number penalty isn't
    # reproducible from the reconstructed position (tenth-rounded). Suspect.
    main_fleet('iodai-nationals-2024-main-fleet', 'IODAI Nationals 2024 — Main Fleet',
               'Howth Yacht Club',
               ['2024-08-15', '2024-08-16', '2024-08-17', '2024-08-18'], nslots=11,
               senior=N + '2024HYCMainS.htm', junior=N + '2024HYCMainJ.htm',
               discards=[(4, 1), (11, 2)], suspect=['1673'], **HYC, event_url='https://iodai.com/irish-optimist-national-championships-2024/'),
    solo('iodai-nationals-2024-regatta-racing', 'IODAI Nationals 2024 — Regatta Racing',
         'Howth Yacht Club', ['2024-08-15', '2024-08-16', '2024-08-17', '2024-08-18'],
         nslots=10, file=N + '2024HYCRR.htm', fleet='Regatta Racing',
         discards=[(4, 1), (10, 2)], **HYC, event_url='https://iodai.com/irish-optimist-national-championships-2024/'),
    solo('iodai-nationals-2024-regatta-coached', 'IODAI Nationals 2024 — Regatta Coached',
         'Howth Yacht Club', ['2024-08-15', '2024-08-16', '2024-08-17'],
         nslots=6, file=N + '2024HYCRC.htm', fleet='Regatta Coached', **HYC, event_url='https://iodai.com/irish-optimist-national-championships-2024/'),

    # --- Sprint Series (RCYC / NYC / LDYC) — combined page, split via Division -
    dict(
        out='iodai-sprint-series-2024', name='IODAI Sprint Series 2024',
        event_url='https://iodai.com/iodai-sprint-series-2024/',
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
         discards=[], **RCYC, event_url='https://iodai.com/2024-irish-sailing-youth-national-championships/'),

    # --- National Training Week @ Royal St. George YC (2 Nov) ------------------
    # One combined Halloween-regatta start (DNC = 75 = 74+1 on the Halloween
    # page); the S/J and Crosbie pages are re-scores of subsets of the same
    # start — skipped as duplicates (see README "National Training Week").
    combined('iodai-ntw-2024-halloween-regatta',
             'IODAI National Training Week 2024 — Halloween Regatta & Crosbie Cup',
             'Royal St. George Yacht Club', ['2024-11-02'], nslots=4,
             files=['2024/ntw/2024NTWHalloween.htm'], fleet='Combined',
             **RSGYC, event_url='https://iodai.com/ntw-2024-halloween-regatta-amp-crosbie-cup/'),
    solo('iodai-ntw-2024-regatta-racing',
         'IODAI National Training Week 2024 — Regatta Racing',
         'Royal St. George Yacht Club', ['2024-11-02'], nslots=3,
         file='2024/ntw/2024NTWRR.htm', fleet='Regatta Racing', discards=[],
         **RSGYC, event_url='https://iodai.com/ntw-2024-halloween-regatta-amp-crosbie-cup/'),
    solo('iodai-ntw-2024-regatta-coached',
         'IODAI National Training Week 2024 — Regatta Coached',
         'Royal St. George Yacht Club', ['2024-11-02'], nslots=3,
         file='2024/ntw/2024NTWRC.htm', fleet='Regatta Coached', discards=[],
         **RSGYC, event_url='https://iodai.com/ntw-2024-halloween-regatta-amp-crosbie-cup/'),
]
