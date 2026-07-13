#!/usr/bin/env python3
"""One-off transcriber: 2012 Nationals PDFs -> Sail100-shaped HTML (#2).

The 2012 Nationals survive only as PDF exports of the old Sail100 results
(naju2012os.pdf / nase2012os.pdf on iodai.com/results-files/), while the whole
pipeline reads HTML. This script converts each PDF's text layer into a minimal
HTML table carrying exactly the published columns (place, sail, prize division,
helm, age, club, series points, per-race points) so `engine.parse_file` can
ingest it like any other Phase-2 page. No values are invented: every cell is
lifted verbatim from the PDF text layer (`pdftotext -layout`), and a per-row
checksum (nett == sum of races minus the two largest, +-2.0 for the era's
tie-averaging) guards against column misalignment. `build.py validate` then
re-scores the fleets against the published Series Points as usual.

Usage:  python3 transcribe.py     (from this directory; needs pdftotext)

Wrapped names: pdftotext renders a tall row as  [fragment / record / fragment]
lines; a record whose own line carries no name takes the adjacent unclaimed
fragments (in order) as its name.
"""
import html
import re
import subprocess
import sys

DIVISIONS = ('Gold', 'Silver', 'Bronze')


def parse_pdf(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                         check=True, capture_output=True, text=True).stdout
    entries = int(re.search(r'Entries:\s*(\d+)', txt).group(1))
    nraces = int(re.search(r'Races Sailed:\s*(\d+)', txt).group(1))
    ndisc = int(re.search(r'Discard:\s*(\d+)', txt).group(1))

    items = []  # ('rec', dict) | ('frag', text) | ('sep', '')
    for line in txt.splitlines():
        s = line.strip().strip('\f')
        if (not s or 'Championships' in s or s.startswith('Entries:')
                or 'Provisional' in s or s.startswith('Series')
                or s.startswith('Place') or 'Sail No' in s
                or 'Sail100' in s
                or re.fullmatch(r'\w{3} \d\d \w{3} \d\d.*', s)):
            # blank/heading lines break frag<->record adjacency
            if items and items[-1][0] != 'sep':
                items.append(('sep', ''))
            continue
        m = re.match(r'^(\d+)\s+(\S+)\s+(%s)\s+(.*)$' % '|'.join(DIVISIONS), s)
        if not m:
            if re.search(r'[A-Za-z]', s) and not re.search(r'\d{3}', s):
                # the senior PDF duplicates one name fragment ('Lucy') as two
                # stacked text objects — keep a single copy
                if items and items[-1] == ('frag', s):
                    continue
                items.append(('frag', s))
                continue
            raise SystemExit(f'unrecognised line: {line!r}')
        place, sail, division, rest = m.groups()
        toks = rest.split()
        if len(toks) < nraces + 1 or any(not re.fullmatch(r'\d+(?:\.\d+)?', t)
                                         for t in toks[-(nraces + 1):]):
            raise SystemExit(f'bad points block: {line!r}')
        nums = toks[-(nraces + 1):]
        mid = toks[:-(nraces + 1)]
        age_i = max((i for i, t in enumerate(mid) if re.fullmatch(r'\d+', t)),
                    default=None)
        if age_i is None:
            raise SystemExit(f'no age token: {line!r}')
        items.append(('rec', dict(
            place=int(place), sail=sail, division=division,
            name=' '.join(mid[:age_i]), age=mid[age_i],
            club=' '.join(mid[age_i + 1:]),
            nett=float(nums[0]), nett_str=nums[0], races=nums[1:])))

    # Attach wrapped-name fragments. A tall row renders as
    # [fragment / record / fragment]; the record's own line may carry none,
    # part, or all of the name. A record "wants" fragments while its inline
    # name is empty, a single token, or hyphen-continued; runs of fragments
    # between two adjacent records split first-to-the-one-above,
    # last-to-the-one-below.
    PARTICLES = {'ni', 'nic', 'o', 'ó', 'ui', 'mac', 'mc', 'de', 'van'}

    def wants(rec):
        nm = rec['name']
        return (not nm or len(nm.split()) == 1 or nm.endswith('-')
                or nm.split()[-1].lower() in PARTICLES)

    def join(*parts):
        out = ''
        for p in parts:
            if not p:
                continue
            out = (out + p) if out.endswith('-') else f'{out} {p}'.strip()
        return out

    i = 0
    while i < len(items):
        if items[i][0] != 'frag':
            i += 1
            continue
        j = i
        while j < len(items) and items[j][0] == 'frag':
            j += 1
        frags = [t for _, t in items[i:j]]
        above = items[i - 1][1] if i > 0 and items[i - 1][0] == 'rec' else None
        below = items[j][1] if j < len(items) and items[j][0] == 'rec' else None
        a_wants = above is not None and wants(above)
        b_wants = below is not None and wants(below)
        if above is not None and below is not None and len(frags) >= 2:
            # a record has at most one fragment line above and one below, so a
            # multi-fragment run between two records splits at the boundary
            above['name'] = join(above['name'], *frags[:-1])
            below['name'] = join(frags[-1], below['name'])
        elif b_wants and not a_wants:
            below['name'] = join(*frags, below['name'])
        elif a_wants and not b_wants:
            above['name'] = join(above['name'], *frags)
        elif all(('frag', t) in items[:i] + items[j:] for t in frags):
            # a row straddling a page break prints its name fragment on both
            # pages (senior 'Lucy' / 'Lucy DONWORTH') — drop the orphan copy
            print(f'note: dropping page-break duplicate fragment {frags}')
        elif above is not None and below is not None and not b_wants:
            # neither wants it by the name-shape heuristic, but a fragment
            # sandwiched between two records that the lower one doesn't need
            # can only be a further surname part of the record above
            # (three-line names: 'Arvind ARUMUGAM MURUGAN')
            above['name'] = join(above['name'], *frags)
        else:
            raise SystemExit(f'cannot place name fragments {frags} '
                             f'(above={above and above["name"]!r} '
                             f'below={below and below["name"]!r})')
        i = j

    recs = [r for k, r in items if k == 'rec']
    # a row straddling a page break is printed whole on both pages (junior
    # place 72) — keep one copy, preferring the more complete name
    dedup = []
    for r in recs:
        p = dedup[-1] if dedup else None
        if (p and (p['place'], p['sail'], p['nett_str'], p['races'])
                == (r['place'], r['sail'], r['nett_str'], r['races'])):
            if len(r['name']) > len(p['name']):
                p['name'] = r['name']
            print(f"note: merging page-break duplicate record "
                  f"{r['place']} {r['sail']} ({p['name']!r})")
            continue
        dedup.append(r)
    recs = dedup
    assert len(recs) == entries, (len(recs), entries)
    assert [r['place'] for r in recs] == list(range(1, entries + 1))
    for r in recs:
        if not r['name']:
            raise SystemExit(f'nameless record: {r}')
        if len(r['races']) != nraces:
            raise SystemExit(f'race-count mismatch: {r}')
        # published nett == races minus the `ndisc` largest (+-2.0: the era
        # prints averaged ties as bare ints)
        pts = [float(x) for x in r['races']]
        delta = r['nett'] - (sum(pts) - sum(sorted(pts)[-ndisc:]))
        if abs(delta) > 2.0:
            raise SystemExit(f'nett checksum off by {delta}: {r}')
    return recs, nraces


