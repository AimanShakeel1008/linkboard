#!/usr/bin/env python3
"""
thread_garble.py — watch two threads corrupt a shared number, then fix it.

What this demo proves
---------------------
Threads live INSIDE one process and SHARE its memory (roommates in one
apartment, unlike the separate-apartment processes in spawn_family.py).
Sharing is fast and convenient — and dangerous. If two threads update the
same variable at the same time, updates get LOST. Silently. No error.

This is called a RACE CONDITION, and it is the single most important bug
class in this whole course. You will meet it again in Phase 4 (two upvotes
eating each other) and slay it properly in Phase 6 (database transactions).

How the corruption works, step by step
--------------------------------------
`counter = counter + 1` LOOKS like one action. It is actually three:
    1. READ the current value of counter          (say it reads 41)
    2. ADD one to it                              (41 + 1 = 42)
    3. WRITE the result back into counter         (counter = 42)

Now imagine two threads, A and B, both doing this at the same moment:
    A reads 41.
    B reads 41 too — A hasn't written yet!
    A writes 42.
    B writes 42.        <- B just OVERWROTE A's update.
Two increments happened. The counter went up by one. One vote vanished.

To make the race easy to see, each thread in this demo deliberately pauses
for a moment BETWEEN its read and its write (time.sleep(0) — "let someone
else go first"). Real code has no such pause, but the gap between read and
write always exists; it's just nanoseconds wide. Rare bugs are WORSE than
frequent ones — they pass your tests and then fire in production. We widen
the gap so you can watch the crime happen in seconds instead of waiting
weeks for it.

Then we run the same job again holding a LOCK (a bathroom-door lock: one
roommate inside at a time), and the answer comes out exactly right.

Usage (inside WSL):
    python3 thread_garble.py
"""

import threading
import time

INCREMENTS_PER_THREAD = 5000   # each thread tries to add 1 this many times
N_THREADS = 2
EXPECTED = INCREMENTS_PER_THREAD * N_THREADS

# The shared variable. ONE copy, visible to every thread in this process.
counter = 0

# The fix for round 2: a mutual-exclusion lock ("mutex").
lock = threading.Lock()


def log(tag: str, msg: str) -> None:
    print(f"[{tag}] {msg}", flush=True)


def unsafe_worker(name: str) -> None:
    """Increment the shared counter WITHOUT any protection."""
    global counter
    for _ in range(INCREMENTS_PER_THREAD):
        current = counter          # step 1: READ
        time.sleep(0)              # deliberately yield: "someone else may run now"
        counter = current + 1      # step 3: WRITE (possibly overwriting a neighbor!)
    log(f"THREAD-{name}", f"finished my {INCREMENTS_PER_THREAD:,} increments (unsafe)")


def safe_worker(name: str) -> None:
    """Same job, but the read-modify-write happens inside a lock."""
    global counter
    for _ in range(INCREMENTS_PER_THREAD):
        with lock:                 # wait for the door, enter, lock it behind us
            current = counter
            time.sleep(0)          # same deliberate pause — now harmless!
            counter = current + 1
        # leaving the `with` block unlocks the door for the next thread
    log(f"THREAD-{name}", f"finished my {INCREMENTS_PER_THREAD:,} increments (safe)")


def run_round(title: str, worker) -> int:
    """Run two threads with the given worker function; return final counter."""
    global counter
    counter = 0
    log("ROUND", f"--- {title} ---")
    log("ROUND", f"two threads will each add 1 to a shared counter "
                 f"{INCREMENTS_PER_THREAD:,} times")
    log("ROUND", f"if nothing goes wrong, the counter should end at {EXPECTED:,}")

    t0 = time.perf_counter()
    threads = [threading.Thread(target=worker, args=(chr(ord('A') + i),))
               for i in range(N_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()   # wait for both threads to finish
    elapsed = time.perf_counter() - t0

    log("ROUND", f"both threads done in {elapsed:.2f} s — final counter: {counter:,}")
    return counter


def main() -> None:
    log("DEMO", "=== Shared-memory race condition demo ===")

    got = run_round("ROUND 1: no lock (the race)", unsafe_worker)
    lost = EXPECTED - got
    if lost > 0:
        log("RESULT", f"expected {EXPECTED:,} but got {got:,} — "
                      f"{lost:,} increments VANISHED ({lost / EXPECTED:.0%} lost!)")
        log("RESULT", "no crash, no error message — the updates are just gone. "
                      "This is why race conditions are so feared.")
    else:
        log("RESULT", f"got exactly {got:,} — the threads happened not to collide "
                      "this run. That's the scariest property of races: "
                      "sometimes they don't fire. Run it again.")

    print(flush=True)
    got = run_round("ROUND 2: with a lock (the fix)", safe_worker)
    if got == EXPECTED:
        log("RESULT", f"exactly {EXPECTED:,}, every single increment survived — "
                      "the lock forced the threads to take turns")
        log("RESULT", "the price: taking turns is slower. Correctness costs "
                      "something. That tradeoff echoes through all of system design.")
    else:
        log("RESULT", f"got {got:,} — this should not happen with the lock; "
                      "re-run and tell Claude if it persists")


if __name__ == "__main__":
    main()
