# LinkBoard — Learning System Design by Building It

A Hacker News–style link-sharing platform, built phase by phase as a hands-on
system design course. It starts as a single file and grows into a full
distributed system: PostgreSQL, Redis, RabbitMQ, Kafka, Elasticsearch,
MongoDB, Cassandra, Docker, Nginx, Kubernetes, CI/CD, observability, cloud
architecture, and AI features — with every concept explained from absolute
basics.

**How this repo works:**
- [curriculum.md](curriculum.md) — the full 27-phase plan (modules M1–M32 + AI).
- [PROGRESS.md](PROGRESS.md) — the single source of truth for where the project stands right now.
- [concepts/](concepts/) — one lesson folder per phase (the "textbook").
- [project/](project/) — the actual LinkBoard codebase, always runnable at every stopping point.

## How to run it right now

**LinkBoard is a real API!** As of Phase 4 it's a **FastAPI JSON REST API**
(submit / list / upvote / comment). Inside WSL:

```bash
cd /mnt/d/Projects/linkboard/project
python3 -m venv .venv && source .venv/bin/activate   # one-time setup
pip install -r requirements.txt
uvicorn app:app --reload --port 8000                 # then open http://localhost:8000/docs
# in another terminal — watch two upvotes eat a vote:
python3 race_demo.py
```

The earlier hand-written raw-socket server (Phases 2–3) is still there and still
runs with `python3 server.py` (no dependencies) — the origin story.

Lessons are styled HTML pages — **open them in your browser** (double-click):

- Phase 0 (done): `concepts/phase-00-tools-of-the-trade/lesson.html`
- Phase 1 (done): `concepts/phase-01-how-a-computer-works/lesson.html` —
  its four runnable demos live in that phase's `playground/` folder.
- Phase 2 (done): `concepts/phase-02-internet-and-protocols/lesson.html` —
  the internet, packets, IP, DNS, TCP/UDP, and the "one slow client freezes
  everyone" demo (`project/slow_client.py`).
- Phase 3 (done): `concepts/phase-03-http-deep-dive/lesson.html` — HTTP taken
  apart properly (methods & idempotency, status codes, headers, cookies,
  keep-alive, TLS), and the server above grown into a real HTTP parser.
- Phase 4 (current): `concepts/phase-04-apis-and-rest/lesson.html` — APIs & REST,
  JSON & serialization, hash maps & big-O, webhooks; LinkBoard becomes a FastAPI
  app (`project/app.py`) and the vote-eating race (`project/race_demo.py`).

## Progress

| Part | Phases | Status |
|---|---|---|
| I — Bedrock | ✅ 00 Linux & Git · ✅ 01 How computers work · ✅ 02 Internet & protocols · ✅ 03 HTTP | ✅ Done |
| II — Building LinkBoard | 🔨 04 APIs & REST · 05 Browser/frontend · 06 PostgreSQL · 07 Security & auth | 🔨 Phase 04 in progress |
| III — Scaling reads & ops | 08 Caching & Redis · 09 Docker, Nginx & scaling | ⬜ |
| IV — Async & data systems | 10 RabbitMQ/SQS/SNS · 11 Kafka · 12 Elasticsearch · 13 MongoDB & NoSQL | ⬜ |
| V — Real-time & writes | 14 WebSockets · 15 Replication, Cassandra & CAP | ⬜ |
| VI — Production engineering | 16 Observability · 17 Testing · 18 CI/CD · 19 Kubernetes | ⬜ |
| VII — Cloud & advanced design | 20 AWS/GCP/Azure · 21 API design · 22 Architecture & DDD · 23 Data engineering · 24 Advanced security | ⬜ |
| VIII — AI & capstone | 25 AI-native design · 26 Capstone | ⬜ |
