#!/usr/bin/env python3
"""
LinkBoard v0 — an HTTP server built from RAW SOCKETS. No framework. No magic.

This is the very first piece of LinkBoard. It exists to prove one thing:
a web server is not magic — it is a program that
  1. asks the operating system for a "socket" (a phone line for bytes),
  2. waits for someone to connect,
  3. reads the bytes they send (which turn out to be plain text),
  4. writes some bytes back (also plain text, plus the page content),
  5. hangs up, and goes back to waiting.

Everything a "real" framework (FastAPI, Express, Rails...) does is a set of
conveniences layered on top of exactly this loop. We build the loop naked
first so that nothing later is ever mysterious.

DELIBERATE FLAW (read this!):
This server handles ONE connection at a time. While it is busy reading from
one client, every other client must wait in line — even if the busy client
is sending its request one byte per second. This is Phase 1's "blocking I/O"
lesson happening to real network traffic. We keep the flaw ON PURPOSE this
phase so you can watch it hurt (run slow_client.py while curling in another
terminal). Fixing it properly is a later phase's job.

Run it (from WSL):
    cd /mnt/d/Projects/linkboard/project
    python3 server.py
Then visit http://localhost:8000 in your browser, or:  curl -v localhost:8000
Stop it with Ctrl+C.
"""

import socket
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# "0.0.0.0" means: accept connections aimed at ANY of this machine's IP
# addresses (localhost, the WSL virtual network address, etc.). If we wrote
# "127.0.0.1" instead, only programs on this same machine could connect.
HOST = "0.0.0.0"

# The port — the "apartment number" clients knock on. Real websites use 80
# (HTTP) or 443 (HTTPS), but ports below 1024 need admin rights, so during
# development everyone uses a high port like 8000.
PORT = 8000

# If a client connects but then sends nothing for this many seconds, we hang
# up on them. Without this, one silent connection would freeze the server
# forever (browsers really do open "spare" connections that never speak!).
CLIENT_TIMEOUT_SECONDS = 5.0

# ---------------------------------------------------------------------------
# LinkBoard's entire "database" (for now): a Python list in memory.
# Phase 4 gives us real submissions; Phase 6 gives us a real database.
# If you restart the server, edits to this list are gone — that fragility
# is a feature of the lesson: you'll feel WHY databases exist later.
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
    """Print one narrated log line with a timestamp, e.g.
    12:03:44.512 [CONN] accepted connection from 127.0.0.1:54321
    flush=True forces the line out immediately (Python normally buffers
    output; buffering would make the logs lag behind reality)."""
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # trim to milliseconds
    print(f"{now} [{tag}] {message}", flush=True)


# ---------------------------------------------------------------------------
# Building responses.
#
# An HTTP response is just text with a strict shape:
#
#     HTTP/1.1 200 OK\r\n            <- status line: version, code, phrase
#     Content-Type: text/html\r\n    <- headers: "label: value" lines
#     Content-Length: 1234\r\n
#     Connection: close\r\n
#     \r\n                           <- ONE blank line = "headers are over"
#     <html>...the actual page...    <- the body
#
# "\r\n" is the two-character line ending HTTP requires (carriage return +
# line feed — a typewriter-era convention that stuck). Not just "\n".
# ---------------------------------------------------------------------------

def build_response(status_line: str, content_type: str, body: str) -> bytes:
    """Assemble a full HTTP response and return it as BYTES.

    Sockets only carry bytes, never Python strings — so the final step of
    every response is .encode("utf-8"), turning text into bytes using the
    UTF-8 agreement (Phase 1, Part A: text is numbers plus an agreement).
    """
    body_bytes = body.encode("utf-8")

    # Content-Length tells the client exactly how many BODY bytes to expect.
    # Without it the client cannot know when the page has finished arriving —
    # it would just sit there waiting for more. It must count the encoded
    # BYTES, not the characters (a non-ASCII character is several bytes!).
    headers = (
        f"{status_line}\r\n"
        f"Content-Type: {content_type}; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"      # "I'll hang up after this response"
        f"\r\n"                        # the sacred blank line
    )
    return headers.encode("utf-8") + body_bytes


