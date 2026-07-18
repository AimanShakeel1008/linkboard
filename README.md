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

**LinkBoard is alive!** As of Phase 2 there's a real server to run — an HTTP
server built from raw sockets. Inside WSL:

```bash
cd /mnt/d/Projects/linkboard/project
python3 server.py            # http://localhost:8000 ; Ctrl+C to stop
# in another terminal:
curl -v localhost:8000       # the homepage, headers and all
```

Lessons are styled HTML pages — **open them in your browser** (double-click):

- Phase 0 (done): `concepts/phase-00-tools-of-the-trade/lesson.html`
- Phase 1 (done): `concepts/phase-01-how-a-computer-works/lesson.html` —
  its four runnable demos live in that phase's `playground/` folder.
- Phase 2 (current): `concepts/phase-02-internet-and-protocols/lesson.html` —
  walks through the server above and the "one slow client freezes everyone"
  demo (`project/slow_client.py`).

## Progress

| Part | Phases | Status |
|---|---|---|
| I — Bedrock | ✅ 00 Linux & Git · ✅ 01 How computers work · 🔨 02 Internet & protocols · 03 HTTP | 🔨 Phase 02 in progress |
| II — Building LinkBoard | 04 APIs & REST · 05 Browser/frontend · 06 PostgreSQL · 07 Security & auth | ⬜ |
| III — Scaling reads & ops | 08 Caching & Redis · 09 Docker, Nginx & scaling | ⬜ |
| IV — Async & data systems | 10 RabbitMQ/SQS/SNS · 11 Kafka · 12 Elasticsearch · 13 MongoDB & NoSQL | ⬜ |
| V — Real-time & writes | 14 WebSockets · 15 Replication, Cassandra & CAP | ⬜ |
| VI — Production engineering | 16 Observability · 17 Testing · 18 CI/CD · 19 Kubernetes | ⬜ |
| VII — Cloud & advanced design | 20 AWS/GCP/Azure · 21 API design · 22 Architecture & DDD · 23 Data engineering · 24 Advanced security | ⬜ |
| VIII — AI & capstone | 25 AI-native design · 26 Capstone | ⬜ |
