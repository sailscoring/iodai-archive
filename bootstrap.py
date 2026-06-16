#!/usr/bin/env python3
"""Generate a draft competitor-identity manifest (sailscoring #218).

Reads every built ``series/*.sailscoring``, clusters the named competitors
through the app's *canonical* matcher (the sibling repo's ``pnpm cluster-rows``,
the same one ``reconcile-identities`` uses), and writes a draft ``manifest.py``:
the golden-record starting point to curate by hand.

Clustering the archive's own rows — rather than the live workspace — keys every
cluster by ``(series-slug, sail)`` directly. (The app mints fresh competitor ids
on import, so the live ids can't be mapped back to a slug afterwards.) It also
matches the issue's philosophy: fix data at source here, re-import.

Needs the sibling app repo at ``../sailscoring`` for the matcher.

    python3 bootstrap.py            # write manifest.py (refuses to clobber)
    python3 bootstrap.py --force    # overwrite an existing manifest.py
"""
import glob
import json
import os
import subprocess
import sys

from identity_manifest import C, emit_manifest_py, mint_slug

APP_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sailscoring')
)
MANIFEST = 'manifest.py'


def load_rows():
    """Every *named* competitor across the built series, tagged with its series
    out-slug (the filename stem) and race year. Returns (rows, blank_count)."""
    rows = []
    blanks = 0
    for path in sorted(glob.glob('series/*.sailscoring')):
        out = os.path.basename(path)[: -len('.sailscoring')]
        data = json.load(open(path, encoding='utf-8'))
        year = (data.get('series', {}).get('startDate', '') or '')[:4]
        for c in data.get('competitors', []):
            name = (c.get('name') or '').strip()
            if not name:
                blanks += 1
                continue  # a sail-only entry can't anchor a person (#218)
            rows.append({
                'out': out,
                'sail': c.get('sailNumber') or '',
                'name': name,
                'club': c.get('club') or '',
                'age': c.get('age'),
                'year': int(year) if year.isdigit() else None,
            })
    return rows, blanks


def cluster(rows):
    """Run the rows through the app's matcher and return its ClusterResult."""
    payload = [
        {
            'competitorId': str(i),
            'name': r['name'],
            'sailNumber': r['sail'],
            'club': r['club'],
            'age': r['age'],
            'raceYear': r['year'],
        }
        for i, r in enumerate(rows)
    ]
    try:
        proc = subprocess.run(
            ['pnpm', '--silent', '--dir', APP_DIR, 'cluster-rows'],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        sys.exit('pnpm not found — bootstrap needs the sibling app repo and pnpm.')
    except subprocess.CalledProcessError as e:
        sys.exit(f'cluster-rows failed:\n{e.stderr}')
    return json.loads(proc.stdout)


def build_identities(rows, result):
    """Turn each cluster into a C(...) entry keyed by (series-slug, sail)."""
    taken = set()
    identities = []
    for cluster_ in result['clusters']:
        members = sorted({
            (rows[int(cid)]['out'], rows[int(cid)]['sail'])
            for cid in cluster_['competitorIds']
        })
        name = cluster_['label']
        stable_key = '|'.join(f'{o}/{s}' for o, s in members)
        identities.append(C(
            slug=mint_slug(name, stable_key, taken),
            name=name,
            rows=members,
            club=cluster_.get('club') or '',
        ))
    return identities


def suggestion_notes(result):
    """The matcher's weak (name-only) review pairs, as commented candidate merges
    for the curator to adjudicate into the manifest."""
    suggestions = result.get('suggestions', [])
    clusters = result['clusters']
    notes = ['# Review suggestions — candidate merges the matcher left for a human',
             f'# to adjudicate ({len(suggestions)}). Merge into one C(...) if the same',
             '# sailor; leave split if genuinely different people:']
    for s in suggestions:
        a, b = clusters[s['a']], clusters[s['b']]
        notes.append(
            f'#   ? "{a["label"]}" ({a["sailNumber"]}, {a.get("club") or "-"})'
            f' ~ "{b["label"]}" ({b["sailNumber"]}, {b.get("club") or "-"})'
        )
    return notes


def main(argv):
    force = '--force' in argv
    if os.path.exists(MANIFEST) and not force:
        sys.exit(f'{MANIFEST} exists — curate it by hand, or pass --force to regenerate the draft.')

    rows, blanks = load_rows()
    result = cluster(rows)
    identities = build_identities(rows, result)

    multi = sum(1 for c in identities if len(c.rows) > 1)
    singletons = len(identities) - multi
    notes = suggestion_notes(result)

    with open(MANIFEST, 'w', encoding='utf-8') as fh:
        fh.write(emit_manifest_py(identities, header_notes=notes))

    print(f'Wrote {MANIFEST}')
    print(f'  named rows:        {len(rows)}')
    print(f'  blank rows skipped:{blanks:>5}  (sail-only; recover or exclude — see IDENTITY-AUDIT.md)')
    print(f'  identities:        {len(identities)}')
    print(f'    multi-series:    {multi}')
    print(f'    singletons:      {singletons}')
    print(f'  review suggestions:{len(result.get("suggestions", [])):>5}  (commented at the top of {MANIFEST})')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
