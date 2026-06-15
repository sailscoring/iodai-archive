"""2019 IODAI events.

Sourced via the Wayback Machine (see SOURCES.md) — the iodai.com event pages
(`results-<region>-2019-<club>`) and the result files under iodai.com/results-files/.
All five championships ran. Each event: separate Senior/Junior scratch fleets
(Main) plus a single combined Regatta fleet.

**Software:** Leinster, Connacht, Munster and the Nationals are Sailwave; the
**Ulsters (Skerries) were scored with Sail100** — a different package, but the
same low-point model, so the engine reconstructs it once the Place/Net/Country
columns are handled (added to engine.parse_file). The **Munster Regatta** wasn't
published as a scored table (only an entry list), so it isn't built.
"""
from .helpers import main_fleet, solo, MYC, SSC, LRYC, HYC

L = '2019/leinsters/'
U = '2019/ulsters/'
C = '2019/connachts/'
M = '2019/munsters/'
N = '2019/nationals/'

SERIES = [
    # --- Leinsters @ Malahide YC (15–16 Jun) — Sailwave ----------------------
    main_fleet('iodai-leinsters-2019-main-fleet', 'IODAI Leinsters 2019 — Main Fleet',
               'Malahide Yacht Club', ['2019-06-15', '2019-06-16'], nslots=6,
               senior=L + 'lese19os.html', junior=L + 'leju19os.html', **MYC),
    # Boat 1587 has RET cells scored 27 (DNF = starters) where the app uses
    # entries+1 = 28; the gap shows after discards. Suspect (source/app base diff).
    solo('iodai-leinsters-2019-regatta', 'IODAI Leinsters 2019 — Regatta',
         'Malahide Yacht Club', ['2019-06-15', '2019-06-16'], nslots=7,
         file=L + 'lere19os.html', fleet='Regatta', suspect=['1587'], **MYC),

    # --- Ulsters @ Skerries SC (25–26 May) — Sail100 -------------------------
    main_fleet('iodai-ulsters-2019-main-fleet', 'IODAI Ulsters 2019 — Main Fleet',
               'Skerries Sailing Club', ['2019-05-25', '2019-05-26'], nslots=3,
               senior=U + 'ulse19os.html', junior=U + 'ulju19os.html', **SSC),
    solo('iodai-ulsters-2019-regatta', 'IODAI Ulsters 2019 — Regatta',
         'Skerries Sailing Club', ['2019-05-25', '2019-05-26'], nslots=4,
         file=U + 'ulre19os.html', fleet='Regatta', **SSC),

    # --- Connachts @ Lough Ree YC (7–8 Sep) — Sailwave ----------------------
    main_fleet('iodai-connachts-2019-main-fleet', 'IODAI Connachts 2019 — Main Fleet',
               'Lough Ree Yacht Club', ['2019-09-07', '2019-09-08'], nslots=6,
               senior=C + 'cose19os.html', junior=C + 'coju19os.html', **LRYC),
    solo('iodai-connachts-2019-regatta', 'IODAI Connachts 2019 — Regatta',
         'Lough Ree Yacht Club', ['2019-09-07', '2019-09-08'], nslots=3,
         file=C + 'core19os.html', fleet='Regatta', **LRYC),

    # --- Munsters @ Wexford Harbour SC (20–21 Jul) — Sailwave (no logo) ------
    # Regatta fleet published only an entry list (no scored results) — not built.
    main_fleet('iodai-munsters-2019-main-fleet', 'IODAI Munsters 2019 — Main Fleet',
               'Wexford Harbour Boat & Tennis Club', ['2019-07-20', '2019-07-21'], nslots=6,
               senior=M + 'muse19os.html', junior=M + 'muju19os.html'),

    # --- Nationals @ Howth YC (15–18 Aug) — Sailwave ------------------------
    main_fleet('iodai-nationals-2019-main-fleet', 'IODAI Nationals 2019 — Main Fleet',
               'Howth Yacht Club',
               ['2019-08-15', '2019-08-16', '2019-08-17', '2019-08-18'], nslots=9,
               senior=N + 'nase19os.html', junior=N + 'naju19os.html',
               discards=[(4, 1), (9, 2)], **HYC),
    solo('iodai-nationals-2019-regatta', 'IODAI Nationals 2019 — Regatta',
         'Howth Yacht Club',
         ['2019-08-15', '2019-08-16', '2019-08-17', '2019-08-18'], nslots=10,
         file=N + 'nare19os.html', fleet='Regatta', discards=[(4, 1), (10, 2)], **HYC),
]
