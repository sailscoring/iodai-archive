# Sources

Provenance for every reconstructed series: the **iodai.com event page** (the
authoritative record of which Sailwave files are the official results) and the
specific Sailwave / iodai.com result file each fleet was built from. Every file
listed has been re-fetched and confirmed to match the data we built against.

Pre-2024 files live at the `sailwave.com/results/` root; 2024–2026 under
`/results/IODAI/`; many 2021 files under `iodai.com/results-files/`. Sourcing each
event starts from its iodai.com page — see README.md.

## How these event pages were found

There's no clean "browse by year/event" path on iodai.com, and the page slugs
aren't uniform (recent years use `<year>-<region>-championships`; older years use
descriptive slugs like `leinster-championships-national-yacht-club`, dated ones
like `mbsc-results-2021`, and even WordPress post-IDs like `28401-2` for the 2023
Munsters). So the method was:

1. **Start at the master index, <https://iodai.com/Results>** — the site's top-nav
   "Results" link. It's a flat, year-grouped list of links to every event's
   results page (2021→present); it gave most slugs directly.
2. **Skip the announcement pages.** For 2024–2025 the index often lists an
   `upgrades-to-gold-and-silver-following-…` post — these announce division
   promotions and carry **no** result links. The real results page is a separate
   post. Rule of thumb: if a page has no `sailwave.com/results` /
   `iodai.com/results-files` links, it's the wrong one.
3. **Probe for the canonical page when the index didn't give it**, using the
   `<year>-<region>-championships` convention (note: 2025 spells it *connacht*,
   2024 *connaught*) and checking for HTTP 200.
4. **Confirm by the links on the page, not its title** — a page is the right one
   when it carries the expected per-fleet set (Senior / Junior / Regatta Racing /
   Regatta Coached).
5. **2021–2023 slugs came from the maintainer's notes** (`IODAI Results.md`), since
   those descriptive / post-ID slugs aren't guessable.

Each file below was then re-fetched from these pages and its results data
confirmed against the copy we built from.

### Earlier years (pre-2021): the Wayback Machine

`iodai.com/Results` only goes back to 2021, but the site's older event pages (and
the result files they link) are preserved in the [Wayback Machine](https://web.archive.org).
The process:

1. **List the year's pages with the CDX API** (one request, no manual snapshot
   walking):
   `https://web.archive.org/cdx/search/cdx?url=iodai.com&matchType=domain&from=YYYY0101&to=YYYY1231&collapse=urlkey&fl=original,timestamp,statuscode`
   That returns every archived iodai.com URL for the year — the "article list".
2. **Filter** to event/result slugs; drop `gallery/`, `category/`, `tag/`, `feed`,
   oembed and social-share URLs.
3. **Fetch each archived page raw** with the `id_` suffix —
   `https://web.archive.org/web/<timestamp>id_/<url>` — which omits the Wayback
   toolbar/rewriting so link extraction is clean.
4. **Extract result links**, catching both absolute `sailwave.com/results/…` and
   **relative** `/results-files/…` (older pages link results relative to the host).
5. **Use era-appropriate snapshots.** A later snapshot of `/results` shows only the
   then-current season; the individual event pages preserve their own links, so
   prefer a snapshot from the event's own year (or shortly after).
6. **Fetch the result files** from the live host first (most `iodai.com/results-files/…`
   and `sailwave.com/results/…` files still resolve); fall back to the archive
   (`…id_/…`) for any that 404.

Result files of this era follow a tidy convention:
`<region><fleet><yy>os.html` — region `le`/`mu`/`na`/`co`(/`ul`), fleet `se`/`ju`/`re`
(and `all` for a combined view), e.g. `lese18os` = Leinster Senior 2018.

**Scoring software & phases.** The engine reconstructs low-point tables —
**Sailwave** (2014→) and the **newer Sail100** export (some 2019 events). **2013
and earlier** use an **older Sail100** that prints final points (positions *and*
penalties) as bare numbers with no result codes — a DNC shows as e.g. `46`,
indistinguishable from 46th place. These are **Phase 2 (best-effort)**: the
`bare_dnc` rule treats any plain score above the fleet size as a DNC-equivalent,
which reconstructs almost every boat exactly and the top-half ranking reliably
(the agreed bar); venues aren't recorded on these pages (left blank). 2014→2026
are full-accuracy Phase 1.

## 2026

