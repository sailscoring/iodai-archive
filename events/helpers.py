"""Shared config helpers for event definitions.

Venue/event logo + URL slots point at the canonical logo library served from
logos.sailscoring.ie (the value the in-app picker stores for a built-in logo —
see `lib/canonical-logos/generated/manifest.ts` in the app repo). Spread a
constant into a series' config to fill its header/footer; absent => empty slot.
Add a new venue constant here as each event is sourced.
"""


def two_per_day(i, days):
    """Map race index `i` (0-based) to a date, two races per day, clamping to the
    last day once `days` runs out. Race dates are approximate — the Sailwave HTML
    carries only a publish timestamp — and can be set per race after import."""
    return days[i // 2] if i // 2 < len(days) else days[-1]


# Event (organiser) — IODAI runs every event here.
IODAI = dict(event_logo='https://logos.sailscoring.ie/iodai.png',
             event_url='https://iodai.com/')


def _logo(name, ext='png'):
    return {'venue_logo': f'https://logos.sailscoring.ie/{name}.{ext}'}


# Venues (host clubs). Each is the venue_logo slot, spread into a series config.
# Only clubs present in the canonical logo library appear here; a host with no
# canonical logo (e.g. East Antrim Boat Club, Monkstown Bay SC) gets no constant
# and simply leaves the slot empty.
WHSC = dict(venue_logo='https://logos.sailscoring.ie/waterford-harbour-sc.png',
            venue_url='https://whsc.ie/')
NYC = _logo('national-yc')
LDYC = _logo('lough-derg-yc')
KYC = _logo('kinsale-yc', 'svg')
LRYC = _logo('lough-ree-yc')
RCYC = _logo('royal-cork-yc', 'svg')
HYC = _logo('hyc')
MYC = _logo('malahide-yc')
GBSC = _logo('galway-bay-sc')
SSC = _logo('skerries-sc')
RSGYC = _logo('rsgyc')
SLYC = _logo('strangford-lough-yc')
BYC = _logo('ballyholme-yc')
RIYC = _logo('riyc')


# IODAI's usual discard scheme: a single discard once 4 races are sailed, which
# is what nearly every fleet uses. The actual discard count is set per-event in
# the SIs, not by a fixed race-count rule (e.g. a 10-race regatta-racing fleet
# may take 1 or 2 discards depending on the event), so a fleet that discarded
# more is given an explicit `discards=` override matching the parentheses on its
# published page. `validate` is the real check.
DISCARDS = [(4, 1)]


def _date_fn(days):
    """A date(slot) callable that spreads races two-per-day across `days`."""
    return lambda i, days=days: two_per_day(i, days)


def main_fleet(out, name, venue, days, nslots, senior=None, junior=None,
               discards=DISCARDS, **venuekw):
    """A Main-Fleet series: Senior and/or Junior as separate scratch fleets
    sharing a finish line, scored independently, with Gold/Silver/Bronze as a
    subdivision. `days` is the list of event day ISO dates (start/end derived
    from its ends). Pass a venue logo constant via **venuekw (e.g. **NYC)."""
    src = []
    if senior:
        src.append(dict(file=senior, fleet='Senior', slot0=0))
    if junior:
        src.append(dict(file=junior, fleet='Junior', slot0=0))
    return dict(
        out=out, name=name, venue=venue, start=days[0], end=days[-1],
        discards=discards, nslots=nslots, sources=src,
        fleet_order=[s['fleet'] for s in src], date=_date_fn(days),
        subdivision=True, boat_class=False, primary='helm', **IODAI, **venuekw)


def solo(out, name, venue, days, nslots, file, fleet, subdivision=False,
         discards=DISCARDS, **venuekw):
    """A single-fleet series (Regatta Racing, Regatta Coached, Crosbie Cup, …)."""
    return combined(out, name, venue, days, nslots, [file], fleet=fleet,
                    subdivision=subdivision, discards=discards, **venuekw)


def combined(out, name, venue, days, nslots, files, fleet='Main',
             subdivision=True, discards=DISCARDS, **venuekw):
    """One scratch fleet assembled from one or more pages. Used when a Main fleet
    that was actually scored as a *single combined* start was published split
    across senior/junior view pages (e.g. 2024 Ulsters @ EABC): loading both
    pages into one fleet restores the contiguous 1..N positions the page scored.
    For such pages the 'Division' column holds Senior/Junior (the prize Gold/
    Silver/Bronze sits in a separate 'Rating' column the engine ignores)."""
    return dict(
        out=out, name=name, venue=venue, start=days[0], end=days[-1],
        discards=discards, nslots=nslots,
        sources=[dict(file=f, fleet=fleet, slot0=0) for f in files],
        fleet_order=[fleet], date=_date_fn(days),
        subdivision=subdivision, boat_class=False, primary='helm',
        **IODAI, **venuekw)
