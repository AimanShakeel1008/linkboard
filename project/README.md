# project/ — the LinkBoard codebase

This folder holds the actual, evolving LinkBoard application. It's always
runnable at every stopping point.

## Phase 3 — LinkBoard v0.3: a hand-written HTTP server

The Phase 2 raw-socket server grew up. It's still built on raw sockets with no
web framework, but it now takes **HTTP itself** seriously — written by hand so
nothing is magic:

- `server.py` — LinkBoard v0.3. A real (if tiny) HTTP engine: a request parser
  (method, path, all headers, body), a `Response` object with a full
  status-code table, real methods (GET, HEAD, POST, PUT, DELETE), the headers
  that matter (Host, Authorization, Location, Cache-Control, Set-Cookie/Cookie,
  Connection), a working cookie visit-counter at `/count`, and HTTP/1.1
  **keep-alive** (many requests over one TCP connection). Heavily logged.
- `slow_client.py` — a client that sends a valid request one byte at a time, to
  prove the server's **deliberate flaw**: it still handles **one connection at a
  time**, so one slow visitor freezes everyone. (Concurrency is a later phase.)

### Run it (inside WSL)

```bash
cd /mnt/d/Projects/linkboard/project
python3 server.py            # starts on http://localhost:8000 ; Ctrl+C to stop
```

Then, in another terminal, exercise the HTTP features:

```bash
curl -v localhost:8000                                 # homepage (200) + all headers
curl -I localhost:8000                                 # HEAD — headers only, no body
curl -v -L localhost:8000/old-home                     # 301 redirect (Location header)
curl -i localhost:8000/secret                          # 401 (no Authorization)
curl -i -H "Authorization: Bearer x" localhost:8000/secret  # 200 (now allowed)
curl -v -c jar.txt -b jar.txt localhost:8000/count     # cookies — run twice, count climbs
curl -i -X POST -d "title=Hi&url=http://x" localhost:8000/submit  # POST (201, not idempotent)
curl -i -X PUT localhost:8000/links                    # PUT (idempotent)
```

The full walkthrough — expected logs, the status-code/cookie/keep-alive demos,
and "break it" experiments — is in the lesson:
[../concepts/phase-03-http-deep-dive/lesson.html](../concepts/phase-03-http-deep-dive/lesson.html)
→ "Run it & watch the logs". The Phase 2 lesson still has the 3-terminal
`slow_client.py` "one slow client freezes everyone" demonstration.
