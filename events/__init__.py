"""All event definitions, newest year first.

Add a year by creating `events/yYYYY.py` with a `SERIES` list and appending its
module here. `build.py` consumes `ALL_SERIES`.
"""
from . import y2026
from . import y2025
from . import y2024
from . import y2023

ALL_SERIES = [
    *y2026.SERIES,
    *y2025.SERIES,
    *y2024.SERIES,
    *y2023.SERIES,
]
