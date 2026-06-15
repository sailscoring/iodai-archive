"""2020 IODAI events.

The 2020 championship season was COVID-disrupted, but the **National
championship** was held — Royal Cork YC, 13–16 August 2020. Sourced from the
iodai.com event page <https://iodai.com/provisional-results-nationals-2020-royal-cork-yacht-club/>
(results files under iodai.com/results-files/; the Regatta fleet on sailwave.com).
No regional results for 2020 have been found. See SOURCES.md.

Main fleet was scored as separate Senior/Junior scratch fleets (each page's
DNC = its own boat count + 1); the Regatta was a single combined fleet.
"""
from .helpers import main_fleet, solo, RCYC

N = '2020/nationals/'

SERIES = [
    # --- Nationals @ Royal Cork YC (13–16 Aug) -------------------------------
    main_fleet('iodai-nationals-2020-main-fleet', 'IODAI Nationals 2020 — Main Fleet',
               'Royal Cork Yacht Club',
               ['2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16'], nslots=10,
               senior=N + 'nase20os.html', junior=N + 'naju20os.html',
               discards=[(4, 1), (10, 2)], **RCYC, event_url='https://iodai.com/provisional-results-nationals-2020-royal-cork-yacht-club/'),
    solo('iodai-nationals-2020-regatta', 'IODAI Nationals 2020 — Regatta',
         'Royal Cork Yacht Club',
         ['2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16'], nslots=6,
         file=N + 'AIBOptimistNationals2020RegattaFleet.htm', fleet='Regatta', **RCYC, event_url='https://iodai.com/provisional-results-nationals-2020-royal-cork-yacht-club/'),
]
