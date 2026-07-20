#!/usr/bin/env python3
"""
LinkBoard v0.3 — a hand-written HTTP server on raw sockets. Still no framework.

WHERE WE CAME FROM (Phase 2):
    The Phase 2 server proved a web server is not magic: open a socket, accept a
    connection, read the bytes (which are just text), write bytes back, hang up.
    But it barely understood HTTP. It grabbed the first line, glanced at the
    method and path, ignored every header, spoke only GET, and slammed the
    connection shut after a single response.

WHAT PHASE 3 ADDS (this file):
    We take HTTP itself seriously and build a real (if tiny) HTTP engine BY HAND,
    so nothing about the protocol stays mysterious:
      * A proper request PARSER (parse_request): request line + all headers into a
        case-insensitive dict + a body read by Content-Length. Malformed input is
        rejected with a real 400, not a crash.
      * A Response OBJECT with a full status-code table (200, 201, 301, 400, 401,
        404, 405, 500 ...), a headers dict, and correct byte serialization.
      * Real methods: GET and HEAD (HEAD = "headers only, no body"), plus POST /
        PUT / DELETE routes that demonstrate idempotency (PUT/DELETE are retry-safe,
        POST is not).
      * Headers that matter, used for real: Host, User-Agent, Accept, Content-Type,
        Content-Length, Authorization (a 401 gate), Location (a 301 redirect),
        Cache-Control, and Set-Cookie / Cookie (a working visit counter).
      * HTTP/1.1 KEEP-ALIVE: one TCP connection now carries MANY requests instead
        of one. This is Phase 2's "reuse the connection so you pay the handshake
        toll once" made real — watch the logs show request #1, #2, #3 all on the
        same connection before it closes.

WHAT WE DELIBERATELY DID *NOT* FIX (still the teaching flaw):
    The server still handles ONE CONNECTION AT A TIME. Keep-alive means one client
    can now hold the single slot across several requests, so a slow or idle client
    can still freeze everyone else (try slow_client.py again). Concurrency is a
    later phase's job; feeling the limit is this phase's job.

Run it (from WSL):
    cd /mnt/d/Projects/linkboard/project
    python3 server.py
Then, in another terminal:
    curl -v localhost:8000                 # homepage, watch the headers
    curl -I localhost:8000                 # a HEAD request (headers only)
    curl -v -c jar.txt -b jar.txt localhost:8000/count   # cookies, run it twice
    curl -v -X POST -d 'title=Hi&url=http://x' localhost:8000/submit
Stop it with Ctrl+C.
"""

import socket
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HOST = "0.0.0.0"   # accept connections on any of this machine's addresses
PORT = 8000        # high, unreserved port (ports < 1024 need admin rights)

# How long we wait for the FIRST byte of a request. If a freshly-accepted
# connection says nothing for this long, we hang up (browsers open silent
# spare connections that never speak).
CLIENT_TIMEOUT_SECONDS = 5.0

# HTTP/1.1 keep-alive: after answering a request we hold the SAME connection
# open, hoping the client sends another request over it (saving a fresh TCP
# handshake). If it stays silent this long, we close the connection and move on.
KEEPALIVE_TIMEOUT_SECONDS = 5.0

# The most requests we'll serve on one connection before insisting on a fresh
# one. A politeness limit real servers set too, so one client can't camp forever.
KEEPALIVE_MAX_REQUESTS = 100

# ---------------------------------------------------------------------------
# LinkBoard's entire "database" (still just a Python list in memory).
# Phase 6 gives us a real database. Restarting the server forgets every edit —
# that fragility is on purpose; you'll feel WHY databases exist later.
# ---------------------------------------------------------------------------

LINKS = [
    {"title": "How a computer actually works (our Phase 1 lesson)",
     "url": "https://example.com/phase-1", "points": 42},
    {"title": "The tail of the packet: what routers do all day",
     "url": "https://example.com/routers", "points": 17},
    {"title": "DNS: the internet's phone book, explained",
     "url": "https://example.com/dns", "points": 31},
    {"title": "Sockets from scratch (you are reading its output right now)",
     "url": "https://example.com/sockets", "points": 55},
]


