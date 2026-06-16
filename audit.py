#!/usr/bin/env python3
"""Name / cross-series-identity data-quality audit of the built series files.

Reads ``series/*.sailscoring`` and reports the issues that fragment or muddle a
sailor's cross-series identity once imported into the app (sailscoring #218):

  1. blank names            -- competitor rows with no name at all
  2. mojibake names         -- UTF-8 read as Latin-1 ("AurÃ¨le" for "Aurèle")
  3. single-token names     -- first-name-only or run-together ("ThomasOLeary")
  4. sail-loan candidates   -- a one-off name sandwiched inside another sailor's
                               continuous run on the same hull: often a typo or
                               nickname split (dan/daniel, curi/cure), sometimes
                               a genuine sibling hand-down (leah/luke) -- always
                               human-adjudicated.

These are all *source* issues (confirmed present in the built files here), so the
fixes belong in this repo, before re-import. This is a stopgap to capture the
ad-hoc audits; the production, DB-side, cross-class version lives with
``reconcile-identities`` in the app (sailscoring #218).

Read-only. Plain stdlib, deterministic output.

    python3 audit.py            # write IDENTITY-AUDIT.md and print a summary
    python3 audit.py --print    # print the full report to stdout, write nothing
"""
import glob
import json
import re
import sys
import unicodedata
from collections import defaultdict

REPORT = 'IDENTITY-AUDIT.md'


def repair_mojibake(name):
    """Best-effort un-mangle of UTF-8-as-Latin-1 ("JosÃ©phine" -> "Joséphine").
    Returns the original if it doesn't cleanly round-trip."""
    try:
        fixed = name.encode('latin-1').decode('utf-8')
        return fixed if fixed != name else name
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def fold(name):
    """Canonical form for "same sailor" grouping: repair mojibake, strip
    diacritics, lowercase, collapse whitespace."""
    s = repair_mojibake(name)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(s.lower().split())


def norm_sail(sail):
    return re.sub(r'[^A-Z0-9]', '', (sail or '').upper())


def load_rows():
    """Every competitor across the built series, with its event + date."""
    rows = []
    for path in sorted(glob.glob('series/*.sailscoring')):
        data = json.load(open(path, encoding='utf-8'))
        s = data.get('series', {})
        name = s.get('name', path)
        date = s.get('startDate', '')
        for c in data.get('competitors', []):
            rows.append({
                'name': c.get('name') or '',
                'sail': c.get('sailNumber') or '',
                'club': c.get('club') or '',
                'age': c.get('age'),
                'series': name,
                'date': date,
            })
    return rows


def audit_blanks(rows):
    out = [r for r in rows if not r['name'].strip()]
    out.sort(key=lambda r: (r['date'], r['sail']))
    return out


def audit_mojibake(rows):
    seen = {}
    for r in rows:
        n = r['name']
        if 'Ã' in n or 'Â' in n:
            seen.setdefault(n, repair_mojibake(n))
    return sorted(seen.items())


def audit_single_token(rows):
    names = {r['name'].strip() for r in rows
             if r['name'].strip() and ' ' not in r['name'].strip()}
    return sorted(names)


def audit_sail_loans(rows):
    """A name appearing exactly once on a hull, with its event date strictly
    inside the date range of another name that used the same hull >= 3 times."""
    by_sail = defaultdict(list)
    for r in rows:
        sail = norm_sail(r['sail'])
        if sail:
            by_sail[sail].append(r)

    flags = []
    for sail, rs in by_sail.items():
        by_name = defaultdict(list)
        for r in rs:
            key = fold(r['name'])
            if key:
                by_name[key].append(r)
        if len(by_name) < 2:
            continue
        spans = {
            name: {
                'rows': rr,
                'min': min(x['date'] for x in rr),
                'max': max(x['date'] for x in rr),
            }
            for name, rr in by_name.items()
        }
        for one, info in spans.items():
            if len(info['rows']) != 1:
                continue
            d = info['rows'][0]['date']
            for other, oinfo in spans.items():
                if other is info or other == one:
                    continue
                if len(oinfo['rows']) >= 3 and oinfo['min'] < d < oinfo['max']:
                    flags.append({
                        'sail': sail,
                        'one': info['rows'][0]['name'],
                        'one_date': d,
                        'cont': oinfo['rows'][0]['name'],
                        'cont_n': len(oinfo['rows']),
                        'cont_from': oinfo['min'][:4],
                        'cont_to': oinfo['max'][:4],
                    })
                    break
    flags.sort(key=lambda f: (f['sail'], f['one_date']))
    return flags


