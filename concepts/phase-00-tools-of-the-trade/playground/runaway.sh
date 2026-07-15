#!/usr/bin/env bash
#
# runaway.sh — deliberately misbehaves so you can practice the hunt:
# notice a busy machine → identify the culprit (top) → find its PID
# (pgrep) → stop it (kill).
#
# It also demonstrates GRACEFUL SHUTDOWN (lesson section 4.3):
#   - plain `kill <PID>` sends SIGTERM → we catch it, say goodbye, exit cleanly
#   - `kill -9 <PID>` sends SIGKILL   → uncatchable; we vanish mid-sentence
#   - Ctrl+C sends SIGINT             → we catch that politely too

set -euo pipefail

# `trap` registers a handler: "when signal X arrives, run this function
# instead of dying instantly." This is exactly how real servers implement
# graceful shutdown — finish in-flight requests, close connections, THEN exit.
say_goodbye() {
  echo ""
  echo "[RUNAWAY] Caught SIGTERM — cleaning up politely. Goodbye."
  exit 0
}
say_goodbye_int() {
  echo ""
  echo "[RUNAWAY] Caught SIGINT (Ctrl+C) — cleaning up politely. Goodbye."
  exit 0
}
trap say_goodbye TERM
trap say_goodbye_int INT
# Note there is NO handler for SIGKILL — the OS forbids catching it.
# That's the whole point of -9: a stop that cannot be refused.

echo "[RUNAWAY] I am PID $$ and I am about to waste CPU in a busy loop."
echo "[RUNAWAY] In another terminal, find me with:  top   or   pgrep -f runaway.sh"
echo "[RUNAWAY] Then stop me with:  kill $$        (polite — watch me say goodbye)"
echo "[RUNAWAY] Or brutally with:   kill -9 $$     (no goodbye possible)"

# The busy loop: ':' is bash's "do nothing" command, so this spins as fast
# as one CPU core allows — which is why I shoot to the top of `top`.
while true; do :; done
