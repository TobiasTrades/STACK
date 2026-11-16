#!/usr/bin/env python3
"""Refresh STACK's cached nearby movie showtimes. API key is read only from Actions secrets."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

KEY = os.environ.get("API_CINEMA_KEY", "").strip()
OUT = Path("data/showtimes.json")

if not KEY:
    print("API_CINEMA_KEY is not configured; keeping the existing showtimes cache.")
    raise SystemExit(0)

# STACK's default home is Middleville, Michigan. A 65 km radius covers the
# nearby Hastings, Grand Rapids, Grandville, Lowell, Plainwell and Allegan cinemas.
params = urlencode({
    "country": "US",
    "near": "42.7131,-85.4620",
    "radius_km": "65",
    "limit": "1000",
})
url = "https://api.api-cinema.com/v1/showtimes?" + params
request = Request(url, headers={
    "Authorization": "Bearer " + KEY,
    "Accept": "application/json",
    "User-Agent": "STACK-Movie-Finder/1.0",
})
with urlopen(request, timeout=45) as response:
    payload = json.loads(response.read().decode("utf-8"))

rows = payload.get("data", [])
showtimes = []
for row in rows:
    if row.get("removedAt"):
        continue
    showtimes.append({
        "startsAt": row.get("startsAt"),
        "format": row.get("format"),
        "version": row.get("version"),
        "bookingUrl": row.get("bookingUrl"),
        "price": row.get("price"),
        "movie": row.get("movie"),
        "cinema": row.get("cinema"),
    })

result = {
    "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "provider": "API Cinema",
    "showtimes": showtimes,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Saved {len(showtimes)} showtimes to {OUT}")
