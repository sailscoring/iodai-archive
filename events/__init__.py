"""All event definitions, newest year first.

Add a year by creating `events/yYYYY.py` with a `SERIES` list and appending its
module here. `build.py` consumes `ALL_SERIES`.
"""
from . import y2026
from . import y2025
from . import y2024
from . import y2023
from . import y2022
from . import y2021
from . import y2020
from . import y2019
from . import y2018
from . import y2017
from . import y2016
from . import y2015
from . import y2014
from . import y2013
from . import y2011
from . import y2010
from . import y2009

ALL_SERIES = [
    *y2026.SERIES,
    *y2025.SERIES,
    *y2024.SERIES,
    *y2023.SERIES,
    *y2022.SERIES,
    *y2021.SERIES,
    *y2020.SERIES,
    *y2019.SERIES,
    *y2018.SERIES,
    *y2017.SERIES,
    *y2016.SERIES,
    *y2015.SERIES,
    *y2014.SERIES,
    *y2013.SERIES,
    *y2011.SERIES,
    *y2010.SERIES,
    *y2009.SERIES,
]