def render(rows):
    blanks = audit_blanks(rows)
    moji = audit_mojibake(rows)
    singles = audit_single_token(rows)
    loans = audit_sail_loans(rows)

    L = []
    L.append('# Competitor identity data-quality audit')
    L.append('')
    L.append('Generated by `python3 audit.py` over the built `series/*.sailscoring`.')
    L.append('These are *source* issues that fragment or muddle a sailor\'s')
    L.append('cross-series identity in the app (sailscoring #218); fix them here and')
    L.append('re-import. Human-adjudicated — none of these are applied automatically.')
    L.append('')
    L.append('## Summary')
    L.append('')
    L.append(f'- {len(rows)} competitor rows across {len(set(r["series"] for r in rows))} series')
    L.append(f'- **{len(blanks)}** blank names')
    L.append(f'- **{len(moji)}** distinct mojibake spellings')
    L.append(f'- **{len(singles)}** single-token names')
    L.append(f'- **{len(loans)}** sail-loan candidates')
    L.append('')

    L.append('## Blank names')
    L.append('')
    L.append('No name on the row — can\'t anchor a competitor. Recover from the')
    L.append('source page or exclude.')
    L.append('')
    if blanks:
        L.append('| Date | Sail | Series |')
        L.append('|------|------|--------|')
        for r in blanks:
            L.append(f'| {r["date"]} | {r["sail"]} | {r["series"]} |')
    else:
        L.append('_None._')
    L.append('')

    L.append('## Mojibake spellings')
    L.append('')
    L.append('UTF-8 decoded as Latin-1 at scrape time. The repair column is a')
    L.append('best-effort re-decode — verify before applying.')
    L.append('')
    if moji:
        L.append('| As stored | Likely correct |')
        L.append('|-----------|----------------|')
        for raw, fixed in moji:
            L.append(f'| `{raw}` | {fixed} |')
    else:
        L.append('_None._')
    L.append('')

    L.append('## Single-token names')
    L.append('')
    L.append('First-name-only or run-together full names — they can\'t be split')
    L.append('into given/surname, so they never match across series.')
    L.append('')
    if singles:
        L.append('| Name |')
        L.append('|------|')
        for n in singles:
            L.append(f'| {n} |')
    else:
        L.append('_None._')
    L.append('')

    L.append('## Sail-loan candidates')
    L.append('')
    L.append('A name used a hull **once**, sandwiched inside another sailor\'s')
    L.append('continuous run on it. Often the same sailor (typo/nickname) the')
    L.append('matcher split; sometimes a genuine sibling hand-down. Review each.')
    L.append('')
    if loans:
        L.append('| Sail | One-off (date) | Continuous user (count, years) |')
        L.append('|------|----------------|--------------------------------|')
        for f in loans:
            L.append(
                f'| {f["sail"]} | {f["one"]} ({f["one_date"]}) '
                f'| {f["cont"]} (×{f["cont_n"]}, {f["cont_from"]}–{f["cont_to"]}) |'
            )
    else:
        L.append('_None._')
    L.append('')
    return '\n'.join(L)


def main(argv):
    rows = load_rows()
    report = render(rows)
    if '--print' in argv:
        print(report)
        return 0
    with open(REPORT, 'w', encoding='utf-8') as fh:
        fh.write(report + '\n')
    # Print the summary block (first lines up to the first blank after Summary).
    for line in report.splitlines():
        if line.startswith('## ') and not line.startswith('## Summary'):
            break
        print(line)
    print(f'\nWrote {REPORT}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
