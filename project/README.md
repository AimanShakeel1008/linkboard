# project/ — the LinkBoard codebase

This folder holds the actual, evolving LinkBoard application. It's always
runnable at every stopping point.

## Phase 4 — LinkBoard v1: a JSON REST API (FastAPI)

LinkBoard grew up into a real API on a real framework. Phases 2–3 built an HTTP
server **by hand** from raw sockets to prove nothing is magic; now that we know
what a framework does, we let one (FastAPI) do the boilerplate — routing,
parsing, validation, JSON serialization, and an auto-generated docs page.

- `app.py` — the FastAPI application: resources (links, comments) acted on by
  HTTP verbs. `GET /links`, `GET /links/{id}`, `POST /links`,
  `POST /links/{id}/upvote`, `POST /links/{id}/comments`. Request-journey
  logging on every request.
- `storage.py` — the "database": a single `links.json` file. Every write is an
  unlocked read-modify-write — the **deliberate flaw** this phase exposes.
- `race_demo.py` — fires two simultaneous upvotes and shows the score rise by
  only **one**. A lost vote — the reason Phase 6 brings a real database.
- `requirements.txt` — `fastapi` + `uvicorn`.

### Run it (inside WSL)

```bash
cd /mnt/d/Projects/linkboard/project

# 1. Create a virtual environment and install the dependencies (one time):
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Start the API (auto-reloads when you edit the code):
uvicorn app:app --reload --port 8000
```

Then, in another terminal (or the browser):

```bash
# The interactive, auto-generated API explorer — open in a browser:
#   http://localhost:8000/docs

curl -s localhost:8000/links | python3 -m json.tool          # list links (JSON)
curl -s -X POST localhost:8000/links \
     -H "Content-Type: application/json" \
     -d '{"title":"A great read","url":"https://example.com"}' | python3 -m json.tool   # submit (201)
curl -s -X POST localhost:8000/links/1/upvote | python3 -m json.tool   # upvote link 1
curl -s -X POST localhost:8000/links/1/comments \
     -H "Content-Type: application/json" \
     -d '{"author":"ada","text":"Loved this!"}' | python3 -m json.tool  # comment (201)
```

### See the race condition (the point of the phase)

With the API running in one terminal, in a second terminal:

```bash
python3 race_demo.py     # no venv needed — pure standard library
```

Watch the server's logs: two `[RACE]` lines both read the **same** old score.
The demo reports the score rose by only **1** for **2** votes — a lost update.
The full walkthrough is in the lesson:
[../concepts/phase-04-apis-and-rest/lesson.html](../concepts/phase-04-apis-and-rest/lesson.html)
→ "Run it & watch the logs".

## The earlier, hand-written server is still here

`server.py` (raw-socket HTTP engine) and `slow_client.py` remain from Phases 2–3
— the origin story, still runnable with plain `python3 server.py`. They need no
dependencies. LinkBoard v1 (`app.py`) is the app we build on from here.
