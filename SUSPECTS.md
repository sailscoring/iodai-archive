> **Historical (ADR-010, July 2026).** Suspects were a *reconstruction*
> concept: boats whose published Nett our re-scoring engine couldn't
> reproduce. Under the as-published regime (sailscoring ADR-010, #283) the
> archive displays the published pages verbatim and recomputes nothing, so
> these discrepancies no longer manifest anywhere — the app now shows exactly
> the (occasionally internally inconsistent) numbers the pages carried. This
> file is kept as an audit of source-data quirks, not as a list of live
> deviations; the `suspect=[...]` flags and `validate` remain part of the
> retired reconstruction pipeline.

# Suspect boats

This file collects every **suspect** flagged across the back-fill, so they're
visible in one place for manual audit. The authoritative definition still lives
in the code: each suspect is a `suspect=[...]` entry in `events/y<year>.py` with a
comment explaining *why*, and `engine.py` (`validate`) reports them.

## What "suspect" means

For every fleet, `python3 build.py validate` re-scores all boats with an
Appendix-A engine (mirroring the app's `lib/scoring.ts`) and compares each boat's
reconstructed **Nett** against the value published on the scraped Sailwave page.
Normally every boat must match exactly or the run fails.

A **suspect** is a boat whose published Nett genuinely can't be reproduced from
the source data — usually because the published cell is internally inconsistent
(a whole-number penalty that doesn't follow from the boat's finishing position, a
tie the page didn't average, or a wrong DNC/DNF base). Rather than fabricate data
or fail the whole fleet, we list that boat's sail number in the series'
`suspect=[...]` flag. `validate` then prints it as `SUSPECT … (tolerated)` and
does **not** count it as a mismatch. Everything else in the fleet still has to be
exact.

Suspects are almost always a single boat deep in a fleet whose *rank* is
unaffected; the discrepancy is a fraction of a point or a single point. None of
them change who won. See README rule 4 and the `suspect-data-tolerance` working
note for the policy.

> Distinct from suspects: `tie_tolerant` years absorb ≤2.0 half-point differences
> from RRS A8.1 tie-averaging (reported as `TIE`), and Phase-2 older-Sail100
> fleets (`bare_dnc`) are a sniff test rather than a hard gate (`PHASE2 n/m off`).
> Those are not listed here — only explicitly flagged suspect boats are.

## The suspects

16 boats across 11 series. "Δ" is re-scored minus published.

| Year | Event / fleet | Sail | Boat | Published | Re-scored | Δ | Why it can't be reproduced |
|------|---------------|------|------|-----------|-----------|----|----------------------------|
| 2024 | Munsters — Main (Junior) | 1391 | Oscar Rowan | 87 | 83.6 | −3.4 | ZFP cell (21.0); published whole-number penalty doesn't follow from his reconstructed position |
| 2024 | Nationals — Main (Senior) | 1673 | Eoin Pierse | 295 | 289.4 | −5.6 | ZFP cell (46.0); whole-number penalty not reproducible from the tenth-rounded position |
| 2022 | Leinsters — Main (Senior) | 1639 | Felix Dion | 61 | 61.5 | +0.5 | Tie for 17th in R1; page scored both boats 17.0, app applies RRS A8.1 averaging (17.5) |
| 2022 | Leinsters — Main (Senior) | 1467 | Andrew O'Neill | 65 | 65.5 | +0.5 | Same R1 tie as 1639 (A8.1 averaging) |
| 2022 | Nationals — Main (Senior) | 1651 | Jude Hynes-Knight | 91 | 89.2 | −1.8 | SCP (scoring-penalty) cell; published whole-number penalty not reproducible under tenth-rounded percentage |
| 2022 | Nationals — Main (Junior) | 1493 | Max O'Hare | 77 | 69.4 | −7.6 | SCP cell; same as 1651 |
| 2021 | Connachts — Main (Senior) | 1643 | Rory Wilson | 163.5 | 164 | +0.5 | Page scored a tie as 163.5 (A8.1 average); reconstruction renders 164 — a 0.5 tie-rounding diff |
| 2021 | Nationals — Regatta | 1464 | Louis Trickett | 173 | 172 | −1 | DNC base is 50 (49 entries) but only 48 boats appear; a counted entrant is missing, so heavily-DNC'd boats reconstruct 1 low per coded race |
| 2021 | Nationals — Regatta | 1214 | Megan Foley | 256 | 254 | −2 | Same missing-entrant DNC base |
| 2021 | Nationals — Regatta | 1351 | Amelia | 264 | 263 | −1 | Same missing-entrant DNC base |
| 2021 | Nationals — Regatta | 1270 | Arthur Fegan | 273 | 268 | −5 | Same missing-entrant DNC base |
| 2021 | Nationals — Regatta | 1234 | Connor O'Sullivan | 300 | 294 | −6 | Same missing-entrant DNC base |
| 2019 | Leinsters — Regatta | 1587 | Katie Fanning | 155 | 157 | +2 | RET cells scored 27 (DNF = starters); app uses entries+1 = 28. Gap shows after discards |
| 2016 | Leinsters — Main (Junior) | 511 | Fiachra Farrelly | 100 | 100.4 | +0.4 | ZFP-style .4 penalty cell |
| 2016 | Ulsters — Main (Junior) | 1439 | Aoife McMahon | 114 | 113.8 | −0.2 | ZFP-style penalty cell |
| 2013 | Leinsters — Main (Junior) | 1087 | Leah Rickard | 188.4 | 187 | −1.4 | Deep junior, ZFP-style .4 penalty |

## Auditing one

To re-confirm the current state at any time:

```
python3 build.py validate 2>&1 | grep -B1 SUSPECT
```

To audit a specific boat, open its fleet's Sailwave page in `sources/<year>/…`,
find the boat by sail number, and compare its per-race cells and Nett against the
re-scored value above. The likely culprits, by category:

- **A8.1 ties** (the `+0.5` rows): the page left a tie un-averaged. The app is the
  RRS-correct one; ranks are unchanged. These are the least worrying.
- **ZFP / SCP penalties** (the larger negative Δ): the published page carries a
  whole-number or `.4` penalty in one race that doesn't follow from the boat's
  reconstructed finishing position. Worth checking the SI/penalty notice if you
  want the exact intended value.
- **Wrong DNC/DNF base** (2021 Nationals Regatta, 2019 Leinsters Regatta): a
  structural mismatch between the page's scoring base and the boats actually
  listed. Affects every heavily-DNC'd boat in the fleet, but only by a point or
  two, and only at the very bottom of the results.

If an audit shows the published value is actually reproducible (e.g. a config
discard/nslots was wrong), fix the config and remove the boat from `suspect=[...]`
— don't leave a stale flag. If the cause turns out to be general (affects many
boats/years), prefer a real engine fix over per-boat flags.
