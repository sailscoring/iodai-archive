#!/usr/bin/env python3
"""Reverse-engineer IODAI Sailwave result pages into importable .sailscoring files.

The published Sailwave HTML carries, per boat per race, a low-point score. For a
scratch (Appendix A) fleet that score IS the finishing position; coded results
render as "<points> <CODE>" (e.g. "63.0 DNC"); discards are parenthesised. We
reverse those cells back into finishes (sortOrder for placings, resultCode for
codes) and emit the .sailscoring JSON the app imports.

Senior/Junior become separate scratch fleets within one series; the engine
scores each fleet independently — for the Sprint Series this also corrects the
published mistake of scoring all boats as one fleet.

This module is year-agnostic. Each year's events live in `events/` and are
collected by `build.py`, which is the CLI entry point (build / validate / adopt).
"""
import os
import re
import math
import html
import json
import sys
import uuid
import collections

# Repo paths — sources are read from sources/, output written to series/.
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.join(HERE, 'sources')
SERIES_DIR = os.path.join(HERE, 'series')
ADOPT_FILE = os.path.join(HERE, 'adopted-series-ids.json')

# Non-race meta columns. Some pages title the sail column 'Sail Number' and the
# helm 'Helm Name' rather than 'Sail'/'Name'; all spellings are listed so they're
# excluded from the race columns (and read back via the fallbacks below).
META = {'Rank', 'Place', 'Tally', 'Fleet', 'Class', 'Sail', 'Sail Number',
        'SailNo', 'Sail no.', 'Sail No', 'Nat', 'Nationality', 'Country',
        'Helm Name', 'HelmName', 'Helmname', 'Helmname-1', 'Helm', 'Name', 'Club',
        'Division', 'Divison', 'Gender', 'HelmSex', 'Helm Sex', 'Age', 'HelmAge',
        'Helmage', 'Helmagegroup', 'HelmAgeGroup', 'Rating', 'Total', 'Nett', 'Net'}
# Position-replacing result codes that can appear in a race cell. ZFP is an
# additive penalty (handled separately), not a position-replacing code.
RESULT_CODES = {'DNC', 'DNS', 'OCS', 'NSC', 'DNF', 'RET', 'DSQ', 'DNE', 'UFD', 'BFD', 'RDG'}
NON_DISCARDABLE = {'DNE'}  # only DNE cannot be excluded (BFD is discardable)

# Deterministic IDs ---------------------------------------------------------
# Every id (series, fleet, competitor, race, finish) is a UUIDv5 derived from a
# stable logical key, so regenerating a file is byte-stable: re-running never
# churns ids. That matters for re-import. The app's "Update from File" path
# matches an existing series by `seriesId` ALONE (then replaces all child rows
# with fresh server ids), so a regenerated file is only importable over a live
# series if it carries that series' id. The fixed namespace keeps the *file's*
# id stable across runs; `adopt` overrides it with the id the app actually
# assigned a live series, since first-time import discards the file's id and
# mints its own (lib/series-file.ts openSeriesFromFile in the app repo).
NS = uuid.UUID('6f9b2c1e-3d4a-5b6c-8d7e-0a1b2c3d4e5f')  # arbitrary fixed namespace


def det(key):
    """Deterministic UUID for a stable logical key."""
    return str(uuid.uuid5(NS, key))


def load_adopted():
    """Map of out-slug -> the seriesId the app assigned a live series, so a
    regenerated file updates that series in place instead of being rejected as
    'a different series'. Empty when nothing has been adopted yet."""
    try:
        with open(ADOPT_FILE, encoding='utf-8') as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


# ---- HTML parsing ---------------------------------------------------------

def cellize(tr):
    cs = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', tr, flags=re.S | re.I)
    # Strip a leading BOM (some pages emit a UTF-8 BOM, read back as 'ï»¿' under
    # cp1252) so a header like 'Helmname' isn't mistaken for a race column.
    return [re.sub(r'^(?:﻿|ï»¿)', '', re.sub(r'<[^>]*>', '', html.unescape(c)).strip())
            for c in cs]


