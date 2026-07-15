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

Stdlib only, like the rest of the pipeline.
"""

import json
import re
import sys
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


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "parse":
        cmd_parse(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "adjustments":
        cmd_adjustments(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "diff":
        cmd_diff(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
