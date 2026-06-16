# CLAUDE.md

Guidance for Claude Code working in this repo. **Read `README.md` first** — it has
the mission, layout, the per-event process, and the status tracker. This file
covers the working conventions and the non-obvious rules that are easy to get
wrong.

## What this repo is

A data pipeline, not an application. It reverse-engineers IODAI's published
[Sailwave](https://www.sailwave.com/results/IODAI/) HTML result pages into
importable `.sailscoring` files, year by year, to populate the production IODAI
workspace in Sail Scoring with a deep historical record. The end goal is to make
the **cross-series identity & ranking** features (see the app repo's
`docs/design/horizon.md`) come alive with real multi-year data.

The job is repetitive but **one-time per past event**: find the pages, add a
config entry, build, validate, import. Work back through the years methodically.

## The task, concretely

For each past year, source these and build a `.sailscoring` file per series
(a series = one group sharing a finish line — see README "Target events"):

- 4 regional championships: **Leinsters, Ulsters, Connachts, Munsters** (3 series each)
- **National championship** (3 series)
- **National Training Week** final-day racing (**Crosbie Cup**)
- **Sprint Series** (only exists from 2025/2026)

Keep the **status tracker table in README.md** up to date as you go.

## Commands

```
python3 build.py validate    # re-score every fleet, diff against the published Nett
python3 build.py             # write series/<out>.sailscoring
python3 build.py adopt <live-export.sailscoring>   # pin a live seriesId, then rebuild
python3 audit.py             # identity data-quality audit -> IDENTITY-AUDIT.md
python3 bootstrap.py         # draft the competitor-identity manifest.py (#218)
```

The build pipeline (`build.py`, `engine.py`, `audit.py`) is plain Python 3 stdlib
— no dependencies, no build step, no tests beyond `validate`. **`bootstrap.py` is
the one exception:** it shells out to the sibling app repo's matcher
(`pnpm --silent --dir ../sailscoring cluster-rows`), so it needs `../sailscoring`
and `pnpm`. That keeps one canonical matcher rather than a Python fork of it.

## Rules that are easy to get wrong

1. **`validate` must pass before you trust or commit a file.** It re-scores each
   fleet with an Appendix-A engine mirroring the app's `lib/scoring.ts` and
   confirms every boat's reconstructed Nett equals the published page. A mismatch
   means the reconstruction (or the config: discards, nslots, fleet split) is
   wrong. Never commit a file that doesn't validate.

2. **Never rename an `out` slug once its series has been imported.** All ids are
   deterministic UUIDv5s derived from `out`; the `seriesId` is `det("<out>/series")`.
   Change `out` and you mint a *new* series the app can't reconcile with the live
   one. The slug is the stable key — treat it as permanent.

3. **Re-importing over a live series needs `adopt`.** A first import discards the
   file's `seriesId` and assigns its own; the app's *Update from File* then
   matches by `seriesId` alone. So to push later races or a correction onto a
   series already in the workspace, run `adopt` with a fresh export of that live
   series (in the app: open it → Actions → Save to File). It records the live id
   in `adopted-series-ids.json` and rebuilds. Commit that file.

4. **Only use real published data.** If you can't find a fleet's Sailwave page,
   leave it unsourced (◻️ in the tracker) — do **not** fabricate, interpolate, or
   guess results. Partial coverage is fine and expected.

5. **Regeneration is byte-stable** (deterministic ids, fixed `exportedAt`). After
   editing a config and rebuilding, `git diff` should show only the series you
   actually changed. If unrelated files churn, something's wrong — investigate
   before committing.

6. **Race dates are approximate.** Sailwave pages carry only a publish timestamp,
   so dates are inferred (two races/day from the event window). Don't over-invest
   in exact per-race dates; they're editable in the app after import.

## Domain quick-reference

- An event = **three independent series**: Main Fleet, Regatta Racing, Regatta
  Coached — each its own course and finish line.
- **Main Fleet** holds **Junior** and **Senior** as separate scratch fleets,
  scored independently (one `.sailscoring` file, two fleets). They share a finish
  line, so they're one series.
- **Gold/Silver/Bronze** is a prize *subdivision* (the `subdivision` field), not a
  fleet — all of a fleet's boats are scored together regardless of division.
- The **Sprint Series** is published scored as one combined fleet; we deliberately
  re-score Senior and Junior separately (matching how IODAI intends it). The
  Sprint config validates against the combined published basis — see the note in
  `engine.validate`.

Full domain context is in the app repo: `../sailscoring/docs/requirements/iodai-use-case.md`,
and `../sailscoring/reference/2025-IODAI-Major-Event-SIs-v1.0.pdf` for the SIs.

## Adding a year or event

1. Download each fleet's final whole-series page into `sources/<year>/<event>/`.
2. Add one config dict per series to `events/y<year>.py` (create it and wire it
   into `events/__init__.py` for a new year). Copy a 2026 entry as a template;
   set `out`, `fleet_order`, `sources`, `discards`, `nslots`, dates, venue, logos.
3. `python3 build.py validate` then `python3 build.py`.
4. Update the status tracker in `README.md`.
5. Add a venue logo constant to `events/helpers.py` if the host club has one in
   the canonical library (`../sailscoring/lib/canonical-logos/generated/manifest.ts`).
   Every IODAI event carries the `IODAI` event logo.

## Git conventions

- Commit logically (one event or one coherent change per commit). Keep the working
  tree validated and building.
- **End every commit message with:**
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
- **Do not push unless asked.** Commit locally; let the human review and push.
- Importing files into the production workspace is a manual step a human performs
  in the app — this repo's job ends at producing a validated `.sailscoring` file
  (and `adopt`ing when updating a live one).