# ---------------------------------------------------------------------------
# Logging — the teaching tool. Every significant step narrates itself.
# ---------------------------------------------------------------------------

def log(tag: str, message: str) -> None:
    """Print one narrated, timestamped log line, flushed immediately so the
    logs never lag behind reality (Python buffers stdout by default)."""
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # trim to milliseconds
    print(f"{now} [{tag}] {message}", flush=True)


# ===========================================================================
# PART 1 — THE STATUS-CODE TABLE
#
# A status code is a THREE-DIGIT number the server sends so the client instantly
# knows how the request went, without reading the page. The first digit is the
# "family" — the gist — and the rest is the specific case:
#     1xx  informational  ("hold on, still going")
#     2xx  success        ("here you go")
#     3xx  redirection    ("it's somewhere else")
#     4xx  client error   ("YOU messed up — bad request, not allowed, not found")
#     5xx  server error    ("*I* messed up")
# Each code has a short "reason phrase" — human text that rides alongside the
# number. Clients act on the NUMBER; the phrase is for humans reading logs.
# ===========================================================================

REASON_PHRASES = {
    200: "OK",                     # success, body follows
    201: "Created",                # a POST/PUT made a new thing
    204: "No Content",             # success, but deliberately no body
    301: "Moved Permanently",      # redirect; update your bookmarks
    302: "Found",                  # redirect; temporary
    304: "Not Modified",           # your cached copy is still good (Phase 8)
    400: "Bad Request",            # we couldn't parse what you sent
    401: "Unauthorized",           # you didn't authenticate (really "unauthenticated")
    403: "Forbidden",              # we know who you are; you still can't
    404: "Not Found",              # no such path
    405: "Method Not Allowed",     # right path, wrong verb
    500: "Internal Server Error",  # our fault; something threw
    501: "Not Implemented",        # we don't support that method at all
}


# ===========================================================================
# PART 2 — THE REQUEST PARSER
#
# An HTTP request is just text with a strict shape. Here is a real one, with the
# invisible line-endings shown as \r\n (carriage-return + line-feed):
#
#     POST /submit HTTP/1.1\r\n        <- request line: METHOD PATH VERSION
#     Host: localhost:8000\r\n         <- a header: "Name: value"
#     Content-Type: application/x-www-form-urlencoded\r\n
#     Content-Length: 21\r\n           <- how many BODY bytes follow the blank line
#     \r\n                             <- ONE blank line = "headers are over"
#     title=Hi&url=http://x            <- the body (only present on POST/PUT/...)
#
# Parsing it means: split off the first line, collect the "Name: value" header
# lines into a dictionary, and (if Content-Length says so) read exactly that many
# more bytes as the body. We do every step by hand.
# ===========================================================================

class BadRequest(Exception):
    """Raised when the bytes we got are not valid HTTP. We turn this into a
    real 400 response instead of letting the server crash on junk input."""


class Request:
    """One parsed HTTP request. Just a tidy holder for the pieces we pulled
    out of the raw bytes, so routing code can read `req.method`, `req.path`,
    `req.header("user-agent")`, `req.cookies`, `req.body` and stay readable."""

    def __init__(self, method, path, version, headers, body):
        self.method = method            # "GET", "POST", ...
        self.path = path                # "/submit"
        self.version = version          # "HTTP/1.1"
        self.headers = headers          # dict, keys already lower-cased
        self.body = body                # bytes (may be b"")
        self.cookies = _parse_cookies(headers.get("cookie", ""))

    def header(self, name, default=""):
        """Look up a header case-insensitively. HTTP header names are
        case-INsensitive ('Host' == 'host' == 'HOST'), so we lower-case every
        name at parse time and here, and callers never have to worry about it."""
        return self.headers.get(name.lower(), default)

    def wants_keep_alive(self):
        """Does the client want to reuse this connection for more requests?
        The rule is version-dependent:
          * HTTP/1.1 defaults to keep-alive UNLESS the client says 'Connection: close'.
          * HTTP/1.0 defaults to close UNLESS the client says 'Connection: keep-alive'.
        This tiny method encodes that real, slightly-fiddly protocol rule."""
        conn = self.header("connection").lower()
        if self.version == "HTTP/1.1":
            return conn != "close"
        return conn == "keep-alive"


