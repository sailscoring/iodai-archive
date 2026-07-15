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

Stdlib only, like the rest of the pipeline.
"""

import json
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
    """Casefold, strip accents, collapse whitespace — the same tolerance the
    identity work needs for e.g. 'Fergus macnamara'."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.casefold().split())


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


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "parse":
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
