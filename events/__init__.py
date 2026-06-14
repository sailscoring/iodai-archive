"""All event definitions, newest year first.

Add a year by creating `events/yYYYY.py` with a `SERIES` list and appending its
module here. `build.py` consumes `ALL_SERIES`.
"""
from . import y2026

ALL_SERIES = [
    *y2026.SERIES,
]