def homepage_html() -> str:
    """The LinkBoard front page, built by gluing strings together.
    (Yes, real apps use template engines. Phase 5 gives us a real frontend.
    Right now the point is: a web page is just text the server sends.)"""
    rows = ""
    for rank, link in enumerate(LINKS, start=1):
        rows += (
            f"    <li>{link['points']} points — "
            f"<a href=\"{link['url']}\">{link['title']}</a></li>\n"
        )
    return (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><meta charset=\"utf-8\"><title>LinkBoard</title></head>\n"
        "<body>\n"
        "  <h1>LinkBoard</h1>\n"
        "  <p>Served to you by a hand-made socket server. "
        "Check the terminal — your visit is in the logs.</p>\n"
        "  <ol>\n"
        f"{rows}"
        "  </ol>\n"
        "</body>\n"
        "</html>\n"
    )


def about_text() -> str:
    return (
        "LinkBoard v0 — Phase 2 of the system design course.\n"
        "An HTTP server made of raw sockets, one connection at a time.\n"
        "No framework was harmed (or used) in the making of this page.\n"
    )


# ---------------------------------------------------------------------------
# Handling one connection, start to finish.
# ---------------------------------------------------------------------------

def handle_connection(conn: socket.socket, addr, request_number: int) -> None:
    """Read one HTTP request from `conn`, send one response, and return.
    `addr` is a (client_ip, client_port) pair the OS gave us with the
    connection. `request_number` is just our own counter for the logs."""

    client = f"{addr[0]}:{addr[1]}"

    # If the client goes silent, don't wait forever — raise an error after
    # CLIENT_TIMEOUT_SECONDS so the server can move on to the next client.
    conn.settimeout(CLIENT_TIMEOUT_SECONDS)

    # -- STEP 1: read bytes until we've seen the end of the headers. --------
    # recv(1024) means "give me whatever has arrived, up to 1024 bytes".
    # Crucial honesty: ONE recv() is NOT guaranteed to return the whole
    # request. TCP hands us a STREAM of bytes with no message boundaries —
    # the request may arrive in one piece, or in twenty. So we loop,
    # collecting pieces, until we spot the blank line ("\r\n\r\n") that
    # marks the end of the headers. (slow_client.py exists to prove this
    # piece-by-piece arrival is real.)
    received = b""                     # bytes collected so far
    chunks = 0                         # how many recv() calls it took
    try:
        while b"\r\n\r\n" not in received:
            chunk = conn.recv(1024)   # BLOCKS here until bytes arrive
            if chunk == b"":
                # recv returning empty bytes means: the client hung up.
                log("CONN", f"#{request_number} {client} disconnected "
                            f"before finishing a request")
                return
            chunks += 1
            received += chunk
            log("RECV", f"#{request_number} got chunk of {len(chunk)} bytes "
                        f"(total so far: {len(received)})")
            if len(received) > 65536:
                # A request whose headers exceed 64 KB is nonsense or abuse.
                log("WARN", f"#{request_number} request too large — hanging up")
                return
    except socket.timeout:
        log("TIMEOUT", f"#{request_number} {client} sent nothing for "
                       f"{CLIENT_TIMEOUT_SECONDS:.0f}s — hanging up "
                       f"(browsers open silent spare connections; this is normal)")
        return

    # -- STEP 2: turn the bytes into text and pick the request apart. -------
    # HTTP headers are text, so we decode bytes -> string. (iso-8859-1 is
    # the traditional byte-safe choice for HTTP headers: every byte maps to
    # some character, so decoding can never crash on weird input.)
    text = received.decode("iso-8859-1")

    # The FIRST line is the request line: "GET /about HTTP/1.1"
    request_line = text.split("\r\n")[0]
    parts = request_line.split(" ")
    if len(parts) != 3:
        log("HTTP", f"#{request_number} malformed request line: {request_line!r}")
        conn.sendall(build_response("HTTP/1.1 400 Bad Request", "text/plain",
                                    "That was not HTTP.\n"))
        return
    method, path, version = parts
    log("HTTP", f"#{request_number} parsed request line: "
                f"method={method} path={path} version={version} "
                f"(read in {chunks} chunk(s))")

    # The remaining lines (until the blank one) are headers. We don't NEED
    # them yet, but let's log a couple so you can see what a browser says
    # about itself. Phase 3 parses headers properly and uses them.
    for line in text.split("\r\n")[1:]:
        if line == "":
            break                     # blank line — headers are over
        if line.lower().startswith(("host:", "user-agent:")):
            log("HEADER", f"#{request_number} {line}")

    # -- STEP 3: route — decide what page this path gets. -------------------
    if method != "GET":
        log("ROUTE", f"#{request_number} {method} not supported yet -> 405")
        response = build_response("HTTP/1.1 405 Method Not Allowed",
                                  "text/plain",
                                  "This tiny server only speaks GET (for now).\n")
    elif path == "/":
        log("ROUTE", f"#{request_number} / -> homepage with "
                     f"{len(LINKS)} links -> 200")
        response = build_response("HTTP/1.1 200 OK", "text/html",
                                  homepage_html())
    elif path == "/about":
        log("ROUTE", f"#{request_number} /about -> 200")
        response = build_response("HTTP/1.1 200 OK", "text/plain",
                                  about_text())
    else:
        log("ROUTE", f"#{request_number} no page at {path} -> 404")
        response = build_response("HTTP/1.1 404 Not Found", "text/plain",
                                  f"LinkBoard has no page at {path}\n")

    # -- STEP 4: send the response bytes back. ------------------------------
    # sendall (not send!) keeps pushing until every byte is handed to the
    # OS — plain send() may deliver only part and expect you to loop.
    conn.sendall(response)
    log("SEND", f"#{request_number} sent {len(response)} bytes to {client}")