def _parse_cookies(cookie_header: str) -> dict:
    """Turn a Cookie header value like 'visits=3; theme=dark' into
    {'visits': '3', 'theme': 'dark'}. Cookies are just a semicolon-separated
    list of name=value pairs the browser echoes back on every request."""
    jar = {}
    for pair in cookie_header.split(";"):
        pair = pair.strip()
        if "=" in pair:
            name, value = pair.split("=", 1)
            jar[name.strip()] = value.strip()
    return jar


def parse_request(raw: bytes) -> Request:
    """Parse a complete request (headers + full body already collected) from
    bytes into a Request object. Raises BadRequest on anything malformed."""

    # Headers are text; split the header block off at the blank line. We decode
    # with iso-8859-1 (latin-1): every byte maps to some character, so decoding
    # header bytes can never crash on weird input. The BODY stays as raw bytes.
    try:
        header_block, _, body = raw.partition(b"\r\n\r\n")
        header_text = header_block.decode("iso-8859-1")
    except Exception as exc:
        raise BadRequest(f"could not decode header bytes: {exc}")

    lines = header_text.split("\r\n")

    # -- The request line: "METHOD PATH VERSION", exactly three space-parts. ----
    request_line = lines[0]
    parts = request_line.split(" ")
    if len(parts) != 3:
        raise BadRequest(f"malformed request line: {request_line!r}")
    method, path, version = parts
    if not version.startswith("HTTP/"):
        raise BadRequest(f"not an HTTP version: {version!r}")

    # -- The header lines: each is "Name: value". Fold names to lower-case. -----
    headers = {}
    for line in lines[1:]:
        if line == "":
            continue
        if ":" not in line:
            raise BadRequest(f"header line has no colon: {line!r}")
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()

    return Request(method, path, version, headers, body)


# ===========================================================================
# PART 3 — THE RESPONSE OBJECT
#
# A response mirrors a request's shape: a status line, some headers, a blank
# line, then the body. Building it as an OBJECT (instead of gluing strings the
# way Phase 2 did) means routes can set a code, tweak headers, attach cookies,
# and let one place worry about correct byte serialization.
# ===========================================================================

class Response:
    def __init__(self, status=200, body=b"", content_type="text/html"):
        self.status = status
        # Body may be given as str (we encode it) or bytes (used as-is).
        self.body = body.encode("utf-8") if isinstance(body, str) else body
        self.headers = {
            "Content-Type": f"{content_type}; charset=utf-8",
            # Server is a courtesy header naming who answered. Real servers send
            # things like "nginx" or "gunicorn"; ours is honest about what it is.
            "Server": "LinkBoard/0.3 (hand-written)",
        }

    def set(self, name, value):
        """Set (or overwrite) a header. Returns self so calls can chain."""
        self.headers[name] = value
        return self

    def add_cookie(self, name, value, max_age=None, path="/"):
        """Attach a Set-Cookie header telling the browser to store name=value
        and echo it back on future requests. NOTE: unlike normal headers, a
        response can carry SEVERAL Set-Cookie lines, so we keep a list and the
        serializer emits one line each. HttpOnly = 'JavaScript can't read this'
        (a small security habit we start early; deepened in Phase 7)."""
        cookie = f"{name}={value}; Path={path}; HttpOnly"
        if max_age is not None:
            cookie += f"; Max-Age={max_age}"
        self.headers.setdefault("_set_cookie_list", []).append(cookie)
        return self

    def to_bytes(self, include_body=True) -> bytes:
        """Serialize the whole response to the exact bytes that go on the wire.
        `include_body=False` is how we answer a HEAD request: identical headers
        (including the Content-Length the body WOULD have had), but no body."""
        reason = REASON_PHRASES.get(self.status, "Unknown")

        # Content-Length must always reflect the real body size in BYTES, even
        # for HEAD (where we don't send the body). The client uses it to know
        # when the response is complete — get it wrong and the client hangs.
        self.headers["Content-Length"] = str(len(self.body))

        # Assemble the status line + header lines. The blank line after the
        # headers is required — it's how the client knows the body is starting.
        lines = [f"HTTP/1.1 {self.status} {reason}"]
        cookie_list = self.headers.pop("_set_cookie_list", [])
        for name, value in self.headers.items():
            lines.append(f"{name}: {value}")
        for cookie in cookie_list:            # each Set-Cookie on its own line
            lines.append(f"Set-Cookie: {cookie}")

        head = ("\r\n".join(lines) + "\r\n\r\n").encode("iso-8859-1")
        if include_body:
            return head + self.body
        return head   # HEAD: headers only, body deliberately omitted


