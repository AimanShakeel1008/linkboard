#!/usr/bin/env bash
#
# make_logs.sh — generates a realistic fake web-server log file (server.log)
# for the Phase 0 grep/awk/sed exercises.
#
# WHY a generator instead of shipping a ready-made log?
#   1. Running it is itself practice (chmod +x, ./script, watching output).
#   2. You can delete server.log and regenerate any time — the playground
#      is disposable by design.
#
# The log line format (columns are what awk will see as $1..$8):
#   DATE        TIME      LEVEL   IP             METHOD PATH        STATUS  DURATION
#   2026-07-15  10:23:01  [INFO]  203.0.113.42   GET    /links      200     23ms

set -euo pipefail   # safety switches — explained in lesson section 9

# Seeding bash's random number generator makes the "random" sequence
# reproducible: everyone who runs this gets a very similar file, so the
# expected outputs in the lesson/exercises will match yours closely.
RANDOM=42

OUT="server.log"
LINES=800

echo "[STEP] Generating fake web-server traffic into $OUT ..."

# Pools of values to pick from. Real logs are skewed (some pages are far
# more popular than others), so popular items appear multiple times in the
# pool — a cheap way to fake a realistic distribution.
PATHS=(/links /links /links /links/42 /links/7 /comments /users/aiman /about /search /search)
METHODS=(GET GET GET GET GET POST POST PUT DELETE)
IPS=(203.0.113.42 203.0.113.42 203.0.113.9 198.51.100.7 192.0.2.11 192.0.2.55 203.0.113.17)

# Start the clock at 10:00:00 and advance it a few random seconds per line,
# so timestamps increase like a real log's would.
hour=10; min=0; sec=0

advance_clock() {
  # Move time forward 1–5 seconds. 60 seconds roll into a minute, etc.
  sec=$(( sec + 1 + RANDOM % 5 ))
  if (( sec >= 60 )); then sec=$(( sec - 60 )); min=$(( min + 1 )); fi
  if (( min >= 60 )); then min=$(( min - 60 )); hour=$(( hour + 1 )); fi
}

emit_line() {
  # $1=level $2=ip $3=method $4=path $5=status $6=duration_ms
  printf "2026-07-15 %02d:%02d:%02d [%s] %s %s %s %s %sms\n" \
    "$hour" "$min" "$sec" "$1" "$2" "$3" "$4" "$5" "$6" >> "$OUT"
}

# Start fresh each run (">" truncates — lesson section 2.5).
> "$OUT"

for (( i = 1; i <= LINES; i++ )); do
  advance_clock

  ip=${IPS[RANDOM % ${#IPS[@]}]}
  method=${METHODS[RANDOM % ${#METHODS[@]}]}
  path=${PATHS[RANDOM % ${#PATHS[@]}]}

  # --- Planted pattern #1: an ERROR burst around 11:42 ------------------
  # For exercise: "when did things go wrong?" (grep ERROR | awk time column)
  if (( hour == 11 && min >= 42 && min <= 44 && RANDOM % 3 == 0 )); then
    emit_line "ERROR" "$ip" "$method" "$path" 500 $(( 400 + RANDOM % 600 ))
    continue
  fi

  # --- Planted pattern #2: one suspicious IP hammering the login page ---
  # For exercise: the top-IPs pipeline (awk | sort | uniq -c | sort -rn)
  if (( RANDOM % 12 == 0 )); then
    emit_line "WARN" "198.51.100.66" "POST" "/login" 401 $(( 10 + RANDOM % 30 ))
    continue
  fi

  # --- Planted pattern #3: /search is consistently slow -----------------
  # For exercise: per-path average duration with awk arithmetic
  if [[ "$path" == "/search" ]]; then
    emit_line "INFO" "$ip" "GET" "/search" 200 $(( 700 + RANDOM % 900 ))
    continue
  fi

  # --- Normal traffic: mostly fast 200s, occasional 404/500 -------------
  roll=$(( RANDOM % 100 ))
  if   (( roll < 90 )); then status=200; level=INFO;  dur=$(( 5 + RANDOM % 80 ))
  elif (( roll < 97 )); then status=404; level=WARN;  dur=$(( 3 + RANDOM % 15 ))
  else                       status=500; level=ERROR; dur=$(( 200 + RANDOM % 800 ))
  fi
  emit_line "$level" "$ip" "$method" "$path" "$status" "$dur"
done

echo "[STEP] Planting an ERROR burst around 11:42 ...           (find it with grep + awk)"
echo "[STEP] Planting a suspicious IP (198.51.100.66) ...       (find it with awk | sort | uniq -c)"
echo "[STEP] Planting a slow endpoint (/search) ...             (find it with awk arithmetic)"
echo "[DONE] Wrote $(wc -l < "$OUT") lines to $OUT — happy hunting. Open exercises.md next."