# Header markers. Sailwave pages use 'Rank' + 'Total'/'Nett'; older Sail100 pages
# use 'Place' + 'Net' and carry no gross 'Total' column (only the net). Both are
# low-point tables (displayed score = finishing position), so the same engine
# reconstructs them once the column names and the missing-Total case are handled.
RANK_HEADERS = ('Rank', 'Place')
NETT_HEADERS = ('Nett', 'Net')


def parse_file(fname):
    """Return (race_col_names, list-of-row-dicts) for one results page (Sailwave or
    Sail100). `fname` is relative to sources/. Each row dict has the meta columns
    by header name plus 'races': the raw race-cell strings in order."""
    with open(os.path.join(SOURCES_DIR, fname), encoding='cp1252', errors='replace') as fh:
        s = fh.read()
    hdr = None
    for tr in re.findall(r'<tr[^>]*>.*?</tr>', s, flags=re.S | re.I):
        c = cellize(tr)
        if any(h in c for h in RANK_HEADERS) and any(h in c for h in NETT_HEADERS):
            hdr = c
            break
    # Race columns run up to the first scoring-total column. Sailwave has a 'Total'
    # then 'Nett'; Sail100 has only the net column at the end.
    if 'Total' in hdr:
        end_i, nett_i = hdr.index('Total'), hdr.index('Total') + 1
    else:
        end_i = nett_i = next(i for i, h in enumerate(hdr) if h in NETT_HEADERS)
    race_idx = [i for i in range(end_i) if hdr[i] not in META]
    race_cols = [hdr[i] for i in race_idx]
    rows = []
    for tr in re.findall(r'<tr[^>]*class="[^"]*summaryrow[^"]*"[^>]*>.*?</tr>', s, flags=re.S | re.I):
        c = cellize(tr)
        row = {hdr[i]: c[i] for i in range(end_i) if hdr[i] in META}
        row['races'] = [c[i] for i in race_idx]
        row['Nett'] = c[nett_i]
        row['Total'] = c[end_i] if 'Total' in hdr else c[nett_i]
        rows.append(row)
    return race_cols, rows


def classify(raw):
    """Classify one race cell. Returns dict:
       {discarded, kind: 'finish'|'code'|'blank', score: float|None,
        code: str|None, penalty: str|None}."""
    discarded = raw.startswith('(') and raw.endswith(')')
    t = raw[1:-1].strip() if discarded else raw.strip()
    m = re.match(r'^([\d.]+)\s+([A-Za-z]{2,5})$', t)
    if m:
        score = float(m.group(1))
        tok = m.group(2).upper()
        if tok.startswith('RDG'):
            # Redress given (RDGa = A9 average): the displayed number IS the
            # awarded points, not a finishing position. Carried through as a
            # stated-redress finish so the app reproduces it exactly.
            return dict(discarded=discarded, kind='redress', score=score, code='RDG', penalty=None)
        if tok in RESULT_CODES:
            return dict(discarded=discarded, kind='code', score=score, code=tok, penalty=None)
        # additive penalty (ZFP/SCP/DPI) sits on top of a real finish
        return dict(discarded=discarded, kind='finish', score=score, code=None, penalty=tok)
    if re.match(r'^[\d.]+$', t):
        return dict(discarded=discarded, kind='finish', score=float(t), code=None, penalty=None)
    return dict(discarded=discarded, kind='blank', score=None, code=None, penalty=None)


def round_tenth(x):
    """Round to the nearest tenth, 0.05 up — RRS Appendix A9 (and the app's
    roundToTenth in lib/scoring.ts). Avoids Python's banker's rounding."""
    return math.floor(x * 10 + 0.5) / 10


def _sail(row):
    """The sail number, however the page titled its column."""
    return (row.get('Sail') or row.get('Sail Number') or row.get('SailNo')
            or row.get('Sail no.') or row.get('Sail No') or '').strip()


def norm_gender(g):
    g = (g or '').strip().upper()
    return g if g in ('M', 'F') else ''


