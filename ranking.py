#!/usr/bin/env python3
"""Season-ranking pages (issue #7): parse and compare.

IODAI publish the national ranking as a Sailwave series — one "race" column
per event (Leinsters, Ulsters, Connaghts, Nationals, Munsters), five sailed,
two discards, three to count. Score cells carry the event place, with
parentheses for discards and codes for non-sailed events (DNC) and
committee-average redress (RDGa).

Commands:
    python3 ranking.py parse <capture.htm>            # structured JSON to stdout
    python3 ranking.py diff <old.htm> <new.htm>       # what changed between revisions
    python3 ranking.py adjustments <capture.htm>      # the rows needing app-side adjustments
    python3 ranking.py emit-config <capture.htm> <series-map.json> <identities.json>
        # the app RankingConfig replicating this sheet (buckets, IRL
        # place recomputation, fleet filter, adjustments)
    python3 ranking.py compare <capture.htm> <ladder.json> [aliases.json]
        # diff the app's computed ladder (`sailscoring ranking standings
        # <id> --json`) against the sheet: ranked set, order, and nett;
        # aliases.json maps sheet helm-names to identity labels

    python3 ranking.py emit-ingest
        # normalize each season's authoritative captures (per
        # sources/<year>/ranking/ingest.json) into as-published/rankings/
        # ingest documents, resolving identities via the manifest(s)
    python3 ranking.py draft-identities
        # C(...) drafts for names no identity resolves - the ranking-only
        # sailors - to curate into ranking_identities.py

Stdlib only, like the rest of the pipeline.
"""

import json
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser


class _TableParser(HTMLParser):
    """Collect the summary table's cells and the page's title/caption lines."""

    def __init__(self):
        super().__init__()
        self.titles = []
        self.captions = []
        self.rows = []
        self._row = None
        self._cell = None
        self._cell_class = ""
        self._text_target = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = attrs.get("class", "")
        if tag == "h3":
            self._text_target = ("title", [])
        elif tag == "div" and "summarycaption" in cls:
            self._text_target = ("caption", [])
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []
            self._cell_class = cls

    def handle_endtag(self, tag):
        if tag == "h3" and self._text_target:
            self.titles.append("".join(self._text_target[1]).strip())
            self._text_target = None
        elif tag == "div" and self._text_target:
            self.captions.append("".join(self._text_target[1]).strip())
            self._text_target = None
        elif tag in ("td", "th") and self._cell is not None:
            self._row.append(
                ("".join(self._cell).strip(), self._cell_class)
            )
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)
        elif self._text_target:
            self._text_target[1].append(data)


SCORE_RE = re.compile(r"^\((?P<dpts>[\d.]+)(?:\s+(?P<dcode>\w+))?\)$|^(?P<pts>[\d.]+)(?:\s+(?P<code>\w+))?$")


def parse_score(text):
    """'1.0' / '(2.0)' / '1.5 RDGa' / '(45.0 DNC)' -> structured score."""
    m = SCORE_RE.match(text)
    if not m:
        raise ValueError(f"unparseable score cell: {text!r}")
    discarded = m.group("dpts") is not None
    return {
        "points": float(m.group("dpts") or m.group("pts")),
        "code": m.group("dcode") or m.group("code"),
        "discarded": discarded,
    }


