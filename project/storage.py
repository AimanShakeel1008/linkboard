#!/usr/bin/env python3
"""
storage.py — LinkBoard v1's "database": a single JSON file on disk.

WHY A JSON FILE (and why it's temporary):
    A real database is Phase 6. Right now we want the SIMPLEST possible thing
    that survives a restart: write our data to a text file as JSON, read it back
    when we start. This is enough to feel what persistence is — and, crucially,
    enough to feel what a JSON file CANNOT do. By the end of this phase you'll
    watch two simultaneous upvotes corrupt each other through this file, and that
    pain is the entire motivation for Phase 6's database and transactions.

WHAT LIVES HERE:
    Every function that touches the data file. Keeping storage in one module
    (instead of scattered through the API code) is a small but real design habit:
    the API layer decides WHAT to do; the storage layer decides HOW it's saved.
    Swap this file for a Postgres version later and the API barely changes.

THE DELIBERATE FLAW:
    Every write is a read-modify-write with NO locking: load the whole file,
    change something in memory, write the whole file back. If two of those
    overlap, one silently clobbers the other (a "lost update"). We even widen the
    danger window on purpose (RACE_WINDOW_SECONDS) so the race is reproducible in
    a demo instead of being a rare heisenbug. This is not a bug to fix here — it's
    the lesson.
"""

import json
import os
import time
from datetime import datetime, timezone

# The data file sits right next to this module, so it doesn't matter where you
# launch the server from — the path is anchored to the code, not the shell's cwd.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "links.json")

# Artificially widen the read-modify-write race window so the two-upvotes demo
# loses a vote every time instead of once in a thousand runs. Set to 0.0 to make
# the server behave "normally" (the race still exists — it's just rare and timing
# dependent, which is exactly what makes real races so nasty to catch).
RACE_WINDOW_SECONDS = 0.15

# What the file looks like the very first time, before anyone submits anything.
SEED = {
    "next_id": 4,
    "links": [
        {"id": 1, "title": "How a computer actually works (Phase 1)",
         "url": "https://example.com/phase-1", "points": 12, "comments": []},
        {"id": 2, "title": "DNS: the internet's phone book (Phase 2)",
         "url": "https://example.com/dns", "points": 8, "comments": []},
        {"id": 3, "title": "HTTP by hand (Phase 3)",
         "url": "https://example.com/http", "points": 5, "comments": []},
    ],
}


def log(tag: str, message: str) -> None:
    """Same narrated, flushed logging as the rest of the project."""
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{now} [{tag}] {message}", flush=True)


def _now_iso() -> str:
    """A timestamp string for comments, e.g. '2026-07-20T14:03:11Z'."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# The two lowest-level operations: read the whole file, write the whole file.
# EVERYTHING else is built on these. Notice we always move ALL the data in and
# out at once — that whole-file rewrite is the simplicity that makes this easy,
# and also the reason it can't scale or stay consistent under concurrency.
# ---------------------------------------------------------------------------

def _read() -> dict:
    """Load the entire JSON file into a Python dict. If the file doesn't exist
    yet (first run), create it from SEED so the app always has something to show.

    SERIALIZATION, named: turning bytes-on-disk into live Python objects is
    DESERIALIZING (json.load); the reverse is SERIALIZING (json.dump). JSON is
    just an agreed text format for that — the same 'text is numbers plus an
    agreement' idea from Phase 1, now for whole objects instead of characters."""
    if not os.path.exists(DATA_FILE):
        log("STORE", f"{os.path.basename(DATA_FILE)} not found — seeding it")
        _write(SEED)
        return json.loads(json.dumps(SEED))   # return a fresh copy, not SEED itself
    start = time.perf_counter()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)                    # DESERIALIZE: text -> Python dict
    ms = (time.perf_counter() - start) * 1000
    log("STORE", f"read {os.path.basename(DATA_FILE)} "
                 f"({len(data['links'])} links) in {ms:.1f}ms")
    return data


def _write(data: dict) -> None:
    """Save the entire dict back to disk as JSON. This REPLACES the whole file
    every time — there's no 'update just one row' here; that's a database's job."""
    start = time.perf_counter()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)           # SERIALIZE: Python dict -> text
    ms = (time.perf_counter() - start) * 1000
    log("STORE", f"wrote {os.path.basename(DATA_FILE)} "
                 f"({len(data['links'])} links) in {ms:.1f}ms")


# ---------------------------------------------------------------------------
# The operations the API actually calls. Each is a small, readable verb.
# ---------------------------------------------------------------------------

def list_links() -> list:
    """Return all links, most-upvoted first (like a Hacker News front page)."""
    data = _read()
    return sorted(data["links"], key=lambda l: l["points"], reverse=True)


def get_link(link_id: int):
    """Return one link by id, or None if there's no such link."""
    data = _read()
    for link in data["links"]:
        if link["id"] == link_id:
            return link
    return None


def add_link(title: str, url: str) -> dict:
    """Create a new link and persist it. Returns the created link (with its new
    id). This is the read-modify-write pattern too, but 'append a new item' rarely
    collides destructively, so we don't dwell on its race here."""
    data = _read()
    link = {
        "id": data["next_id"],
        "title": title,
        "url": url,
        "points": 1,            # a submission starts with its author's implicit vote
        "comments": [],
    }
    data["links"].append(link)
    data["next_id"] += 1
    _write(data)
    log("STORE", f"added link id={link['id']} '{title}'")
    return link


def upvote_link(link_id: int):
    """Add one point to a link. Returns the updated link, or None if not found.

    *** THIS IS THE RACE-PRONE FUNCTION — the whole point of the phase. ***
    Look at the shape: (1) READ the current points, (2) compute new = old + 1,
    (3) WRITE it back. Between step 1 and step 3 there is a gap. If a SECOND
    upvote runs its step 1 during that gap, both read the SAME old value, both
    compute the same new value, and the second write overwrites the first — two
    upvotes, but points only went up by one. A vote vanished. That's a 'lost
    update', and RACE_WINDOW_SECONDS below makes the gap wide enough to see it
    every time."""
    data = _read()
    link = next((l for l in data["links"] if l["id"] == link_id), None)
    if link is None:
        return None

    old_points = link["points"]                       # STEP 1: read
    log("RACE", f"upvote id={link_id}: read points={old_points} "
                f"(now thinking for {RACE_WINDOW_SECONDS}s — the danger window)")

    # STEP 2 (with an artificially widened gap). In real code the gap is tiny —
    # a few microseconds between reading and writing — but it is ALWAYS there.
    time.sleep(RACE_WINDOW_SECONDS)
    new_points = old_points + 1

    link["points"] = new_points                       # STEP 3: modify + write
    _write(data)
    log("RACE", f"upvote id={link_id}: wrote points={new_points} "
                f"(if another upvote read {old_points} too, its vote is now LOST)")
    return link


def add_comment(link_id: int, author: str, text: str):
    """Attach a comment to a link. Returns the updated link, or None if missing."""
    data = _read()
    link = next((l for l in data["links"] if l["id"] == link_id), None)
    if link is None:
        return None
    comment = {"author": author, "text": text, "at": _now_iso()}
    link["comments"].append(comment)
    _write(data)
    log("STORE", f"added comment to id={link_id} by {author!r}")
    return link
