#!/usr/bin/env python3
"""Compile the curated manifest.py into the app's manifest.json (sailscoring #218).

The app's `reconcile-identities --manifest` needs each series' *live* seriesId,
but the app mints those fresh on import, so the archive can't derive them. Get
them from the running app's CLI and feed the dump in here:

    sailscoring series list --json > series-dump.json     # against the IODAI workspace
    python3 compile.py series-dump.json                    # writes manifest.json

The dump maps series *name* -> live id; this script knows out-slug -> name (the
built series files carry both), so it resolves out-slug -> live id and emits the
manifest.json the app consumes. Validate the result before applying with a dry
run: `pnpm reconcile-identities <workspace> --manifest manifest.json`.
"""
import glob
import json
import os
import sys

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


def main(argv):
    if len(argv) < 2:
        sys.exit('usage: python3 compile.py <series-dump.json>  '
                 '(from: sailscoring series list --json)')
    if not os.path.exists('manifest.py'):
        sys.exit('manifest.py not found — run bootstrap.py and curate it first.')

    import manifest  # the curated golden record

    names = out_to_name()
    live = name_to_id(argv[1])

    # Resolve out-slug -> live id via the series name. Report names the dump
    # didn't cover rather than silently producing an incomplete map.
    out_to_id = {}
    unresolved_names = []
    for out, name in names.items():
        if name in live:
            out_to_id[out] = live[name]
        else:
            unresolved_names.append((out, name))

    try:
        compiled = compile_manifest(manifest.IDENTITIES, out_to_id)
    except ValueError as e:
        msg = str(e)
        if unresolved_names:
            msg += ('\n\n' + str(len(unresolved_names)) + ' series in the corpus had no '
                    'match in the dump (name mismatch or not imported); e.g.:\n  '
                    + '\n  '.join(f'{o}  ->  {n!r}' for o, n in unresolved_names[:10]))
        sys.exit(msg)

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(compiled, fh, ensure_ascii=False, indent=2)
        fh.write('\n')

    print(f'Wrote {OUT}')
    print(f'  identities:        {len(compiled["identities"])}')
    print(f'  series referenced: {len(compiled["series"])}')
    print(f'\nValidate before applying:')
    print(f'  pnpm reconcile-identities <workspace> --manifest {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
