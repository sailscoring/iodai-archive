#!/usr/bin/env python3
"""Transcribe the 2021 draft ranking PDFs (issue #7).

The only published 2021 rankings are print-to-PDF captures of the scorer's
*local* Sailwave preview (the print footer points at C:\\...\\Temp\\blw*.htm)
with the text vector-outlined - no text layer, nothing uploaded anywhere
else. So: render at 200dpi (pdftoppm), OCR (rapidocr), reconstruct the
table from box coordinates, and verify every row arithmetically - the
sheet is 'Sailed: 6, Discards: 3, To count: 3', so Nett must equal the sum
of the three unparenthesised event cells. Rows that fail any check are
listed for human (visual) transcription; the emitted transcription JSON is
the reviewed, committed artifact the ingest consumes.

Run from the repo root with the OCR venv's python:
    <venv>/bin/python sources/2021/ranking/transcribe.py <boxes.json>
"""
import json
import re
import sys

# Column anchors from the header band (200dpi, consistent across pages).
COLS = [
    ('rank', 85, 160), ('fleet', 160, 220), ('division', 220, 300),
    ('rating', 300, 375), ('sail', 375, 435), ('name', 435, 565),
    ('gender', 565, 645), ('club', 645, 745), ('nat', 745, 800),
    ('age', 800, 895), ('ev1', 895, 985), ('ev2', 985, 1068),
    ('ev3', 1068, 1150), ('ev4', 1150, 1235), ('ev5', 1235, 1320),
    ('ev6', 1320, 1405), ('total', 1405, 1493), ('nett', 1493, 1600),
]
EVENTS = ['ev1', 'ev2', 'ev3', 'ev4', 'ev5', 'ev6']
RANK_RE = re.compile(r'^(\d{1,3})(st|nd|rd|th)?$')
NUM_RE = re.compile(r'[\d,]+\.?\d*')


def col_of(x):
    for name, x0, x1 in COLS:
        if x0 <= x < x1:
            return name
    return None


def bands(boxes, pitch=14):
    out, cur = [], []
    for b in sorted(boxes, key=lambda b: b['y']):
        if cur and b['y'] - cur[-1]['y'] > pitch:
            out.append(cur)
            cur = []
        cur.append(b)
    if cur:
        out.append(cur)
    return out


def clean_number(text):
    """OCR numerics: '3,012.0' -> 3012.0; '(3.000.0' -> 3000.0 (the comma /
    second dot is a misread thousands separator)."""
    t = text.replace(',', '').replace(' ', '')
    parts = t.split('.')
    if len(parts) > 2:
        t = ''.join(parts[:-1]) + '.' + parts[-1]
    try:
        return float(t)
    except ValueError:
        return None


def reconstruct(pages):
    rows = []
    problems = []
    for page in pages:
        boxes = [b for b in page if b['y'] > 60 and b['y'] < 2270]
        for band in bands(boxes):
            first = sorted(band, key=lambda b: b['x0'])[0]
            m = RANK_RE.match(first['text'].strip())
            if m and first['x0'] < 160:
                rows.append({'cells': {}, 'rank': int(m.group(1)), 'minconf': 1.0})
            if not rows:
                continue
            row = rows[-1]
            for b in band:
                c = col_of(b['x0'])
                if c is None:
                    continue
                row['cells'].setdefault(c, []).append(b['text'])
                row['minconf'] = min(row['minconf'], b['conf'])
    out = []
    for row in rows:
        cells = {k: ' '.join(v).strip() for k, v in row['cells'].items()}
        # Sail digits fused onto the name ('1646Caoilinn ...').
        name = cells.get('name', '')
        sail = cells.get('sail', '')
        fused = re.match(r'^(\d{2,5})\s*(.*)$', name)
        if fused:
            sail = (sail + fused.group(1)) if sail.isdigit() is False else fused.group(1)
            name = fused.group(2)
        if sail and not cells.get('sail'):
            cells['sail'] = sail
        events = [cells.get(e, '') for e in EVENTS]
        nett = clean_number(cells.get('nett', ''))
        counted = [
            clean_number(e) for e in events if e and not e.startswith('(')
        ]
        check = (
            nett is not None
            and len([c for c in counted if c is not None]) >= 1
            and abs(sum(c for c in counted if c is not None) - nett) < 0.01
        )
        out.append({
            'rank': row['rank'],
            'name': re.sub(r'\s+', ' ', name).strip(),
            'sail': cells.get('sail', ''),
            'fleetcol': cells.get('fleet', ''),
            'division': cells.get('division', ''),
            'gender': cells.get('gender', ''),
            'club': cells.get('club', ''),
            'nat': cells.get('nat', ''),
            'age': cells.get('age', ''),
            'events': events,
            'total': cells.get('total', ''),
            'nett': cells.get('nett', ''),
            'nettOk': check,
            'minconf': round(row['minconf'], 3),
        })
    return out


def main():
    boxes = json.load(open(sys.argv[1]))
    for fleet, prefix in [('senior', 'sen-'), ('junior', 'jun-')]:
        pages = [
            boxes[k]
            for k in sorted(boxes, key=lambda k: int(k.split('-')[1].split('.')[0]))
            if k.startswith(prefix)
        ]
        rows = reconstruct(pages)
        seq = all(rows[i]['rank'] == i + 1 for i in range(len(rows)))
        bad = [r for r in rows if not r['nettOk']]
        print(f"{fleet}: {len(rows)} rows, rank-sequence {'ok' if seq else 'BROKEN'}, "
              f"{len(bad)} rows fail the nett check")
        for r in bad:
            print(f"  rank {r['rank']:>3} {r['name']!r} events={r['events']} nett={r['nett']!r}")
        json.dump(rows, open(f'raw-transcription-{fleet}.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
