#!/usr/bin/env python3
"""
blocking_waiter.py — feel what "blocking I/O" means, and why servers care.

What this demo proves
---------------------
When a program asks for something that takes time — bytes from the network,
data from a disk — it usually just STOPS and waits until the answer arrives.
That stopping is called BLOCKING. The CPU isn't working hard during the
wait; it's doing NOTHING (for this program). The program is like a waiter
standing frozen at one table until the kitchen finishes that table's food,
ignoring every other customer in the restaurant.

This is THE reason web servers need tricks (threads, or async — both coming
in later phases) to serve many users at once. You'll see this exact problem
again in Phase 2, when one slow visitor freezes our raw-socket server for
everybody else.

How the demo works
------------------
We simulate fetching three web pages. Each "fetch" is 2 seconds of pure
waiting (time.sleep stands in for "waiting for bytes to arrive over the
network" — from the program's point of view they are identical: you asked
the operating system for something and you're parked until it's ready).

ROUND 1 — one waiter (sequential, blocking):
    fetch page 1 (wait 2 s), THEN page 2 (wait 2 s), THEN page 3 (wait 2 s).
    Total: ~6 seconds. The waits ADD UP because nothing overlaps.

ROUND 2 — three waiters (one thread per fetch):
    all three fetches start at once; all three waits overlap.
    Total: ~2 seconds. Same work, one-third the time — because "waiting"
    parallelizes for free. Nobody needed a faster CPU. The time was never
    being spent ON the CPU.

Usage (inside WSL):
    python3 blocking_waiter.py
"""

import threading
import time

PAGES = ["homepage", "top-links", "comments"]
FETCH_SECONDS = 2.0   # how long each pretend network call takes

start_time = time.perf_counter()


def log(tag: str, msg: str) -> None:
    # Every line shows the elapsed time since the demo started, so you can
    # SEE which waits overlapped and which ones stacked up.
    t = time.perf_counter() - start_time
    print(f"[{t:5.2f}s] [{tag}] {msg}", flush=True)


def fetch_page(page: str) -> None:
    """Pretend to download a page. The sleep is the 'network wait'."""
    log("FETCH", f"requesting '{page}' — now BLOCKED waiting for the response "
                 f"({FETCH_SECONDS:.0f} s of doing absolutely nothing)")
    time.sleep(FETCH_SECONDS)   # <-- the block. The OS parks us here.
    log("FETCH", f"'{page}' arrived! Unblocked, moving on.")


def main() -> None:
    global start_time

    log("DEMO", "=== Blocking I/O demo: one waiter vs three ===")
    print(flush=True)

    # ---- ROUND 1: sequential (one waiter serves every table, in order) ----
    start_time = time.perf_counter()
    log("ROUND-1", "ONE waiter, three tables, one at a time:")
    for page in PAGES:
        fetch_page(page)
    sequential = time.perf_counter() - start_time
    log("ROUND-1", f"all three pages fetched in {sequential:.2f} s — "
                   "the three 2-second waits ADDED UP (2+2+2)")
    print(flush=True)

    # ---- ROUND 2: one thread per fetch (three waiters, one per table) ----
    start_time = time.perf_counter()
    log("ROUND-2", "THREE waiters, one per table, all at once:")
    threads = [threading.Thread(target=fetch_page, args=(p,)) for p in PAGES]
    for t in threads:
        t.start()   # all three fetches begin ~simultaneously
    for t in threads:
        t.join()    # wait until every fetch has finished
    threaded = time.perf_counter() - start_time
    log("ROUND-2", f"all three pages fetched in {threaded:.2f} s — "
                   "the three waits OVERLAPPED")
    print(flush=True)

    log("RESULT", f"sequential {sequential:.2f} s  vs  threaded {threaded:.2f} s "
                  f"({sequential / threaded:.1f}x faster)")
    log("RESULT", "same work, same CPU — we only stopped waiting in single file.")
    log("RESULT", "Phase 2 shows the dark side: our first web server will "
                  "block on ONE slow visitor while everyone else stares at "
                  "a loading spinner.")


if __name__ == "__main__":
    main()
