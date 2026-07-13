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
| **IODAI Trials** (2015–2020; team selection, superseded by the Youth Nationals) | 1: single combined fleet | low |
| **Irish Sailing Youth Nationals** (Optimist; not IODAI-run) | 1 | low |

A "series" here is **one group sharing a finish line** (the app's rule): an event
with Main + two regatta fleets is *three* independent series, not one. Main Fleet
holds Junior and Senior as separate scratch fleets scored independently;
Gold/Silver/Bronze is a prize subdivision within each.

## Status tracker

✅ sourced & built · ◻️ not yet sourced · — didn't exist / not held that year

| Year | Leinsters | Ulsters | Connachts | Munsters | Nationals | Trials | Crosbie Cup | Sprint |
|-----:|:---------:|:-------:|:---------:|:--------:|:---------:|:------:|:-----------:|:------:|
| 2026 | ◻️ | ✅ | ◻️ | ✅ | ◻️ | — | ◻️ | ✅ |
| 2025 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | ✅ |
| 2024 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | ✅ |
| 2023 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2022 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2021 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2020 | — | — | — | — | ✅ | ✅¶ | — | — |
| 2019 | ✅ | ✅* | ✅ | ✅† | ✅ | ✅ | ◻️ | — |
| 2018 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2017 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2016 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2015 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ | — |
| 2014 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2013‡ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2012 | — | ✅§ | — | — | — | — | — | — |
| 2011‡ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2010‡ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |
| 2009‡ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ◻️ | — |

‡ **Phase 2 (best-effort).** 2013 and earlier use an older **Sail100** that prints
final points — positions *and* DNC-type penalties — as bare numbers with no result
codes (a DNC shows as e.g. `46`, indistinguishable from 46th place). The engine's
`bare_dnc` rule treats any plain score above the fleet size as a DNC-equivalent,
which reconstructs almost every boat exactly and the **top-half ranking of each
fleet reliably** — the agreed bar for this phase (a few deep-fleet boats may be a
place out; venues aren't on the pages, so they're left blank/editable). 2014→2026
remain full-accuracy Phase 1. **2009–2011** are now built on this basis
(spot-checked: every fleet's winner reconstructs correctly; a few big/short-series
fleets are looser mid-pack — Munster 2009 Junior is the weakest). Some 2010/2011
Junior pages weren't found (those Main fleets are Senior-only). § **2012** is
almost entirely missing — barely archived, and only one results file survives on
the site (Ulster **Senior**, built; reconstructs exactly). No other 2012
region/fleet or results index could be located on iodai.com or in the Wayback
Machine.

**2020**: COVID-disrupted. The **regionals were cancelled** — IODAI's own page
states "Due to Covid-19, we have cancelled the first two regionals in May and
June," with a separate `leinsters-cancelled` notice, and the Wayback CDX listing
of iodai.com in 2020 shows no 2020 regional results pages. Only the **National
championship went ahead** (Royal Cork YC, 13–16 Aug) and is sourced — its page
isn't in the `/Results` index (`provisional-results-nationals-2020-royal-cork-yacht-club`).

Also sourced: the **Irish Sailing Youth Nationals (Optimist)** for 2022–2026 —
not IODAI-run, but IODAI republishes its Optimist results and the same sailors
appear, so it's useful for the identity work. For IODAI it carries the
team-selection purpose the pre-2021 **Trials** served (#3/#4); no Optimist
Youth Nationals page earlier than 2022 has been located.

**Trials** (`iodai-trials-<year>`): IODAI's team-selection events, 2015–2019
built as their own event type — one series, one combined scratch fleet ranking
Senior + Junior together (the pages' Senior/Junior column is informational).
Modeled separately from the Youth Nationals (different organiser, name and
slug family) but the two form **one selection lineage** for the identity and
ranking work: Trials (→2020) → no event in 2021 → Youth Nationals (2022→).
¶ **2020**: no separate trials regatta was held — the trials ranking was the
**combined Senior+Junior overall standings of the Nationals** (the
`naall20os.html` overall page, kept in `sources/2020/nationals/`). Those races
are already in the workspace as the built 2020 Nationals Main Fleet, and a
series = one finish-line group, so building a second series from the same
races would double-count every sailor's appearance in the identity timeline —
deliberately **not** built as a separate `.sailscoring` file.

\* **Sail100** (not Sailwave) was used for the 2019 Ulsters — the engine handles
both (same low-point model). † 2019 Munster Regatta published only an entry list
(no scored results), so only the Main fleet is built. Pre-2021 events were sourced
via the Wayback Machine; see SOURCES.md.

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
audit.py                  identity data-quality audit -> IDENTITY-AUDIT.md
bootstrap.py              generate a draft manifest.py from the app's matcher
compile.py                compile curated manifest.py -> manifest.json (for the app)
identity_manifest.py      the C(...) manifest record + slug minting + serialiser
manifest.py               the curated competitor-identity golden record (#218)
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

A handful of boats carry published Nett values that genuinely can't be
reproduced from the source (un-averaged ties, whole-number penalties, wrong
DNC/DNF bases). These are flagged `suspect=[...]` in the config, tolerated by
`validate`, and collected in [SUSPECTS.md](SUSPECTS.md) for manual audit.

Separately, `python3 audit.py` reports **name / cross-series-identity**
data-quality issues in the built files — blank names, mojibake, single-token
names, and sail-number "loan" candidates — into [IDENTITY-AUDIT.md](IDENTITY-AUDIT.md).
These muddle a sailor's recurring identity once imported (sailscoring #218); fix
them at source here and re-import. A stopgap capture of the ad-hoc audits — the
production, DB-side, cross-class version lives with `reconcile-identities` in the app.

All ids are deterministic (UUIDv5 of a stable key), so rebuilding is byte-stable
— re-running after more races publish changes only the new race data, never ids.

## Competitor identity manifest (#218)

The same sailor recurs across years under different sail numbers, name spellings,
and clubs. `manifest.py` is the **golden record** that ties those rows together
into one cross-series competitor — version-controlled, so re-importing the corpus
and applying the manifest reproduces the same competitors (and the same public
URLs) every time, instead of clicking through the app's reconcile UI.

```
python3 bootstrap.py            # draft manifest.py from the app's matcher
python3 bootstrap.py --force    # regenerate the draft (discards hand-curation)
```

`bootstrap.py` clusters every *named* competitor through the app's **canonical
matcher** — the sibling repo's `pnpm cluster-rows`, the very matcher
`reconcile-identities` uses — and writes a draft `manifest.py`. It clusters the
archive's own rows (not the live workspace) so every cluster is keyed by
`(series-slug, sail)` directly; the app mints fresh competitor ids on import, so
the live ids can't be mapped back to a slug after the fact. **Needs the sibling
app repo at `../sailscoring`** (and `pnpm`) for the matcher.

Then **curate by hand**: merge the nickname/typo splits the matcher leaves as
review suggestions (commented at the top of the draft), split over-merged
namesakes, fix names ([IDENTITY-AUDIT.md](IDENTITY-AUDIT.md) catalogues the source
issues), assign slugs. Each `C(...)` is one competitor; its `rows` are the
`(series-slug, sail)` pairs it appears under. The slug is the stable key and the
public-URL handle — mint it once, never change it. The 149 blank-name rows are
excluded from the draft (a sail-only entry can't anchor a person); recover or
exclude them at source.

**Compile, then apply.** `manifest.py` is readable (`(series-slug, sail)` rows),
but the app needs each series' *live* seriesId — which it mints fresh on import,
so the archive can't derive it. Dump them from the running app and compile:

```
sailscoring series list --json > series-dump.json   # against the IODAI workspace
python3 compile.py series-dump.json                  # writes manifest.json
```

`compile.py` joins the dump's series *names* to out-slugs (the built files carry
both) to fill the slug→id map, and emits the `manifest.json` the app consumes. It
errors loudly if any referenced series has no live id rather than emit a partial
map. Then apply it out-of-band — the `.sailscoring` format stays identity-free
and portable:

```
pnpm reconcile-identities <workspace> --manifest manifest.json            # dry run: validate + preview
pnpm reconcile-identities <workspace> --manifest manifest.json --apply    # write identities + links
```

## Licensing

This repository contains three kinds of material, licensed separately:

- **Code** — `build.py`, `engine.py`, `events/`: [MIT](LICENSE).
- **Reconstructed results & docs** — `series/*.sailscoring`, `README.md`,
  `SOURCES.md`, `IODAI Results.md`: [CC0 1.0](LICENSE-DATA) (public-domain
  dedication). These are reconstructions of published race results; results are
  facts and not themselves copyrightable.
- **Source pages** — `sources/**`: **not covered by either license.** These are
  verbatim HTML result pages published by IODAI via Sailwave, included only for
  reproducibility (`build.py validate`). All rights remain with their owners.