# ===========================================================================
# PART 4 — THE ROUTES (what each path + method actually does)
#
# A "route" is a decision: given this method and path, what response? Each
# handler below teaches one HTTP idea. The router (route()) picks among them.
# ===========================================================================

def homepage_html() -> str:
    rows = ""
    for link in LINKS:
        rows += (f"    <li>{link['points']} points — "
                 f"<a href=\"{link['url']}\">{link['title']}</a></li>\n")
    return (
        "<!DOCTYPE html>\n<html>\n<head><meta charset=\"utf-8\">"
        "<title>LinkBoard</title></head>\n<body>\n"
        "  <h1>LinkBoard</h1>\n"
        "  <p>Served by a hand-written HTTP server. Your visit is in the logs.</p>\n"
        f"  <ol>\n{rows}  </ol>\n"
        "  <p><a href=\"/submit-form\">Submit a link</a> · "
        "<a href=\"/count\">Your visit count (a cookie demo)</a></p>\n"
        "</body>\n</html>\n"
    )


def submit_form_html() -> str:
    """A tiny HTML form so you can POST from a browser, not just curl. The form's
    method=POST and action=/submit is the browser's way of saying 'send these
    fields in a POST body to /submit' — exactly what curl -d does by hand."""
    return (
        "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\">"
        "<title>Submit a link</title></head><body>\n"
        "  <h1>Submit a link to LinkBoard</h1>\n"
        "  <form method=\"POST\" action=\"/submit\">\n"
        "    <p><label>Title: <input name=\"title\"></label></p>\n"
        "    <p><label>URL: <input name=\"url\"></label></p>\n"
        "    <p><button type=\"submit\">Post it</button></p>\n"
        "  </form>\n"
        "  <p><a href=\"/\">← back to the board</a></p>\n"
        "</body></html>\n"
    )


def parse_form_body(body: bytes) -> dict:
    """Decode an application/x-www-form-urlencoded body — the format both HTML
    forms and `curl -d` send by default. It looks like 'title=Hi&url=http%3A%2F%2Fx':
    fields joined by '&', name and value joined by '=', and unsafe characters
    percent-encoded (space -> '+' or '%20', ':' -> '%3A'). We undo that here."""
    from urllib.parse import parse_qs   # stdlib helper; does the percent-decoding
    fields = {}
    for name, values in parse_qs(body.decode("utf-8", "replace")).items():
        fields[name] = values[0]        # take the first value for each field
    return fields