def emit(recs, nraces, title, out):
    rows = []
    for r in recs:
        cells = ([r['place'], r['sail'], r['division'], r['name'], r['age'],
                  r['club'], r['nett_str']] + r['races'])
        tds = ''.join(f'<td>{html.escape(str(c))}</td>' for c in cells)
        rows.append(f'<tr>{tds}</tr>')
    hdr = ''.join(f'<td>{h}</td>' for h in
                  ['Series Place', 'Sail No', 'Division', 'Helm', 'Age',
                   'Club', 'Series Points']
                  + [f'Race {i + 1}' for i in range(nraces)])
    doc = (f'<html>\n<head><title>{title}</title></head>\n<body>\n'
           f'<h1>{title}</h1>\n'
           '<p>Transcribed from the published PDF by transcribe.py — see '
           'SOURCES.md.</p>\n'
           f'<table>\n<tr>{hdr}</tr>\n' + '\n'.join(rows)
           + '\n</table>\n</body>\n</html>\n')
    with open(out, 'w', encoding='cp1252', newline='\r\n') as fh:
        fh.write(doc)
    print(f'wrote {out}  ({len(recs)} boats, {nraces} races)')


for pdf, title, out in [
    ('nase2012os.pdf',
     'Irish Optimist National Championships 2012 - Senior Division',
     'nase2012os.html'),
    ('naju2012os.pdf',
     'Irish Optimist National Championships 2012 - Junior Division',
     'naju2012os.html'),
]:
    recs, nraces = parse_pdf(pdf)
    emit(recs, nraces, title, out)