### Ulsters
Event page: <https://iodai.com/2026-ulster-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2026ULSTERSSLYCSM.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2026ULSTERSSLYCJM.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2026ULSTERSRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2026ULSTERSRC.htm>

### Munsters
Event page: <https://iodai.com/2026-munster-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2026MUNSTERSWHSCSM.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2026MUNSTERSWHSCJM.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2026MunstersWHSCRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2026MunstersWHSCRC.htm>

### Sprint Series
Event page: <https://iodai.com/iodai-sprint-series-2026/>  
- Sprint: <https://sailwave.com/results/IODAI/2026Sprint%20SeriesOverall.htm>

### Irish Sailing Youth Nationals (Optimist)
Event page: <https://iodai.com/2026-irish-sailing-youth-national-championships/>  
- Optimist: <https://sailwave.com/results/IODAI/YNBYC2026.htm>

## 2025

### Leinsters
Event page: <https://iodai.com/2025-leinster-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2025LeinstersNYCS.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2025LeinstersNYC.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2025LeinstersRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2025LeinstersRC.htm>

### Ulsters
Event page: <https://iodai.com/2025-ulster-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2025UlstersEABCS.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2025UlstersEABCJ.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2025UlstersEABCRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2025UlstersEABCRC.htm>

### Connachts
Event page: <https://iodai.com/2025-connacht-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2025ConnachtsLDYCSM.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2025ConnachtsLDYCJM.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2025ConnachtsLDYCRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2025ConnachtsLDYCRC.htm>

### Munsters
Event page: <https://iodai.com/2025-munster-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2025MunstersKYCSM.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2025MunstersKYCJM.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2025MunstersKYCRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2025MunstersKYCRC.htm>

### Nationals
Event page: <https://iodai.com/2025-irish-optimist-national-championships/>  
- Main (Senior): <https://sailwave.com/results/IODAI/2025NationalsLRYCSM.htm>
- Main (Junior): <https://sailwave.com/results/IODAI/2025NationalsLRYCJM.htm>
- Regatta Racing: <https://sailwave.com/results/IODAI/2025NationalsLRYCRR.htm>
- Regatta Coached: <https://sailwave.com/results/IODAI/2025NationalsLRYCRC.htm>

### Sprint Series
Event page: <https://iodai.com/iodai-sprint-series-2025/>  
- Sprint (Senior): <https://sailwave.com/results/IODAI/2025SprintOverallS.htm>
- Sprint (Junior): <https://sailwave.com/results/IODAI/2025SprintOverallJ.htm>

### Irish Sailing Youth Nationals (Optimist)
Event page: <https://iodai.com/2025-irish-sailing-youth-national-championships/>  
- Optimist: <https://www.sailwave.com/results/IODAI/YouthNationals.htm>

  The generic `YouthNationals.htm` filename identifies itself in its title as
  "Irish Sailing Youth Nationals 2025 at Royal St. George Yacht Club"; the race
  titles carry per-race dates (24–27 Apr 2025).

