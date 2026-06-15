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

**Scoring-software caveat.** The reconstruction engine assumes **Sailwave** output
(low-point summary tables). IODAI used Sailwave for recent years, but earlier
pages (≈2009 onward, post the 2013/14 site revamp) were produced with **Sail100**,
whose HTML differs. Years are flagged below where non-Sailwave software was used;
those can't be reconstructed by this pipeline without separate parsing.

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
