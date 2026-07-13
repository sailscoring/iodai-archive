#!/usr/bin/env python3
"""Interactive namesake review for the curated manifest (sailscoring #218).

Walks you through every group of competitors that share (or nearly share) a name
but are left as separate identities — the matcher's weak name-only suggestions
plus exact-name collisions the curation surfaced — and records a 1/2/3 verdict
for each. Resumable: progress is saved after every answer.

    python3 review.py            # review (resumes where you left off)
    python3 review.py --refresh  # rebuild the candidate groups from the manifest
    python3 review.py --md       # also write NAMESAKE-REVIEW.md (static copy)
    python3 review.py --apply     # fold the MERGE verdicts into manifest.py

Building the groups needs the sibling app repo at ../sailscoring (the matcher).
Reviewing and applying do not.
"""
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

import manifest

GROUPS = 'namesake-groups.json'      # cached candidate groups (display data)
VERDICTS = 'namesake-verdicts.json'  # your decisions
MD = 'NAMESAKE-REVIEW.md'


def fold(name):
    """Grouping key: NFKD-strip diacritics (like audit.fold), then drop
    everything but letters — apostrophes, hyphens, digits *and spacing* — so
    `Ó`/`O`, `O Neill`/`O'Neill` and `X- Y`/`X-Y` all collide (#5)."""
    s = unicodedata.normalize('NFKD', name.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s)


def year_of(out):
    m = re.search(r'(19|20)\d{2}', out)
    return m.group(0) if m else '????'


def _span(rows):
    years = sorted({year_of(o) for o, _ in rows})
    return years[0] if len(years) == 1 else f'{years[0]}–{years[-1]}'


# ── build candidate groups (needs the matcher) ────────────────────────────────

