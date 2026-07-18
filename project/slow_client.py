#!/usr/bin/env python3
"""
slow_client.py — a deliberately CRUEL client that proves the server's flaw.

A normal client (your browser, curl) sends its whole request in a burst.
This one sends the exact same valid HTTP request, but ONE CHARACTER AT A
TIME, pausing between characters. It is a perfectly polite, standards-abiding
request — just slow.

Why it matters:
Our server (server.py) reads one connection to completion before it will
even look at the next caller. So while this trickle is dribbling in, the
server is stuck in recv(), blocked, unable to serve anyone else. This is
Phase 1's "blocking I/O" made painfully visible on a network.

HOW TO STAGE THE DEMONSTRATION (three terminals, all in WSL):

  Terminal 1 — start the victim:
      cd /mnt/d/Projects/linkboard/project
      python3 server.py

  Terminal 2 — unleash the slow client:
      cd /mnt/d/Projects/linkboard/project
      python3 slow_client.py

  Terminal 3 — WHILE the slow client is still dribbling, try a normal request:
      curl localhost:8000

  Watch: the curl in terminal 3 HANGS. It gets no answer until the slow
  client in terminal 2 finishes. One slow visitor froze the whole shop.
  In terminal 1's logs you can see exactly why: the server is stuck
  logging one-byte [RECV] chunks, never reaching the next accept().
"""

import socket
import time

HOST = "localhost"
PORT = 8000

# A normal, valid HTTP/1.1 GET request. Note the blank line at the end
# (\r\n\r\n) — that is what tells the server "my headers are done".
REQUEST = (
    "GET / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "User-Agent: slow-client-on-purpose\r\n"
    "\r\n"
)

# Pause between characters. 0.25s * ~55 characters ≈ 14 seconds of the
# server being held hostage — plenty of time to run the curl in terminal 3.
DELAY_BETWEEN_CHARS = 0.25


def main() -> None:
    print(f"[SLOW] connecting to {HOST}:{PORT} ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[SLOW] connected. Now sending the request ONE byte every "
          f"{DELAY_BETWEEN_CHARS}s.")
    print("[SLOW] >>> GO NOW to terminal 3 and run:  curl localhost:8000")
    print("[SLOW] >>> watch it hang until this finishes.\n")

    for i, char in enumerate(REQUEST, start=1):
        # Send exactly one character (encoded to one byte).
        sock.sendall(char.encode("iso-8859-1"))
        shown = char.replace("\r", "\\r").replace("\n", "\\n")
        print(f"[SLOW] sent byte {i:2d}/{len(REQUEST)}: '{shown}'", flush=True)
        time.sleep(DELAY_BETWEEN_CHARS)

    print("\n[SLOW] full request sent. Reading the server's reply...")
    # Now read whatever the server sends back, until it closes the connection.
    reply = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        reply += chunk
    sock.close()

    # Show just the status line so you can confirm it really worked.
    status_line = reply.decode("iso-8859-1").split("\r\n")[0]
    print(f"[SLOW] server replied: {status_line}")
    print(f"[SLOW] got {len(reply)} bytes total. Done — the shop is free again.")


if __name__ == "__main__":
    main()
