#!/usr/bin/env python3
"""
race_demo.py — watch two simultaneous upvotes EAT one another.

This is the payoff of Phase 4. LinkBoard stores its data in a JSON file, and the
upvote path is a read-modify-write with no locking (see storage.py). That's fine
when requests arrive one at a time. But the real world doesn't arrive one at a
time. This script fires TWO upvotes at the SAME MOMENT and shows that the link's
score goes up by only ONE — a vote silently vanished. It's called a LOST UPDATE,
and it is the single clearest reason databases (and transactions) exist.

HOW IT WORKS:
    1. Read link #1's current score.
    2. Launch two threads that each POST an upvote at the same instant.
    3. Read the score again.
    Expected if all is well: +2. What you'll actually see: +1.

No extra libraries — just Python's standard library (urllib + threading), so this
runs with plain `python3` while the API server runs in another terminal.

Run it (with the API already running in another terminal):
    python3 race_demo.py
"""

import json
import threading
import urllib.request
from datetime import datetime

BASE = "http://localhost:8000"
LINK_ID = 1                 # the link we'll hammer with two votes
VOTERS = 2                  # how many simultaneous upvotes to fire


def log(tag: str, message: str) -> None:
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{now} [{tag}] {message}", flush=True)


def get_points(link_id: int) -> int:
    """Read a link's current score via GET /links/{id}."""
    with urllib.request.urlopen(f"{BASE}/links/{link_id}") as resp:
        link = json.loads(resp.read())
    return link["points"]


def upvote(link_id: int, voter: int, barrier: threading.Barrier) -> None:
    """One voter. The barrier makes ALL voters wait, then release together, so
    the upvotes truly overlap instead of politely queueing one after another."""
    barrier.wait()          # everybody lines up here, then GO at the same instant
    log("VOTER", f"voter {voter} sending its upvote NOW")
    req = urllib.request.Request(f"{BASE}/links/{link_id}/upvote", method="POST")
    with urllib.request.urlopen(req) as resp:
        link = json.loads(resp.read())
    log("VOTER", f"voter {voter} got back points={link['points']}")


def main() -> None:
    log("DEMO", f"=== two-simultaneous-upvotes race, link id={LINK_ID} ===")

    try:
        before = get_points(LINK_ID)
    except Exception as exc:
        log("DEMO", f"couldn't reach the API at {BASE} — is the server running? ({exc})")
        return

    log("DEMO", f"score BEFORE: {before}")
    log("DEMO", f"firing {VOTERS} upvotes at the exact same moment...")

    # A Barrier releases all threads simultaneously once VOTERS of them arrive.
    barrier = threading.Barrier(VOTERS)
    threads = [
        threading.Thread(target=upvote, args=(LINK_ID, i + 1, barrier))
        for i in range(VOTERS)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    after = get_points(LINK_ID)
    log("DEMO", f"score AFTER: {after}")

    gained = after - before
    log("DEMO", f"we cast {VOTERS} votes; the score rose by {gained}")
    if gained < VOTERS:
        lost = VOTERS - gained
        log("DEMO", f"*** {lost} vote(s) LOST to a race condition. ***")
        log("DEMO", "Both upvotes read the same old score, both wrote old+1, and "
                    "the second write clobbered the first. THIS is why Phase 6 "
                    "brings a database with transactions.")
    else:
        log("DEMO", "No vote lost this run. Try again — with RACE_WINDOW_SECONDS "
                    " in storage.py at 0, a real race is rare and timing-dependent, "
                    "which is exactly what makes it so dangerous in production.")


if __name__ == "__main__":
    main()