def build_groups():
    import bootstrap

    ids = manifest.IDENTITIES
    by_slug = {c.slug: c for c in ids}
    row_to_slug = {(o, s): c.slug for c in ids for o, s in c.rows}

    edges = set()
    rows, _ = bootstrap.load_rows()
    result = bootstrap.cluster(rows)
    clusters = result['clusters']

    def cluster_slug(ci):
        for cid in clusters[ci]['competitorIds']:
            slug = row_to_slug.get((rows[int(cid)]['out'], rows[int(cid)]['sail']))
            if slug:
                return slug
        return None

    for sug in result.get('suggestions', []):
        a, b = cluster_slug(sug['a']), cluster_slug(sug['b'])
        if a and b and a != b:
            edges.add(frozenset((a, b)))
    by_name = defaultdict(list)
    for c in ids:
        by_name[fold(c.name)].append(c.slug)
    for slugs in by_name.values():
        for i in range(len(slugs)):
            for j in range(i + 1, len(slugs)):
                edges.add(frozenset((slugs[i], slugs[j])))

    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        a, b = tuple(e)
        parent[find(a)] = find(b)
    comps = defaultdict(set)
    for e in edges:
        for s in e:
            comps[find(s)].add(s)

    groups = []
    for slugs in comps.values():
        members = sorted((by_slug[s] for s in slugs), key=lambda c: -len(c.rows))
        clubs = {re.sub(r'[^a-z]', '', (c.club or '').lower()) for c in members if c.club}
        sails_sets = [{re.sub(r'[^A-Z0-9]', '', s.upper()) for _, s in c.rows} for c in members]
        shared = any(sails_sets[i] & sails_sets[j]
                     for i in range(len(members)) for j in range(i + 1, len(members)))
        if len(clubs) > 1:
            bucket, why = 'likely-namesake', 'different clubs'
        elif shared:
            bucket, why = 'likely-same', 'same club and a shared sail number'
        elif any(not c.club for c in members):
            bucket, why = 'uncertain', 'one side has no club recorded'
        else:
            bucket, why = 'judgment', 'same club, different sail numbers'
        groups.append({
            'key': '|'.join(sorted(slugs)),
            'name': members[0].name,
            'bucket': bucket,
            'why': why,
            'entries': [{
                'slug': c.slug, 'name': c.name, 'club': c.club or '',
                'rows': sorted([o, s] for o, s in c.rows),
                'sails': sorted({s for _, s in c.rows}),
                'span': _span(c.rows),
            } for c in members],
        })
    order = {'likely-same': 0, 'judgment': 1, 'uncertain': 2, 'likely-namesake': 3}
    groups.sort(key=lambda g: (order[g['bucket']], fold(g['name'])))
    json.dump({'groups': groups}, open(GROUPS, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    return groups


def load_groups(refresh):
    if refresh or not os.path.exists(GROUPS):
        print('Building candidate groups via the matcher…')
        return build_groups()
    return json.load(open(GROUPS, encoding='utf-8'))['groups']


def load_verdicts():
    if os.path.exists(VERDICTS):
        return json.load(open(VERDICTS, encoding='utf-8'))
    return {}


def save_verdicts(v):
    json.dump(v, open(VERDICTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


# ── rendering ─────────────────────────────────────────────────────────────────

BUCKET_LABEL = {
    'likely-same': 'LIKELY SAME (same club + shared sail)',
    'judgment': 'JUDGMENT (same club, different sail)',
    'uncertain': 'UNCERTAIN (a club is missing)',
    'likely-namesake': 'LIKELY NAMESAKE (different clubs)',
}


def show(g, i, total, verdict):
    print('\n' + '=' * 74)
    print(f' {i + 1}/{total}   [{BUCKET_LABEL[g["bucket"]]}]')
    print(f' "{g["name"]}"')
    print('-' * 74)
    for n, e in enumerate(g['entries'], 1):
        print(f' [{n}] {e["slug"]}')
        print(f'     {e["club"] or "(no club)"} · {len(e["rows"])} rows · {e["span"]} · sails {e["sails"]}')
        for o, s in e['rows']:
            print(f'        {o}  {s}')
    if verdict:
        d = verdict['decision']
        extra = f" -> {verdict.get('into')}" if d == 'merge' else ''
        print(f' (current: {d}{extra})')
    print('-' * 74)


# ── interactive loop ──────────────────────────────────────────────────────────

def review(groups):
    v = load_verdicts()
    total = len(groups)
    decided = sum(1 for g in groups if g['key'] in v)
    i = next((k for k, g in enumerate(groups) if g['key'] not in v), 0)
    print(f'{total} groups, {decided} already decided. '
          '1=merge  2=keep  3=unsure  b=back  q=save&quit')
    while 0 <= i < total:
        g = groups[i]
        show(g, i, total, v.get(g['key']))
        try:
            ans = input(' 1=merge 2=keep 3=unsure (b/q) > ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if ans == 'q':
            break
        if ans == 'b':
            i = max(0, i - 1)
            continue
        if ans == '2':
            v[g['key']] = {'decision': 'keep', 'name': g['name'],
                           'slugs': [e['slug'] for e in g['entries']]}
        elif ans == '3':
            v[g['key']] = {'decision': 'unsure', 'name': g['name'],
                           'slugs': [e['slug'] for e in g['entries']]}
        elif ans == '1':
            into = g['entries'][0]['slug']
            if len(g['entries']) > 1:
                pick = input(f'   merge into which? 1-{len(g["entries"])} '
                             '[1, most rows] > ').strip()
                if pick.isdigit() and 1 <= int(pick) <= len(g['entries']):
                    into = g['entries'][int(pick) - 1]['slug']
            v[g['key']] = {'decision': 'merge', 'into': into, 'name': g['name'],
                           'slugs': [e['slug'] for e in g['entries']]}
        else:
            continue  # unrecognised — re-show same item
        save_verdicts(v)
        i += 1
    save_verdicts(v)
    counts = defaultdict(int)
    for g in groups:
        counts[v.get(g['key'], {}).get('decision', 'undecided')] += 1
    print('\nSaved.', dict(counts))
    if i >= total:
        print('All groups reviewed. Apply with: python3 review.py --apply')


# ── apply MERGE verdicts ──────────────────────────────────────────────────────

def apply():
    import curate
    from identity_manifest import emit_manifest_py

    v = load_verdicts()
    ids = list(manifest.IDENTITIES)
    have = {c.slug for c in ids}
    applied = 0
    for rec in v.values():
        if rec.get('decision') != 'merge':
            continue
        into = rec['into']
        froms = [s for s in rec['slugs'] if s != into and s in have]
        if into not in have or not froms:
            continue
        ids = curate.merge(ids, into, froms,
                           note='namesake review: confirmed same sailor')
        applied += 1
    open('manifest.py', 'w', encoding='utf-8').write(
        emit_manifest_py(ids, header_notes=curate.load_header()))
    print(f'Applied {applied} merges -> {len(ids)} identities.')
    print('Recompile with: python3 compile.py series-dump.json')


def write_md(groups):
    L = ['# Namesake review (static copy) — see `python3 review.py` for the interactive version', '']
    for g in groups:
        L.append(f'## "{g["name"]}" — _{g["why"]}_')
        for e in g['entries']:
            L.append(f'- `{e["slug"]}` — {e["club"] or "(no club)"} · {len(e["rows"])} rows · {e["span"]} · sails {e["sails"]}')
        L.append('')
    open(MD, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'Wrote {MD}')


def main(argv):
    if '--apply' in argv:
        return apply()
    groups = load_groups('--refresh' in argv)
    if '--md' in argv:
        write_md(groups)
        return 0
    review(groups)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
