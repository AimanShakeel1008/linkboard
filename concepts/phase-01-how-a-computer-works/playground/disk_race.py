#!/usr/bin/env python3
"""
disk_race.py — FEEL the difference between sequential and random disk reads.

What this demo proves
---------------------
Reading a file from front to back (sequential) is dramatically faster than
jumping around and reading random pieces of it (random access) — even on an
SSD, and catastrophically so on a spinning hard drive.

This one fact quietly shapes half of system design:
  - why databases append to logs instead of updating files in place,
  - why Kafka (Phase 11) is fast,
  - why database indexes (Phase 6) are built the way they are.

How the demo works
------------------
1. It creates a 256 MB file full of random bytes in /tmp (inside WSL's own
   fast Linux disk — NOT on /mnt/d, which goes through a slow Windows
   translation layer and would muddy the results).
2. It reads the WHOLE file front to back in 4 KB chunks, and times it.
3. It reads the SAME number of 4 KB chunks, but from random positions,
   and times that.
4. It prints a comparison.

The sneaky extra lesson: the page cache
---------------------------------------
Linux keeps recently-read file data in spare RAM ("the page cache") so a
second read of the same data never touches the disk at all. That would make
both tests instantly fast and ruin the comparison. So by default this script
asks the kernel to FORGET the file from RAM before each test
(posix_fadvise DONTNEED — no sudo needed).

Run it a second time with --keep-cache and watch both tests become
lightning fast: that IS the page cache, your first cache of the course.

Usage (inside WSL):
    python3 disk_race.py               # fair fight, cold cache
    python3 disk_race.py --keep-cache  # rematch with the page cache ON
"""

import argparse
import os
import random
import sys
import time

# ---- Tunables -------------------------------------------------------------

FILE_PATH = "/tmp/linkboard_disk_demo.bin"   # /tmp lives on WSL's fast ext4 disk
FILE_SIZE = 256 * 1024 * 1024                # 256 MB test file
CHUNK = 4 * 1024                             # read in 4 KB pieces (a common
                                             # "page" size — the unit disks and
                                             # the kernel like to think in)
N_CHUNKS = FILE_SIZE // CHUNK                # 65,536 reads in each test


def log(tag: str, msg: str) -> None:
    """All output goes through here so every line has a narrated [TAG]."""
    print(f"[{tag}] {msg}", flush=True)


def make_test_file() -> None:
    """Create the 256 MB test file once; reuse it on later runs."""
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) == FILE_SIZE:
        log("SETUP", f"test file already exists: {FILE_PATH} (256 MB) — reusing it")
        return
    log("SETUP", f"creating test file {FILE_PATH} (256 MB of random bytes)...")
    log("SETUP", "this takes a few seconds and only happens once")
    written = 0
    t0 = time.perf_counter()
    with open(FILE_PATH, "wb") as f:
        # Write 4 MB at a time. os.urandom gives us random bytes so the file
        # can't be compressed or deduplicated behind our backs.
        block = os.urandom(4 * 1024 * 1024)
        while written < FILE_SIZE:
            f.write(block)
            written += len(block)
    log("SETUP", f"done writing in {time.perf_counter() - t0:.1f} s")


def drop_from_page_cache(fd: int) -> None:
    """
    Ask the kernel to forget this file's data from RAM (the page cache),
    so the next read is forced to go to the actual disk.

    POSIX_FADV_DONTNEED = "I won't need these bytes; feel free to evict them."
    It's advisory (a polite request), but Linux honors it for our purpose.
    """
    os.fsync(fd)  # make sure nothing is waiting to be written first
    os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)


def sequential_read(keep_cache: bool) -> float:
    """Read the whole file front to back, 4 KB at a time. Returns seconds."""
    fd = os.open(FILE_PATH, os.O_RDONLY)
    try:
        if not keep_cache:
            log("SEQ", "asking the kernel to forget this file from RAM (cold cache)")
            drop_from_page_cache(fd)
        log("SEQ", f"reading all {N_CHUNKS:,} chunks of 4 KB, front to back...")
        t0 = time.perf_counter()
        while os.read(fd, CHUNK):
            pass  # we only care about the reading, not the contents
        elapsed = time.perf_counter() - t0
        mb_per_s = (FILE_SIZE / (1024 * 1024)) / elapsed
        log("SEQ", f"done: 256 MB in {elapsed:.2f} s  ({mb_per_s:,.0f} MB/s, "
                   f"{elapsed / N_CHUNKS * 1e6:.1f} µs per chunk on average)")
        return elapsed
    finally:
        os.close(fd)


def random_read(keep_cache: bool) -> float:
    """Read the SAME number of 4 KB chunks, but from random offsets."""
    fd = os.open(FILE_PATH, os.O_RDONLY)
    try:
        if not keep_cache:
            log("RANDOM", "asking the kernel to forget this file from RAM (cold cache)")
            drop_from_page_cache(fd)
        # Pre-compute the random positions so the timing measures ONLY disk
        # work, not random-number generation. Each position is aligned to a
        # 4 KB boundary — the same chunk grid the sequential test used.
        offsets = [random.randrange(N_CHUNKS) * CHUNK for _ in range(N_CHUNKS)]
        log("RANDOM", f"reading {N_CHUNKS:,} chunks of 4 KB from random positions...")
        t0 = time.perf_counter()
        for i, off in enumerate(offsets):
            os.pread(fd, CHUNK, off)  # pread = "read CHUNK bytes at position off"
            # Progress heartbeat so a slow disk doesn't look like a hang:
            if i % 16384 == 0 and i > 0:
                pct = i / N_CHUNKS * 100
                log("RANDOM", f"...{pct:.0f}% done ({time.perf_counter() - t0:.1f} s so far)")
        elapsed = time.perf_counter() - t0
        mb_per_s = (FILE_SIZE / (1024 * 1024)) / elapsed
        log("RANDOM", f"done: 256 MB in {elapsed:.2f} s  ({mb_per_s:,.0f} MB/s, "
                      f"{elapsed / N_CHUNKS * 1e6:.1f} µs per chunk on average)")
        return elapsed
    finally:
        os.close(fd)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sequential vs random disk reads")
    parser.add_argument("--keep-cache", action="store_true",
                        help="do NOT flush the page cache first (watch RAM win)")
    args = parser.parse_args()

    if sys.platform == "win32":
        log("ERROR", "run this inside WSL (Ubuntu), not Windows Python — "
                     "the demo relies on Linux's page-cache controls")
        sys.exit(1)

    log("DEMO", "=== Disk race: sequential vs random reads ===")
    if args.keep_cache:
        log("DEMO", "page cache is ON — both tests may be served from RAM, not disk")
    else:
        log("DEMO", "page cache will be flushed before each test — this is a real disk test")

    make_test_file()
    seq = sequential_read(args.keep_cache)
    rnd = random_read(args.keep_cache)

    log("RESULT", "----------------------------------------------")
    log("RESULT", f"sequential: {seq:6.2f} s")
    log("RESULT", f"random:     {rnd:6.2f} s")
    if rnd > seq:
        log("RESULT", f"random access was {rnd / seq:.1f}x SLOWER — same file, "
                      f"same amount of data, only the ORDER changed")
    else:
        log("RESULT", "random wasn't slower — you're almost certainly reading "
                      "from the page cache (RAM). Re-run WITHOUT --keep-cache.")
    log("HINT", "now try:  python3 disk_race.py --keep-cache   (the RAM rematch)")
    log("HINT", f"cleanup when done with the lesson:  rm {FILE_PATH}")


if __name__ == "__main__":
    main()