def parse_file(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        p = _TableParser()
        p.feed(f.read())

    header = [c[0] for c in p.rows[0]]
    fixed = ["Rank", "Fleet", "Division", "Nat", "Sail", "Helm", "Club", "Gender", "Age"]
    if header[: len(fixed)] != fixed or header[-2:] != ["Total", "Nett"]:
        raise ValueError(f"{path}: unexpected column layout {header}")
    events = header[len(fixed) : -2]

    sailors = []
    for row in p.rows[1:]:
        cells = [c[0] for c in row]
        if len(cells) != len(header):
            raise ValueError(f"{path}: ragged row {cells}")
        scores = {ev: parse_score(cells[len(fixed) + i]) for i, ev in enumerate(events)}
        sailors.append(
            {
                "rank": int(re.sub(r"\D", "", cells[0])),
                "nat": cells[3],
                "sail": cells[4],
                "helm": cells[5],
                "club": cells[6],
                "gender": cells[7],
                "age": cells[8],
                "scores": scores,
                "total": float(cells[-2]),
                "nett": float(cells[-1]),
            }
        )

    return {
        "file": path,
        "provisional_as_of": next(
            (t for t in p.titles if "provisional" in t.lower()), None
        ),
        "division": next((t for t in p.titles if "Division" in t), None),
        "caption": p.captions[0] if p.captions else None,
        "events": events,
        "sailors": sailors,
    }


def cmd_parse(path):
    print(json.dumps(parse_file(path), indent=2))


def cmd_adjustments(path):
    """Rows whose score is a code other than DNC: the committee-entered
    places that must become app-side adjustments (asterisk + note)."""
    data = parse_file(path)
    out = []
    for s in data["sailors"]:
        for ev, sc in s["scores"].items():
            if sc["code"] and sc["code"] != "DNC":
                out.append(
                    {
                        "helm": s["helm"],
                        "sail": s["sail"],
                        "event": ev,
                        "place": sc["points"],
                        "code": sc["code"],
                        "discarded": sc["discarded"],
                    }
                )
    print(json.dumps(out, indent=2))


def cmd_diff(old_path, new_path):
    old, new = parse_file(old_path), parse_file(new_path)
    print(f"old: {old['provisional_as_of']}  ({len(old['sailors'])} sailors)")
    print(f"new: {new['provisional_as_of']}  ({len(new['sailors'])} sailors)")
    if old["caption"] != new["caption"]:
        print(f"caption: {old['caption']!r} -> {new['caption']!r}")

    def by_sail(data):
        return {s["sail"]: s for s in data["sailors"]}

    o, n = by_sail(old), by_sail(new)
    for sail in sorted(o.keys() | n.keys(), key=lambda s: (s not in o, s not in n, s)):
        if sail not in n:
            print(f"- removed: {sail} {o[sail]['helm']} (was rank {o[sail]['rank']})")
        elif sail not in o:
            print(f"- added:   {sail} {n[sail]['helm']} (rank {n[sail]['rank']})")
        else:
            a, b = o[sail], n[sail]
            changes = []
            if a["rank"] != b["rank"]:
                changes.append(f"rank {a['rank']}->{b['rank']}")
            if a["nett"] != b["nett"]:
                changes.append(f"nett {a['nett']}->{b['nett']}")
            for ev in old["events"]:
                if a["scores"].get(ev) != b["scores"].get(ev):
                    changes.append(
                        f"{ev} {a['scores'][ev]!r}->{b['scores'][ev]!r}"
                    )
            if changes:
                print(f"- {sail} {a['helm']}: " + "; ".join(changes))


def norm_name(name):
    """Casefold, strip accents, then keep letters and digits only — the
    published record spells the same sailor 'Jack McDowell', 'JACK
    MCDOWELL', and 'Jack MC DOWELL', splits O'Shea into 'O Shea', appends
    footnote asterisks, and hides soft hyphens in names, so comparison
    ignores spacing and punctuation entirely. Uniqueness is still enforced
    at resolution, so a (vanishing) letters-only collision degrades to
    unresolved, never to a wrong link."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s.casefold() if c.isalnum())


def qualified(sailor, events):
    """The rule (Team Selection Policy para 2): sailed the Nationals and at
    least two regionals. A committee redress (RDGa) counts as sailed; a DNC
    doesn't."""
    sailed = {ev for ev, sc in sailor["scores"].items() if sc["code"] != "DNC"}
    regionals = [ev for ev in events if ev != "Nationals"]
    return "Nationals" in sailed and len(sailed & set(regionals)) >= 2


def cmd_emit_config(sheet_path, series_map_path, identities_path):
    sheet = parse_file(sheet_path)
    series_map = json.load(open(series_map_path))
    for ev in sheet["events"]:
        if ev not in series_map:
            raise SystemExit(f"series map is missing {ev!r}")
    ids = json.load(open(identities_path))
    identities = ids["items"] if isinstance(ids, dict) else ids
    fleet = (sheet["division"] or "").replace("Division", "").strip()
    if fleet not in ("Senior", "Junior"):
        raise SystemExit(f"can't derive fleet from {sheet['division']!r}")

    known_series = set(series_map.values())

    def resolve_identity(helm, sail):
        # Sail number within one of this ranking's series is the precise key;
        # a normalized-name match is the fallback.
        by_sail = [
            i
            for i in identities
            if any(
                e["seriesId"] in known_series and e["sailNumber"] == sail
                for e in i.get("entries", [])
            )
        ]
        if len(by_sail) == 1:
            return by_sail[0]["id"]
        by_name = [i for i in identities if norm_name(i["label"]) == norm_name(helm)]
        if len(by_name) == 1:
            return by_name[0]["id"]
        raise SystemExit(
            f"can't resolve identity for {helm!r} ({sail}): "
            f"{len(by_sail)} sail matches, {len(by_name)} name matches"
        )

    regionals = [ev for ev in sheet["events"] if ev != "Nationals"]
    adjustments = []
    for s in sheet["sailors"]:
        for ev, sc in s["scores"].items():
            if sc["code"] and sc["code"] != "DNC":
                adjustments.append(
                    {
                        "identityId": resolve_identity(s["helm"], s["sail"]),
                        "seriesId": series_map[ev],
                        "place": sc["points"],
                        "note": f"{sc['code']} on the published ranking — {ev} missed on representational duty",
                    }
                )

    config = {
        "buckets": [
            {
                "id": "national",
                "name": "National",
                "seriesIds": [series_map["Nationals"]],
                "countBest": 1,
                "requiredMin": 1,
            },
            {
                "id": "regional",
                "name": "Regional",
                "seriesIds": [series_map[ev] for ev in regionals],
                "countBest": 2,
                "requiredMin": 2,
            },
        ],
        "nationality": "IRL",
        "recomputePlaces": True,
        "fleet": fleet,
        **({"adjustments": adjustments} if adjustments else {}),
    }
    print(json.dumps(config, indent=2))


def cmd_compare(sheet_path, ladder_path, aliases_path=None):
    sheet = parse_file(sheet_path)
    ladder = json.load(open(ladder_path))
    rows = ladder["result"]["rows"]
    ineligible = ladder["result"]["ineligible"]

    aliases = {}
    if aliases_path:
        aliases = {
            norm_name(k): norm_name(v)
            for k, v in json.load(open(aliases_path)).items()
            if not k.startswith("_")
        }

    def sheet_name(helm):
        n = norm_name(helm)
        return aliases.get(n, n)

    by_name = {sheet_name(s["helm"]): s for s in sheet["sailors"]}
    problems = []

    # 1. Every app row matches a sheet sailor, and vice versa for the
    #    qualified set.
    app_matched = {}
    for row in rows:
        s = by_name.get(norm_name(row["label"]))
        if not s:
            problems.append(f"app ranks {row['label']!r} — not on the sheet")
        else:
            app_matched[row["identityId"]] = s
    expected_ranked = {
        sheet_name(s["helm"]) for s in sheet["sailors"] if qualified(s, sheet["events"])
    }
    app_ranked = {norm_name(r["label"]) for r in rows}
    for name in sorted(expected_ranked - app_ranked):
        problems.append(f"sheet-qualified {by_name[name]['helm']!r} missing from app ladder")
    for name in sorted(app_ranked - expected_ranked):
        problems.append(f"app ranks {by_name.get(name, {}).get('helm', name)!r} — not sheet-qualified")

    # 2. Nett equality: for qualified sailors the sheet's counted scores are
    #    exactly the app's (Nationals + best two regionals), so nett == total.
    for row in rows:
        s = app_matched.get(row["identityId"])
        if s and abs(row["total"] - s["nett"]) > 1e-9:
            problems.append(
                f"{row['label']}: app total {row['total']} != sheet nett {s['nett']}"
            )

    # 3. Order: walking the app ladder, sheet ranks must ascend — except
    #    within an app tie (equal totals), where the sheet breaks the tie
    #    (RRS A8) and either order is fine.
    prev_sheet_rank, prev_total = 0, None
    for row in rows:
        s = app_matched.get(row["identityId"])
        if not s:
            continue
        if row["total"] != prev_total and s["rank"] < prev_sheet_rank:
            problems.append(
                f"order: {row['label']} (sheet rank {s['rank']}) listed after sheet rank {prev_sheet_rank}"
            )
        prev_sheet_rank = max(prev_sheet_rank, s["rank"])
        prev_total = row["total"]

    ineligible_names = [i["label"] for i in ineligible]
    print(f"sheet: {len(sheet['sailors'])} sailors, {len(expected_ranked)} qualified")
    print(f"app:   {len(rows)} ranked, {len(ineligible_names)} not yet ranked")
    if ladder.get("unmatchedCount"):
        print(f"app:   {ladder['unmatchedCount']} unmatched entries (identity gaps)")
    if ladder.get("unflaggedCount"):
        print(f"app:   {ladder['unflaggedCount']} sailors with no nationality")
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("\nPASS — ranked set, order, and nett all match the sheet.")


# ─── As-published ranking ingest (#7 / app #309) ────────────────────────────

EVENT_NAMES = {
    # IODAI have spelled Connacht at least four ways across the record.
    'connaughts', 'connachts', 'connaghts', 'connauchts',
    'leinsters', 'ulsters', 'munsters', 'nationals',
}
NAME_HEADERS = {'name', 'helm', 'helmname'}


def slug_key(label):
    k = re.sub(r'[^a-z0-9]+', '-', label.casefold()).strip('-')
    return k or 'col'


def parse_table_general(path):
    """Normalise any of the HTML-era ranking tables (2014, 2018-2019,
    2022-2025): a header row starting 'Rank', a name column, event columns
    named after the five championships, everything else lead/summary."""
    with open(path, encoding='utf-8', errors='replace') as f:
        p = _TableParser()
        p.feed(f.read())
    header_i = next(
        i for i, row in enumerate(p.rows) if row and row[0][0].strip() == 'Rank'
    )
    header = [c[0].strip().lstrip('﻿') for c in p.rows[header_i]]
    event_idx = [i for i, h in enumerate(header) if h.casefold() in EVENT_NAMES]
    name_idx = next(
        i for i, h in enumerate(header) if h.casefold() in NAME_HEADERS
    )
    first_event = min(event_idx)
    lead_idx = [
        i for i in range(1, first_event) if i != name_idx and i not in event_idx
    ]
    summary_idx = [
        i for i in range(max(event_idx) + 1, len(header)) if i != name_idx
    ]

    rows = []
    for raw in p.rows[header_i + 1:]:
        cells = [c[0].strip() for c in raw]
        if len(cells) != len(header) or not cells[0]:
            continue
        digits = re.sub(r'\D', '', cells[0])
        if not digits:
            continue
        rows.append({
            'rankLabel': cells[0],
            'rank': int(digits),
            'name': re.sub(r'\s+', ' ', cells[name_idx]).strip(),
            'leadCells': [cells[i] for i in lead_idx],
            'eventCells': [
                {'text': cells[i], 'discard': cells[i].startswith('(')}
                for i in event_idx
            ],
            'summaryCells': [cells[i] for i in summary_idx],
        })
    return {
        'leadColumns': [
            {'key': slug_key(header[i]), 'label': header[i]} for i in lead_idx
        ],
        'leadLabels': [header[i] for i in lead_idx],
        'eventHeaders': [{'label': header[i]} for i in event_idx],
        'summaryColumns': [
            {'key': slug_key(header[i]), 'label': header[i]} for i in summary_idx
        ],
        'rows': rows,
    }


def parse_pdf_ranking(path):
    """Normalise the PDF-era finals (2015-2017): `pdftotext -layout` text
    with a 'Rank Helm/Hem Club Age M/F <events> Points' header. The 2015
    files carry font artifacts - '%' or tab+CR+NBSP runs printed between
    words - so they parse token-wise after normalisation; the clean years
    slice names/clubs on header column positions, recomputed per page
    (later pages shift). Values like '3000' (DNC-equivalent) and averaged
    fractions are kept verbatim."""
    import subprocess
    raw = subprocess.run(
        ['pdftotext', '-layout', path, '-'], capture_output=True, text=True,
    ).stdout
    tokens_mode = '\t' in raw or '%' in raw
    txt = (
        raw.replace('\r', ' ')
        .replace('\u00a0', ' ')
        .replace('\t', ' ')
        .replace('%', ' ')
    )
    lines = txt.split('\n')

    def is_header(l):
        return (
            l.strip().startswith('Rank')
            and sum(1 for t in l.split() if t.casefold() in EVENT_NAMES) >= 3
        )

    first_header = next(l for l in lines if is_header(l))
    events = [t for t in first_header.split() if t.casefold() in EVENT_NAMES]
    tail_len = len(events) + 1  # events + Points

    rows = []
    for line in lines:
        if is_header(line):
            continue
        toks = line.split()
        if not toks or not re.fullmatch(r'\d{1,3}', toks[0]):
            continue
        if len(toks) < tail_len + 2:
            continue
        tail = toks[-tail_len:]
        rest = toks[1:-tail_len]
        mf = rest.pop() if rest and rest[-1] in ('M', 'F') else ''
        age = rest.pop() if rest and re.fullmatch(r'\d{1,2}', rest[-1]) else ''
        if tokens_mode:
            club = rest.pop() if rest else ''
            name = ' '.join(rest)
        else:
            # Columns are >=2-space separated whatever a page's offsets
            # (later pages carry no header and shift), so split the row on
            # runs of spaces: name, then club; the numeric tail came from
            # tokens above.
            body = re.match(r'\s*\d{1,3}\s+(\S.*)$', line).group(1)
            fields = re.split(r'\s{2,}', body.strip())
            name = fields[0]
            club = fields[1] if len(fields) > 1 else ''
            # A blank club cell collapses the split onto the age/sex chunk.
            if club == f'{age} {mf}'.strip() or club == age:
                club = ''
            # A long name (or long club) can squeeze the name-club gap to a
            # single space; peel the age/sex suffix if it rode along, then
            # peel club-ish tokens off the name's tail.
            def clubish(tok):
                return tok in ('&', 'Other') or (
                    re.fullmatch(r"[A-Z][A-Za-z&/]{1,7}", tok) is not None
                    and sum(c.isupper() for c in tok) >= len(tok) - 2
                )

            suffix = f'{age} {mf}'.strip()
            if suffix and name.endswith(' ' + suffix):
                name = name[: -len(suffix)].strip()
                club = ''
            if not club:
                toks2 = name.split()
                clubtoks = []
                while len(toks2) > 1 and clubish(toks2[-1]):
                    clubtoks.insert(0, toks2.pop())
                name = ' '.join(toks2)
                club = ' '.join(clubtoks)
        name = re.sub(r'\s+', ' ', name).strip()
        if not name:
            continue
        rows.append({
            'rankLabel': toks[0],
            'rank': int(toks[0]),
            'name': name,
            'leadCells': [club, age, mf],
            'eventCells': [{'text': t, 'discard': False} for t in tail[:-1]],
            'summaryCells': [tail[-1]],
        })
    # Some files fragment each visual row across physical lines (text
    # objects at jittered y-coordinates). When line-wise parsing doesn't
    # produce a clean 1..n rank sequence, reassemble from the token stream:
    # a row closes when it already carries its numeric tail and the next
    # token is the next expected rank.
    if not rows or not all(rows[i]['rank'] == i + 1 for i in range(len(rows))):
        rows = _rows_from_token_stream(lines, is_header, tail_len)

    return {
        'leadColumns': [
            {'key': 'club', 'label': 'Club'},
            {'key': 'age', 'label': 'Age'},
            {'key': 'mf', 'label': 'M/F'},
        ],
        'leadLabels': ['Club', 'Age', 'M/F'],
        'eventHeaders': [{'label': e} for e in events],
        'summaryColumns': [{'key': 'points', 'label': 'Points'}],
        'rows': rows,
    }


def _parse_pdf_row_tokens(toks, tail_len):
    tail = toks[-tail_len:]
    rest = toks[1:-tail_len]
    mf = rest.pop() if rest and rest[-1] in ('M', 'F') else ''
    age = rest.pop() if rest and re.fullmatch(r'\d{1,2}', rest[-1]) else ''
    club = rest.pop() if rest else ''
    name = re.sub(r'\s+', ' ', ' '.join(rest)).strip()
    if not name:
        return None
    return {
        'rankLabel': toks[0],
        'rank': int(toks[0]),
        'name': name,
        'leadCells': [club, age, mf],
        'eventCells': [{'text': t, 'discard': False} for t in tail[:-1]],
        'summaryCells': [tail[-1]],
    }


def _rows_from_token_stream(lines, is_header, tail_len):
    NUM = re.compile(r'\d+(?:\.\d+)?')
    toks = []
    seen_header = False
    for line in lines:
        if is_header(line):
            seen_header = True
            continue
        if not seen_header:
            continue
        # Page-break furniture: repeated titles and print footers
        # ("9/6/15 9:24 AM", "1 of 2", "2015 Junior Final").
        stripped = line.strip().strip('\f')
        if re.search(r'Fleet|Ranking|Provisional|Final|\b[AP]M\b|\bof \d+\b|\d+/\d+/\d+', stripped):
            continue
        toks.extend(stripped.split())

    def complete(cur):
        return len(cur) > tail_len and all(
            NUM.fullmatch(t) for t in cur[-tail_len:]
        )

    rows = []
    current = []
    expected = 1
    for tok in toks:
        if current and complete(current):
            # Between rows: discard print furniture the line filter missed
            # (ultra-fragmented footers) until the next rank arrives.
            if tok == str(expected + 1):
                row = _parse_pdf_row_tokens(current, tail_len)
                if row:
                    rows.append(row)
                expected += 1
                current = [tok]
            continue
        if not current:
            if tok == str(expected):
                current = [tok]
        else:
            current.append(tok)
    if current and complete(current):
        row = _parse_pdf_row_tokens(current, tail_len)
        if row:
            rows.append(row)
    return rows


def load_all_identities():
    """The curated golden records: manifest.py plus (when present) the
    ranking-only entries in ranking_identities.py."""
    import manifest as manifest_mod
    entries = list(manifest_mod.IDENTITIES)
    try:
        import ranking_identities
        entries += list(ranking_identities.IDENTITIES)
    except ImportError:
        pass
    return entries


def _name_words(name):
    s2 = unicodedata.normalize("NFKD", name)
    s2 = "".join(c for c in s2 if not unicodedata.combining(c))
    return set(re.findall(r"[a-z]+", s2.casefold()))


def build_resolver(season, aliases):
    """name/sail -> identity slug for one season. Resolution order: alias
    (exact printed name -> curated label), sail number within the season's
    series rows (guarded by a shared name token), then normalized-name
    match (unique matches only)."""
    entries = load_all_identities()
    by_sail = {}
    for e in entries:
        for series_slug, sail in getattr(e, 'rows', []):
            if f'-{season}-' in series_slug or series_slug.endswith(str(season)):
                by_sail.setdefault(str(sail), set()).add(e.slug)
    by_name = {}
    for e in entries:
        by_name.setdefault(norm_name(e.name), set()).add(e.slug)
    alias_map = {
        norm_name(k): v for k, v in aliases.items() if not k.startswith('_')
    }

    def resolve(name, sail):
        n = norm_name(name)
        if n in alias_map:
            slugs = by_name.get(norm_name(alias_map[n]), set())
            if len(slugs) == 1:
                return next(iter(slugs))
        if sail:
            slugs = by_sail.get(str(sail), set())
            if len(slugs) == 1:
                slug = next(iter(slugs))
                owner = next(e for e in entries if e.slug == slug)
                if _name_words(owner.name) & _name_words(name):
                    return slug
        slugs = by_name.get(n, set())
        if len(slugs) == 1:
            return next(iter(slugs))
        return None

    return resolve


def season_configs():
    import glob as _glob
    out = []
    for path in sorted(_glob.glob('sources/*/ranking/ingest.json')):
        cfg = json.load(open(path))
        cfg['_dir'] = os.path.dirname(path)
        out.append(cfg)
    return out


def emit_doc(cfg, fleet_cfg, resolve):
    import engine
    season = cfg['season']
    fleet = fleet_cfg.get('fleet')
    key = f"iodai-ranking-{season}" + (f"-{fleet.casefold()}" if fleet else '')
    capture_path = os.path.join(cfg['_dir'], fleet_cfg['capture'])
    if fleet_cfg.get('format') == 'pdf':
        table = parse_pdf_ranking(capture_path)
    else:
        table = parse_table_general(capture_path)
    sail_i = next(
        (i for i, lbl in enumerate(table['leadLabels'])
         if lbl.casefold().startswith('sail')),
        None,
    )
    unresolved = []
    rows = []
    for r in table['rows']:
        sail = r['leadCells'][sail_i] if sail_i is not None else None
        slug = resolve(r['name'], sail)
        if slug is None:
            unresolved.append((r['name'], sail))
        rows.append({
            'identity': slug,
            'rank': r['rank'],
            'rankLabel': r['rankLabel'],
            'name': r['name'],
            'leadCells': r['leadCells'],
            'eventCells': r['eventCells'],
            'summaryCells': r['summaryCells'],
        })
    doc = {
        'formatVersion': 1,
        'ranking': {
            'id': engine.det(f'{key}/ranking'),
            'name': (
                f"IODAI National Ranking {season}"
                + (f" — {fleet}" if fleet else '')
            ),
            'slug': (
                f"national-ranking-{season}"
                + (f"-{fleet.casefold()}" if fleet else '')
            ),
            'season': season,
            **({'fleetLabel': fleet} if fleet else {}),
            **({'ruleNote': cfg['ruleNote']} if cfg.get('ruleNote') else {}),
            'source': fleet_cfg.get('source', {}),
        },
        'table': {
            **(
                {'caption': fleet_cfg['caption']}
                if fleet_cfg.get('caption')
                else {}
            ),
            'leadColumns': table['leadColumns'],
            'eventHeaders': table['eventHeaders'],
            'summaryColumns': table['summaryColumns'],
            'rows': rows,
        },
    }
    return key, doc, unresolved


def cmd_emit_ingest(out_dir='as-published/rankings'):
    os.makedirs(out_dir, exist_ok=True)
    total_unresolved = []
    for cfg in season_configs():
        aliases_path = os.path.join(cfg['_dir'], 'aliases.json')
        aliases = (
            json.load(open(aliases_path)) if os.path.exists(aliases_path) else {}
        )
        resolve = build_resolver(cfg['season'], aliases)
        for fleet_cfg in cfg['fleets']:
            key, doc, unresolved = emit_doc(cfg, fleet_cfg, resolve)
            path = os.path.join(out_dir, f'{key}.json')
            json.dump(doc, open(path, 'w'), indent=1, ensure_ascii=False)
            linked = sum(1 for r in doc['table']['rows'] if r['identity'])
            print(
                f"{key}: {len(doc['table']['rows'])} rows, {linked} linked -> {path}"
            )
            for name, sail in unresolved:
                total_unresolved.append(
                    (cfg['season'], fleet_cfg.get('fleet'), name, sail)
                )
    if total_unresolved:
        print(
            f'\n{len(total_unresolved)} unresolved rows (curate via draft-identities):'
        )
        for season, fleet, name, sail in total_unresolved:
            print(
                f'  {season} {fleet or "-":<7} {name}'
                + (f' ({sail})' if sail else '')
            )
    return 0


def cmd_draft_identities():
    """Print C(...) drafts for every unresolved row — the ranking-only
    sailors — grouping the same normalized name across seasons."""
    from identity_manifest import mint_slug
    taken = {e.slug for e in load_all_identities()}
    groups = {}
    for cfg in season_configs():
        aliases_path = os.path.join(cfg['_dir'], 'aliases.json')
        aliases = (
            json.load(open(aliases_path)) if os.path.exists(aliases_path) else {}
        )
        resolve = build_resolver(cfg['season'], aliases)
        for fleet_cfg in cfg['fleets']:
            key, doc, unresolved = emit_doc(cfg, fleet_cfg, resolve)
            for name, sail in unresolved:
                g = groups.setdefault(
                    norm_name(name), {'name': name, 'rankings': []}
                )
                g['rankings'].append(key)
    for n, g in sorted(groups.items()):
        stable = '|'.join(sorted(set(g['rankings'])))
        slug = mint_slug(g['name'], stable, taken)
        rr = ', '.join(f'"{k}"' for k in sorted(set(g['rankings'])))
        print(f'    C(slug="{slug}", name="{g["name"]}",')
        print(f'      ranking_rows=[{rr}], rows=[]),')
    print(f'# {len(groups)} ranking-only sailors', file=sys.stderr)



def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "emit-ingest":
        sys.exit(cmd_emit_ingest(*sys.argv[2:3]))
    elif len(sys.argv) >= 2 and sys.argv[1] == "draft-identities":
        cmd_draft_identities()
    elif len(sys.argv) >= 3 and sys.argv[1] == "parse":
        cmd_parse(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "adjustments":
        cmd_adjustments(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "diff":
        cmd_diff(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 5 and sys.argv[1] == "emit-config":
        cmd_emit_config(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) >= 4 and sys.argv[1] == "compare":
        cmd_compare(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
