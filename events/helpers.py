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

# Venues (host clubs).
WHSC = dict(venue_logo='https://logos.sailscoring.ie/waterford-harbour-sc.png',
            venue_url='https://whsc.ie/')
