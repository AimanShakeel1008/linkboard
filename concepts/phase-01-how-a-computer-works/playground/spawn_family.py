#!/usr/bin/env python3
"""
spawn_family.py — create a family of processes and go LOOK at them.

What this demo proves
---------------------
A "process" is not an abstract idea: it's a real thing the operating system
creates, tracks with an ID number (a PID), and shows you in `ps` and `top`.
This script becomes a parent and spawns three children, then everyone sits
around "working" (sleeping and printing heartbeats) for 60 seconds — long
enough for you to inspect the family from a SECOND terminal.

While it runs, open another WSL terminal and try:

    pstree -p $(pgrep -f spawn_family.py | head -1)
        # draws the family tree: parent -> three children

    ps -f -u $USER | grep spawn_family
        # one line per process; note the PID and PPID (parent PID) columns

    top   (then press 'q' to quit)
        # the live dashboard; our processes barely use CPU because
        # sleeping costs nothing — they're waiting, not computing

Each child also proves it has its OWN PRIVATE MEMORY: every process sets the
same variable `secret` to a different value, and nobody overwrites anybody —
because a process's memory is a private apartment, not a shared house.
(Contrast with thread_garble.py, where threads DO share memory and pay for it.)
"""

import multiprocessing
import os
import time

WORK_SECONDS = 60          # how long the family stays alive for inspection
HEARTBEAT_EVERY = 10       # seconds between "I'm alive" messages

# Every process that imports this file gets its own copy of this variable.
# The parent and each child will write different values into it — and none
# of the writes will be visible to the others. Private apartments.
secret = "unset"


def log(tag: str, msg: str) -> None:
    print(f"[{tag}] (pid {os.getpid()}) {msg}", flush=True)


def child_work(name: str) -> None:
    """What each child process runs. It has its own PID and its own memory."""
    global secret
    secret = f"{name}'s private value"
    log("CHILD", f"hello, I am child '{name}' — my parent is pid {os.getppid()}")
    log("CHILD", f"I set secret = \"{secret}\" in MY memory (nobody else sees this)")

    start = time.time()
    while time.time() - start < WORK_SECONDS:
        time.sleep(HEARTBEAT_EVERY)
        remaining = int(WORK_SECONDS - (time.time() - start))
        log("CHILD", f"'{name}' still alive, secret is still \"{secret}\" "
                     f"(~{max(remaining, 0)} s left)")

    log("CHILD", f"'{name}' finished — exiting now. My PID will disappear from ps.")


def main() -> None:
    global secret
    secret = "the parent's value"
    log("PARENT", "=== Process family demo ===")
    log("PARENT", f"I am the parent. MY parent (PPID) is {os.getppid()} — "
                  "that's the shell you launched me from!")
    log("PARENT", f"spawning 3 children; we'll all stay alive ~{WORK_SECONDS} s")
    log("PARENT", "NOW: open a second terminal and run:  "
                  "pstree -p " + str(os.getpid()))

    children = []
    for name in ("alice", "bob", "carol"):
        # multiprocessing.Process asks the OS for a brand-new process.
        # Under the hood on Linux this uses the fork() system call:
        # the kernel clones the parent, then the clone runs child_work.
        p = multiprocessing.Process(target=child_work, args=(name,), name=name)
        p.start()
        log("PARENT", f"spawned child '{name}' with pid {p.pid}")
        children.append(p)

    # The parent waits for every child to finish. A parent that exits
    # without waiting leaves "orphans" — the kernel reassigns them to
    # process 1 (init/systemd), the building's ultimate landlord.
    for p in children:
        p.join()
        log("PARENT", f"child '{p.name}' (pid {p.pid}) has exited "
                      f"with code {p.exitcode}")

    log("PARENT", f"my secret is still \"{secret}\" — no child's write ever "
                  "touched MY memory. Separate apartments confirmed.")
    log("PARENT", "all children done — parent exiting. Demo over.")


if __name__ == "__main__":
    main()