def norm_age(a):
    a = (a or '').strip()
    return int(a) if a.isdigit() else None


# ---- Extraction: source rows -> competitor records ------------------------

def load_competitors(cfg):
    """Return (competitors, fleet_names). Each competitor carries its classified
    race cells keyed by slot index."""
    comps = []
    fleet_names = list(cfg['fleet_order'])
    for src in cfg['sources']:
        _, rows = parse_file(src['file'])
        for row in rows:
            # Fleet comes from a page column when fleet_from_col is set (default
            # 'Fleet', but e.g. the 2024 Sprint splits Senior/Junior via the
            # 'Division' column — set fleet_col to point at it), else it's fixed.
            fleet = (row.get(src.get('fleet_col', 'Fleet'))
                     if src.get('fleet_from_col') else src['fleet'])
            name = (row.get('Helm Name') or row.get('HelmName') or row.get('Helmname')
                    or row.get('Helmname-1') or row.get('Helm') or row.get('Name') or '')
            cells = {}
            for j, raw in enumerate(row['races']):
                cells[src['slot0'] + j] = classify(raw)
            comps.append(dict(
                id=det(f"{cfg['out']}/competitor/{fleet}/{_sail(row)}/{name.strip()}"),
                fleet=fleet,
                sail=_sail(row),
                name=name.strip(),
                club=(row.get('Club') or '').strip(),
                nat=(row.get('Nat') or row.get('Nationality') or row.get('Country') or '').strip(),
                gender=norm_gender(row.get('Gender') or row.get('HelmSex') or row.get('Helm Sex')),
                age=norm_age(row.get('Age') or row.get('HelmAge') or row.get('Helmage')
                             or row.get('Helmagegroup') or row.get('HelmAgeGroup')),
                # The prize division (Gold/Silver/Bronze) is in 'Rating' on pages
                # that also carry a Senior/Junior 'Division' column, else in
                # 'Division'/'Divison' itself.
                subdivision=((row.get('Rating') or row.get('Division') or row.get('Divison') or '').strip()
                             if cfg['subdivision'] else ''),
                boat_class=(row.get('Class') or '').strip() if cfg['boat_class'] else '',
                cells=cells,
                published_nett=row['Nett'],
                published_total=row['Total'],
            ))
    return comps, fleet_names


# ---- Finish reconstruction ------------------------------------------------

def race_finishers(group, slot):
    """Order one fleet's finishers in a race by their true crossing position.

    Normal finishers sit at their displayed score (= finishing position in a
    scratch fleet). Two kinds of finisher float OUT of that sequence, leaving a
    gap at their real position: an additive-penalty boat (e.g. ZFP) whose
    displayed score is inflated, and a redress boat (RDG) whose score is replaced
    by an average. Both still crossed the line, so they must keep occupying a
    finishing slot — otherwise the boats behind renumber and shift up. We place
    each back at a gap (an integer position missing from 1..F). Returns a list of
    (effective_position, competitor, cell) sorted by position."""
    normal, floating = [], []
    for c in group:
        cell = c['cells'].get(slot)
        if not cell:
            continue
        if cell['kind'] == 'finish' and not cell['penalty']:
            normal.append((c, cell))
        elif (cell['kind'] == 'finish' and cell['penalty']) or cell['kind'] == 'redress':
            floating.append((c, cell))
    # Positions the normal finishers occupy. Tied boats share a displayed score
    # but sit on consecutive places (e.g. two 14.0s occupy 14 and 15), so expand
    # each tie group — otherwise the skipped number reads as a vacancy and a
    # floating boat is wrongly slotted into it.
    norm = sorted(cell['score'] for _, cell in normal)
    used = set()
    i = 0
    while i < len(norm):
        j = i
        while j < len(norm) and norm[j] == norm[i]:
            j += 1
        base = int(round(norm[i]))
        used.update(range(base, base + (j - i)))
        i = j
    n_fin = len(normal) + len(floating)
    missing = [p for p in range(1, n_fin + 1) if p not in used]
    floating.sort(key=lambda t: t[1]['score'])
    float_pos = {id(cell): p for (_, cell), p in zip(floating, missing)}
    items = [(cell['score'], c, cell) for c, cell in normal]
    items += [(float_pos.get(id(cell), cell['score']), c, cell) for c, cell in floating]
    items.sort(key=lambda t: (t[0], t[1]['sail']))
    return items


