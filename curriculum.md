# System Design from Zero — The Complete Curriculum (M1–M32 + AI)

**The Project: "LinkBoard"** — a Hacker News–style link-sharing platform (users submit links, vote, comment, get feeds, search, live updates, and AI features). It starts as a single file and evolves, phase by phase, into a full distributed system: PostgreSQL, Redis, RabbitMQ, Kafka, Elasticsearch, MongoDB, Cassandra, Docker, Nginx, Kubernetes, CI/CD, observability, cloud architecture, and AI (summaries, semantic search, RAG chat).

This curriculum covers **all 32 modules you specified (M1–M32), plus M33: AI Systems** — organized into 27 phases across 8 parts. Every module topic is mapped to a phase (see the Coverage Map at the end); nothing is dropped.

**How this works (your rules, baked in):**
- **Claude writes the code.** You read and understand it.
- **Claude never executes anything — you do.** No installs, no running servers, no git commands from Claude. Everything executable comes to you as a "Run These Steps" block: exact copy-paste commands, what each does, and the exact output to expect. You run them, report back (or paste output), and Claude interprets what the logs prove.
- **The project is always runnable.** At the end of every phase — and every session — the app starts and works end-to-end with documented steps. Never left broken.
- **Logging is a teaching tool.** The code narrates itself in plain language (`[CACHE MISS] homepage not in Redis — falling back to Postgres`) so you can watch requests flow through the system.
- **Every concept is explained twice:** in the lesson document (the *why* and *how*) and inline as code comments (the *what*).
- **Total-beginner explanations, always.** Every lesson assumes zero computer science background. Simplest possible language, everyday analogies, then the technical term. Over-explaining is fine; under-explaining is never allowed (see the Teaching Standard — it is the heart of this project).
- **Challenges are pressure-free:** part of each lesson, with answers hidden in collapsible sections.
- **Every lesson ends with a git commit and push** (commands given to you; you run them).
- **The project spans many sessions.** `PROGRESS.md` is the single source of truth; every new session starts by reading it, so resuming is one word: *"Resume."*

**Pace:** 27 phases. Some take a few days, some a couple of weeks. There is no clock — depth beats speed. Expect a 6–12 month journey done properly. That's not a bug; this is the equivalent of several university courses plus years of on-the-job exposure, compressed and hands-on.

