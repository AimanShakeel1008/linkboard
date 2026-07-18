# project/ — the LinkBoard codebase

This folder holds the actual, evolving LinkBoard application.

## Phase 2 — LinkBoard v0: a raw-socket HTTP server

LinkBoard begins life here as an HTTP server built from **raw sockets** — no
web framework, every step narrated in the logs. It serves a tiny hard-coded
list of links so you can see a real request travel from your browser, through
the operating system, into a Python `recv()`, and back out as bytes.

- `server.py` — the server. Handles **one connection at a time, on purpose**
  (Phase 1's blocking-I/O lesson, now on the network). Serves `/` (an HTML
  homepage) and `/about` (plain text); everything else is a 404.
- `slow_client.py` — a client that sends a valid request one byte at a time,
  to prove that one slow visitor freezes the whole single-threaded server.

### Run it (inside WSL)

```bash
cd /mnt/d/Projects/linkboard/project
python3 server.py            # starts on http://localhost:8000 ; Ctrl+C to stop
```

Then, in another terminal (or your browser):

```bash
curl -v localhost:8000       # the homepage, headers and all
curl localhost:8000/about    # the about page
curl -i localhost:8000/nope  # a 404
```

The full walkthrough — including how to stage the "one slow client freezes
everyone" demonstration with `slow_client.py` — is in the lesson:
[../concepts/phase-02-internet-and-protocols/lesson.html](../concepts/phase-02-internet-and-protocols/lesson.html)
→ "Run it & watch the logs".