def build_finishes(comps, fleet_names, nslots):
    """Return {slot: [finish-dicts]}. sortOrder is assigned per (slot, fleet);
    fleets are offset so sortOrder stays distinct within a race."""
    by_slot = collections.defaultdict(list)
    for slot in range(nslots):
        for fi, fleet in enumerate(fleet_names):
            group = [c for c in comps if c['fleet'] == fleet]
            for c in group:
                cell = c['cells'].get(slot)
                if cell and cell['kind'] == 'code':
                    by_slot[slot].append(dict(
                        id=det(f"{c['id']}/finish/{slot}"), competitorId=c['id'], sortOrder=None,
                        resultCode=cell['code'], startPresent=None,
                        penaltyCode=None, penaltyOverride=None))
            offset = fi * 10000
            prev_pos = None
            # Finishers — including ZFP and redress boats, which race_finishers
            # has placed back into the order at their vacated position so the
            # boats behind keep their finishing place.
            for k, (pos, c, cell) in enumerate(race_finishers(group, slot)):
                f = dict(
                    id=det(f"{c['id']}/finish/{slot}"), competitorId=c['id'],
                    sortOrder=offset + k + 1, resultCode=None, startPresent=None,
                    penaltyCode=cell['penalty'], penaltyOverride=None)
                if cell['kind'] == 'redress':
                    f['resultCode'] = 'RDG'
                    f['penaltyCode'] = None
                    f['redressMethod'] = 'stated'
                    f['redressPoints'] = cell['score']
                elif cell['penalty'] and cell['penalty'] not in ('ZFP', 'SCP'):
                    # Generic penalty (e.g. Sailwave 'PEN') — the displayed value is
                    # the final race points, not a recomputable percentage. Map to
                    # DPI (additive_stated) with an override that lands the boat on
                    # exactly that score from its reconstructed position.
                    f['penaltyCode'] = 'DPI'
                    f['penaltyOverride'] = round_tenth(cell['score'] - pos)
                if prev_pos is not None and pos == prev_pos:
                    f['tiedWithPrevious'] = True
                prev_pos = pos
                by_slot[slot].append(f)
    return by_slot


# ---- .sailscoring assembly ------------------------------------------------

def enabled_fields(cfg):
    fields = ['club', 'nationality', 'gender', 'age']
    if cfg['subdivision']:
        fields.append('subdivision')
    if cfg['boat_class']:
        fields.append('boatClass')
    return fields


