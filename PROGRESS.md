# PROGRESS.md — LinkBoard Project State

> Single source of truth for where this project stands.
> Claude Code: read this file FIRST in every session (see CLAUDE.md).
> Keep every section below accurate at all times.

## Current Status

| Field | Value |
|---|---|
| Current phase | Phase 01 — How a Computer Actually Works |
| Phase status | In progress — lesson + 4 playground demos written; awaiting user's demo runs |
| Last updated | 2026-07-16 |
| Last session ended | (session ongoing) |
| Next concrete action | User reads the lesson and runs the 4 demos (disk_race, spawn_family, thread_garble, blocking_waiter) per its "Run it & watch the logs" section, then reports back |

## How to Run the Project Right Now

```bash
# No app to run yet — Phase 2 adds the first server.
# Phase 1 demos (inside WSL; plain python3, no installs):
#   cd /mnt/d/Projects/linkboard/concepts/phase-01-how-a-computer-works/playground
#   python3 disk_race.py          # then: python3 disk_race.py --keep-cache
#   python3 spawn_family.py       # inspect from a 2nd terminal (pstree/ps/top)
#   python3 thread_garble.py
#   python3 blocking_waiter.py
# Full walkthrough with expected output (open in a browser):
#   concepts/phase-01-how-a-computer-works/lesson.html → "Run it & watch the logs"
```

## Phase Checklist

**Part I — Bedrock**
- [x] Phase 00 — Tools of the trade: Linux & Git (M23, M28) + repo/GitHub setup ✅ 2026-07-16
- [ ] Phase 01 — How a computer actually works (M6, M7)
- [ ] Phase 02 — The internet & protocols (M1, M2) + raw socket server
- [ ] Phase 03 — HTTP deep dive (M3)

**Part II — Building LinkBoard**
- [ ] Phase 04 — LinkBoard v1: APIs & REST (M9)
- [ ] Phase 05 — The browser: LinkBoard gets a frontend (M4)
- [ ] Phase 06 — Databases: PostgreSQL (M8 + M15 PG-advanced)
- [ ] Phase 07 — Security basics & authentication (M10 + M3.9)

**Part III — Scaling Reads & Ops Basics**
- [ ] Phase 08 — Caching & Redis in depth (M5, M11)
- [ ] Phase 09 — Docker, Nginx & horizontal scaling (M19, M22)

**Part IV — Async & Data Systems**
- [ ] Phase 10 — Message queues: RabbitMQ, SQS & SNS (M17, M18)
- [ ] Phase 11 — Kafka & event streaming (M16)
- [ ] Phase 12 — Search: Elasticsearch (M14)
- [ ] Phase 13 — NoSQL landscape: MongoDB & choosing databases (M12 + M15)

**Part V — Real-Time & Scaling Writes**
- [ ] Phase 14 — Real-time: WebSockets & live updates (M4.7)
- [ ] Phase 15 — Scaling writes: replication, Cassandra & CAP (M13 + M15)

**Part VI — Production Engineering**
- [ ] Phase 16 — Observability (M26)
- [ ] Phase 17 — Testing (M29)
- [ ] Phase 18 — CI/CD (M21)
- [ ] Phase 19 — Kubernetes (M20)

**Part VII — Cloud & Advanced Design**
- [ ] Phase 20 — Cloud: AWS, GCP & Azure (M24, M25)
- [ ] Phase 21 — Advanced API design (M30)
- [ ] Phase 22 — Architecture patterns & DDD (M27)
- [ ] Phase 23 — Data engineering (M31 + M15 ClickHouse)
- [ ] Phase 24 — Advanced security (M32)

**Part VIII — AI & Capstone**
- [ ] Phase 25 — AI-native system design (M33)
- [ ] Phase 26 — Capstone: design doc, estimation drills, mock interviews

## Mid-Phase Checkpoint

> Filled in ONLY when a session ends before a phase is complete.
> Cleared when the phase is finished.