def route(req: Request) -> Response:
    """Choose a Response for this Request. This is the whole 'what does the app
    DO' layer — in Phase 4 a framework will do this dispatch for us; here it's a
    plain if/elif chain so the mechanism is visible."""

    path = req.path.split("?")[0]   # ignore any ?query=string for routing (Phase 4)

    # ---- 405 gate: which methods each path understands. --------------------
    # We answer 405 Method Not Allowed WITH an 'Allow' header listing the verbs
    # that path DOES accept — the spec requires it, and it's genuinely helpful.
    allowed = {
        "/": ["GET", "HEAD"],
        "/about": ["GET", "HEAD"],
        "/submit-form": ["GET", "HEAD"],
        "/count": ["GET", "HEAD"],
        "/secret": ["GET", "HEAD"],
        "/old-home": ["GET", "HEAD"],
        "/submit": ["POST"],
        "/links": ["GET", "HEAD", "PUT", "DELETE"],
    }
    if path in allowed and req.method not in allowed[path]:
        log("ROUTE", f"{req.method} {path} not allowed here -> 405 "
                     f"(Allow: {', '.join(allowed[path])})")
        return (Response(405, f"{req.method} is not allowed on {path}.\n",
                         "text/plain")
                .set("Allow", ", ".join(allowed[path])))

    # ---- GET / HEAD routes --------------------------------------------------
    if path == "/":
        log("ROUTE", f"/ -> homepage with {len(LINKS)} links -> 200")
        return Response(200, homepage_html(), "text/html")

    if path == "/about":
        log("ROUTE", "/about -> 200")
        return Response(200,
                        "LinkBoard v0.3 — Phase 3, HTTP by hand.\n"
                        "Methods, status codes, headers, cookies, keep-alive —\n"
                        "all hand-written, still no framework.\n",
                        "text/plain")

    if path == "/submit-form":
        log("ROUTE", "/submit-form -> the HTML form -> 200")
        return Response(200, submit_form_html(), "text/html")

    # ---- 301 redirect: teach the 3xx family --------------------------------
    if path == "/old-home":
        log("ROUTE", "/old-home -> 301 redirect to / (Location header)")
        # A redirect is a status in the 300s plus a 'Location' header telling the
        # client where to go instead. Browsers/curl -L follow it automatically.
        return (Response(301, "This page moved. See you at /.\n", "text/plain")
                .set("Location", "/"))

    # ---- 401 gate: teach the Authorization header --------------------------
    if path == "/secret":
        auth = req.header("authorization")
        if not auth:
            log("ROUTE", "/secret with no Authorization header -> 401")
            # 401 tells the client 'you must authenticate', and WWW-Authenticate
            # tells it HOW. (Real auth is Phase 7; this just shows the mechanism.)
            return (Response(401, "You must authenticate to see the secret.\n",
                             "text/plain")
                    .set("WWW-Authenticate", 'Basic realm="LinkBoard"'))
        log("ROUTE", f"/secret WITH Authorization ({auth[:12]}...) -> 200")
        return Response(200, "The secret: HTTP is just text over a socket.\n",
                        "text/plain")

    # ---- cookies: a working visit counter ----------------------------------
    if path == "/count":
        # Read the 'visits' cookie the browser echoed back (0 if first visit),
        # add one, and Set-Cookie the new value so next time it comes back higher.
        try:
            visits = int(req.cookies.get("visits", "0"))
        except ValueError:
            visits = 0
        visits += 1
        log("ROUTE", f"/count -> visit #{visits} for this client "
                     f"(cookie was {req.cookies.get('visits', 'absent')}) -> 200")
        resp = Response(200,
                        f"You've visited /count {visits} time(s).\n"
                        f"Re-run with the same cookie jar and watch it climb.\n",
                        "text/plain")
        resp.add_cookie("visits", str(visits), max_age=3600)
        # Cache-Control: don't cache a per-user, changing page (Phase 8 topic).
        resp.set("Cache-Control", "no-store")
        return resp

    # ---- POST /submit: teach POST + why it's NOT idempotent ----------------
    if path == "/submit":
        fields = parse_form_body(req.body)
        title = fields.get("title", "").strip()
        url = fields.get("url", "").strip()
        if not title or not url:
            log("ROUTE", "POST /submit missing title/url -> 400")
            return Response(400, "Both 'title' and 'url' are required.\n",
                            "text/plain")
        # Each POST APPENDS a new link. Send the same POST twice -> two links.
        # THAT is non-idempotence: repeating the call changes the world again.
        LINKS.append({"title": title, "url": url, "points": 1})
        log("ROUTE", f"POST /submit added '{title}' -> now {len(LINKS)} links -> 201")
        # 201 Created is the honest status when a request MAKES a new resource.
        return (Response(201,
                         f"Added '{title}'. LinkBoard now has {len(LINKS)} links.\n"
                         f"(Submit again and you'll get a SECOND copy — POST is "
                         f"not idempotent.)\n",
                         "text/plain")
                .set("Location", "/"))

    # ---- PUT / DELETE /links: teach idempotency by contrast ----------------
    if path == "/links":
        if req.method == "PUT":
            # PUT sets points to a fixed value. Doing it 1x or 100x lands in the
            # SAME state (all points = 100). Repeating is safe: that's idempotent.
            for link in LINKS:
                link["points"] = 100
            log("ROUTE", "PUT /links set every link's points to 100 -> 200 "
                         "(idempotent: repeating changes nothing further)")
            return Response(200, "All links set to 100 points. "
                                 "Do it again — same result.\n", "text/plain")
        if req.method == "DELETE":
            # DELETE removes them. Once gone, deleting again is still 'gone' —
            # same end state, so DELETE is idempotent too.
            count = len(LINKS)
            LINKS.clear()
            log("ROUTE", f"DELETE /links removed {count} links -> 200 "
                         f"(idempotent: deleting again leaves it still empty)")
            return Response(200, f"Deleted {count} links. The board is empty. "
                                 f"Delete again — still empty.\n", "text/plain")
        # GET /links: a plain text listing.
        log("ROUTE", f"GET /links -> listing {len(LINKS)} links -> 200")
        listing = "".join(f"{l['points']:>4}  {l['title']}\n" for l in LINKS)
        return Response(200, listing or "(no links yet)\n", "text/plain")

    # ---- 404 fallback -------------------------------------------------------
    log("ROUTE", f"no route for {req.method} {path} -> 404")
    return Response(404, f"LinkBoard has no page at {path}\n", "text/plain")


