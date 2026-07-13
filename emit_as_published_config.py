"""Emit `as-published.config.json` from the event definitions (ADR-010,
sailscoring#283) — the input to the app repo's `pnpm archive-generate`.

The event modules under `events/` already encode the whole mapping — which
capture files compose which series, names, venues, dates, logos — so this is
a dump, not new knowledge. Series ids come from `manifest.json`'s pinned
slug→UUID map (the ids already live in the production workspace, so the
as-published ingest updates those series in place via `--convert`).

Scope: **2025 and earlier only.** 2026 events are the current season and stay
full-fidelity per the ADR — scored in-app, never ingested here.

    python3 emit_as_published_config.py
"""

import glob
import importlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CUTOFF_YEAR = 2026  # exclusive: series from this year on are full-fidelity

# Known series-kind suffixes on the archive slugs; stripping one yields the
# event's shared published slug (three series publish into one event page).
KIND_SUFFIXES = ('-main-fleet', '-regatta-racing', '-regatta-coached', '-regatta')


def kebab(name: str) -> str:
    out = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return out or 'fleet'


def published_slug(out: str) -> str:
    for suffix in KIND_SUFFIXES:
        if out.endswith(suffix):
            return out[: -len(suffix)]
    # Full-slug specials: the Sprint Series is its own page; the (non-IODAI)
    # Youth Nationals strips the class qualifier.
    if out.endswith('-optimist'):
        return out[: -len('-optimist')]
    return out


def series_year(s) -> int:
    m = re.search(r'(\d{4})', s.get('start') or '') or re.search(r'-(\d{4})(?:-|$)', s['out'])
    return int(m.group(1)) if m else 0


def fleets_for(s):
    fleets = []
    used = set()
    for src in s['sources']:
        if src.get('fleet_from_col'):
            # One published table carrying a Fleet column (the Sprint Series
            # pages): as published, that's a single page.
            name, sub = 'Overall', 'overall'
        else:
            name = src['fleet']
            sub = kebab(name)
        n = 2
        base = sub
        while sub in used:
            sub = f'{base}-{n}'
            n += 1
        used.add(sub)
        fleets.append({
            'name': name,
            'subPath': sub,
            'file': 'sources/' + src['file'],
        })
    return fleets


def main() -> int:
    manifest = json.load(open('manifest.json'))
    slug_to_id = manifest['series']

    entries = []
    skipped_current = 0
    for path in sorted(glob.glob('events/y*.py')):
        mod = importlib.import_module('events.' + os.path.basename(path)[:-3])
        for s in mod.SERIES:
            if series_year(s) >= CUTOFF_YEAR:
                skipped_current += 1
                continue
            out = s['out']
            if out not in slug_to_id:
                print(f'  ! {out}: not in manifest.json series map — skipped', file=sys.stderr)
                continue
            entry = {
                'key': out,
                'id': slug_to_id[out],
                'publishedSlug': published_slug(out),
                'name': s['name'],
                'source': 'sailwave',
                'fleets': fleets_for(s),
            }
            if s.get('venue'):
                entry['venue'] = s['venue']
            if s.get('start'):
                entry['startDate'] = s['start']
            if s.get('end'):
                entry['endDate'] = s['end']
            if s.get('event_url'):
                entry['eventUrl'] = s['event_url']
            if s.get('venue_url'):
                entry['venueUrl'] = s['venue_url']
            if s.get('venue_logo'):
                entry['venueLogoUrl'] = s['venue_logo']
            if s.get('event_logo'):
                entry['eventLogoUrl'] = s['event_logo']
            entries.append(entry)

    config = {
        'version': 1,
        'out': 'as-published',
        'identities': 'manifest.json',
        'series': entries,
    }
    with open('as-published.config.json', 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'as-published.config.json: {len(entries)} series '
          f'({skipped_current} current-season series left full-fidelity)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
