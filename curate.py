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


# ── Block: mojibake repair ────────────────────────────────────────────────────
# Names mangled by an upstream cp1252/latin-1 decode. Three classes (per the
# audit): clean-twin merges the mangling split apart; lost-byte cases (U+FFFD)
# reconstructed by hand; and the mechanical rest, repaired programmatically.

# Clean twin existed separately because the mangled form folds differently — the
# repair re-unites them (the "Dion family" effect).
MOJIBAKE_MERGES = [
    ('aurele-dion-dds9', ['aurele-dion-fz7y'], 'Aurèle Dion', 'mojibake variant folded'),
    ('josephine-dion-jmf9', ['josephine-dion-smx7'], 'Joséphine Dion', 'mojibake variant folded'),
    ('paidi-a-coistealbha-wsrv', ['paidi-a-coistealbha-c35s'], 'Paidí A Coistealbha', 'mojibake variant folded'),
    ('siun-ni-choistealbha-tvx7', ['siun-ni-choistealbha-hr8p', 'si-n-n-choistealbha-m3bj'], 'Siún Ní Choistealbha', 'mojibake and spelling variants folded'),
    ('molly-oa-tmflaherty-eap6', ['molly-o-flaherty-fqxf'], "Molly O'Flaherty", 'mojibake apostrophe variants folded'),
    ('connor-oa-tmsullivan-hysc', ['connor-o-sullivan-p5tf', 'connor-o-sullivan-nrr3'], "Connor O'Sullivan", 'mojibake apostrophe and placeholder-sail variants folded'),
    ('amy-o-halloran-rcvx', ['amy-oa-tmhalloran-2b49'], "Amy O'Halloran", 'mojibake apostrophe variant folded'),
    ('olivia-cure-u53f', ['olivia-cur-966u'], 'Olivia Cure', 'mojibake variant folded'),
    ('joe-landers-eugt', ['joe-landers-ym7k'], 'Joe Landers', 'lost-byte variant folded'),
    ('skye-o-callaghan-xhvf', ['skye-oa-tmcallaghan-4kym'], "Skye O'Callaghan", 'mojibake apostrophe variant folded'),
    ('siofra-buckley-trbr', ['siofra-buckley-gquj'], 'Síofra Buckley', 'mojibake variant folded'),
]

# Lost-byte (U+FFFD) or wrong-accent-at-source cases: codec can't recover them,
# reconstructed by hand from the obvious name; plus two fada restorations.
MOJIBAKE_MANUAL = {
    'caolan-pepper-v9ns': 'Caolán Pepper',                       # source carried grave; canonical fada
    'a-a-igo-rama-rez-ferna-ndez-j837': 'Íñigo Ramírez Fernández',
    'fion-n-dollard-76g7': 'Fionán Dollard',
    'oscar-luain-8qa7': 'Oscar Ó Luain',
    'caoimhe-nic-thr-infhir-w5v7': 'Caoimhe Nic Thréinfhir',
    'aine-cahill-ujh3': 'Áine Cahill',                            # fada restored
    'tomas-a-coistealbha-dfpz': 'Tomás A Coistealbha',            # fada restored
}

# Handled in the cross-hull block (merge + repair together).
_DEFER = {'max-oa-tmhare-7bva'}
_MARKERS = ('Ã', 'Â', 'â€')


def demojibake(s):
    """Reverse a cp1252/latin-1-then-utf-8 mis-decode; straighten the curly
    apostrophe it yields."""
    for codec in ('cp1252', 'latin-1'):
        try:
            fixed = s.encode(codec).decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if fixed != s:
            s = fixed
            break
    return s.replace('’', "'")


def block_mojibake(ids):
    for into, froms, name, note in MOJIBAKE_MERGES:
        ids = merge(ids, into, froms, name=name, note=note)
    for slug, name in MOJIBAKE_MANUAL.items():
        ids = rename(ids, slug, name=name)
    # Mechanical repair of the remaining mangled names.
    for c in ids:
        if c.slug in _DEFER:
            continue
        if any(m in c.name for m in _MARKERS):
            c.name = demojibake(c.name)
    # Nothing but the deferred entry should carry a marker now.
    leftover = [c.slug for c in ids
                if c.slug not in _DEFER
                and any(m in c.name for m in ('Ã', 'Â', 'â€', 'ï¿½', '�'))]
    assert not leftover, f'unrepaired mojibake: {leftover}'
    return ids


