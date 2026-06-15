#!/usr/bin/env python3
"""Bulk-onboard the generated .sailscoring files into the IODAI workspace.

Drives the `sailscoring` CLI (ADR-009) to import → publish → categorise →
archive every series in `series/`, one *event* at a time. An event's series
(Main Fleet's Senior+Junior, Regatta Racing, Regatta Coached — or the older
single Regatta) co-publish under one shared slug, so each year's championship
gets a single public page at `/p/{workspace}/{slug}` with per-fleet sub-pages.

The phases run via a single combined `sailscoring import` invocation per event,
which performs them in the required order (categorise is blocked once a series
is archived). Re-running is safe: import keys on file content (idempotent
replay), and publish/categorise/archive are set-operations.

Conventions (see README.md / the app's docs/cli.md):

  Slug    region    -> {year}-{connachts|leinsters|munsters|ulsters}
          nationals -> {year}-nationals
          sprint    -> {year}-sprint-series
          youth     -> {year}-youth-nationals
  Fleets are sub-paths under the slug — /senior, /junior, /regatta-racing,
  /regatta-coached, or just /regatta where there's a single regatta fleet.
  e.g. /p/iodai/2026-munsters/senior
  Category -> the year (e.g. "2025")

Usage:
  python3 onboard.py                 # dry-run, all years <= 2025 (newest first)
  python3 onboard.py --year 2025     # dry-run, just 2025 (the test run)
  python3 onboard.py --year 2025 --apply
  python3 onboard.py --apply         # the full historical load

Auth/target: the CLI uses the saved token from `sailscoring auth login` (or
SAILSCORING_TOKEN / SAILSCORING_BASE_URL). Workspace defaults to `iodai`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

SERIES_DIR = Path(__file__).resolve().parent / "series"

# Human label per region token, for the dry-run log only. The publish slug is
# just `{year}-{region}` (e.g. /p/iodai/2026-munsters), with fleets as
# sub-paths: /senior, /junior, /regatta-racing, /regatta-coached.
REGION_LABEL = {
    "connachts": "Connacht Championships",
    "leinsters": "Leinster Championships",
    "munsters": "Munster Championships",
    "ulsters": "Ulster Championships",
    "nationals": "National Championships",
}

RE_REGION = re.compile(
    r"^iodai-(connachts|leinsters|munsters|ulsters|nationals)-(\d{4})-(.+)\.sailscoring$"
)
RE_SPRINT = re.compile(r"^iodai-sprint-series-(\d{4})\.sailscoring$")
RE_YOUTH = re.compile(r"^irish-sailing-youth-nationals-(\d{4})-optimist\.sailscoring$")


@dataclass
class Event:
    """One event = one shared publish slug, co-publishing all its series."""

    year: int
    key: str  # stable display/sort key, e.g. "munsters", "sprint-series"
    label: str  # human label, e.g. "Munster Championships"
    slug: str  # publish slug, e.g. "2025-munster-championships"
    files: list[Path] = field(default_factory=list)


# Display order of events within a year.
EVENT_ORDER = {
    "leinsters": 0,
    "ulsters": 1,
    "connachts": 2,
    "munsters": 3,
    "nationals": 4,
    "sprint-series": 5,
    "youth-nationals": 6,
}


def classify(path: Path) -> tuple[int, str, str, str] | None:
    """Return (year, key, label, slug) for a series file, or None if unknown."""
    name = path.name
    m = RE_REGION.match(name)
    if m:
        region, year_s = m.group(1), m.group(2)
        year = int(year_s)
        return year, region, REGION_LABEL[region], f"{year}-{region}"
    m = RE_SPRINT.match(name)
    if m:
        year = int(m.group(1))
        return year, "sprint-series", "Sprint Series", f"{year}-sprint-series"
    m = RE_YOUTH.match(name)
    if m:
        year = int(m.group(1))
        return year, "youth-nationals", "Youth Nationals", f"{year}-youth-nationals"
    return None


def collect_events(series_dir: Path) -> list[Event]:
    events: dict[tuple[int, str], Event] = {}
    unknown: list[str] = []
    for path in sorted(series_dir.glob("*.sailscoring")):
        result = classify(path)
        if result is None:
            unknown.append(path.name)
            continue
        year, key, label, slug = result
        ev = events.setdefault((year, key), Event(year, key, label, slug))
        ev.files.append(path)
    if unknown:
        print(
            f"warning: {len(unknown)} unrecognised file(s) skipped:\n  "
            + "\n  ".join(unknown),
            file=sys.stderr,
        )
    return sorted(
        events.values(),
        key=lambda e: (-e.year, EVENT_ORDER.get(e.key, 99)),
    )


def build_command(ev: Event, args: argparse.Namespace) -> list[str]:
    cmd = [args.bin, "import"]
    cmd += [str(p) for p in ev.files]
    cmd += ["--workspace", args.workspace]
    cmd += ["--publish-slug", ev.slug]
    cmd += ["--category", str(ev.year)]
    if not args.no_archive:
        cmd += ["--archive"]
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Onboard IODAI .sailscoring files into the workspace via the sailscoring CLI.",
    )
    parser.add_argument(
        "--year",
        type=int,
        action="append",
        help="restrict to this exact year (repeatable). Overrides --min/--max-year.",
    )
    parser.add_argument(
        "--max-year",
        type=int,
        default=2025,
        help="upper bound, inclusive (default 2025 — i.e. 2025 and earlier).",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=None,
        help="lower bound, inclusive (default: no lower bound).",
    )
    parser.add_argument(
        "--workspace",
        default="iodai",
        help="target workspace slug (default: iodai).",
    )
    parser.add_argument(
        "--bin",
        default="sailscoring",
        help="path to the sailscoring CLI (default: sailscoring on PATH).",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="import + publish + categorise but do not archive.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="actually run the commands (default: dry-run, print only).",
    )
    parser.add_argument(
        "--series-dir",
        type=Path,
        default=SERIES_DIR,
        help=f"directory of .sailscoring files (default: {SERIES_DIR}).",
    )
    args = parser.parse_args()

    if not args.series_dir.is_dir():
        print(f"error: series dir not found: {args.series_dir}", file=sys.stderr)
        return 2

    events = collect_events(args.series_dir)

    if args.year:
        years = set(args.year)
        events = [e for e in events if e.year in years]
    else:
        events = [
            e
            for e in events
            if e.year <= args.max_year
            and (args.min_year is None or e.year >= args.min_year)
        ]

    if not events:
        print("no matching events.", file=sys.stderr)
        return 1

    total_files = sum(len(e.files) for e in events)
    mode = "APPLY" if args.apply else "DRY-RUN"
    scope = (
        f"year(s) {sorted(set(args.year))}"
        if args.year
        else f"<= {args.max_year}" + (f", >= {args.min_year}" if args.min_year else "")
    )
    print(
        f"[{mode}] {len(events)} event(s), {total_files} file(s) — "
        f"workspace '{args.workspace}', scope {scope}\n"
    )

    failures: list[Event] = []
    current_year: int | None = None
    for ev in events:
        if ev.year != current_year:
            current_year = ev.year
            print(f"── {ev.year} " + "─" * 40)
        cmd = build_command(ev, args)
        print(f"  {ev.label}  →  /p/{args.workspace}/{ev.slug}  ({len(ev.files)} series)")
        if args.apply:
            print(f"    $ {' '.join(cmd)}")
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"    ✗ exit {result.returncode}", file=sys.stderr)
                failures.append(ev)
            else:
                print("    ✓ done")
        else:
            print(f"    $ {' '.join(cmd)}")
        print()

    if not args.apply:
        print("dry-run only — re-run with --apply to execute.")
        return 0

    if failures:
        print(
            f"\n{len(failures)} event(s) failed:\n  "
            + "\n  ".join(f"{e.year} {e.label}" for e in failures),
            file=sys.stderr,
        )
        return 1
    print(f"\nall {len(events)} event(s) onboarded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
