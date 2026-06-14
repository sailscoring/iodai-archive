#!/usr/bin/env python3
"""CLI for building IODAI .sailscoring files from Sailwave result pages.

    python3 build.py                 # write series/*.sailscoring
    python3 build.py validate        # re-score and diff against published Nett
    python3 build.py adopt <file>    # pin a live series' id, then rebuild

`<file>` for adopt is a .sailscoring exported from the running app (Actions →
Save to File): it records the seriesId the app assigned so the regenerated file
re-imports over that live series. See README.md.
"""
import sys

import engine
from events import ALL_SERIES


def main(argv):
    if len(argv) > 1 and argv[1] == 'validate':
        return 0 if engine.validate(ALL_SERIES) else 1
    if len(argv) > 1 and argv[1] == 'adopt':
        if len(argv) < 3:
            sys.exit('usage: python3 build.py adopt <live-export.sailscoring>')
        engine.adopt(ALL_SERIES, argv[2])
        return 0
    engine.build(ALL_SERIES)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