# ---------------------------------------------------------------------------
# The server itself: socket -> bind -> listen -> accept, forever.
# ---------------------------------------------------------------------------

def main() -> None:
    log("BOOT", "=== LinkBoard v0 — raw socket HTTP server ===")
    log("BOOT", "one connection at a time, on purpose — see the file docstring")

    # Ask the OS for a socket: AF_INET = IPv4 addresses,
    # SOCK_STREAM = TCP (the reliable, ordered, connection-based kind).
    # This is a syscall — the doorbell from Phase 1, Part G.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Without this line: after Ctrl+C, restarting within ~30-60 s fails with
    # "Address already in use", because the OS keeps the old port reserved
    # briefly (a TCP safety state called TIME_WAIT). This flag says "I know,
    # let me have it anyway" — standard for servers.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind = claim the address. listen = start queueing incoming connections
    # (the OS holds a short line of callers we haven't answered yet; 16 is
    # the most it will hold before turning new callers away).
    server_socket.bind((HOST, PORT))
    server_socket.listen(16)
    log("LISTEN", f"listening on {HOST}:{PORT} — "
                  f"open http://localhost:{PORT} or: curl localhost:{PORT}")

    request_number = 0
    try:
        while True:
            log("WAIT", "blocked in accept() — doing absolutely nothing "
                        "until someone connects")
            # accept() BLOCKS until a client completes the TCP handshake,
            # then returns a NEW socket just for that client (the listening
            # socket stays open for future callers).
            conn, addr = server_socket.accept()
            request_number += 1
            log("CONN", f"#{request_number} accepted connection from "
                        f"{addr[0]}:{addr[1]}")
            try:
                handle_connection(conn, addr, request_number)
            except ConnectionError as exc:
                # Client vanished mid-conversation (closed laptop, killed
                # curl...). A server must shrug this off, not crash.
                log("CONN", f"#{request_number} connection error: {exc}")
            finally:
                conn.close()
                log("CLOSE", f"#{request_number} connection closed")
    except KeyboardInterrupt:
        # Ctrl+C lands here — close the listening socket and exit cleanly.
        print()  # move past the ^C on its own line
        log("SHUTDOWN", "Ctrl+C received — closing the listening socket. Bye.")
        server_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
