#!/usr/bin/env bash
#
# heartbeat.sh — the cron exercise target (lesson section 8 / run Part F).
#
# It appends ONE timestamped line per run. Scheduled via cron every minute,
# the growing file is visible proof that cron is running your code on
# schedule, with no terminal attached.
#
# Design notes (both are cron lessons in miniature):
#   * We keep our own state file to count beats — each cron run is a brand
#     new process that remembers NOTHING from the previous run. Any memory
#     between runs must live in a file (or later: a database).
#   * We print to stdout and let the CRONTAB LINE redirect it
#     (>> /tmp/heartbeat.log 2>&1). Cron itself is silent; if you don't
#     capture output yourself, it evaporates.

set -euo pipefail

# $HOME works even under cron's minimal environment; a relative path would not.
STATE_FILE="$HOME/.heartbeat_count"

# Read the previous count if the state file exists, else start at 0.
count=0
if [[ -f "$STATE_FILE" ]]; then
  count=$(cat "$STATE_FILE")
fi
count=$(( count + 1 ))
echo "$count" > "$STATE_FILE"

echo "[HEARTBEAT] $(date '+%Y-%m-%d %H:%M:%S') — cron ran me. Beat #$count"
