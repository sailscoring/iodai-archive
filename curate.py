#!/usr/bin/env python3
"""Apply hand-adjudicated identity decisions to manifest.py (sailscoring #218).

Each decision was made by reviewing the full hull history behind an
IDENTITY-AUDIT flag. This script encodes them as explicit, slug-keyed operations
so the curation is auditable and re-runnable, and rewrites manifest.py in place.
Run one block at a time (a commit per block):

    python3 curate.py merges          # sail-number loan / spelling / apostrophe folds
    python3 curate.py mojibake        # repair mangled-encoding name fields
    python3 curate.py single-token    # run-together / first-name / phantom rows
    python3 curate.py cross-hull      # same sailor across different hulls

Operations are loud: a missing slug raises, so a stale decision fails fast rather
than silently no-opping. Notes are deliberately clinical — what was folded, not
who is related to whom.
"""
import re
import sys

import manifest
from identity_manifest import emit_manifest_py

MANIFEST = 'manifest.py'


def load_header():
    """Preserve the comment block between the import and IDENTITIES (the matcher's
    open review-suggestions) verbatim across rewrites."""
    text = open(MANIFEST, encoding='utf-8').read()
    m = re.search(r'^from identity_manifest import C\n(.*?)\nIDENTITIES = \[',
                  text, re.S | re.M)
    if not m:
        return None
    return [ln for ln in m.group(1).splitlines() if ln.startswith('#')]


def by_slug(ids):
    idx = {}
    for c in ids:
        idx[c.slug] = c
    return idx


def merge(ids, into, froms, *, name=None, club=None, note=None):
    """Fold `froms` into `into`: union rows, set canonical fields, drop `froms`."""
    idx = by_slug(ids)
    survivor = idx[into]  # KeyError = stale decision, fail loud
    rows = list(survivor.rows)
    seen = {tuple(r) for r in rows}
    for f in froms:
        for r in idx[f].rows:
            if tuple(r) not in seen:
                rows.append(tuple(r))
                seen.add(tuple(r))
    survivor.rows = sorted(rows)
    if name is not None:
        survivor.name = name
    if club is not None:
        survivor.club = club
    if note is not None:
        survivor.note = note
    drop = set(froms)
    return [c for c in ids if c.slug not in drop]


def rename(ids, slug, *, name=None, club=None, note=None):
    """Edit fields on one entry in place (no merge)."""
    c = by_slug(ids)[slug]
    if name is not None:
        c.name = name
    if club is not None:
        c.club = club
    if note is not None:
        c.note = note
    return ids


# ── Block: sail-number loan / spelling / apostrophe / mojibake folds ───────────
# (into, [froms], canonical name, clinical note). The matcher under-merged these:
# a one-off row split from the sailor's continuous run on the same hull.
MERGES = [
    ('daniel-o-beirne-qt9y', ['dan-o-beirne-fnzr'], "Daniel O'Beirne", 'nickname variant folded'),
    ('paddy-cure-gpfd', ['paddy-cur-w6xv'], 'Paddy Cure', 'mojibake variant folded'),
    ('conal-a-dubhghaill-vvar', ['conol-o-dubhghaill-w4bc'], 'Conal Ó Dubhghaill', 'anglicised spelling and mojibake folded'),
    ('dylan-farrell-bvmx', ['dyllon-farrelly-3n6g'], 'Dylan Farrell', 'spelling variant folded'),
    ('charlie-cullen-xwzd', ['charles-cullen-ysh9'], 'Charlie Cullen', 'formal-name variant folded'),
    ('dara-donnelly-r5vd', ['dara-donnolly-ptxs'], 'Dara Donnelly', 'spelling variant folded'),
    ('conall-mac-thr-infhir-pvq4', ['conall-mac-threinfhir-hyyg'], 'Conall Mac Thréinfhir', 'mojibake and spelling folded'),
    ('killian-o-regan-gd5n', ['killian-o-regan-zg9c'], "Killian O'Regan", 'apostrophe normalised'),
    ('kirsten-quinn-2g6e', ['kirstin-quinn-33qy'], 'Kirsten Quinn', 'spelling variant folded'),
    ('lauren-o-callaghan-g4n6', ['lauren-o-callaghan-j73h'], "Lauren O'Callaghan", 'stray space and apostrophe normalised'),
    ('zoe-ohare-e952', ['zoe-o-hare-ttjj'], "Zoe O'Hare", 'apostrophe normalised'),
    ('cathal-o-regan-ka96', ['cathal-o-regan-t3k7'], "Cathal O'Regan", 'apostrophe normalised'),
    ('oran-collins-tnj2', ['a-ran-collins-fsdc'], 'Óran Collins', 'mojibake variant folded'),
    ('eabha-brennan-hobbs-8a9p', ['aeabha-brennan-hobbs-ud5x', 'eabha-brennan-hobbs-4gpf', 'a-abha-brennan-hobbs-g5ag'], 'Éabha Brennan-Hobbs', 'spelling and mojibake variants folded'),
    ('tp-hogan-2adm', ['thomas-hogan-pyw3'], 'Thomas Hogan', 'also recorded as "TP Hogan"'),
    ('oliver-simington-uave', ['ollie-simington-6k7j'], 'Oliver Simington', 'nickname variant folded'),
    ('eoin-o-sullivan-h7yv', ['eoin-o-sullivan-r2g7'], "Eoin O'Sullivan", 'apostrophe normalised'),
    ('abigail-o-sullivan-7dyd', ['abigail-o-sullivan-dk6a'], "Abigail O'Sullivan", 'apostrophe normalised'),
    ('eoin-pierse-rhx4', ['eoin-pierce-qgze'], 'Eoin Pierse', 'spelling variant folded'),
    ('oliver-ryan-vvtf', ['ollie-ryan-rcqs'], 'Oliver Ryan', 'nickname variant folded'),
    ('jamie-blennnerhassett-jqkm', ['jamie-blennerhassett-h4k9'], 'Jamie Blennerhassett', 'repeated-letter typo corrected'),
    ('isabelle-passberger-nnme', ['issabelle-passberger-5ngw'], 'Isabelle Passberger', 'spelling typo corrected'),
    ('james-dwyer-matthews-qxuv', ['james-dwyer-e2zk'], 'James Dwyer Matthews', 'dropped surname part restored'),
    ('aoibhin-farrelly-4kkw', ['aoibheann-farrelly-7ydh', 'aoibhinn-farrelly-d8rt'], 'Aoibhín Farrelly', 'spelling variants folded'),
    ('edie-cobbe-o-neill-t884', ['eddie-o-neill-ksq4'], "Edie Cobbe O'Neill", 'duplicate registration across regatta fleets at one event'),
]


def block_merges(ids):
    for into, froms, name, note in MERGES:
        ids = merge(ids, into, froms, name=name, note=note)
    return ids


BLOCKS = {
    'merges': block_merges,
}


def main(argv):
    if len(argv) < 2 or argv[1] not in BLOCKS:
        sys.exit(f'usage: python3 curate.py <{"|".join(BLOCKS)}>')
    header = load_header()
    before = len(manifest.IDENTITIES)
    ids = BLOCKS[argv[1]](list(manifest.IDENTITIES))
    open(MANIFEST, 'w', encoding='utf-8').write(emit_manifest_py(ids, header_notes=header))
    print(f'block {argv[1]}: {before} -> {len(ids)} identities ({before - len(ids)} folded)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