def build_series_file(cfg):
    comps, fleet_names = load_competitors(cfg)
    finishes = build_finishes(comps, fleet_names, cfg['nslots'])
    # `adopt` overrides the default (deterministic) seriesId with the id the app
    # gave a live series, so re-importing this file updates that series in place.
    series_id = load_adopted().get(cfg['out']) or det(f"{cfg['out']}/series")
    snap = det(f"{cfg['out']}/snapshot")
    fleet_ids = {name: det(f"{cfg['out']}/fleet/{name}") for name in fleet_names}

    file = dict(
        formatVersion=6,
        seriesId=series_id,
        snapshotId=snap,
        snapshotHistory=[snap],
        # Fixed (not now()) so regeneration is byte-stable — anchored to the
        # event's last day rather than the run time.
        exportedAt=f"{cfg['end']}T12:00:00+00:00",
        series=dict(
            id=series_id, name=cfg['name'], venue=cfg['venue'],
            startDate=cfg['start'], endDate=cfg['end'],
            venueLogoUrl=cfg.get('venue_logo', ''), eventLogoUrl=cfg.get('event_logo', ''),
            venueUrl=cfg.get('venue_url', ''), eventUrl=cfg.get('event_url', ''),
            discardThresholds=[dict(minRaces=m, discardCount=d) for m, d in cfg['discards']],
            dnfScoring='seriesEntries',
            ftpHost='', ftpPath='',
            includeJsonExport=True,
            enabledCompetitorFields=enabled_fields(cfg),
            primaryPersonLabel=cfg['primary'],
            subdivisionLabel='Division',
            scoringMode='scratch',
        ),
        fleets=[dict(id=fleet_ids[name], name=name, displayOrder=i, scoringSystem='scratch')
                for i, name in enumerate(fleet_names)],
        competitors=[],
        races=[],
    )

    for c in comps:
        rec = dict(id=c['id'], fleetIds=[fleet_ids[c['fleet']]], sailNumber=c['sail'],
                   name=c['name'], club=c['club'], gender=c['gender'], age=c['age'])
        if c['nat']:
            rec['nationality'] = c['nat']
        if c['subdivision']:
            rec['subdivision'] = c['subdivision']
        if c['boat_class']:
            rec['boatClass'] = c['boat_class']
        file['competitors'].append(rec)

    for slot in range(cfg['nslots']):
        file['races'].append(dict(
            id=det(f"{cfg['out']}/race/{slot}"), raceNumber=slot + 1, date=cfg['date'](slot),
            starts=[], finishes=finishes.get(slot, [])))

    return file, comps, fleet_names


# ---- Validation: re-score and diff against published Nett ------------------

def score_fleet(comps, nslots, discards):
    """Minimal scratch Appendix-A scoring mirroring lib/scoring.ts, over the
    given competitor set (one fleet). Returns {compid: (total, nett)}."""
    n = len(comps)
    penalty = n + 1
    pts = {c['id']: [None] * nslots for c in comps}
    codes = {c['id']: [None] * nslots for c in comps}
    excluded = [False] * nslots
    for slot in range(nslots):
        placed = race_finishers(comps, slot)   # (effective_position, comp, cell)
        excluded[slot] = len(placed) == 0
        # rank placed finishers with tie-averaging (RRS A8.1)
        rank_pts = {}
        i = 0
        while i < len(placed):
            j = i + 1
            while j < len(placed) and placed[j][0] == placed[i][0]:
                j += 1
            avg = (i + 1 + j) / 2  # average of ranks i+1..j
            for k in range(i, j):
                rank_pts[placed[k][1]['id']] = avg
            i = j
        for c in comps:
            cell = c['cells'].get(slot)
            if cell is None or cell['kind'] == 'blank':
                continue
            if cell['kind'] == 'code':
                pts[c['id']][slot] = penalty
                codes[c['id']][slot] = cell['code']
            elif cell['kind'] == 'redress':
                # Stated redress: the awarded average points, discardable as normal.
                pts[c['id']][slot] = cell['score']
                codes[c['id']][slot] = None
            else:
                base = rank_pts[c['id']]
                # Additive percentage penalty (ZFP/SCP): 20% of the DNF score
                # (here `penalty`), rounded to a tenth, capped at DNF — mirrors
                # applyScoringPenalty in lib/scoring.ts.
                if cell['penalty'] in ('ZFP', 'SCP'):
                    pen = round(20 * penalty / 10) / 10
                    base = min(round_tenth(base + pen), penalty)
                elif cell['penalty']:
                    # Generic stated penalty (PEN/DPI): the displayed value is the
                    # final points (mirrors the DPI override emitted in build).
                    base = cell['score']
                pts[c['id']][slot] = base
                codes[c['id']][slot] = None
    sailed = sum(1 for e in excluded if not e)
    ndisc = 0
    for m, d in sorted(discards):
        if sailed >= m:
            ndisc = d
    out = {}
    for c in comps:
        scores = []
        for slot in range(nslots):
            if excluded[slot]:
                continue
            p = pts[c['id']][slot]
            if p is None:
                continue  # fleet absent this race (counts as nothing, like exclusion)
            scores.append((p, codes[c['id']][slot]))
        total = sum(p for p, _ in scores)
        # drop worst `ndisc` discardable scores
        discardable = sorted([p for p, code in scores if code not in NON_DISCARDABLE], reverse=True)
        nett = total - sum(discardable[:ndisc])
        out[c['id']] = (round_tenth(total), round_tenth(nett))
    return out


