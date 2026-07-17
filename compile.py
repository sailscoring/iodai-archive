#!/usr/bin/env python3
"""Compile the curated manifest.py into the app's manifest.json (sailscoring #218).

The app's identity apply (`sailscoring as-published identities`) needs each
series' *live* seriesId,
but the app mints those fresh on import, so the archive can't derive them. Get
them from the running app's CLI and feed the dump in here:

    sailscoring series list --json > series-dump.json     # against the IODAI workspace
    python3 compile.py series-dump.json                    # writes manifest.json
    python3 compile.py series-dump.json --allow-missing    # tolerate not-yet-imported series
    python3 compile.py series-dump.json --mint-missing     # pin ids for brand-new archive series

The dump maps series *name* -> live id; this script knows out-slug -> name (the
built series files carry both), so it resolves out-slug -> live id and emits the
manifest.json the app consumes. Validate the result before applying with a dry
run: `sailscoring as-published identities manifest.json --workspace <slug>`
(CI applies it automatically on push — see .github/workflows/as-published.yml).

By default it fails if any referenced series has no live id (usually a name
mismatch or a series not yet imported), and points at the closest dump names so
you can tell which. Pass --allow-missing to compile against the imported subset:
members in unresolved series are dropped, the golden record in manifest.py stays
complete, and a later re-compile picks them up once they're imported.

--mint-missing covers the other direction — a series that exists in the archive
but was *never* in the workspace (ADR-010: the as-published ingest CREATES a
series from the id we send, so brand-new archive series never appear in a dump
first). It mints the deterministic id the built .sailscoring already carries
(det("<out>/series")) and pins it in adopted-series-ids.json, making the id
committed data; the ingest then creates the series under that id and every
later dump returns it. Pre-2026 series only: a 2026+ full-fidelity series gets
its id from the app on first import (then `build.py adopt`), and pre-minting
one here would pin a lie.
"""
import difflib
import glob
import json
import os
import re
import sys

import engine
from identity_manifest import compile_manifest

OUT = 'manifest.json'


def out_to_name():
    """Map each series out-slug (filename stem) to its series name."""
    mapping = {}
    for path in sorted(glob.glob('series/*.sailscoring')):
        out = os.path.basename(path)[: -len('.sailscoring')]
        data = json.load(open(path, encoding='utf-8'))
        mapping[out] = data.get('series', {}).get('name', '')
    return mapping


def name_to_id(dump_path):
    """Map series name -> live seriesId from a `sailscoring series list --json`
    dump (either {"items": [...]} or a bare list of {id, name})."""
    data = json.load(open(dump_path, encoding='utf-8'))
    items = data.get('items', data) if isinstance(data, dict) else data
    mapping = {}
    for s in items:
        name, sid = s.get('name'), s.get('id')
        if not name or not sid:
            continue
        if name in mapping and mapping[name] != sid:
            sys.exit(f'duplicate series name in dump, ambiguous: {name!r}')
        mapping[name] = sid
    return mapping


def diagnose_missing(unresolved_names, live_names):
    """For each unresolved series, point at the closest name in the dump so a
    name mismatch (close match exists) is distinguishable from a not-imported
    series (no close match)."""
    lines = []
    for out, name in unresolved_names:
        close = difflib.get_close_matches(name, live_names, n=1, cutoff=0.6)
        hint = f'closest in dump: {close[0]!r}' if close else 'no close match — not imported?'
        lines.append(f'  {out}\n      want: {name!r}\n      {hint}')
    return '\n'.join(lines)


def mint_missing(unresolved):
    """Pin deterministic ids for pre-2026 series never seen by the workspace
    (see the module docstring). Returns the newly pinned {out: id} map."""
    minted = {}
    for out, _name in unresolved:
        m = re.search(r'(19|20)\d{2}', out)
        if not m or int(m.group(0)) >= 2026:
            print(f'  ! {out}: not pre-2026 — not minting (import + adopt instead)')
            continue
        minted[out] = engine.det(f'{out}/series')
    if minted:
        pinned = engine.load_adopted()
        pinned.update(dict(sorted(minted.items())))
        with open(engine.ADOPT_FILE, 'w', encoding='utf-8') as fh:
            json.dump(pinned, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
        print(f'Minted + pinned {len(minted)} series ids in adopted-series-ids.json:')
        for out, sid in sorted(minted.items()):
            print(f'  + {out}  {sid}')
    return minted


def _all_identities():
    """manifest.py plus the ranking-only entries (ranking_identities.py):
    one golden record, two curation files."""
    import manifest
    try:
        import ranking_identities
        return list(manifest.IDENTITIES) + list(ranking_identities.IDENTITIES)
    except ImportError:
        return list(manifest.IDENTITIES)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith('--')]
    allow_missing = '--allow-missing' in argv
    if not args:
        sys.exit('usage: python3 compile.py <series-dump.json> [--allow-missing | --mint-missing]  '
                 '(from: sailscoring series list --json)')
    if not os.path.exists('manifest.py'):
        sys.exit('manifest.py not found — run bootstrap.py and curate it first.')

    identities = _all_identities()  # the curated golden record(s)

    names = out_to_name()
    live = name_to_id(args[0])
    adopted = engine.load_adopted()  # out -> live id, explicit and rename-proof

    # Resolve out-slug -> live id. adopted-series-ids.json wins (an explicit
    # mapping survives in-app renames); otherwise join on the series name. Series
    # renamed in the app and not adopted fall through to unresolved.
    out_to_id = {}
    unresolved_names = []
    for out, name in names.items():
        if out in adopted:
            out_to_id[out] = adopted[out]
        elif name in live:
            out_to_id[out] = live[name]
        else:
            unresolved_names.append((out, name))

    if '--mint-missing' in argv and unresolved_names:
        minted = mint_missing(unresolved_names)
        out_to_id.update(minted)
        unresolved_names = [(o, n) for o, n in unresolved_names if o not in minted]

    # Which unresolved series are actually referenced by the manifest? (Corpus
    # series no competitor in the manifest appears in don't matter.)
    referenced = {slug for c in identities for slug, _ in c.rows}
    missing_referenced = [(o, n) for o, n in unresolved_names if o in referenced]

    if missing_referenced and not allow_missing:
        sys.exit(
            f'no live seriesId for {len(missing_referenced)} referenced series '
            '(renamed in the app, or not yet imported):\n'
            + diagnose_missing(missing_referenced, list(live.keys()))
            + '\n\nIf a series was renamed in the app, add its out-slug -> live id to '
            'adopted-series-ids.json (rename-proof). Otherwise import it, or re-run '
            'with --allow-missing to compile against the imported subset.'
        )

    compiled = compile_manifest(identities, out_to_id, allow_missing=allow_missing)

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(compiled, fh, ensure_ascii=False, indent=2)
        fh.write('\n')

    print(f'Wrote {OUT}')
    print(f'  identities:        {len(compiled["identities"])}')
    print(f'  series referenced: {len(compiled["series"])}')
    if missing_referenced:
        dropped = len(identities) - len(compiled['identities'])
        print(f'  series skipped:    {len(missing_referenced)}  (not in dump; --allow-missing)')
        print(f'  identities dropped:{dropped:>4}  (all their series were skipped)')
        for o, n in missing_referenced:
            print(f'      - {o}  ({n})')
    print(f'\nValidate before applying:')
    print(f'  sailscoring as-published identities {OUT} --workspace <slug>')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
