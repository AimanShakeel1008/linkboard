# Phase 0 Playground — The Log Hunt (12 exercises)

Run `./make_logs.sh` first so `server.log` exists. Then work these in order —
they build on each other. Try each in the terminal before opening the answer.
Your exact numbers may differ slightly from mine; the *shape* of the answer
is what matters. Nothing is graded.

Column cheat-sheet for `server.log` (for awk):
`$1`=date  `$2`=time  `$3`=level  `$4`=IP  `$5`=method  `$6`=path  `$7`=status  `$8`=duration

---

### 1. How many requests did the server handle in total?

<details><summary>Show answer</summary>

```bash
wc -l server.log
```
One log line = one request, so counting lines counts requests (~800).
</details>

### 2. Show every ERROR line. Then just *count* them.

<details><summary>Show answer</summary>

```bash
grep ERROR server.log        # see them
grep -c ERROR server.log     # count them (-c = count)
```
</details>

### 3. Show only the lines that are NOT plain INFO traffic.

<details><summary>Show answer</summary>

```bash
grep -v INFO server.log
```
`-v` inverts the match — "everything except." You get the WARNs and ERRORs.
</details>

### 4. Something went wrong in a burst. Around what time? (Hint: look at the timestamps of the ERROR lines.)

<details><summary>Show answer</summary>

```bash
grep ERROR server.log | awk '{print $2}' | cut -c1-5 | sort | uniq -c
```
Filter to errors → keep the time column → keep just `HH:MM` (`cut -c1-5`
keeps characters 1–5) → count per minute. One cluster of minutes dominates:
**around 11:42–11:44** — the planted incident. In real life this is how you
answer "when did the outage start?"
</details>

### 5. Which are the top 5 IP addresses by request count? Does one look suspicious?

<details><summary>Show answer</summary>

```bash
awk '{print $4}' server.log | sort | uniq -c | sort -rn | head -5
```
THE classic pipeline (lesson 3.4). `198.51.100.66` ranks high — and if you
inspect it (next exercise) it's hammering one URL. Suspicious indeed.
</details>

### 6. What exactly is that suspicious IP doing? Show its lines; summarize its behavior.

<details><summary>Show answer</summary>

```bash
grep 198.51.100.66 server.log | head -10
grep -c 198.51.100.66 server.log
```
Every line is `POST /login` answered with `401` (unauthorized): dozens of
failed login attempts = a brute-force password-guessing attack. Phase 7
builds the defense (rate limiting); Phase 8 rebuilds it on Redis.
</details>

### 7. What's the average response duration across ALL requests?

<details><summary>Show answer</summary>

```bash
awk '{sum += $8; n++} END {printf "%.1fms average over %d requests\n", sum/n, n}' server.log
```
awk quietly ignores the "ms" suffix when doing arithmetic on `23ms`.
</details>

### 8. Which *path* is slow? Compute the average duration **per path**.

<details><summary>Show answer</summary>

```bash
awk '{sum[$6] += $8; n[$6]++} END {for (p in sum) printf "%-12s %6.1fms avg (%d reqs)\n", p, sum[p]/n[p], n[p]}' server.log
```
`sum[$6]` is an awk *associative array* — a running total per path (your
first hash map in action! Phase 4 formalizes it). `/search` averages
~700–1500ms while everything else sits under ~100ms: the planted slow
endpoint. Phase 12 explains *why* search is the thing that gets slow — and
fixes it properly.
</details>

### 9. Print the 3 slowest individual requests.

<details><summary>Show answer</summary>

```bash
sort -k8 -rn server.log | head -3
```
Sort by column 8 (`-k8`), numerically and reversed (`-rn`), take three.
</details>

### 10. Produce a copy of the log with all IPs anonymized to `x.x.x.x` (don't modify the original).

<details><summary>Show answer</summary>

```bash
sed -E 's/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/x.x.x.x/' server.log > anonymized.log
head -3 anonymized.log
```
The regex reads: "one-or-more digits, a literal dot (escaped `\.`), four
times." Redirecting with `>` writes a NEW file; the original is untouched
(no `-i`). Anonymizing logs like this is a real compliance task.
</details>

### 11. How many *distinct* pages (paths) were requested?

<details><summary>Show answer</summary>

```bash
awk '{print $6}' server.log | sort -u | wc -l
```
`sort -u` = sort and keep uniques (a shortcut for `sort | uniq`).
</details>

### 12. Watch the log grow live: run `tail -f server.log` in one terminal, and in a second terminal append a fake line with `echo`. See it appear instantly.

<details><summary>Show answer</summary>

Terminal 1:
```bash
tail -f server.log
```
Terminal 2:
```bash
echo '2026-07-15 12:00:00 [INFO] 127.0.0.1 GET /made-by-hand 200 1ms' >> server.log
```
The line pops up in terminal 1 the instant you press Enter — `tail -f` is
literally watching the file for growth. From Phase 2 on, this is how you'll
watch LinkBoard's own logs while you click and curl. (`Ctrl+C` to stop.)
</details>

---

Done? Head back to `lesson.html` — section 12, Part E (the runaway process). 🎯