def validate(series):
    ok = True
    for cfg in series:
        _, comps, fleet_names = build_series_file(cfg)
        print(f'\n=== {cfg["name"]} ===')
        # Validate per natively-scored fleet (published page == that fleet's own
        # scoring). Exception: a Sprint whose published page scored all boats as
        # ONE combined fleet (set validate_combined=True). When IODAI instead
        # publishes per-fleet Sprint pages (2025-style OverallS/OverallJ), leave
        # the flag off and each fleet validates against its own page.
        if cfg.get('validate_combined'):
            groups = [('combined (published basis)', comps)]
        else:
            groups = [(f, [c for c in comps if c['fleet'] == f]) for f in fleet_names]
        # Boats whose published score is internally inconsistent with standard
        # scoring (documented in the year's config) are tolerated: reported as
        # SUSPECT, not counted as failures. Keeps validation strict everywhere
        # else while acknowledging the bad source cell. See README rule 4.
        suspect = set(cfg.get('suspect', ()))
        for label, group in groups:
            scored = score_fleet(group, cfg['nslots'], cfg['discards'])
            mism = 0
            sus = 0
            for c in group:
                nett_str = c['published_nett'].strip()
                if not nett_str:
                    continue  # roster row (participation fleet, no score published)
                want = float(nett_str)
                got = scored[c['id']][1]
                if abs(got - want) <= 0.01:
                    continue
                if c['sail'] in suspect:
                    sus += 1
                    print(f'   SUSPECT  {c["sail"]:>6} {c["name"][:18]:18} '
                          f'published nett={want:g} re-scored={got:g} (tolerated)')
                    continue
                mism += 1
                if mism <= 8:
                    print(f'   MISMATCH {c["sail"]:>6} {c["name"][:18]:18} '
                          f'published nett={want:g} re-scored={got:g}')
            tag = 'OK' if mism == 0 else f'{mism}/{len(group)} MISMATCH'
            if sus:
                tag += f' (+{sus} suspect)'
            if mism:
                ok = False
            print(f'   [{tag}] {label} ({len(group)} boats)')
    print('\nVALIDATION', 'PASSED' if ok else 'FAILED')
    return ok


# ---- Output ---------------------------------------------------------------

def build(series):
    os.makedirs(SERIES_DIR, exist_ok=True)
    for cfg in series:
        file, _, fleets = build_series_file(cfg)
        path = os.path.join(SERIES_DIR, f"{cfg['out']}.sailscoring")
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(file, fh, indent=2, ensure_ascii=False)
        print(f"wrote series/{cfg['out']}.sailscoring  "
              f"({len(file['competitors'])} competitors, {len(fleets)} fleet(s), "
              f"{len(file['races'])} races)")


def adopt(series, live_path):
    """Record the seriesId the app gave a live series, so the regenerated file
    re-imports over it (the app's 'Update from File' matches on seriesId alone).
    The live file is a .sailscoring exported from the running app; its series is
    matched to a config entry by name. Then re-run the build."""
    with open(live_path, encoding='utf-8') as fh:
        live = json.load(fh)
    live_name = live.get('series', {}).get('name', '')
    live_id = live.get('seriesId')
    cfg = next((c for c in series if c['name'] == live_name), None)
    if not cfg:
        names = '\n  '.join(c['name'] for c in series)
        sys.exit(f"No event matches the live file's series name {live_name!r}.\n"
                 f"Known series:\n  {names}")
    if not live_id:
        sys.exit(f"{live_path} has no seriesId.")
    adopted = load_adopted()
    adopted[cfg['out']] = live_id
    with open(ADOPT_FILE, 'w', encoding='utf-8') as fh:
        json.dump(adopted, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f"adopted {live_id} for {cfg['out']} ({live_name})")
    print('re-running build so the file carries the adopted id...')
    build(series)
