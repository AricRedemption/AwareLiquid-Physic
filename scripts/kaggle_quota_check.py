#!/usr/bin/env python3
"""KAGGLE-QUOTA (wave-10 round 108, AMM-023): read remaining Kaggle GPU quota.

User directive 2026-09-22: Kaggle training dispatch is quota-driven — the
loop reads the remaining GPU balance and decides what / how much to train
per the preregistered mapping. The thresholds below are the SINGLE SOURCE
OF TRUTH; docs/kaggle-quota-protocol.md references them, never re-states
them (instance values live at the execution point only).

Honest scope: Kaggle's stable public API (api/v1) has no quota endpoint.
This tool best-effort reads the authenticated web-session quota endpoint
the Kaggle UI itself uses (unofficial — may change without notice) through
the `kaggle` package's session when that package is installed. Dispatch
gating must only trust reads with status "ok"; anything else is a
structured refusal to dispatch.

Failure codes (also the exit code):
  0  ok                       — gpu_hours_remaining read and tiered
  3  KAGGLE_NO_CREDS          — no ~/.kaggle/kaggle.json (user material,
                                 not a decision: drop the token in place)
  4  KAGGLE_DEP_MISSING       — `kaggle` package not importable
  5  KAGGLE_QUOTA_READ_FAILED — endpoint unreachable / response unparsable

Output (stdout, JSON):
  {"status": "ok" | "<failure code>",
   "gpu_hours_remaining": float | null,
   "tier": "<mapping tier>" | null,
   "meta": {"ts": iso8601, "source": str, "note": str}}

Zero training; network read only; deterministic given the same response.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CREDS_PATH = Path.home() / ".kaggle" / "kaggle.json"
QUOTA_ENDPOINT = "https://www.kaggle.com/api/i/computequota.QuotaService/GetUserQuota"

# Preregistered quota→dispatch mapping (GPU·hours remaining). Single source;
# docs/kaggle-quota-protocol.md describes the tiers without restating numbers.
TIERS = (
    (2.0, "PROBE_ONLY"),    # < 2h  → smoke/pipeline validation on Kaggle only
    (8.0, "SHORT_RUN"),     # < 8h  → one short preregistered T3 candidate
    (20.0, "FULL_RUN"),     # < 20h → one full multi-seed terminal run
    (float("inf"), "MULTI_RUN"),  # ≥ 20h → queue several, weekly budget respected
)
# No confirmed read ⇒ NO_READ: never dispatch on a stale or failed read.
TIER_NO_READ = "NO_READ"


def tier_for(hours: float | None) -> str:
    if hours is None:
        return TIER_NO_READ
    for cap, name in TIERS:
        if hours < cap:
            return name
    return TIERS[-1][1]


def load_creds(path: Path = CREDS_PATH) -> dict | None:
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict) and data.get("username") and data.get("key"):
            return data
    except (OSError, ValueError):
        pass
    return None


def read_quota_hours(creds: dict, poster=None) -> float | None:
    """POST the quota endpoint. `poster` is injectable for tests:
    poster(creds, url) -> parsed float | None. Live path needs the `kaggle`
    package present (it brings `requests`); auth is passed explicitly so no
    global kaggle state is touched."""
    if poster is not None:
        return poster(creds, QUOTA_ENDPOINT)
    import importlib.util
    if importlib.util.find_spec("kaggle") is None:
        raise DependencyMissing()
    import requests  # kaggle depends on requests; present whenever kaggle is
    r = requests.post(
        QUOTA_ENDPOINT,
        json={},
        auth=(creds["username"], creds["key"]),
        timeout=30,
    )
    if r.status_code != 200:
        return None
    try:
        body = r.json()
        seconds = body["quota"]["gpuRequestQuota"]["remaining"]
        return round(float(seconds) / 3600.0, 2)
    except (ValueError, KeyError, TypeError):
        return None


class DependencyMissing(Exception):
    pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--creds", type=Path, default=CREDS_PATH,
                        help="kaggle.json path (default ~/.kaggle/kaggle.json)")
    args = parser.parse_args()

    meta = {"ts": datetime.now(timezone.utc).isoformat(),
            "source": "kaggle web-session quota endpoint (unofficial)",
            "note": ""}

    creds = load_creds(args.creds)
    if creds is None:
        meta["note"] = f"no readable creds at {args.creds}"
        print(json.dumps({"status": "KAGGLE_NO_CREDS", "gpu_hours_remaining": None,
                          "tier": TIER_NO_READ, "meta": meta}))
        return 3
    try:
        hours = read_quota_hours(creds)
    except DependencyMissing:
        meta["note"] = "kaggle package not importable in this interpreter"
        print(json.dumps({"status": "KAGGLE_DEP_MISSING", "gpu_hours_remaining": None,
                          "tier": TIER_NO_READ, "meta": meta}))
        return 4
    except Exception as e:  # network/parsing failures are outcomes, not crashes
        meta["note"] = f"read failed: {type(e).__name__}"
        print(json.dumps({"status": "KAGGLE_QUOTA_READ_FAILED",
                          "gpu_hours_remaining": None,
                          "tier": TIER_NO_READ, "meta": meta}))
        return 5
    if hours is None:
        meta["note"] = "endpoint reachable but response unparsable/changed"
        print(json.dumps({"status": "KAGGLE_QUOTA_READ_FAILED",
                          "gpu_hours_remaining": None,
                          "tier": TIER_NO_READ, "meta": meta}))
        return 5
    print(json.dumps({"status": "ok", "gpu_hours_remaining": hours,
                      "tier": tier_for(hours), "meta": meta}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
