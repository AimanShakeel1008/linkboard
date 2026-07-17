# Phase 01 Playground — How a Computer Actually Works

Four small, heavily-narrated demos. Run them **inside WSL (Ubuntu)**, in this
order — each one is explained step by step in `../lesson.html` (open it in
your browser), including the exact output to expect.

| Script | What you'll see |
|---|---|
| `disk_race.py` | Sequential disk reads demolish random reads — and the page cache demolishes both. |
| `spawn_family.py` | A parent process spawns three children; you inspect the family live with `ps`, `pstree`, `top`. Each process has private memory. |
| `thread_garble.py` | Two threads share memory and silently lose updates (a race condition), then a lock fixes it. |
| `blocking_waiter.py` | Three 2-second waits take 6 s in single file but 2 s overlapped — the heart of blocking I/O. |

## Quick start

```bash
cd /mnt/d/Projects/linkboard/concepts/phase-01-how-a-computer-works/playground

python3 disk_race.py              # ~1-2 min incl. one-time 256 MB file creation
python3 disk_race.py --keep-cache # the RAM rematch
python3 spawn_family.py           # runs ~60 s; inspect from a 2nd terminal
python3 thread_garble.py          # a few seconds
python3 blocking_waiter.py        # ~8 seconds

rm /tmp/linkboard_disk_demo.bin   # cleanup after disk_race
```

No packages to install — everything uses Python's standard library.
Ubuntu ships with `python3` preinstalled (check with `python3 --version`).