### National Training Week (Halloween Regatta & Crosbie Cup)
Event page: <https://iodai.com/ntw-2025-halloween-regatta-crosbie-cup/>  
- Halloween Regatta (combined, built): <https://www.sailwave.com/results/IODAI/2025NTWLDYCHalloweenCup.htm>
- Regatta Racing: <https://www.sailwave.com/results/IODAI/2025HalloweenRegattaLDYCRR.htm>
- Regatta Coached (0-race roster): <https://www.sailwave.com/results/IODAI/2025HalloweenRegattaLDYCRC.htm>
- Not built (views of the same start): Senior/Junior re-scores
  (<https://www.sailwave.com/results/IODAI/2025NTWLDYCSM.htm>,
  <https://www.sailwave.com/results/IODAI/2025NTWLDYCJM.htm>) and the Crosbie
  page with carried combined-start positions
  (<https://www.sailwave.com/results/IODAI/2025NTWLDYCCrosbie.htm>) — kept in
  sources/ for reference. See README "National Training Week".

### Season rankings (#7)
Published as a Sailwave series — one "race" column per event (Leinsters,
Ulsters, Connaghts, Nationals, Munsters; 5 sailed, 2 discards, 3 to count).
Revisions are separate files; the **final revision is authoritative**:

- Senior, final (Dec 9, 44 sailors): <https://www.sailwave.com/results/IODAI/2025SNRNR.htm>
- Junior, final (Oct 3, 49 sailors): <https://www.sailwave.com/results/IODAI/2025JNRNR.htm>
- Senior, earlier revisions (Sept 22/23, 43 sailors):
  <https://www.sailwave.com/results/IODAI/2025SNRRA.htm>,
  <https://www.sailwave.com/results/IODAI/2025SNRRAalt.htm>
- Junior, earlier revision (Sept 23, content-identical to final):
  <https://www.sailwave.com/results/IODAI/2025JNRRA.htm>

The Senior September→December delta (see `python3 ranking.py diff`) is
domain-significant: a 44th sailor was added (every DNC moved 44→45), and the
Donagh sisters' **Ulsters RDGa redress was revoked** — Maeve's counted `1.5
RDGa` became a discarded DNC, swapping ranks 1 and 2, so **Emily Donagh is the
final 2025 Senior champion** on a 4.0 nett tie-break. Six Senior + one Junior
`RDGa` entries (all for the **Connaghts**) survive to the final sheets — the
committee-average redress the app replicates as manual adjustments. Both
sheets are all-IRL (the "excluding non-Irish sailors" compression happens when
event places enter the ranking).

## 2024

### Leinsters
Event page: <https://iodai.com/2024-leinster-championships/>  
- Main (Senior): <https://sailwave.com/results/2024MYCMainS.htm>
- Main (Junior): <https://sailwave.com/results/2024MYCMainJ.htm>
- Regatta Racing: <https://sailwave.com/results/2024MYCRR.htm>
- Regatta Coached: <https://sailwave.com/results/2024MYCRC.htm>

### Ulsters
Event page: <https://iodai.com/2024-ulster-championships/>  
- Main (Senior): <https://sailwave.com/results/2024UlstersMainS.htm>
- Main (Junior): <https://sailwave.com/results/2024UlstersMainJ.htm>
- Regatta Racing: <https://sailwave.com/results/2024UlstersRR.htm>
- Regatta Coached: <https://sailwave.com/results/2024UlstersRC.htm>

### Connachts
Event page: <https://iodai.com/2024-connaught-championships/>  
- Main (Senior): <https://sailwave.com/results/2024GBSCMainS.htm>
- Main (Junior): <https://sailwave.com/results/2024GBSCMainJ.htm>
- Regatta Racing: <https://sailwave.com/results/2024GBSCRR.htm>
- Regatta Coached: <https://sailwave.com/results/2024GBSCRC.htm>

### Munsters
Event page: <https://iodai.com/2024-munster-championships/>  
- Main (Senior): <https://sailwave.com/results/RCYC24MainS.htm>
- Main (Junior): <https://sailwave.com/results/RCYC24MainJ.htm>
- Regatta Racing: <https://sailwave.com/results/RCYC24RR.htm>
- Regatta Coached: <https://sailwave.com/results/RCYC24RC.htm>

### Nationals
Event page: <https://iodai.com/irish-optimist-national-championships-2024/>  
- Main (Senior): <https://sailwave.com/results/2024HYCMainS.htm>
- Main (Junior): <https://sailwave.com/results/2024HYCMainJ.htm>
- Regatta Racing: <https://sailwave.com/results/2024HYCRR.htm>
- Regatta Coached: <https://sailwave.com/results/2024HYCRC.htm>

### Sprint Series
Event page: <https://iodai.com/iodai-sprint-series-2024/>  
- Sprint: <https://sailwave.com/results/2024SprintSeriesALL.htm>

### Irish Sailing Youth Nationals (Optimist)
Event page: <https://iodai.com/2024-irish-sailing-youth-national-championships/>  
Irish Sailing Live: <https://irishsailinglive.ie/event-results/847/2024-04-04/482>  
- Optimist: <https://sailwave.com/results/IODAI/2024YNOptimist.htm>

  Our copy was confirmed against the Irish Sailing Live record (event 847, Royal
  Cork YC, 4 Apr 2024, `ResultsFrom: Sailwave`): identical 38 boats and Nett
  scores. Irish Sailing Live links its own current-year pages from
  <https://www.sailing.ie/Events/Irish-Sailing-Youth-National-Championships>.

### National Training Week (Halloween Regatta & Crosbie Cup)
Event page: <https://iodai.com/ntw-2024-halloween-regatta-amp-crosbie-cup/>  
- Halloween Regatta (combined, built): <https://sailwave.com/results/IODAI/2024NTWHalloween.htm>
- Regatta Racing: <https://www.sailwave.com/results/IODAI/2024NTWRR.htm>
- Regatta Coached: <https://www.sailwave.com/results/IODAI/2024NTWRC.htm>
- Not built (subset re-scores of the same start): MainS / MainJ / Crosbie
  (<https://www.sailwave.com/results/IODAI/2024NTWMainS.htm>,
  <https://www.sailwave.com/results/IODAI/2024NTWMainJ.htm>,
  <https://www.sailwave.com/results/IODAI/2024NTWCrosbie.htm>) — kept in
  sources/ for reference.

## 2023

### Leinsters
Event page: <https://iodai.com/leinster-championships-national-yacht-club/>  
- Main (Senior): <https://sailwave.com/results/NYCMainS.htm>
- Main (Junior): <https://sailwave.com/results/MainJ.htm>
- Regatta Racing: <https://sailwave.com/results/NYCRR23.html>
- Regatta Coached: <https://sailwave.com/results/NYCRC23.html>

### Ulsters
Event page: <https://iodai.com/ulster-championships-east-antrim-boat-club/>  
- Main (Senior): <https://sailwave.com/results/EABCMainS.htm>
- Main (Junior): <https://sailwave.com/results/EABCMainJ.htm>
- Regatta Racing: <https://sailwave.com/results/EABCRR.htm>
- Regatta Coached: <https://sailwave.com/results/EABCRC.htm>

### Connachts
Event page: <https://iodai.com/connaught-championships-lough-ree-yacht-club/>  
- Main (Senior): <http://sailwave.com/results/23LRYCMainS.htm>
- Main (Junior): <http://sailwave.com/results/23LRYCMainJ.htm>
- Regatta Racing: <http://sailwave.com/results/23LRYCRR.htm>
- Regatta Coached: <http://sailwave.com/results/23LRYCRC.htm>

### Munsters
Event page: <https://iodai.com/28401-2/>  
- Main (Senior): <http://sailwave.com/results/23WHSCMainS.htm>
- Main (Junior): <http://sailwave.com/results/23WHSCMainJ.htm>
- Regatta Racing: <http://sailwave.com/results/23WHSCRR.htm>
- Regatta Coached: <http://sailwave.com/results/23WHSCRC.htm>

### Nationals
Event page: <https://iodai.com/irish-optimist-national-championships-2023/>  
- Main (Senior): <https://sailwave.com/results/BYC23MainS.html>
- Main (Junior): <https://sailwave.com/results/BYC23MainJ.html>
- Regatta Racing: <https://sailwave.com/results/BYC23RR.html>

### Irish Sailing Youth Nationals (Optimist)
- Optimist: <https://www.sailwave.com/results/YNHYC2023Main.html>

  "2023 Irish Sailing Investwise Youth Nationals at Howth Yacht Club
  13-16 April 2023" per the page header.

### National Training Week (Halloween Regatta & Crosbie Cup)
Event page: <https://iodai.com/national-training-week-2023/>  
- Halloween Regatta (combined, built): <https://www.sailwave.com/results/RCYC23Main.htm>
- Regatta Racing: <https://www.sailwave.com/results/RCYC23RR.htm>
- Regatta Coached (0-race roster): <https://www.sailwave.com/results/RCYC23RC.htm>
- Not built (subset re-scores of the same start): MainS / MainJ / MainC
  ('Crobie' sic) (<https://www.sailwave.com/results/RCYC23MainS.htm>,
  <https://www.sailwave.com/results/RCYC23MainJ.htm>,
  <https://www.sailwave.com/results/RCYC23MainC.htm>) — kept in sources/ for
  reference.

## 2022

### Leinsters
Event page: <https://iodai.com/skerries-leinsters-results/>  
- Main (Senior): <https://sailwave.com/results/SSC2022S.html>
- Main (Junior): <https://sailwave.com/results/SSC2022J.html>
- Regatta: <https://sailwave.com/results/SSC2022R.html>

### Ulsters
Event page: <https://iodai.com/optimist-ulsters-hyc-results/>  
- Main (Senior): <https://sailwave.com/results/OHYC2022S.html>
- Main (Junior): <https://sailwave.com/results/OHYC2022J.html>
- Regatta Racing: <https://sailwave.com/results/OHYC2022RR.html>
- Regatta Coached: <https://sailwave.com/results/OHYC2022RC.html>

### Connachts
Event page: <https://iodai.com/galway-bay-connaughts-results/>  
- Main (Senior): <https://sailwave.com/results/G2022S.html>
- Main (Junior): <https://sailwave.com/results/G2022J.html>
- Regatta: <https://sailwave.com/results/G2022R.html>

### Munsters
Event page: <https://iodai.com/rcyc-munsters-results/>  
- Main (Senior): <https://sailwave.com/results/RCYC2022M.html>
- Main (Junior): <https://sailwave.com/results/RCYC2022J.html>
- Regatta: <https://sailwave.com/results/RCYC2022R.html>

### Nationals
Event page: <https://iodai.com/optimist-nationals-results/>  
- Main (Senior): <https://sailwave.com/results/ONATS2022S.html>
- Main (Junior): <https://sailwave.com/results/ONATS2022J.html>
- Regatta Racing: <https://sailwave.com/results/ONATS2022RR.html>
- Regatta Coached: <https://sailwave.com/results/ONATS2022RC2.html>

### Irish Sailing Youth Nationals (Optimist)
- Optimist: <https://www.sailwave.com/results/ballyholmyc/I%20Y%2022%20OPTIMIST.htm>

  "Irish Sailing Youth National Championship 2022 at Ballyholme Yacht Club" per
  the page title; results final 24 Apr 2022. The page carries no per-race dates,
  so the 21–24 Apr window is approximate (rule 6).

### National Training Week (Halloween Regatta & Crosbie Cup)
Event page: <https://iodai.com/ntw-results-2022/>  
- Halloween Regatta (combined, built): <https://www.sailwave.com/results/NTW22.html>
- Not built (views of the same start): Senior/Junior filtered views carrying
  the combined scores (<https://www.sailwave.com/results/NTWS22.html>,
  <https://sailwave.com/results/NTWJ22.html>) and the NTWC122 group re-score
  (<https://sailwave.com/results/NTWC122.html>) — kept in sources/ for
  reference. No regatta-fleet pages were published for 2022.

## 2021

### Leinsters
Event page: <https://iodai.com/results-leinsters-2021/>  
- Main (Senior): <https://iodai.com/results-files/leinster2021SF.html>
- Main (Junior): <https://iodai.com/results-files/leinster2021JF.html>
- Regatta: <https://iodai.com/results-files/leinster2021R.html>

### Ulsters
Event page: <https://iodai.com/eabc-results-2021/>  
- Main (Senior): <https://iodai.com/results-files/EABC2021SF.html>
- Main (Junior): <https://iodai.com/results-files/EABC2021JF.html>
- Regatta: <https://iodai.com/results-files/EABC2021R.html>

### Connachts
Event page: <https://iodai.com/results-connaughts-2021/>  
- Main (Senior): <https://iodai.com/results-files/Conn2021SF.html>
- Main (Junior): <https://iodai.com/results-files/Conn2021JF.html>
- Regatta: <https://iodai.com/results-files/Conn2021R.html>

### Munsters
Event page: <https://iodai.com/mbsc-results-2021/>  
- Main (Senior): <https://sailwave.com/results/MBSC2021SF.html>
- Main (Junior): <https://sailwave.com/results/MBSC2021J1.html>
- Regatta: <https://sailwave.com/results/MBSC21R.html>

### Nationals
Event page: <https://iodai.com/iodai-nationals-2021-results/>  
- Main (Senior): <https://iodai.com/results-files/Nats2021SF.html>
- Main (Junior): <https://iodai.com/results-files/Nats2021JF.html>
- Regatta: <https://iodai.com/results-files/Nats2021R.html>

### National Training Week (Halloween Regatta & Crosbie Cup)
Event page: <https://iodai.com/ntw-results-2021/>  
- Halloween Regatta (combined, built): <https://www.sailwave.com/results/NTW21.html>
- Regatta: <https://sailwave.com/results/NTWR21.html>
- Not built (filtered views carrying the combined scores): S / J / Crosbie
  (<https://www.sailwave.com/results/NTWS21.html>,
  <https://sailwave.com/results/NTWJ21.html>,
  <https://sailwave.com/results/NTWC21.html>) — kept in sources/ for
  reference.

## 2020

Only the Nationals has been found (the 2020 season was COVID-disrupted). Its
event page is not listed in the `/Results` index.

### Nationals
Event page: <https://iodai.com/provisional-results-nationals-2020-royal-cork-yacht-club/>  
- Main (Senior): <https://iodai.com/results-files/nase20os.html>
- Main (Junior): <https://iodai.com/results-files/naju20os.html>
- Regatta: <https://sailwave.com/results/AIBOptimistNationals2020RegattaFleet.htm>

  (A combined Senior+Junior view, `naall20os.html`, is also linked but not built —
  the per-fleet pages are used.)

## 2019

Sourced via Wayback (the `results-<region>-2019-<club>` pages); files live under
iodai.com/results-files/. **Ulsters used Sail100** (flagged); the **Munster Regatta**
published only an entry list (not built).

### Leinsters — Sailwave
Event page: <https://iodai.com/results-leinsters-2019-malahide-yacht-club/>  
- Main (Senior): <https://iodai.com/results-files/lese19os.html>
- Main (Junior): <https://iodai.com/results-files/leju19os.html>
- Regatta: <https://iodai.com/results-files/lere19os.html>

### Ulsters — **Sail100**
Event page: <https://iodai.com/results-ulsters-2019-skerries-sailing-club/>  
- Main (Senior): <https://iodai.com/results-files/ulse19os.html>
- Main (Junior): <https://iodai.com/results-files/ulju19os.html>
- Regatta: <https://iodai.com/results-files/ulre19os.html>

### Connachts — Sailwave
Event page: <https://iodai.com/results-connaughts-2019-lough-ree-yacht-club/>  
- Main (Senior): <https://iodai.com/results-files/cose19os.html>
- Main (Junior): <https://iodai.com/results-files/coju19os.html>
- Regatta: <https://iodai.com/results-files/core19os.html>

### Munsters — Sailwave
Event page: <https://iodai.com/results-munsters-2019-wexford-harbour-sailing-club/>  
- Main (Senior): <https://iodai.com/results-files/muse19os.html>
- Main (Junior): <https://iodai.com/results-files/muju19os.html>
- Regatta: entry list only (`mure19os.html`) — not built.

### Nationals — Sailwave
Event page: <https://iodai.com/results-nationals-2019-howth-yacht-club/>  
- Main (Senior): <https://iodai.com/results-files/nase19os.html>
- Main (Junior): <https://iodai.com/results-files/naju19os.html>
- Regatta: <https://iodai.com/results-files/nare19os.html>

### Optimist Trials
- Trials: <https://iodai.com/results-files/trials2019.html>

  "Irish Optimist Trials 2019 at Royal Cork Yacht Club — 25-28 April 2019";
  one combined 60-boat fleet over 8 races. The last standalone Trials: the
  2020 trials ranking was the Nationals overall standings
  (<https://iodai.com/results-files/naall20os.html>, kept in
  sources/2020/nationals/ — deliberately not built as a separate series, see
  README), there was none in 2021, and from 2022 the selection role passed to
  the Irish Sailing Youth Nationals.

## 2018

Sourced via Wayback; files under iodai.com/results-files/ (`<region><fleet>18os.html`;
Nationals capitalised). All Sailwave. The Main-fleet pages used non-standard tie
scoring (tied boats don't consume the next place), so a handful of boats re-score
±0.5–1 under RRS A8.1 — tolerated (`tie_tolerant`), ranks unaffected.

### Leinsters — Howth YC
Event page: <https://iodai.com/leinsters-2018-hyc-results/>  
- Main (Senior/Junior): <https://iodai.com/results-files/lese18os.html> · <https://iodai.com/results-files/leju18os.html>
- Regatta: <https://iodai.com/results-files/lere18os.html>

### Ulsters — Malahide YC
Event page: <https://iodai.com/ulsters-2018-myc/>  (via Wayback)  
- Main (Senior/Junior): <https://iodai.com/results-files/ulse18os.html> · <https://iodai.com/results-files/ulju18os.html>
- Regatta: <https://iodai.com/results-files/ulre18os.html>

### Connachts — Lough Derg YC
Event page: <https://iodai.com/connaughts-2018-results-ldyc/>  
- Main (Senior/Junior): <https://iodai.com/results-files/cose18os.html> · <https://iodai.com/results-files/coju18os.html>
- Regatta: <https://iodai.com/results-files/core18os.html>

### Munsters — Tralee Bay SC
Event page: <https://iodai.com/munsters-2018-results-tbsc/>  
- Main (Senior/Junior): <https://iodai.com/results-files/muse18os.html> · <https://iodai.com/results-files/muju18os.html>
- Regatta: <https://iodai.com/results-files/mure18os.html>

### Nationals — Kinsale YC
Event page: <https://iodai.com/nationals-2018-kyc-results/>  
- Main (Senior/Junior): <https://iodai.com/results-files/Nase18os.html> · <https://iodai.com/results-files/Naju18os.html>
- Regatta: <https://iodai.com/results-files/Nare18os.html>

### Optimist Trials
- Trials: <https://iodai.com/results-files/trials2018.html>

  "Irish Optimist Trials 2018 at Royal St. George Yacht Club — 5-8 April
  2018"; one combined 78-boat fleet over 10 races (duplicate empty 'Ranking'
  header handled by parse_file's first-non-empty rule).

## 2017

Sourced via Wayback; files under iodai.com/results-files/ (`<region><fleet>17os.html`).
All Sailwave, all five events (separate Senior/Junior Main + Regatta). Discards
read per fleet (2017 discarded later than recent years). Non-standard tie scoring
→ `tie_tolerant`. Venues: Leinster/NYC, Ulster/Royal North of Ireland YC,
Connacht/WHSC, Munster/Kinsale YC, Nationals/Royal Irish YC.

- Leinster: `lese17os` · `leju17os` · `lere17os`
- Ulster: `ulse17os` · `ulju17os` · `ulre17os`
- Connacht: `cose17os` · `coju17os` · `core17os`
- Munster: `muse17os` · `muju17os` · `mure17os`
- Nationals: `nase17os` · `naju17os` · `nare17os`

(all under <https://iodai.com/results-files/>; event pages e.g.
<https://iodai.com/leinsters-2017-results-nyc/>, `nationals-2017-results-riyc`.)

### Optimist Trials
- Trials: <https://iodai.com/results-files/trials2017.html>

  "2017 Optimist Trials — April 20th to April 23rd, 2017 at Ballyholme Yacht
  Club"; one combined 62-boat fleet over 13 races. The page's club header is
  the typo 'Ckub' and one cell carries a 'Z30' (Z-flag 30%) penalty — both
  handled in engine.py.

## 2016

Sourced via Wayback; files under iodai.com/results-files/ (`<region><fleet>16os.html`).
All Sailwave. Pages put Net/Total *before* the race columns (handled in the
engine). Non-standard tie scoring → `tie_tolerant`. Venues: Leinster/Royal St
George, Ulster/Malahide SC, Connacht/Foynes, Munster/CRYC, Nationals/Lough Derg.
The Nationals Regatta page (`nare16os`) has no results table — not built.

- Leinster: `lese16os` · `leju16os` · `lere16os`
- Ulster: `ulse16os` · `ulju16os` · `ulre16os`
- Connacht: `cose16os` · `coju16os` · `core16os`
- Munster: `muse16os` · `muju16os` · `mure16os`
- Nationals: `nase16os` · `naju16os` (Regatta `nare16os` not built)

(all under <https://iodai.com/results-files/>; event pages e.g.
`nationals-2016-results-ldyc`, `munsters-2016-results-rcyc`.)

### Optimist Trials
- Trials: <https://iodai.com/results-files/trials2016.html>

  "2016 Optimist Trials — March 31st to April 3rd, 2016 at Howth Yacht Club";
  one combined 57-boat fleet over 11 races (the lone 'Total' column is the
  nett).

## 2015

Sourced via Wayback; files under iodai.com/results-files/ (`<region><fleet>15os.html`).
All Sailwave, all five events (Main + Regatta). Some pages use ALL-CAPS headers
and a single 'Total' (net) column (handled in the engine). Venues: Leinster/Howth,
Ulster/Ballyholme, Connacht/Lough Ree, Munster/Kinsale, Nationals/Skerries.
Ulster and Connacht pages carry no date (approximate).

- Leinster: `lese15os` · `leju15os` · `lere15os`
- Ulster: `ulse15os` · `ulju15os` · `ulre15os`
- Connacht: `cose15os` · `coju15os` · `core15os`
- Munster: `muse15os` · `muju15os` · `mure15os`
- Nationals: `nase15os` · `naju15os` · `nare15os`

(all under <https://iodai.com/results-files/>; event pages e.g.
<https://iodai.com/leinsters-2015-results-hyc/>.)

### Optimist Trials
- Trials: <https://iodai.com/results-files/trials2015.html>

  "Optimist Trials 2015 at Royal Cork Yacht Club — 9-12 April 2015"; one
  combined 61-boat fleet over 13 races.

## 2014

Sourced via Wayback; files under iodai.com/results-files/ (`<region><fleet>14os.html`).
All Sailwave, all five events (Main + Regatta). Venues: Leinster/Royal Irish,
Ulster/Skerries, Connacht/Galway Bay, Munster/Tralee Bay, Nationals/Royal Cork.
One page labels its net column 'Total Points' (handled in the engine).

- Leinster: `lese14os` · `leju14os` · `lere14os`
- Ulster: `ulse14os` · `ulju14os` · `ulre14os`
- Connacht: `cose14os` · `coju14os` · `core14os`
- Munster: `muse14os` · `muju14os` · `mure14os`
- Nationals: `nase14os` · `naju14os` · `nare14os`

(all under <https://iodai.com/results-files/>.)

## 2013 — Phase 2 (older Sail100, best-effort)

Files under iodai.com/results-files/ (`<region><fleet>13os.html`). All five events,
Main + Regatta. Pages record entries/races/discards but no venue (blank) and only
a publish timestamp (dates approximate). Reconstructed via `bare_dnc`; top-half
rankings reliable. Discards [(5,1)] regionals, [(5,1),(10,2)] Nationals.

- Leinster (8 Sep): `lese13os` · `leju13os` · `lere13os`
- Ulster (26 May): `ulse13os` · `ulju13os` · `ulre13os`
- Connacht (5–6 Oct): `cose13os` · `coju13os` · `core13os`
- Munster (~May): `muse13os` · `muju13os` · `mure13os`
- Nationals (15–18 Aug): `nase13os` · `naju13os` · `nare13os`

## 2012 — Phase 2 (two events survive)

2012 was barely archived. Ulster **Senior** (`ulse12os.html`) is the only HTML
results file remaining on the site; the **Nationals** survive as PDF exports of
the old Sail100 results (surfaced by Alex Walsh — #2). All other 2012
region/fleet filenames 404 and aren't in the Wayback Machine, and no 2012
results index was archived, so the rest can't be sourced. Dates approximate
(Ulsters: only a Jan-2013 re-publish stamp; Nationals: a 'Sat 04 Aug 12' print
timestamp anchors the final day). Venues not recorded.

### Ulsters
- Ulster Senior: <https://iodai.com/results-files/ulse12os.html>

  Reconstructs exactly (27/27). Built Senior-only.

### Nationals
- Main (Senior): <https://iodai.com/results-files/nase2012os.pdf>
- Main (Junior): <https://iodai.com/results-files/naju2012os.pdf>

  PDFs, not HTML — transcribed to the pipeline's Sail100-HTML shape by
  `sources/2012/nationals/transcribe.py` (every cell lifted verbatim from the
  PDF text layer; a per-row nett checksum guards against column misalignment;
  the PDFs are kept alongside the generated HTML). Senior reconstructs exactly
  (47/47); Junior 95/96 — one deep-fleet boat (IRL1393, published nett 726.9)
  carries a bare 90.9 redress/average score that the position-based engine
  can't bit-reconstruct, within the Phase-2 bar.

## 2009–2011 — Phase 2 (older Sail100, best-effort)

Files under iodai.com/results-files/ (`<region><fleet><yy>os.html`, yy = 09/10/11),
reconstructed via `bare_dnc`; every fleet's winner is correct, most fleets
near-exact, a few large/short-series fleets looser mid-pack. Venues blank; dates
from publish timestamps (approximate). Some 2010/2011 Junior pages were not
published (those Main fleets are Senior-only). Discards [(4,1)] regional,
[(4,1),(8,2)] Nationals. (Per-file names follow the `os.html` convention above.)

## Linked but not built

These pages are linked from the iodai.com event pages above but deliberately
not turned into series (see README.md):

- **National Training Week / Crosbie Cup** (all years) — the Crosbie page carries
  each boat's finishing position from the *combined* Halloween-regatta start, not
  a position within the Crosbie group, so it isn't a contiguous scratch result.
- **2022 Ulsters Bronze re-scores** (`OHYC2022SB`/`OHYC2022JB`) — Bronze-only views
  of the same boats already carried on the primary Senior/Junior pages.
- **2023 Nationals Regatta Coached** (`BYC23RC`) — linked but the page has no
  results table.
- **Sprint per-venue / combined pages** (e.g. 2025 `2025SprintRCYC/MYC/WHSC`,
  `2025SprintOverall`) — superseded by the per-fleet Overall pages we build from.

The **Irish Sailing Youth Nationals** is an Irish Sailing event IODAI republishes,
not an IODAI championship; its results live on Irish Sailing Live (and the iodai.com
event pages don't carry a direct Sailwave link). The 2024 Optimist file was
confirmed against the Irish Sailing Live record — see the 2024 entry above.