# ── Block: single-token names ─────────────────────────────────────────────────
# Run-together names that won't match (GeorgeROBINSON), first names recovered
# from the hull, and one phantom all-DNC registration.
SINGLE_MERGES = [
    ('george-robinson-p46f', ['georgerobinson-8ger'], 'George Robinson', 'run-together name folded'),
    ('jess-tottenham-zcrs', ['jesstottenham-acup'], 'Jess Tottenham', 'run-together home-hull row folded'),
    ('noah-john-carty-ezta', ['noahjohn-v2ku', 'noahjohn-carty-2ym4'], 'Noah John Carty', 'run-together and compound-name variants folded'),
    ('allden-carty-pfeu', ['allden-snqe'], 'Allden Carty', 'first-name-only row recovered from hull'),
    ('amelia-chapman-rnvz', ['amelia-uwzy'], 'Amelia Chapman', 'first-name-only row recovered from hull'),
    ('finn-cullen-fsvb', ['finn-jd7b'], 'Finn Cullen', 'first-name-only row recovered from hull'),
    ('indie-crosbie-gvr9', ['indie-4b8d'], 'Indie Crosbie', 'first-name-only row recovered from hull'),
    ('zita-tempany-wfgc', ['zita-madb'], 'Zita Tempany', 'first-name-only row recovered from hull'),
    ('jonathan-dempsey-6vz3', ['dempsey-8cfx'], 'Jonathan Dempsey', 'phantom all-DNC registration folded into the competing entry'),
]

# Run-together names with no twin — just split the tokens.
SINGLE_RENAMES = {
    'jasongarland-g6ds': 'Jason Garland',
    'thomasoleary-7u8u': "Thomas O'Leary",
}

# Audit false-positives: complete names joined by a non-breaking space (2013
# Nationals visitors). Collapse to a clean display form.
NBSP_RENAMES = {
    'alexandra-schonrock-q5b2': 'Alexandra Schonrock',
    'alex-king-pcwj': 'Alex King',
    'arthur-fry-f7x6': 'Arthur Fry',
    'ellen-main-tk7z': 'Ellen Main',
    'freya-black-hah8': 'Freya Black',
    'hannah-roberts-straw-5qv6': 'Hannah Roberts-Straw',
    'hannah-tucker-k9vz': 'Hannah Tucker',
    'haydn-sewell-84vu': 'Haydn Sewell',
    'jamie-cook-k88k': 'Jamie Cook',
    'rhys-lewis-kdg9': 'Rhys Lewis',
    'ryan-bush-jgs5': 'Ryan Bush',
    'vita-heathcote-qmsx': 'Vita Heathcote',
}


def block_single_token(ids):
    for into, froms, name, note in SINGLE_MERGES:
        ids = merge(ids, into, froms, name=name, note=note)
    for slug, name in {**SINGLE_RENAMES, **NBSP_RENAMES}.items():
        ids = rename(ids, slug, name=name)
    return ids


# ── Block: cross-hull name normalisation ──────────────────────────────────────
# Same sailor split across hulls by a spelling/casing/mojibake variant.
CROSS_HULL_MERGES = [
    ('max-oa-tmhare-7bva', ['max-o-hare-2q67', 'max-o-hare-ayf8'], "Max O'Hare", 'spelling and mojibake variants folded'),
]
CROSS_HULL_RENAMES = {
    'nicole-rose-quinn-6sdp': 'Nicole Quinn',     # recorded with and without middle name
    'robin-mullett-93hk': 'Robin Mullett',        # capitalisation normalised
}


def block_cross_hull(ids):
    for into, froms, name, note in CROSS_HULL_MERGES:
        ids = merge(ids, into, froms, name=name, note=note)
    for slug, name in CROSS_HULL_RENAMES.items():
        ids = rename(ids, slug, name=name)
    return ids


BLOCKS = {
    'merges': block_merges,
    'mojibake': block_mojibake,
    'single-token': block_single_token,
    'cross-hull': block_cross_hull,
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
