# PROGRESS.md — LinkBoard Project State

> Single source of truth for where this project stands.
> Claude Code: read this file FIRST in every session (see CLAUDE.md).
> Keep every section below accurate at all times.

## Current Status

| Field | Value |
|---|---|
| Current phase | Phase 00 — Tools of the Trade: Linux & Git |
| Phase status | In progress — lesson + playground written; awaiting user's one-time setup run |
| Last updated | 2026-07-15 |
| Last session ended | Mid-phase checkpoint (session ongoing) |
| Next concrete action | User runs "Run These Steps — Part A" (git init, GitHub remote, first push), then WSL install + playground exercises (lesson Parts B–G) |

## How to Run the Project Right Now

```bash
# No app to run yet — Phase 2 adds the first server.
# Phase 0 practice commands live in:
#   concepts/phase-00-tools-of-the-trade/lesson.md  → "Run it & watch the logs"
# Playground quick start (inside WSL):
#   cd /mnt/d/Projects/linkboard/concepts/phase-00-tools-of-the-trade/playground
#   chmod +x *.sh && ./make_logs.sh
```

## Phase Checklist

**Part I — Bedrock**
- [ ] Phase 00 — Tools of the trade: Linux & Git (M23, M28) + repo/GitHub setup
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

- **What's done so far:** Phase 0 lesson written (`concepts/phase-00-tools-of-the-trade/lesson.md`); Linux playground written (make_logs.sh, exercises.md, runaway.sh, heartbeat.sh, git_xray.sh + README); repo skeleton done (README.md rewritten to match the 27-phase curriculum, .gitignore extended, .gitattributes added, project/README.md placeholder).
- **What remains (concrete steps):** 1) User runs Part A: git init, GitHub remote, first commit + push. 2) User installs WSL (lesson Part B). 3) User works playground Parts C–F (log hunt, runaway process, cron heartbeat). 4) User runs git_xray.sh (Part G). 5) Wrap phase: verify, mark done, end-of-phase commit.
- **Files touched this session:** everything under `concepts/phase-00-tools-of-the-trade/`, README.md, .gitignore, .gitattributes, project/README.md, PROGRESS.md.
- **Decisions made:** (a) Linux material taught via WSL/Ubuntu on the user's Windows 11 machine (Git Bash noted as partial fallback) — WSL is also needed for Docker in Phase 9. (b) Playground lives inside the phase folder, keeping `project/` reserved for LinkBoard itself. (c) `.gitattributes` forces LF endings on `*.sh` so scripts written on Windows run in WSL. (d) Pre-existing README.md described an obsolete 13-phase draft plan referencing files that never existed; replaced to match curriculum.md.
- **Exact next step on resume:** Ask whether Part A (git/GitHub setup) was run; interpret any pasted output; then guide Parts B–G.
- **Project runnable?** Yes-with-notes: nothing to "run" by design — first server arrives in Phase 2; playground scripts are self-contained.
- **Infra currently expected to be running (docker compose services):** none.

## Session Log

> One entry per session, newest first: date, what happened, where we stopped.

| Date | Summary |
|---|---|
| 2026-07-16 | User feedback: Phase 0 lesson draft was too high-level/cryptic for a beginner. Rewrote lesson.md fully at beginner pace (story-first diagrams, one idea per sentence, "try it now" blocks, expanded Git half). Recorded the correction as a permanent rule in CLAUDE.md ("Feedback log"). Still waiting on user to run Part A (git init + first push). |
| 2026-07-15 | Phase 0 started. Wrote the full Linux & Git lesson + playground (log hunt, runaway process, cron, git x-ray) and the repo skeleton (README, .gitignore, .gitattributes, project/ placeholder). Handed user the one-time setup steps (git init, GitHub remote, first push); waiting on their run report. |

## Key Decisions So Far

> Short running list; full reasoning lives in each phase's lesson.

- Linux is practiced through **WSL (Ubuntu)** on the user's Windows 11 machine; Git Bash is a partial fallback. WSL doubles as the foundation Docker needs in Phase 9.
- `.gitattributes` pins `*.sh` (and text generally) to **LF line endings** so scripts authored on Windows run inside WSL without `bad interpreter: ^M` failures.
- Phase exercise material lives in `concepts/phase-NN-*/playground/`; `project/` is reserved exclusively for the LinkBoard app (first code in Phase 2).