# ===========================================================================
# PART 5 — READING A REQUEST OFF THE (keep-alive) CONNECTION
#
# With keep-alive, one connection carries several requests back-to-back. A single
# recv() might return part of one request, a whole request, or even bytes that
# spill into the NEXT request. So we keep a per-connection byte buffer and a
# reader that: (1) reads until it has the full header block, (2) reads any body
# named by Content-Length, (3) returns the parsed request AND the leftover bytes
# (the start of the next request) for the following read.
# ===========================================================================

def read_one_request(conn, buffer, first):
    """Return (Request, leftover_bytes). Return (None, b"") when the client has
    closed the connection or gone idle. `first` picks which idle timeout to use:
    a fresh connection vs. one waiting for its next keep-alive request."""

    # Choose the timeout: the first request on a connection uses CLIENT_TIMEOUT;
    # subsequent ones use the (usually equal) keep-alive idle timeout.
    conn.settimeout(CLIENT_TIMEOUT_SECONDS if first else KEEPALIVE_TIMEOUT_SECONDS)

    # -- Read until we have the full header block (ends at the blank line). ----
    while b"\r\n\r\n" not in buffer:
        try:
            chunk = conn.recv(4096)
        except socket.timeout:
            # No (more) data arrived in time. On a keep-alive wait this is the
            # normal, quiet way a connection ends; on a first read it's a silent
            # client we give up on.
            return None, b""
        if chunk == b"":
            return None, b""            # client closed the connection
        buffer += chunk
        log("RECV", f"got chunk of {len(chunk)} bytes (buffer now {len(buffer)})")

    # -- Split headers from whatever body bytes already arrived. ---------------
    header_block, _, rest = buffer.partition(b"\r\n\r\n")

    # We must parse headers first to learn the body length. Decode just to peek
    # at Content-Length; parse_request re-parses cleanly afterward.
    header_text = header_block.decode("iso-8859-1", "replace")
    content_length = 0
    for line in header_text.split("\r\n")[1:]:
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":", 1)[1].strip())
            except ValueError:
                content_length = 0
            break

    # -- Keep reading until we have the whole body (rest may be short). --------
    body = rest
    while len(body) < content_length:
        try:
            chunk = conn.recv(4096)
        except socket.timeout:
            break
        if chunk == b"":
            break
        body += chunk
        log("RECV", f"reading body: {len(body)}/{content_length} bytes")

    # The exact request is header_block + separator + the first content_length
    # body bytes. Anything beyond that is the START of the next request — hand it
    # back as the leftover buffer so keep-alive's next read picks it up.
    exact = header_block + b"\r\n\r\n" + body[:content_length]
    leftover = body[content_length:]
    request = parse_request(exact)
    return request, leftover


# ===========================================================================
# PART 6 — HANDLING ONE CONNECTION (now a keep-alive LOOP)
# ===========================================================================

