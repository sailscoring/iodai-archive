# IODAI historical results → Sail Scoring

Reconstructs the **Irish Optimist Dinghy Association (IODAI)** event results,
year by year, from the published [Sailwave](https://www.sailwave.com/results/IODAI/)
HTML pages into importable `.sailscoring` files, and uses them to populate the
production IODAI workspace in [Sail Scoring](https://app.sailscoring.ie).

## Why

The payoff is the **cross-series identity and ranking** work on the Sail Scoring
horizon (`docs/design/horizon.md` in the app repo — the competitor-identity
spine, the workspace season ladder, and the per-competitor multi-year career-arc
page). Those features only come alive with *years of real history* in one
workspace: a sailor's whole Optimist arc — joining as a regatta-coached
eight-year-old, climbing through the junior and senior main-fleet years, to their
last races before ageing out. This repo builds that historical record so the
features have something rich to show.

See `docs/requirements/iodai-use-case.md` in the app repo for the IODAI domain
(three independent series per event, Junior/Senior fleets, Gold/Silver/Bronze
divisions, shared finish line) and `reference/2025-IODAI-Major-Event-SIs-v1.0.pdf`
for the sailing instructions.

## Target events per year

> **Focus (current):** the **4 regional championships** and the **National
> championship**. The Sprint Series, National Training Week / Crosbie Cup, and the
> (non-IODAI) Youth Nationals are lower priority — keep what's already built and
> validated, but don't invest further effort there unless asked. New sourcing
> should prioritise filling regional + Nationals gaps in the tracker.

IODAI runs ~7 events a season. For each past year we want:

| Event | Series produced | Priority |
|-------|-----------------|----------|
| **4 regional championships** — Leinsters, Ulsters, Connachts, Munsters | 3 each: Main (Senior + Junior fleets), Regatta Racing, Regatta Coached | **primary** |
| **National championship** | 3: Main, Regatta Racing, Regatta Coached | **primary** |
| **National Training Week** — final-day racing (Crosbie Cup) | 1+ | low |
| **Sprint Series** (runs from 2024) | 1: Main, Senior + Junior scored separately | low |
| **Irish Sailing Youth Nationals** (Optimist; not IODAI-run) | 1 | low |

A "series" here is **one group sharing a finish line** (the app's rule): an event
with Main + two regatta fleets is *three* independent series, not one. Main Fleet
holds Junior and Senior as separate scratch fleets scored independently;
Gold/Silver/Bronze is a prize subdivision within each.

## Status tracker

✅ sourced & built · ◻️ not yet sourced · — didn't exist / not held that year

| Year | Leinsters | Ulsters | Connachts | Munsters | Nationals | Crosbie Cup | Sprint |
|-----:|:---------:|:-------:|:---------:|:--------:|:---------:|:-----------:|:------:|
| 2026 | ◻️ | ✅ | ◻️ | ✅ | ◻️ | ◻️ | ✅ |
| 2025 | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | ✅ |
| 2024 | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | ✅ |
| 2023 | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2022 | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2021 | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2020 | ◻️ | ◻️ | ◻️ | ◻️ | ✅ | — | — |

**2020**: COVID-disrupted, but the **National championship was held** (Royal Cork
YC, 13–16 Aug) and is sourced. Its iodai.com page isn't in the `/Results` index —
it's `provisional-results-nationals-2020-royal-cork-yacht-club`. No 2020 *regional*
results have been found yet (◻️); they may not have run, or may be published under
slugs not yet located — absence isn't proof, so they're left open rather than —.

Also sourced: the **Irish Sailing Youth Nationals (Optimist)** for 2024 and 2026
— not IODAI-run, but IODAI republishes its Optimist results and the same sailors
appear, so it's useful for the identity work. Years before 2021 remain to be
worked back through.

**`SOURCES.md`** records, per event, the iodai.com page and the exact Sailwave
result file each fleet was built from — the provenance trail behind every series.

The **Crosbie Cup** (National Training Week final day) is not reconstructable by
this pipeline: its published page carries each boat's finishing position from the
*combined* Halloween-regatta start rather than a position within the Crosbie
group, so the race cells aren't a contiguous scratch result. Left unsourced until
the engine can model carried scores. See the note in `events/y2025.py`.

## Layout

```
build.py                  CLI: build / validate / adopt
engine.py                 reusable engine — HTML parsing, .sailscoring assembly,
                          deterministic ids, validation, adopt
events/
  helpers.py              two_per_day(), venue/event logo constants
  y2026.py                2026 series configs (one dict per series)
  __init__.py             aggregates every year into ALL_SERIES
sources/<year>/<event>/   raw Sailwave HTML, as downloaded
series/                   generated .sailscoring files (import these)
adopted-series-ids.json   live seriesId per series, once imported (see "adopt")
```

## Per-event process (once per past event)

1. **Find the event's iodai.com page first.** Each event has an official page on
   <https://iodai.com/> that links to its canonical Sailwave result pages — e.g.
   <https://iodai.com/2026-munster-championships/>,
   <https://iodai.com/2026-ulster-championships/>,
   <https://iodai.com/iodai-sprint-series-2026/>,
   <https://iodai.com/2026-irish-sailing-youth-national-championships/>. This page
   is the authoritative record of *which* Sailwave files are the official results,
   as opposed to test artifacts or superseded provisional uploads also visible on
   the Sailwave site. Start the detective work here, then follow its links to the
   Sailwave pages — one per *(fleet × view)*. You want the final, whole-series page
   for each fleet (Senior, Junior, Regatta Racing, Regatta Coached), not per-day or
   provisional views. <https://www.sailwave.com/results/IODAI/> is the fallback
   index if an event has no iodai.com page.
2. **Download** each page into `sources/<year>/<event>/` verbatim (`curl -O`).
3. **Add a config** entry per series to `events/y<year>.py` (create the file and
   wire it into `events/__init__.py` for a new year). Set `out` (the file slug —
   also the stable id key, never rename it after import), `fleet_order`,
   `sources`, `discards`, `nslots`, dates, venue, and logos. Copy a 2026 entry as
   a template.
4. **Build & validate:**
   ```
   python3 build.py validate    # re-scores each fleet, diffs against published Nett
   python3 build.py             # writes series/<out>.sailscoring
   ```
   `validate` must pass (every boat's reconstructed Nett matches the page) before
   the file is trustworthy.
5. **Import** `series/<out>.sailscoring` into the IODAI workspace
   (Series list → Import Series).

## Updating or re-importing a live series (`adopt`)

A *first* import discards the file's `seriesId` and mints a new one, but the
app's **Actions → Update from File** matches an existing series by `seriesId`
*alone*. So to push a correction or later races onto a series already in the
workspace, the file must carry that live series' id:

```
# In the app: open the series → Actions → Save to File. Then:
python3 build.py adopt path/to/live-export.sailscoring
```

`adopt` matches the export to a config by series name, records its id in
`adopted-series-ids.json`, and rebuilds so that file re-imports over the live
series. The mapping is committed, so later regenerations stay re-importable.

## How the reconstruction works

In a scratch Appendix-A fleet the displayed low-point score *is* the finishing
position, so each race cell maps back to a finish: a bare number → placing
(`sortOrder`), `"<pts> <CODE>"` → coded finish (`resultCode`), an additive
penalty like `ZFP` → a finish with `penaltyCode`. Parentheses (a discard) are
dropped — the app's engine recomputes discards. `validate` re-scores with a
low-point engine mirroring the app's `lib/scoring.ts` and confirms the
reconstructed Nett matches the published page, every boat.

All ids are deterministic (UUIDv5 of a stable key), so rebuilding is byte-stable
— re-running after more races publish changes only the new race data, never ids.