**Prerequisites:** Basic ability to read code in one language (we'll use Python). Everything else — down to "what is a bit" — is taught inside.

**Hardware note:** Later phases run real infrastructure (Kafka, Elasticsearch, Cassandra, Kubernetes) locally via Docker. A machine with 16GB RAM handles everything if you run one stack at a time; each phase's lesson includes exactly what to start and stop.

---

## The Teaching Standard (The Most Important Section)

The non-negotiable quality bar for every explanation in `concepts/`, applying to every module and every line of code:

**1. Assume nothing.** The reader is smart but may have never heard the term. Never use jargon without first explaining it in plain words. If a concept depends on another concept, explain that one too — all the way down to everyday intuition.

**2. Plain language first, precise language second.** Every idea is introduced the way you'd explain it to a curious friend with zero CS background — *then* the technical term is attached. First "a way to find something instantly instead of checking every item one by one," then the word *index*.

**3. Analogies for everything abstract.** Caches, hashes, queues, locks, load balancers, transactions, partitions, consensus — each gets a concrete real-world analogy (a library, a restaurant kitchen, a coat check, a post office). The analogy comes first; the mechanism is mapped onto it. Where the analogy breaks down is called out too, so no wrong intuition sticks.

**4. Over-explaining is welcome; under-explaining is forbidden.** When in doubt, say more. Lessons have no length limit. A reader who knows something can skim; a reader who doesn't can never recover from a gap.

**5. Show, don't just assert.** Back claims with something you can *run and see*: a timing experiment, a deliberately broken example, a before/after measurement, an annotated log trace. "Trust me" is not an explanation.

**6. Define in context and keep a glossary.** First use of a term = inline definition. Every `lesson.md` ends with a glossary of terms it introduced.

**7. Explain the *why*, not just the *how*.** Every design choice answers: what problem does this solve, what were the alternatives, what does it cost us?

**8. No relevant concept is skipped.** If a topic touches a fundamental — what a byte is, what compiling means, how the OS schedules work — it gets explained from scratch, no matter how basic.

If any lesson ever violates this standard, the fix is to expand it, never to trim it.

---

## Repository Structure

```
linkboard/
├── CLAUDE.md                    # Rules for Claude Code (separate file, provided)
├── curriculum.md                # This file — the full plan
├── PROGRESS.md                  # Single source of truth for current state
├── README.md                    # Project overview + how to run it right now
├── concepts/                    # THE LESSONS — one folder per phase
│   ├── phase-00-tools-of-the-trade/lesson.md
│   ├── phase-01-how-computers-work/lesson.md
│   └── ...
└── project/                     # THE ACTUAL CODE — evolves each phase
```

- **`concepts/`** is your textbook: theory, code walkthrough, "Run it & watch the logs," experiments, glossary, collapsible challenges.
- **`project/`** is the living codebase — runnable at every stopping point.
- **`PROGRESS.md`** is how the project survives across sessions.

## Working Across Sessions (The Resume Mechanism)

The repo itself is the memory. **(1) `PROGRESS.md`** always holds: current phase + status, exact next action, current run commands, the full phase checklist, a session log, and — if a session ended mid-phase — a Mid-Phase Checkpoint (what's done, what remains, files touched, precise next step). **(2) The session-start protocol** (in `CLAUDE.md`): every new session, Claude reads `PROGRESS.md` and the current phase here, summarizes where you are, and waits for your go-ahead. **(3) The checkpoint procedure:** say *"let's pause"* and Claude brings the code to a runnable state, writes the checkpoint, and hands you the git commands to commit and push (`(WIP) [checkpoint]` message). Every checkpoint lands on GitHub, so you can resume from any machine. **Your resume ritual is one word: "Resume."**

## How to Drive This with Claude Code

The rules live in the separate **`CLAUDE.md`** (place it in the repo root; Claude Code reads it automatically). Your loop each phase:
1. Open `claude`, say *"Resume"* (or *"Let's do Phase N"*).
2. Read the lesson, then the code it references. Ask "why" freely.
3. Follow "Run it & watch the logs" *yourself* — install, start, curl, click — comparing against the expected output. Paste anything confusing back for interpretation.
4. Run the "break it / observe it" experiments (you execute; Claude explains).
5. Peek at challenge answers whenever you want.
6. Say *"wrap up the phase"* — Claude gives verification steps, updates PROGRESS.md and README, then hands you the git commands.

## The Collapsible-Answer Format

```markdown
### Challenge: Why does the database not just index every column?

<details>
<summary>Show answer</summary>

Every index speeds up reads on that column but must be updated on every
write, costing time and disk space...
</details>
```

You think first, click when ready. Nothing is graded.

---
---

# PART I — BEDROCK (Phases 0–3)

## Phase 0 — Tools of the Trade: Linux & Git
**Covers: M23 (Linux), M28 (Git)** — first, because you'll use both every single day of this journey.

**Concepts:** the terminal as a conversation with the OS; navigating and inspecting (`grep/awk/sed/find/tail`); watching processes (`ps/top/kill`); talking to networks (`curl/dig/netstat/ss`); permissions (`chmod/chown`); SSH, `scp`, `rsync`; `cron`; shell scripting basics. Git from the inside out: the object model (blob/tree/commit), why Git stores snapshots not diffs, branches as movable pointers, merge vs rebase, `cherry-pick`/`bisect`/`reflog` as rescue tools, GitFlow vs trunk-based, semantic versioning.

**Code Claude writes:** a guided "Linux playground" of small scripts and exercises (a log file to grep/awk/sed through, a runaway process to find and kill, a cron job that appends to a file), plus the repo skeleton and PROGRESS.md. **You** run `git init`, connect GitHub, and make the first push — commands provided step-by-step.

**End of lesson:** first commit + push (you run the commands — as with every phase from here on).

## Phase 1 — How a Computer Actually Works
**Covers: M6 (Computers), M7 (OS)**

**Concepts:** binary, bits, bytes (why computers only know two symbols, and how that becomes everything); CPU, cores, and the L1/L2/L3 cache staircase; RAM vs storage; HDD vs SSD and why the difference reshapes system design; what happens between writing code and the CPU executing it (compile → execute, interpreters); processes and threads (an apartment-vs-roommates analogy); context switching and its cost; the kernel as the building superintendent; virtual memory and paging (every process gets a "fake" private address space); file systems; blocking vs non-blocking I/O (the single most important idea for understanding servers); system calls — the doorbell between your program and the kernel.

**Code Claude writes:** tiny runnable demos with narrated logs — a script contrasting sequential disk reads vs random reads (timed), a process-spawning demo, a thread demo where two threads garble shared state, and a blocking-I/O demo you'll feel again in Phase 4.

## Phase 2 — The Internet & Protocols
**Covers: M1 (Internet), M2 (Protocols)**

**Concepts:** internet vs the web (roads vs the trucks driving on them); packets and routers (letters and post offices); IP addresses, IPv4 vs IPv6, DHCP; the DNS resolution chain (root → TLD → authoritative) and TTL; the full journey URL → DNS → TCP → HTTP → render; bandwidth vs latency (width of the pipe vs length of the pipe); the OSI 7-layer model in plain terms; TCP vs UDP (certified mail vs shouting); the TCP three-way handshake; ports; firewalls; NAT (why your laptop's IP isn't its "real" internet address); VPNs.

**Code Claude writes:** the LinkBoard origin story — an HTTP server built from **raw sockets**, no framework, logging every step (`[SOCKET] listening on :8000`, `[CONN] accepted 127.0.0.1`, `[HTTP] parsed GET /`), plus a slow-client script so you can watch blocking happen live, and `dig`/`curl` field exercises tracing DNS and TCP yourself.

## Phase 3 — HTTP Deep Dive
**Covers: M3 (HTTP)**

**Concepts:** request/response and what "stateless" really means; anatomy of a request (method, path, headers, body — it's just structured text); every important method + idempotency (why PUT is retry-safe and POST isn't); status code families with the codes worth memorizing; headers that matter (`Content-Type`, `Authorization`, `Cache-Control`, `Set-Cookie`…); HTTP/1.1 vs /2 vs /3-QUIC (one lane → multiplexed lanes → rebuilt on UDP); HTTPS and the TLS handshake step by step; cookies; sessions vs JWT introduced conceptually here (practiced hands-on in Phase 7).

**Code Claude writes:** upgrades the raw-socket server into a proper mini HTTP parser (methods, headers, status codes — handwritten so nothing is magic), plus experiments inspecting real headers with `curl -v` against major websites.

---

# PART II — BUILDING LINKBOARD (Phases 4–7)

## Phase 4 — LinkBoard v1: APIs & REST
**Covers: M9 (APIs — API concept, REST, JSON, XML vs JSON vs Protobuf, rate limiting & webhooks conceptually; auth in Phase 7; GraphQL deepened in Phase 21)**

**Concepts:** what an API is (a restaurant menu — you order by name, the kitchen is hidden); REST resource design; JSON and serialization (how objects become bytes on a wire); XML vs JSON vs Protobuf tradeoffs; why frameworks exist; webhooks ("don't call us, we'll call you"); plus data-structure fundamentals in context — hash maps (O(1) lookup, the soul of routing/caching/indexing), arrays vs linked lists, big-O as "what happens at 1000x".

**Code Claude writes:** LinkBoard v1 — FastAPI app: submit link, list links, upvote, comment; JSON-file storage; request-journey logging (`[REQUEST] POST /links`, `[STORE] writing links.json`). Plus a two-simultaneous-upvotes script so you watch a race condition eat a vote in the logs — your first taste of why databases exist.

## Phase 5 — The Browser: LinkBoard Gets a Face
**Covers: M4 (Browser — rendering engine, DOM, critical render path, browser cache, cookie/localStorage/sessionStorage, CORS + preflight; WebSockets get their own moment in Phase 14)**

**Concepts:** what a rendering engine does; the DOM as a live family tree of the page; the critical render path (why pages feel slow); browser caching; cookie vs localStorage vs sessionStorage (three drawers with different rules); CORS and preflight requests — explained by *hitting the CORS wall yourself* and then understanding why browsers built it.

**Code Claude writes:** a clean vanilla HTML/JS/CSS frontend for LinkBoard (list, submit, vote, comment) served separately from the API so CORS breaks on purpose — then the fix, with the preflight `OPTIONS` request visible in the logs.

## Phase 6 — Databases: PostgreSQL
**Covers: M8 (Databases) + PostgreSQL-advanced from M15 (JSONB, window functions, CTEs)**

**Concepts:** why databases exist (what your JSON file couldn't do); SQL from zero; primary/foreign/composite keys; B-tree indexes (a library card catalog — and why databases chose B-trees over other structures); ACID with the vote race as the running example; normalization and when to denormalize; SQL vs NoSQL (the honest tradeoff, previewing Part IV); connection pooling (why opening a connection per request kills you); JSONB, window functions, CTEs; reading `EXPLAIN ANALYZE`; the N+1 problem.

**Code Claude writes:** full migration to Postgres (users, links, votes, comments), a 1M-row seed script, query timing in the logs (`[DB] feed query 230ms` → `4ms` after indexing), the transaction fix for the race, an N+1 found and fixed, and window-function queries powering "top links this week."

## Phase 7 — Security Basics & Authentication
**Covers: M10 (Security Basics) + M3.9 (sessions vs JWT, hands-on)**

**Concepts:** symmetric vs asymmetric encryption (shared secret vs padlock-and-key); hashing + salting (a fingerprint, not a lockbox — and why you *can't* "decrypt" a password); why password hashing must be *slow* (bcrypt/argon2) while other hashing is fast; TLS certificates and how trust chains work; authentication vs authorization (who are you vs what may you do); SQLi, XSS, CSRF, MITM — each demonstrated safely against your own app, then fixed; correct password storage; sessions vs JWT in practice and why the choice matters enormously in Phase 9.

**Code Claude writes:** signup/login with salted-hash passwords, session auth (JWT variant shown side-by-side), a token-bucket rate limiter (`[RATELIMIT] user 42: 3 tokens left`), a deliberately vulnerable endpoint you exploit with SQLi and then fix with parameterized queries, and a CSRF demo + defense.

---

# PART III — SCALING READS & OPS BASICS (Phases 8–9)

## Phase 8 — Caching & Redis, In Depth
**Covers: M5 (Caching), M11 (Redis — complete)**

**Concepts:** the speed hierarchy + latency numbers worth memorizing; browser cache headers; CDNs (moving bytes closer to humans); server-side caching patterns (cache-aside, write-through, write-behind); invalidation + TTL ("one of the two hard problems"); eviction — LRU/LFU/FIFO (LRU implemented from scratch: hash map + doubly linked list); cache stampede and prevention; what *not* to cache. Then Redis properly: every data structure (string, hash, list, set, sorted set, stream) with a LinkBoard use for each; RDB vs AOF persistence; pub/sub; MULTI/EXEC transactions; the classic use cases — cache, session store, rate limiter, leaderboard, distributed lock — *each built into LinkBoard*; Redis Cluster and Sentinel conceptually; Redis vs Memcached.

**Code Claude writes:** Redis cache-aside on the homepage (`[CACHE HIT] homepage (2ms)` vs `[CACHE MISS] → Postgres (48ms) → cached 30s`); sessions moved to Redis; the rate limiter rebuilt on Redis; a **trending-links leaderboard on a sorted set**; a distributed lock demo; a stampede demonstration + fix; and a load-test script (before/after req/sec numbers go in the lesson).

## Phase 9 — Docker, Nginx & Horizontal Scaling
**Covers: M19 (Docker), M22 (Nginx)**

**Concepts:** image vs container (recipe vs cooked dish); Dockerfile instructions (FROM/RUN/COPY/CMD) and image layers; container networking (bridge/overlay); volumes; docker-compose; containers vs VMs (namespaces + cgroups in plain words). Nginx: reverse proxy, SSL termination, load balancing with `upstream` (round-robin, least-connections), rate limiting at the edge; Nginx vs Apache. Plus the scaling ideas these unlock: vertical vs horizontal scaling, statelessness (the Phase 7/8 payoff — sessions in Redis mean *any* instance can serve *any* request), health checks, failover, and naming your single points of failure.

**Code Claude writes:** Dockerfiles + a compose stack running **3 LinkBoard instances behind Nginx** with Postgres and Redis; instance names in every log line (`[app-2] [REQUEST] GET /links`) so you literally watch round-robin distribute traffic; a kill-an-instance-mid-load-test script so you watch failover happen; local self-signed TLS termination at Nginx.

---

# PART IV — ASYNC & DATA SYSTEMS (Phases 10–13)

## Phase 10 — Message Queues: RabbitMQ, SQS & SNS
**Covers: M17 (RabbitMQ), M18 (SQS + SNS)**

**Concepts:** why slow work leaves the request path (sync vs async); AMQP's cast of characters — producer, exchange, queue, binding, consumer (a mail room analogy); all four exchange types (direct/topic/fanout/headers) with a LinkBoard use for each; manual vs auto-ack; dead-letter queues; persistence; at-least-once vs at-most-once, why "exactly once" is mostly a lie, and idempotent consumers as the answer; backpressure. Then the managed-cloud versions: SQS (standard vs FIFO, visibility timeout, DLQ) and SNS (pub/sub fan-out) — and the honest comparison table vs Kafka (previewing Phase 11).

**Code Claude writes:** a RabbitMQ worker for comment notifications with the full journey logged (`[API] published → exchange 'events'`, `[WORKER] got job id=abc123 (attempt 1)`, `[WORKER] done 340ms`); a topic-exchange demo routing different event kinds; a poison message landing in a DLQ; a kill-the-worker-mid-job experiment proving redelivery; idempotency keys so retries can't double-send.

## Phase 11 — Kafka & Event Streaming
**Covers: M16 (Kafka — complete)**

**Concepts:** the log as a data structure (an append-only diary — this idea also underlies database replication, seen again in Phase 15); topics, partitions, offsets, brokers; the producer side (keys, partitioner, batching); consumer groups and lag; why ordering is guaranteed per-partition only; retention and compaction (a queue that *remembers*); at-least-once vs exactly-once semantics honestly; Kafka Connect and CDC (databases broadcasting their changes); Kafka Streams conceptually; Schema Registry and why schemas need governance; Kafka vs RabbitMQ vs SQS — when each is right.

**Code Claude writes:** an `activity` event stream — every view/vote/comment becomes an event; a consumer group recomputing trending scores from the stream; a second consumer group (analytics counter) reading the *same* events independently — the aha-moment Kafka demo; lag made visible in logs while you pause a consumer; a keyed-partitioning experiment proving per-key ordering.

## Phase 12 — Search: Elasticsearch & the ELK Idea
**Covers: M14 (Elasticsearch — complete)**

**Concepts:** why `LIKE '%rust%'` can't scale; the inverted index (a book's index page — word → locations), built tiny by hand first; documents, indices, shards, replicas; relevance scoring with BM25 in plain words (rare words matter more; short fields matter more); query DSL (match/term/bool); aggregations; the ELK stack (Logstash → Elasticsearch → Kibana) — which returns for log search in Phase 16; tokenization and stemming.

**Code Claude writes:** Elasticsearch indexing for links + comments with a sync pipeline from Postgres; a search endpoint returning ranked results; a three-way side-by-side comparison endpoint — SQL `LIKE` vs Postgres FTS vs Elasticsearch — with timings and result quality logged so the difference is *felt*, not asserted.

## Phase 13 — The NoSQL Landscape: MongoDB & Choosing Databases
**Covers: M12 (MongoDB — complete) + M15 remainder (DynamoDB intro, ClickHouse/Neo4j/InfluxDB conceptually, choosing the right DB; DynamoDB deepened in Phase 15, ClickHouse hands-on in Phase 23)**

**Concepts:** the document model and BSON (storing the whole "file folder" together vs shredding across tables); collections; index types (single/compound/text/geo); the aggregation pipeline ($match/$group/$lookup) as an assembly line; replica sets; sharding and the shard-key decision; MongoDB's ACID transactions; the honest MongoDB vs PostgreSQL comparison. Then the wider map: DynamoDB (partition key, GSI/LSI), Neo4j (graphs and Cypher — "friends of friends"), InfluxDB (time-series), ClickHouse (columnar OLAP) — each in plain terms with the question that matters: *how do I choose?*

**Code Claude writes:** LinkBoard's **activity feed documents** moved to MongoDB (a genuinely document-shaped workload), an aggregation pipeline powering "your weekly digest," and a written **database decision matrix** for every store LinkBoard now touches — the artifact interviewers love.

---

# PART V — REAL-TIME & SCALING WRITES (Phases 14–15)

## Phase 14 — Real-Time: WebSockets & Live Updates
**Covers: M4.7 (WebSockets) + Redis pub/sub in anger**

**Concepts:** the escalation ladder — polling → long-polling → SSE → WebSockets — and the true cost of each; the handshake that upgrades HTTP into a two-way phone line; persistent connections vs your stateless architecture (a socket lives on ONE server → Redis pub/sub broadcasts across instances); heartbeats, reconnection; what open connections cost (file descriptors, memory, the C10K problem); event loops properly understood (why async exists).

**Code Claude writes:** live comments and vote counters — no refresh — across all 3 instances, the cross-instance hop visible in logs: `[app-1] [WS] comment on link 7 → publishing`, `[app-3] [WS] received via pub/sub → pushing to 4 clients`.

## Phase 15 — Scaling Writes: Replication, Cassandra & CAP
**Covers: M13 (Cassandra — complete) + DynamoDB from M15 + replication/sharding/CAP fundamentals**

**Concepts:** read replicas and replication lag (you upvote, refresh, your vote is "gone" — read-your-own-writes); sync vs async replication; the write-ahead log — the same append-only-diary idea from Kafka, now powering replication and crash recovery; leader election conceptually; sharding (range vs hash); **consistent hashing and the ring** (why naive `hash % N` reshuffles everything); Cassandra top to bottom — wide-column model, partition key + clustering key, replication factor, tunable consistency (ONE/QUORUM/ALL), eventual consistency, the write path (commitlog → memtable → SSTable), compaction, and when Cassandra is the right tool; DynamoDB as the managed cousin (partition key, GSI/LSI); CAP stated honestly (during a partition: consistency or availability) + PACELC; network partitions and clock skew — why "what happened first?" is genuinely hard.

**Code Claude writes:** a Postgres read replica with routing logged (`[DB-ROUTER] write → primary`, `read → replica (lag 120ms)`) and a read-your-own-writes fix; a 3-node Cassandra compose stack storing **vote counters**, with a consistency-level experiment — write at ONE, read at ONE vs QUORUM, and *watch stale reads happen and then disappear* in the logs; a written sharding design for LinkBoard at 500M users.

---

# PART VI — PRODUCTION ENGINEERING (Phases 16–19)

## Phase 16 — Observability
**Covers: M26 (complete)**

**Concepts:** the three pillars — metrics (how much/how fast), logs (what happened), traces (where time went); Prometheus's pull model and PromQL; Grafana dashboards and alerts; the ELK stack for log search (Elasticsearch returns!); distributed tracing with OpenTelemetry/Jaeger — one request ID followed across app → queue → worker; Datadog/New Relic as the managed versions; percentiles (why p99 matters and averages lie); SLI/SLO/SLA + error budgets; alerting best practices (alert on symptoms, not causes); Little's Law — the one queueing formula explaining why systems collapse *suddenly*.

**Code Claude writes:** Prometheus + Grafana (req/sec, p50/p99, cache hit rate, queue depth, DB connections, consumer lag); structured JSON logging with request IDs shipped into Elasticsearch and searched in Kibana; OpenTelemetry tracing across the whole request path; graceful degradation (`[DEGRADED] Redis unreachable — serving stale homepage`); and a **chaos hour**: kill Redis under load, watch the dashboard, survive.

## Phase 17 — Testing
**Covers: M29 (complete)**

**Concepts:** the testing pyramid (unit/integration/e2e) and why it's a pyramid, not a column; TDD's red-green-refactor loop, actually practiced; test doubles disentangled — mock vs stub vs spy vs fake; contract testing (Pact) — how services promise not to break each other; load testing with k6; chaos engineering as a discipline (what Phase 16's chaos hour becomes when done on purpose, with hypotheses).

**Code Claude writes:** a real test suite for LinkBoard — unit tests for scoring/rate-limiting logic, integration tests against real Postgres/Redis (via compose), an e2e happy-path test, one feature built strictly TDD so you watch red→green→refactor happen, k6 load scenarios with pass/fail thresholds, and a documented chaos experiment.

## Phase 18 — CI/CD
**Covers: M21 (complete)**

**Concepts:** pipeline stages (build → test → package → deploy); GitHub Actions anatomy (Jenkins compared conceptually); deployment strategies — rolling, blue-green, canary — with restaurant-menu-change analogies; feature flags (deploy ≠ release); Infrastructure as Code (Terraform/Ansible conceptually — infrastructure as a recipe, not a memory); GitOps and ArgoCD (the repo as the source of truth for what's *running* — the same idea as your PROGRESS.md, applied to production).

**Code Claude writes:** a GitHub Actions workflow that runs your Phase 17 suite on every push (runs on GitHub's machines — you just push and watch), builds the Docker image, and (optionally) publishes it; a homemade feature-flag system in LinkBoard with a flag-guarded feature; a written deployment-strategy decision doc.

## Phase 19 — Kubernetes
**Covers: M20 (complete)**

**Concepts:** why orchestration exists (compose is a house; K8s is a city with a planning department); Pods, Deployments, Services, Ingress, ConfigMaps, Secrets — each mapped to something LinkBoard already has; the scheduler; ClusterIP vs NodePort vs LoadBalancer; HPA (autoscaling); rolling updates and rollbacks; PV/PVC for state; Helm as the package manager; the kubectl essentials you'll actually use.

**Code Claude writes:** full K8s manifests for LinkBoard on a local **kind** cluster — Deployments for app/worker, Services, Ingress, ConfigMaps/Secrets; an HPA experiment (load-test and watch replicas scale in `kubectl get pods -w`); a rolling update deployed and then rolled back on purpose; a starter Helm chart.

---

# PART VII — CLOUD & ADVANCED DESIGN (Phases 20–24)

## Phase 20 — Cloud: AWS, GCP & Azure
**Covers: M24 (AWS — complete), M25 (GCP + Azure)**

**Concepts:** the mental model — everything you built by hand has a rentable managed equivalent; compute (EC2/Lambda/ECS/EKS — and the serverless tradeoff); storage (S3/EBS/EFS — object vs block vs file, explained with a warehouse/hard-drive/shared-folder analogy); databases (RDS/Aurora/DynamoDB/ElastiCache); networking (VPC, security groups, Route53, CloudFront); messaging (SQS/SNS/EventBridge); IAM (the permission system everything else depends on); CloudWatch; the Well-Architected pillars; then the translation table to GCP (Compute Engine/Cloud Run/GKE/BigQuery/Pub-Sub) and Azure (VMs/AKS/Blob/Service Bus); the shared responsibility model.

**Code Claude writes:** the **"LinkBoard on AWS" architecture document** — every container in your compose file mapped to its AWS/GCP/Azure service with reasoning and rough monthly cost math; Terraform snippets *read as literature* (understanding IaC without needing a paid account); an optional free-tier walkthrough (S3 static hosting + one Lambda) with exact steps if you want hands-on — the phase is complete without spending money.

## Phase 21 — Advanced API Design
**Covers: M30 (complete) + M9's GraphQL deepened**

**Concepts:** OpenAPI/Swagger — the API contract as a machine-readable document; gRPC + Protocol Buffers (binary contracts, streaming, why internal services love it); GraphQL properly — schema, resolvers, the N+1-resolver trap and DataLoader; API versioning strategies and their costs; API gateways (Kong/AWS API Gateway) — one front door for auth, rate limiting, routing; documentation as a first-class deliverable.

**Code Claude writes:** an OpenAPI spec for LinkBoard with auto-generated Swagger UI; a small internal **gRPC trending service** (proto file + server + client) so REST vs gRPC is felt; a GraphQL endpoint over LinkBoard data with a DataLoader fixing the resolver N+1 — visible in the query logs.

## Phase 22 — Architecture Patterns & DDD
**Covers: M27 (complete)**

**Concepts:** Layered architecture; Hexagonal / ports-and-adapters (the app core as a machine with sockets; Postgres/Redis just plug in); Clean Architecture's dependency rule (dependencies point *inward*); event-driven architecture (which LinkBoard already *is* — now named and formalized); CQRS (separate the write path from the read path — your cache and Kafka consumers were already doing this); Event Sourcing (store the events, derive the state — your Kafka activity stream, taken seriously); the Saga pattern for cross-service transactions, choreography vs orchestration; Strangler Fig (how real systems migrate); Sidecar; DDD essentials — bounded contexts, aggregates, ubiquitous language.

**Code Claude writes:** a refactor of one LinkBoard slice (voting) into hexagonal shape — same behavior, dependencies inverted, with a before/after dependency diagram; an explicit CQRS read model for the feed; a saga worked example (account deletion across Postgres + Mongo + Elasticsearch) with compensating actions logged when a step fails on purpose.

## Phase 23 — Data Engineering
**Covers: M31 (complete) + ClickHouse hands-on from M15**

**Concepts:** OLTP vs OLAP (cash registers vs the accountant's office); row vs columnar storage and why analytics loves columns; data warehouses (Snowflake/BigQuery/Redshift) vs data lakes; ETL vs ELT; batch (Spark) vs streaming (Flink/Kafka Streams) processing; Parquet; orchestration with Airflow and transformation with dbt (conceptually); CDC with Debezium — your Postgres broadcasting its changes into Kafka, closing a loop opened in Phase 11.

**Code Claude writes:** a real mini data platform — Kafka activity events landed as **Parquet** files, loaded into **ClickHouse**, with analytics queries (daily actives, retention cohorts, top domains) that visibly crush Postgres on the same questions (timings logged side-by-side); a cron-driven mini-pipeline with Airflow-style structure; a Debezium CDC demo streaming Postgres changes into Kafka.

## Phase 24 — Advanced Security
**Covers: M32 (complete)**

**Concepts:** OAuth2 flows properly — authorization code (+PKCE), client credentials — told as a story (valet keys, hotel check-in); OIDC ("log in with Google", demystified); JWT deep dive — HS256 vs RS256, expiry, refresh-token rotation; secrets management and Vault (why secrets don't belong in code or env files at scale); zero trust and mTLS (services proving identity to *each other*); the OWASP Top 10 as an audit checklist applied to LinkBoard; DDoS and WAFs; SAST/DAST scanning wired into CI.

**Code Claude writes:** **"Login with GitHub"** OAuth2/OIDC for LinkBoard with every redirect and token exchange logged so the flow is visible; JWT refresh-token rotation; a Vault dev-server demo replacing env-file secrets; a written OWASP Top-10 audit of LinkBoard (findings + fixes); a security-scan job added to the Phase 18 pipeline.

---

# PART VIII — AI & CAPSTONE (Phases 25–26)

## Phase 25 — AI-Native System Design
**Covers: M33 (AI — the module your list didn't include, added by design)**

The newest chapter of system design — and it *reuses* everything: queues (Phase 10) for async AI jobs, streaming (Phase 14) for token-by-token responses, caching (Phase 8) for cost control, circuit breakers (Phase 16) for a flaky dependency, vector search as the semantic sibling of Phase 12's inverted index.

**Concepts:** an LLM is just a dependency — a slow, expensive, occasionally-wrong HTTP API — so treat it like one (timeouts, retries, fallbacks, circuit breakers); sync vs async AI (summaries → queue; chat → streaming); what a token is; next-token prediction intuition for how LLMs work; embeddings — meaning turned into a list of numbers — and cosine similarity with everyday geometry; vector databases and ANN indexes (HNSW) vs exact search; RAG — retrieve → augment → generate — chunking, grounding, citations, and when RAG beats fine-tuning; cost engineering — semantic caching (cache *similar* prompts, not just identical ones), batching, the model-router pattern, the latency-cost-quality triangle; AI in production safely — prompt injection (user content entering prompts is *untrusted input* — Phase 7 returns), guardrails, evals as the unit tests of AI features, model versioning and A/B tests; the ML big picture — training vs inference, why GPUs, batch vs real-time inference, feature stores, recommendation architecture (candidate generation → ranking), data flywheels.

**Code Claude writes:** async AI link summaries via the queue with cost in the logs (`[AI] link 42: 1,204 tokens in → 2.3s ($0.0031)`); semantic search + "related links" with pgvector, side-by-side with Phase 12's Elasticsearch so you can compare keyword vs meaning; **"Chat with LinkBoard"** — a RAG endpoint streaming tokens over the Phase 14 plumbing (`[RAG] query embedded (12ms) → top 5 chunks (18ms) → generating…`); a semantic cache + AI cost panel on the Grafana dashboard; AI comment moderation as a queue consumer; a prompt-injection attack (a malicious link title hijacking the summarizer) demonstrated, then defended.

**Practical note:** needs an LLM API key (your Anthropic key works) stored as a secret — Phase 24's secrets practice, applied. Designed to cost only a few dollars total.

## Phase 26 — Capstone: Design Docs & the Interview Layer

1. **The LinkBoard Design Document** — as if proposing it at a company: requirements; back-of-envelope math (DAU → QPS → storage/year → bandwidth); the full architecture diagram spanning everything from Part I to Part VIII; data model; every major decision with alternatives considered (your per-phase decision docs feed straight in).
2. **Back-of-envelope drills** — worked estimates for LinkBoard at 10M DAU and five other systems (chat app, video upload, ride-sharing…), including token/GPU cost math.
3. **Mock interviews** — Claude plays interviewer for the classics (URL shortener, news feed, notification system, rate limiter) and the modern AI prompts (ChatGPT-style app, semantic search, ML-ranked feed), pushing on your choices, then explaining a strong answer. By now you've *lived* every component in this curriculum — these read as review, not memorization.

**End:** final commit + push, and a README that reads like a portfolio piece.

---
---

## Module → Phase Coverage Map (all 32 + AI)

| Module | Phase(s) |
|---|---|
| M1 Internet | 2 |
| M2 Protocols | 2 |
| M3 HTTP | 3 (sessions/JWT practice: 7) |
| M4 Browser | 5 (WebSockets: 14) |
| M5 Caching | 8 |
| M6 Computers | 1 |
| M7 OS | 1 |
| M8 Databases | 6 |
| M9 APIs | 4 (auth: 7; rate limiting: 7–8; GraphQL deep: 21) |
| M10 Security Basics | 7 |
| M11 Redis | 8 |
| M12 MongoDB | 13 |
| M13 Cassandra | 15 |
| M14 Elasticsearch | 12 (ELK for logs: 16) |
| M15 Other DBs | 6 (PG advanced), 13 (landscape + choosing), 15 (DynamoDB), 23 (ClickHouse) |
| M16 Kafka | 11 (CDC hands-on: 23) |
| M17 RabbitMQ | 10 |
| M18 SQS + SNS | 10 (cloud context: 20) |
| M19 Docker | 9 |
| M20 Kubernetes | 19 |
| M21 CI/CD | 18 |
| M22 Nginx | 9 |
| M23 Linux | 0 (used daily thereafter) |
| M24 AWS | 20 |
| M25 GCP + Azure | 20 |
| M26 Observability | 16 |
| M27 Architecture Patterns | 22 |
| M28 Git | 0 (used daily thereafter) |
| M29 Testing | 17 |
| M30 API Design | 21 |
| M31 Data Engineering | 23 |
| M32 Advanced Security | 24 |
| **M33 AI Systems** | **25** |

*Anything relevant that isn't on this list still gets explained the moment LinkBoard touches it. The list is a floor, not a ceiling.*

## Principles for the Journey

1. **Over-explain, never under-explain.** The Teaching Standard governs everything. Every lesson is written for a total beginner. A lesson is too short before it is ever too long.
2. **Always runnable, always narrating.** The app works at every stopping point, and its logs teach you the flow of every request.
3. **Break it before you fix it.** Every phase's problem is *felt* (via a load test or deliberate bug) before the solution is learned.
4. **Measure everything.** Before/after numbers go into each lesson.
5. **Claude writes; you understand — and you execute.** Claude never runs a single command. Every install, run, experiment, and git push happens through your hands, guided by exact steps with expected output. Asking for *more* detail always gets you deeper and simpler, never shorter.
6. **Answers are always available.** Challenges ship with collapsible answers — think first, reveal freely.
7. **The repo is the memory.** `PROGRESS.md` + checkpoints mean any session resumes exactly where you left off, from any machine.
8. **Commit and push every phase.** Your GitHub history becomes proof of the journey.
9. **One stack at a time.** Later phases include stop/start instructions so your machine never runs Kafka + Cassandra + Elasticsearch + K8s simultaneously.
10. **No module left behind.** All 32 modules + AI are mapped; if a phase touches something basic, it's explained from scratch.
11. **Don't skip Part I.** Everyone wants to. Everyone regrets it.