def handle_connection(conn, addr, conn_number):
    """Serve one TCP connection start to finish. Thanks to keep-alive this now
    loops, serving multiple requests over the SAME socket until the client says
    'Connection: close', goes idle, hangs up, or hits our per-connection limit."""

    client = f"{addr[0]}:{addr[1]}"
    buffer = b""             # bytes read but not yet consumed (spillover)
    served = 0               # requests answered on THIS connection

    while served < KEEPALIVE_MAX_REQUESTS:
        first = (served == 0)
        try:
            req, buffer = read_one_request(conn, buffer, first)
        except BadRequest as exc:
            # The bytes weren't valid HTTP. Answer a real 400 and stop reusing
            # this connection (we no longer trust where the byte stream is).
            log("HTTP", f"conn#{conn_number} bad request: {exc} -> 400")
            conn.sendall(Response(400, f"Bad request: {exc}\n",
                                  "text/plain").to_bytes())
            return

        if req is None:
            # Client closed or went idle. Normal end of a keep-alive connection.
            if served == 0:
                log("TIMEOUT", f"conn#{conn_number} {client} sent nothing "
                               f"in {CLIENT_TIMEOUT_SECONDS:.0f}s — hanging up "
                               f"(a silent spare connection; this is normal)")
            else:
                log("IDLE", f"conn#{conn_number} {client} sent no further request "
                            f"in {KEEPALIVE_TIMEOUT_SECONDS:.0f}s — closing "
                            f"keep-alive after {served} request(s)")
            return

        served += 1
        log("HTTP", f"conn#{conn_number} req#{served}: "
                    f"{req.method} {req.path} {req.version}")
        # Show a couple of the headers so you can watch what a browser says.
        for name in ("host", "user-agent"):
            if req.header(name):
                log("HEADER", f"conn#{conn_number} {name}: {req.header(name)}")

        # -- Decide the response (routing), guarding against handler crashes. --
        try:
            resp = route(req)
        except Exception as exc:
            # A route threw. A server must turn its OWN bugs into a 500, not die.
            log("ERROR", f"conn#{conn_number} handler crashed: {exc} -> 500")
            resp = Response(500, "Something broke on our end.\n", "text/plain")

        # -- Decide keep-alive: honor the client's wish AND our own limits. ----
        keep = req.wants_keep_alive() and served < KEEPALIVE_MAX_REQUESTS
        resp.set("Connection", "keep-alive" if keep else "close")
        if keep:
            resp.set("Keep-Alive",
                     f"timeout={int(KEEPALIVE_TIMEOUT_SECONDS)}, "
                     f"max={KEEPALIVE_MAX_REQUESTS}")

        # -- Send it. HEAD gets headers only (no body), everything else full. --
        include_body = (req.method != "HEAD")
        payload = resp.to_bytes(include_body=include_body)
        conn.sendall(payload)
        log("SEND", f"conn#{conn_number} req#{served} -> {resp.status} "
                    f"{REASON_PHRASES.get(resp.status, '?')}, {len(payload)} bytes "
                    f"({'keep-alive' if keep else 'closing'})")

        if not keep:
            return   # client asked to close, or we hit the limit


# ===========================================================================
# PART 7 — THE SERVER LOOP: socket -> bind -> listen -> accept, forever.
# (Unchanged in spirit from Phase 2 — still ONE connection at a time.)
# ===========================================================================

def main() -> None:
    log("BOOT", "=== LinkBoard v0.3 — hand-written HTTP server (Phase 3) ===")
    log("BOOT", "now speaks real HTTP: methods, status codes, headers, cookies, "
                "keep-alive")
    log("BOOT", "STILL one connection at a time, on purpose — see the docstring")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(16)
    log("LISTEN", f"listening on {HOST}:{PORT} — "
                  f"open http://localhost:{PORT} or: curl -v localhost:{PORT}")

    conn_number = 0
    try:
        while True:
            log("WAIT", "blocked in accept() — doing nothing until someone connects")
            conn, addr = server_socket.accept()
            conn_number += 1
            log("CONN", f"conn#{conn_number} accepted from {addr[0]}:{addr[1]}")
            try:
                handle_connection(conn, addr, conn_number)
            except ConnectionError as exc:
                log("CONN", f"conn#{conn_number} connection error: {exc}")
            finally:
                conn.close()
                log("CLOSE", f"conn#{conn_number} connection closed")
    except KeyboardInterrupt:
        print()
        log("SHUTDOWN", "Ctrl+C received — closing the listening socket. Bye.")
        server_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