- **What's done so far:** Phase 1 lesson written in full (`concepts/phase-01-how-a-computer-works/lesson.md`: bits/bytes, CPU + memory staircase, RAM vs disk, compile vs interpret, processes, threads + race condition, kernel/syscalls/virtual memory, blocking I/O). Playground written: `disk_race.py` (sequential vs random reads + page cache), `spawn_family.py` (process tree with private memory), `thread_garble.py` (race condition + lock fix), `blocking_waiter.py` (blocking I/O overlap), plus playground README.
- **What remains (concrete steps):** 1) User runs the four demos per the lesson's "Run it & watch the logs" section and reports output. 2) Optionally works the "Break it / observe it" experiments. 3) Wrap phase: mark done, update README table, end-of-phase commit.
- **Files touched this session:** everything under `concepts/phase-01-how-a-computer-works/`, `concepts/assets/lesson.css` (new shared lesson stylesheet), `concepts/phase-00-tools-of-the-trade/lesson.html` + `concepts/phase-01-how-a-computer-works/lesson.html` (new HTML lessons), CLAUDE.md (LESSON FORMAT rule), PROGRESS.md, README.md, both playground READMEs, exercises.md.
- **Pending user action:** delete the two superseded `lesson.md` files (commands provided in chat) — until then both formats coexist; `lesson.html` is canonical.
- **Decisions made:** (a) Demos in plain Python 3 stdlib — no installs needed; Ubuntu ships python3. (b) disk_race writes its 256 MB test file to `/tmp` (WSL's ext4 disk), not `/mnt/d`, for honest disk numbers; uses posix_fadvise DONTNEED to flush the page cache without sudo. (c) thread_garble uses an explicit read→sleep(0)→write pattern so the race fires reliably on modern Python (documented honestly in the lesson). (d) spawn_family runs ~60 s on purpose so the user can inspect it from a second terminal.
- **Exact next step on resume:** Ask whether the four demos were run; interpret pasted output; then wrap the phase (end-of-phase workflow).
- **Project runnable?** Yes — nothing to run in `project/` yet by design (first server is Phase 2); the four playground demos are self-contained.
- **Infra currently expected to be running (docker compose services):** none.

## Session Log

> One entry per session, newest first: date, what happened, where we stopped.

| Date | Summary |
|---|---|
| 2026-07-17 | **Lessons switched to styled HTML (user decision).** Built `concepts/assets/lesson.css` (shared design: gradient banner, orange/teal/violet palette, terminal-style code blocks, sticky TOC, light+dark) and converted Phase 00 + Phase 01 lessons to `lesson.html`. HTML is now the only lesson format (CLAUDE.md "LESSON FORMAT" rule); old `lesson.md` files to be deleted by user. Phase 01 demos still awaiting user run. |
| 2026-07-16 (later still) | **Phase 01 started.** Wrote the full lesson (binary → CPU/memory staircase → disk → compile/interpret → processes → threads/races → kernel/syscalls/virtual memory → blocking I/O) and the 4-demo playground (disk_race, spawn_family, thread_garble, blocking_waiter). Waiting on user to run the demos. |
| 2026-07-16 (later) | **Phase 00 completed.** User confirmed everything in the lesson done: git init + GitHub remote + first push (Part A), WSL/Ubuntu installed (Part B), playground exercises worked through (log hunt, runaway process, cron heartbeat — Parts C–F), git x-ray (Part G). Marked phase done; next up is Phase 01 (How a Computer Actually Works). |
| 2026-07-16 | User feedback: Phase 0 lesson draft was too high-level/cryptic for a beginner. Rewrote lesson.md fully at beginner pace (story-first diagrams, one idea per sentence, "try it now" blocks, expanded Git half). Recorded the correction as a permanent rule in CLAUDE.md ("Feedback log"). Still waiting on user to run Part A (git init + first push). |
| 2026-07-15 | Phase 0 started. Wrote the full Linux & Git lesson + playground (log hunt, runaway process, cron, git x-ray) and the repo skeleton (README, .gitignore, .gitattributes, project/ placeholder). Handed user the one-time setup steps (git init, GitHub remote, first push); waiting on their run report. |

## Key Decisions So Far

> Short running list; full reasoning lives in each phase's lesson.

- Linux is practiced through **WSL (Ubuntu)** on the user's Windows 11 machine; Git Bash is a partial fallback. WSL doubles as the foundation Docker needs in Phase 9.
- `.gitattributes` pins `*.sh` (and text generally) to **LF line endings** so scripts authored on Windows run inside WSL without `bad interpreter: ^M` failures.
- Phase exercise material lives in `concepts/phase-NN-*/playground/`; `project/` is reserved exclusively for the LinkBoard app (first code in Phase 2).
- Lessons are **styled HTML pages** (`lesson.html`, opened in a browser), all sharing `concepts/assets/lesson.css` for one consistent design. Markdown lessons retired 2026-07-17. Full formatting rules: CLAUDE.md → "LESSON FORMAT".
