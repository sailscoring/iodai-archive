#!/usr/bin/env python3
"""Competitor-identity golden-record manifest (sailscoring #218).

Defines the ``C(...)`` record that ``manifest.py`` (the curated golden record) is
written in, plus the slug minting and draft serialisation that ``bootstrap.py``
uses to generate that draft. Plain stdlib.

A manifest entry is one cross-series competitor. Its ``rows`` are
``(series-slug, sail)`` pairs — the file slug (``out``) of each series the
sailor appears in, and the sail number they carried there. That key is readable
and stable (the archive owns both halves), and the app's
``as-published identities`` apply resolves it to a competitor at apply time.

The slug is the manifest *key* and the public-URL handle. It's minted once from
the name plus a short suffix derived deterministically from the entry's rows, so
a regenerated draft is byte-stable and the same sailor keeps the same slug
across runs. Curate the name freely afterwards — the slug never moves.
"""
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field


@dataclass
class C:
    """One cross-series competitor in the manifest."""
    slug: str
    name: str
    rows: list  # list of (series_slug, sail) tuples
    club: str = ""
    nat: str = ""
    note: str = ""
    # Season-ranking memberships (app #309): the ranking document keys this
    # sailor appears in. A ranking-only sailor has ranking_rows and no series
    # rows - the identity exists to anchor those rows and their career arc.
    ranking_rows: list = field(default_factory=list)


def repair_mojibake(name):
    """Un-mangle UTF-8-read-as-Latin-1 ("JosÃ©phine" -> "Joséphine"); identity
    if it doesn't cleanly round-trip. Mirrors audit.py so slugs come out clean
    even from mangled source names."""
    try:
        fixed = name.encode('latin-1').decode('utf-8')
        return fixed if fixed != name else name
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def slugify_name(name):
    """Name -> slug base: repair mojibake, strip diacritics, lowercase, hyphenate
    runs of non-alphanumerics. Mirrors the app's slugifyName (lib/competitor-slug.ts)
    so a draft slug looks like one the app would mint. Falls back to 'competitor'."""
    s = repair_mojibake(name)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s or 'competitor'


# Same unambiguous alphabet the app uses for slug suffixes (no 0/o/1/l/i).
_SUFFIX_ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789'
_SUFFIX_LEN = 4


def _suffix(stable_key):
    """A deterministic 4-char suffix from a stable key, in the app's alphabet."""
    digest = hashlib.sha1(stable_key.encode('utf-8')).digest()
    n = int.from_bytes(digest[:8], 'big')
    out = ''
    for _ in range(_SUFFIX_LEN):
        n, r = divmod(n, len(_SUFFIX_ALPHABET))
        out += _SUFFIX_ALPHABET[r]
    return out


def mint_slug(name, stable_key, taken):
    """A unique slug for ``name``: base + a suffix derived from ``stable_key``.
    Extends the key on the (vanishing) chance of a collision so it always
    terminates. Adds the result to ``taken``."""
    base = slugify_name(name)
    key = stable_key
    for _ in range(20):
        candidate = f'{base}-{_suffix(key)}'
        if candidate not in taken:
            taken.add(candidate)
            return candidate
        key += '+'
    # Astronomically unlikely; widen the suffix rather than loop forever.
    candidate = f'{base}-{_suffix(key)}-{_suffix(key + "!")}'
    taken.add(candidate)
    return candidate


def _pystr(s):
    """A double-quoted Python string literal (json.dumps round-trips cleanly)."""
    return json.dumps(s, ensure_ascii=False)


def _render_entry(c):
    rows = ', '.join(f'({_pystr(slug)}, {_pystr(sail)})' for slug, sail in c.rows)
    parts = [f'slug={_pystr(c.slug)}', f'name={_pystr(c.name)}']
    if c.club:
        parts.append(f'club={_pystr(c.club)}')
    if c.nat:
        parts.append(f'nat={_pystr(c.nat)}')
    head = ', '.join(parts)
    line = f'    C({head},\n      rows=[{rows}]'
    if c.note:
        line += f',\n      note={_pystr(c.note)}'
    line += '),'
    return line


MANIFEST_VERSION = 1


def compile_manifest(identities, out_to_id, *, allow_missing=False):
    """Compile curated ``C`` entries into the JSON the app's
    ``as-published identities`` apply consumes.

    ``out_to_id`` maps each series out-slug to its *live* seriesId in the target
    workspace. The result embeds a ``series`` slug->id map (only the slugs the
    manifest actually references) so member rows stay readable while the app
    stays workspace-agnostic.

    By default, raises ValueError listing every referenced out-slug with no live
    id — a partial map would silently drop those members, and a missing id is
    usually a name mismatch or a not-yet-imported series worth surfacing. With
    ``allow_missing`` (the workspace holds only a subset of the corpus, e.g. the
    latest events aren't imported yet), members in unresolved series are dropped
    and identities left empty are omitted; the golden record in manifest.py stays
    complete and a later re-compile picks them up.
    """
    referenced = sorted({slug for c in identities for slug, _ in c.rows})
    missing = [slug for slug in referenced if slug not in out_to_id]
    if missing and not allow_missing:
        raise ValueError(
            'no live seriesId for ' + str(len(missing)) + ' referenced series:\n  '
            + '\n  '.join(missing)
        )

    series_map = {slug: out_to_id[slug] for slug in referenced if slug in out_to_id}
    out_identities = []
    for c in identities:
        rows = [(slug, sail) for slug, sail in c.rows if slug in out_to_id]
        if not rows:
            continue  # every series this competitor appeared in is unresolved
        entry = {'slug': c.slug, 'name': c.name,
                 'members': [[slug, sail] for slug, sail in rows]}
        if c.club:
            entry['club'] = c.club
        if c.nat:
            entry['nationality'] = c.nat
        if c.note:
            entry['note'] = c.note
        out_identities.append(entry)

    return {'version': MANIFEST_VERSION, 'series': series_map, 'identities': out_identities}


def emit_manifest_py(identities, *, header_notes=None):
    """Render a list of ``C`` to ``manifest.py`` source. Entries are sorted by
    name then slug for a stable, reviewable diff."""
    ordered = sorted(identities, key=lambda c: (c.name.lower(), c.slug))
    L = [
        '#!/usr/bin/env python3',
        '"""IODAI competitor-identity golden record (sailscoring #218).',
        '',
        'A DRAFT generated by `python3 bootstrap.py` from the app\'s canonical',
        'matcher. Curate by hand: merge nicknames/typos the matcher split, split',
        'over-merged namesakes, fix names, assign slugs. Each C(...) is one',
        'cross-series competitor; rows are (series-slug, sail) pairs.',
        '',
        'The slug is the stable key and public-URL handle — never change it once',
        'a sailor has been reconciled. Edit names freely; the slug stays put.',
        '"""',
        'from identity_manifest import C',
        '',
    ]
    if header_notes:
        L.extend(header_notes)
        L.append('')
    L.append('IDENTITIES = [')
    L.extend(_render_entry(c) for c in ordered)
    L.append(']')
    return '\n'.join(L) + '\n'
