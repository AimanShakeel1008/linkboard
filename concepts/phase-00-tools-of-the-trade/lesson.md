# Phase 0 — Tools of the Trade: Linux & Git

> **Covers:** M23 (Linux), M28 (Git)
> **Why first:** every single phase after this one happens *inside a terminal* and
> ends with a *git commit*. These two tools are the pencil and notebook of the
> whole journey. Learn them now and everything else gets easier.

---

## 0. What you'll be able to do by the end of this phase

- Open a terminal and feel at home: move around, look inside files, search them.
- Slice and dice a real log file with `grep`, `awk`, `sed`, `sort`, `tail`.
- Find a misbehaving program on your machine and stop it (`ps`, `top`, `kill`).
- Ask the network questions with `curl` and `dig`.
- Read and change file permissions (`chmod`) and understand what `755` means.
- Understand what SSH, `scp`, and `rsync` are for (we'll use them for real in later phases).
- Schedule a task to run automatically with `cron`.
- Write a small shell script and read the ones I wrote for you.
- Understand Git *from the inside*: what a commit actually is, why branches are
  cheap, what merge vs rebase really do, and how to rescue yourself with
  `reflog` and `bisect`.
- Put this repo on GitHub with your first push.

There is **zero assumed knowledge** below. If you already know a section, skim it.

---

## 1. First, your machine: Windows, and the Linux inside it

### 1.1 What is an operating system? (CS fundamental 🧱)

Your computer's hardware — the chip that computes (CPU), the fast temporary
memory (RAM), the disk, the network card — is like an orchestra of instruments.
None of them know how to cooperate on their own. The **operating system (OS)**
is the conductor: a big program that starts when the computer turns on and then
manages everything — which program gets to use the CPU right now, where files
live on disk, who may talk to the network.

Windows is one OS. macOS is another. **Linux** is a third — and it's the one
that matters most for this course, because **almost every server on the
internet runs Linux**. When LinkBoard eventually "runs in the cloud," it will
run on Linux machines. (Why? It's free, open-source, rock-solid, and built to
be operated remotely through text commands — we'll appreciate each of those
properties as we go.)

### 1.2 So how do we practice Linux on your Windows laptop?

Windows 11 has a wonderful feature called **WSL — Windows Subsystem for
Linux**. Plain words: *a real Linux system running inside your Windows machine,
side by side with it.* You open a terminal, type `wsl`, and you're "in Linux" —
real Linux commands, real Linux behavior — without rebooting or installing a
second computer.

**Analogy:** WSL is like having a fully equipped guest workshop inside your
house. Your house is Windows; the workshop is Linux. You walk in whenever you
want to use its tools, and walk out when you're done. (Where the analogy
breaks: the workshop can see and touch your house's files too — your Windows
`D:\` drive appears inside Linux at `/mnt/d/` — so it's more connected than a
real separate room.)

We will install WSL in this phase's "Run it & watch the logs" section. Two
reasons it's worth it now:

1. This phase's Linux material needs a real Linux (things like `cron` and
   proper process tools don't exist on plain Windows).
2. **Docker** (Phase 9) runs on top of WSL on Windows anyway — so this install
   is an investment, not a detour.

> **Fallback note:** Git for Windows ships with "Git Bash," a mini
> Linux-flavored terminal. Most *text* commands in this lesson (`grep`, `awk`,
> `sed`, `ls`, `cat`) work there too. But `cron`, `top`, and real process
> management do not. Use Git Bash in a pinch; use WSL for the full lesson.

---

## 2. The terminal: a conversation with the operating system

### 2.1 What a terminal actually is

Long before mice and windows, people controlled computers by *typing sentences
at them*. That's still the most powerful way, and it's how every server is
managed today (servers don't have screens attached!).

- The **terminal** is the window you type into.
- The **shell** is the program *listening* on the other side, reading what you
  type, running it, and printing the answer. On Linux the standard shell is
  called **bash** (there are others, like `zsh`; same ideas).
- The **prompt** is the short text the shell prints when it's ready for your
  next command — often something like `aiman@laptop:~$`. The `~` means "you are
  currently in your home folder" and `$` means "I'm ready, type something."

**Analogy:** the shell is a hyper-literal assistant standing at a counter. You
say a command, it does *exactly* that — no more, no less, no guessing what you
meant — and reports back. Its literalness is why it feels harsh at first and
why it's so dependable later.

### 2.2 Anatomy of a command

```bash
ls -l /var/log
```

Three parts:
- `ls` — the **command** (a small program; `ls` means "list files").
- `-l` — a **flag/option** (a switch that changes behavior; `-l` = "long
  format, show details"). Flags start with `-` (short) or `--` (long, like
  `--help`).
- `/var/log` — an **argument** (the thing to operate on; here, a folder).

Nearly every command accepts `--help`, and `man ls` opens its full manual
("man" = manual). When lost: `man <command>` or `<command> --help`.

### 2.3 The file system is a tree (CS fundamental 🧱)

Files on a computer are organized like an upside-down tree. On Linux the top
(the "root") is written `/`. Everything lives beneath it:

```
/                    ← the root: the top of everything
├── home/
│   └── aiman/       ← your personal folder ("home"), shortcut: ~
├── etc/             ← system configuration files
├── var/
│   └── log/         ← where programs write their logs
├── tmp/             ← scratch space, wiped on reboot
└── mnt/
    └── d/           ← in WSL: your Windows D:\ drive!
```

A **path** is the address of a file in this tree: `/home/aiman/notes.txt`.
- An **absolute path** starts at the root: `/var/log/syslog`.
- A **relative path** starts from *where you currently are*: `playground/server.log`.
- `.` means "the folder I'm in," `..` means "one folder up."

### 2.4 The commands you'll use constantly

| Command | Plain-language meaning |
|---|---|
| `pwd` | "Where am I?" (print working directory) |
| `ls` | "What's here?" (`ls -la` = details + hidden files) |
| `cd somewhere` | "Go there" (`cd ..` = up one, `cd ~` = home) |
| `mkdir name` | "Make a folder" (`mkdir -p a/b/c` makes the whole chain) |
| `cat file` | "Print the whole file to the screen" |
| `less file` | "Open the file in a scrollable viewer" (`q` to quit) |
| `head -20 file` / `tail -20 file` | "Show the first / last 20 lines" |
| `cp a b` / `mv a b` | "Copy / move-or-rename a to b" |
| `rm file` | "Delete" — **no recycle bin. Gone is gone.** |
| `touch file` | "Create an empty file (or update its timestamp)" |
| `echo hello` | "Print this text" (sounds useless; wildly useful in scripts) |
| `history` | "What have I typed recently?" |

Hidden files: on Linux, any file whose name starts with a dot (like `.gitignore`)
is "hidden" — `ls` skips it unless you say `ls -a`. That's the whole mechanism;
nothing magical.

### 2.5 The superpower: pipes and redirection (CS fundamental 🧱)

Every Linux program has three standard "hoses" attached to it:

- **stdin** ("standard input") — where it reads from (usually your keyboard),
- **stdout** ("standard output") — where its normal answers go (usually your screen),
- **stderr** ("standard error") — where its complaints go (also your screen, but a *separate hose* so you can split them).

Because these are standardized, you can **connect programs together like
garden hoses**:

```bash
# The pipe "|" plugs stdout of the left program into stdin of the right one.
cat server.log | grep ERROR | wc -l
# read the file → keep only lines containing ERROR → count the lines
```

**Analogy:** an assembly line. Each worker (program) does ONE small job well
and passes the result down the belt. `grep` only filters. `sort` only sorts.
`wc` only counts. Ten tiny tools that compose beat one giant tool that doesn't.
This is called the **Unix philosophy**, and (spoiler) it's also the soul of
good system design: small components with clean interfaces, composed.

Redirection sends output to *files* instead of the screen:

```bash
echo "hello" >  out.txt   # write (OVERWRITES the file)
echo "again" >> out.txt   # append (adds to the end)
some_command 2> errors.txt   # send only the error hose (stderr) to a file
some_command > all.txt 2>&1  # send BOTH hoses into one file
```

You'll see `2>&1` in the wild constantly. Decoded: hose `2` (stderr), redirect
(`>`), into wherever hose `&1` (stdout) currently points.

---

## 3. Slicing text: grep, awk, sed & friends

Servers narrate their lives into **log files** — long text files where each
line is one event. Being able to interrogate a log file is *the* everyday
superpower of anyone who runs systems. Our playground has a script that
generates a realistic fake web-server log (`server.log`) with lines like:

```
2026-07-15 10:23:01 [INFO]  203.0.113.42  GET  /links        200  23ms
2026-07-15 10:23:04 [ERROR] 198.51.100.7  POST /links        500  812ms
```

Read one line out loud: on July 15 at 10:23:01, severity INFO, the visitor at
IP address 203.0.113.42 requested the page `/links` using GET, the server
answered with status 200 ("OK"), and it took 23 milliseconds. (Every one of
those pieces — IP, GET, status codes — gets its own deep lesson in Phases 2–3.
For now they're just columns of text to practice on.)

### 3.1 `grep` — keep only matching lines

Plain words: *"show me only the lines that contain this."* The name is ancient
Unix lore (g/re/p = "globally search a regular expression and print") — just
think "filter."

```bash
grep ERROR server.log            # lines containing "ERROR"
grep -c ERROR server.log         # just count them
grep -v INFO server.log          # -v inVerts: lines NOT containing INFO
grep -n "500" server.log         # show line numbers too
grep -i error server.log         # -i = case-insensitive
grep "GET /links " server.log    # any literal text works, not just words
```

`grep` can also match *patterns* rather than exact text, using **regular
expressions** ("regex") — a mini-language for describing text shapes, e.g.
`grep -E " 5[0-9][0-9] "` finds any 500-class status (500, 502, 503…). Regex
deserves its own hour; we'll pick pieces up as needed.

### 3.2 `awk` — think in columns

Plain words: *"treat each line as columns and let me compute with them."*
`awk` automatically splits every line on whitespace and names the columns
`$1, $2, $3…` (`$0` = the whole line).

Our log's columns: `$1`=date `$2`=time `$3`=level `$4`=IP `$5`=method
`$6`=path `$7`=status `$8`=duration.

```bash
awk '{print $6}' server.log                 # just the path column
awk '$7 == 500 {print $4, $6}' server.log   # IP + path of every 500 error
awk '{sum += $8; n++} END {print sum/n "ms avg"}' server.log
# ^ add up column 8 across all lines, then print the average at the END
# (awk conveniently ignores the "ms" suffix when doing math on "23ms")
```

That last one is a real thing you'll do in production: "what's our average
response time?" answered in one line, no spreadsheet.

### 3.3 `sed` — find & replace as a stream

Plain words: *"edit text as it flows past."* (**s**tream **ed**itor.) The one
form to know:

```bash
sed 's/ERROR/PROBLEM/' server.log     # replace first ERROR per line (prints result; file untouched)
sed 's/ERROR/PROBLEM/g' server.log    # /g = every occurrence on the line
sed -i 's/foo/bar/g' file.txt         # -i = actually modify the file in place (careful!)
```

`s/old/new/` — "substitute old with new." That's 90% of real-world `sed` use.

### 3.4 `sort`, `uniq`, `wc` — the counting crew

```bash
wc -l server.log                       # how many lines (= events) total?
awk '{print $4}' server.log | sort | uniq -c | sort -rn | head -5
# ^ THE classic pipeline, worth reading slowly:
#   print every IP → sort them (uniq needs neighbors grouped) →
#   collapse repeats and COUNT them (-c) → sort by count, biggest first (-rn) →
#   top 5. Translation: "who are my top 5 visitors?"
```

You will type a variant of that pipeline hundreds of times in your career:
top IPs, top URLs, top error messages, top slow endpoints.

### 3.5 `find` — search by file properties

`grep` searches *inside* files; `find` searches *for* files:

```bash
find . -name "*.log"              # every .log file under the current folder
find . -name "*.sh" -type f       # only regular files (-type d = folders)
find /var/log -mtime -1           # modified in the last 1 day
find . -name "*.tmp" -delete      # find AND delete (test without -delete first!)
```

### 3.6 `tail -f` — watch a log live

```bash
tail -f server.log
```

`-f` = "follow": print the last lines, then **keep waiting** and print each new
line the instant it's appended. This is how you watch a live server breathe.
From Phase 2 onward, you'll routinely have one terminal running the app and
another running `tail -f` (or just watching the app's own output). `Ctrl+C`
stops it — and that's general: **`Ctrl+C` politely stops the currently running
foreground program** in any terminal.

---

## 4. Processes: programs in motion

### 4.1 What a process is (CS fundamental 🧱)

A program *file* on disk (like `python` or `chrome.exe`) is just a recipe. A
**process** is that recipe *actually cooking*: the OS has loaded it into
memory, given it a slice of CPU time, and it's running. Open Chrome three
times → one program, three processes. Each process gets a unique number, its
**PID** (process ID) — its ticket number in the OS's system. (Phase 1 goes
much deeper: threads, context switching, scheduling.)

### 4.2 Seeing processes

```bash
ps aux                 # snapshot of ALL processes right now
ps aux | grep python   # ...filtered to ones mentioning "python" (pipes again!)
top                    # live, self-updating dashboard (q to quit)
```

In `ps aux`, the columns you care about: `USER` (who owns it), `PID` (its
number), `%CPU` and `%MEM` (how much of the machine it's eating), and the
command at the end. In `top`, processes are sorted by CPU by default — a
runaway process floats straight to the top. 100% means "fully using one CPU
core."

### 4.3 Stopping processes: signals

You stop a process by sending it a **signal** — a tiny standardized message
from the OS.

```bash
kill 1234          # send SIGTERM to PID 1234: "please shut down cleanly"
kill -9 1234       # send SIGKILL: the OS removes it immediately, no appeal
pgrep -f runaway   # find PIDs whose command line matches "runaway"
pkill -f runaway   # find AND signal them in one step
```

**Analogy:** `SIGTERM` is a tap on the shoulder — "we're closing, please
finish up" — and a well-written program uses the chance to save its work and
exit cleanly. `SIGKILL` (`-9`) is security lifting the person out of the chair
mid-sentence — instant, but whatever they were writing is lost. **Always try
plain `kill` first**; reach for `-9` only when a process ignores you. (`Ctrl+C`
in a terminal sends a cousin signal, SIGINT — "interrupt".)

This matters for system design later: "graceful shutdown" — finishing
in-flight requests when asked to stop — is exactly a program handling SIGTERM
well, and Kubernetes (Phase 19) sends SIGTERM to your containers every single
deploy.

The playground's `runaway.sh` deliberately pins a CPU core so you can practice
the full hunt: notice → identify (`top`) → find PID (`pgrep`) → terminate.

---

## 5. Talking to networks (a taste — Phase 2 is the feast)

Two commands to meet today, because we'll use them constantly:

**`curl`** — make a web request from the terminal. When your browser opens a
page, it sends a request and renders the response; `curl` sends the same
request and just shows you the raw response.

```bash
curl https://example.com          # fetch a page, print its raw HTML
curl -i https://example.com      # -i: also show response HEADERS (metadata)
curl -v https://example.com      # -v: verbose — the entire conversation, both directions
```

From Phase 4 on, `curl` is how you'll poke LinkBoard's API directly.

**`dig`** — ask the internet's phone book. Humans use names
(`example.com`); computers connect to numeric addresses (IPs). **DNS** is the
global directory translating one to the other, and `dig example.com` shows you
the lookup happening. Full DNS chain — root servers, TTLs, caching — in Phase 2.

Also in the toolbox (previewed now, used later): `ping host` ("are you
alive? how far away?"), and `ss -tlnp` ("which programs on *this* machine are
listening for network connections, on which ports?" — indispensable from
Phase 2 on, e.g. to answer "is something already using port 8000?").

---

## 6. Permissions: who may do what

Every file on Linux has an owner and a permission list. `ls -l` shows it:

```
-rwxr-xr--  1 aiman aiman  512 Jul 15 10:00 make_logs.sh
```

Decode `-rwxr-xr--` in three groups of three after the first character
(`-`=file, `d`=directory):

| Chunk | Who | Meaning here |
|---|---|---|
| `rwx` | the **owner** (aiman) | may **r**ead, **w**rite, e**x**ecute |
| `r-x` | the owner's **group** | may read and execute, not modify |
| `r--` | **everyone else** | may only read |

"Execute" on a script/program means "may run it." That's why a freshly
written script won't run until you mark it executable:

```bash
chmod +x make_logs.sh       # add execute permission
./make_logs.sh              # now it runs
```

(Why `./`? For safety the shell only runs commands from trusted system
folders by default. `./` says "the one right here, yes I mean it.")

The numeric form you'll see everywhere: each chunk becomes a digit by adding
r=4, w=2, x=1. So `chmod 755` = owner `7`(4+2+1=rwx), group `5`(4+1=r-x),
others `5` — the standard for scripts. `chmod 600` = owner read/write only,
everyone else nothing — the standard for secrets (SSH keys refuse to work
without it, on purpose). `chown user file` changes the owner; `sudo cmd` runs
one command as the all-powerful **root** administrator account ("**s**uper
**u**ser **do**") — Linux will ask for your password and you should feel a
tiny jolt of caution every time.

---

## 7. SSH, scp, rsync — operating machines you can't touch

Real servers live in data centers; you'll never sit at their keyboards. **SSH
(Secure Shell)** gives you a *terminal on a remote machine, encrypted*, as if
you were there: `ssh aiman@server-address` → the prompt you get is *theirs*,
every command runs *there*.

SSH's login trick is worth understanding because Git uses it too: instead of
passwords, it uses a **key pair** — two mathematically linked files. The
**public key** is like a padlock you can hand out freely (you put a copy on
every server / on GitHub); the **private key** is the only key that opens it,
and it *never leaves your machine* (that's the file that must be `chmod 600`).
When you connect, the server snaps your padlock shut on a random challenge;
only your private key can pop it open; proof complete, no password ever
crosses the wire. (Asymmetric cryptography, properly explained in Phase 7 —
today the padlock picture is enough.)

Copying files rides on top of SSH:
- `scp file.txt user@server:/home/user/` — simple copy, whole file, every time.
- `rsync -avz folder/ user@server:/backup/` — the smart mover: compares both
  sides and sends **only what changed**. Re-run it and it finishes in a
  second. This "only ship the difference" idea returns over and over in
  system design (replication, CDNs, Docker layers).

We have no remote server yet — these get hands-on in the cloud phases. But
you may create an SSH key for GitHub in this phase's setup (optional; HTTPS
works fine too).

---

## 8. cron — the machine's alarm clock

**cron** is a background service that runs commands *on a schedule* you
define. Every user has a **crontab** ("cron table") — edit it with
`crontab -e`, list it with `crontab -l`. Each line: five time fields, then
the command.

```
┌───────── minute (0–59)
│ ┌─────── hour (0–23)
│ │ ┌───── day of month (1–31)
│ │ │ ┌─── month (1–12)
│ │ │ │ ┌─ day of week (0–7, both 0 and 7 = Sunday)
* * * * *  command-to-run        # * means "every"
```

Examples: `* * * * *` = every minute. `30 2 * * *` = daily at 02:30.
`0 9 * * 1` = Mondays at 09:00. (crontab.guru is a great decoder site.)

Two classic gotchas, both of which you'll meet in the exercise:
1. **cron runs with a minimal environment** — your fancy PATH and variables
   aren't there. Always use absolute paths in cron lines.
2. **cron is silent.** No terminal, no visible output. If you want evidence,
   redirect output to a file yourself (`>> /path/to/log 2>&1` — both hoses,
   appended). Our exercise does exactly this.

Cron is the great-grandparent of every "scheduled job" system you'll ever
meet (GitHub Actions schedules, Kubernetes CronJobs, Airflow in Phase 23 —
all speak this same five-field syntax).

> **WSL note:** WSL doesn't always start background services automatically.
> The run section includes the one command to start cron and how to check it.

---

## 9. Shell scripting: gluing commands into programs

A shell script is just commands in a file, run top to bottom. Everything you
type interactively can be scripted. The essentials, all of which appear in
the playground scripts you're about to read:

```bash
#!/usr/bin/env bash
# ^ The "shebang" line: tells the OS which interpreter runs this file.
#   (#! = "hash-bang" → "shebang". This exact line = "find bash and use it.")

set -euo pipefail
# Safety switches, highly recommended in every script:
#   -e  : stop immediately if any command fails (don't barrel on into chaos)
#   -u  : using an undefined variable is an error (catches typos)
#   -o pipefail : a pipeline fails if ANY stage fails, not just the last

NAME="LinkBoard"              # variable: NO spaces around = (a classic trap)
echo "Hello from $NAME"       # use with $  — "double quotes" allow $expansion
echo 'literal $NAME'          # 'single quotes' = completely literal

TODAY=$(date +%F)             # $(...) = command substitution:
                              # run the command, use its output as a value

if [ -f server.log ]; then    # [ ... ] tests things; -f = "file exists?"
  echo "log exists"
else
  echo "no log yet"
fi

for i in 1 2 3; do            # loops
  echo "round $i"
done

greet() {                     # functions
  echo "hi, $1"               # $1 = the function's first argument
}
greet "aiman"
```

One more idea that matters everywhere: **exit codes**. Every command finishes
with a number — `0` = success, anything else = failure. The shell stores the
last one in `$?`. This convention is load-bearing: `if` statements check it,
`set -e` watches it, and later your CI pipeline (Phase 18) decides
"tests passed → deploy" purely by exit codes.

---

## 10. Git from the inside out

### 10.1 The problem

You've lived the problem: `essay_final.doc`, `essay_final_v2.doc`,
`essay_FINAL_really.doc`. Code makes it worse — many files changing together,
several people editing at once, and the burning question "it worked
yesterday, WHAT changed?"

A **version control system** answers all of it: every saved state is kept
forever, labeled, diff-able, and shareable. **Git** (2005, Linus Torvalds,
built to manage Linux itself) is the one that won.

### 10.2 Mental model #1: snapshots, not diffs

Intuition says a version tool stores *changes* ("line 12 edited"). Git does
the opposite: **every commit is a complete snapshot of your entire project**,
like a photo of your whole desk taken each time you hit save.

"Doesn't that waste huge space?" No — and the trick is beautiful. If a file
didn't change between snapshots, Git doesn't store it again; the new snapshot
just **points at the file it already has**. To make that safe, Git names every
stored object by a **hash** of its content.

**What's a hash? (CS fundamental 🧱 — this idea returns in Phases 4, 6, 7, 8, 15!)**
A hash function is a machine that eats any data and spits out a fixed-length
fingerprint, e.g. `d670460b4b4aece5915caf5c68d12f560a9fe3e4`. Three properties
matter: the same input *always* gives the same fingerprint; a one-character
change gives a wildly different fingerprint; and you can't reconstruct the
input from the fingerprint. So: **identical content ⇒ identical hash ⇒ store
it once**. And if a file is ever corrupted on disk, its content no longer
matches its name — Git notices instantly. Content-addressed storage: the
fingerprint *is* the filename.

### 10.3 Mental model #2: the three areas

Between "I edited a file" and "it's saved in history" there's a staging step:

```
 Working directory  --git add-->   Staging area   --git commit-->   Repository
 (your real files,                 (the "photo                      (permanent
  freely editable)                  lineup": what                    history in
                                    the NEXT snapshot                the .git/
                                    will contain)                    folder)
```

**Analogy:** you're a photographer. The working directory is the messy studio.
`git add` places chosen items on the set — you compose the shot. `git commit`
clicks the shutter; the photo goes in the permanent album. The staging area
exists so a commit can be a *curated, coherent* set of changes ("the login
fix") rather than "whatever happened to be lying around."

The daily loop, forever: edit → `git status` (what changed?) → `git add` →
`git commit -m "message"`. And `git diff` shows edits not yet staged, while
`git log --oneline` lists the album.

### 10.4 Inside `.git/`: blobs, trees, commits

Everything lives in the hidden `.git/` folder, as objects of three kinds:

- **blob** — file *contents* (just the bytes; no name, no date).
- **tree** — a *folder listing*: names, pointing at blobs and other trees.
- **commit** — the snapshot record: points at one root tree, plus author,
  date, message, and — crucially — **the hash of the parent commit**.

Because each commit names its parent, commits form a **chain** (properly: a
DAG — a chain that can also fork and re-join, as branches do):

```
A ← B ← C ← D   (D's parent is C; C's is B; ... "history" = follow the arrows)
```

One profound consequence: a commit's hash covers its content *and its
parent's hash*, which covered *its* parent's… so **you cannot alter any
historical commit without every later hash changing**. History is
tamper-evident, like a wax seal over a wax seal over a wax seal. Hold that
thought — the same "hash-chained, append-only log" idea reappears as Kafka's
log (Phase 11) and the database write-ahead log (Phase 15). The playground's
`git_xray.sh` dissects your very first commit into these objects so you can
see all of this with your own eyes.

### 10.5 Branches: just sticky notes

Given the chain of commits, what's a branch? Prepare for an anticlimax:
**a branch is a 41-byte file containing one commit hash.** That's all. A
sticky note saying "the branch called `main` is currently at commit D." Commit
again → Git moves the sticky note to E. **HEAD** is one more sticky note
saying which branch *you're on right now*.

That's why branches are free and instant in Git (in older systems, branching
copied the whole project!). Make them casually:

```bash
git switch -c experiment    # new branch here + switch to it (-c = create)
# ...hack freely, commit freely; main is untouched...
git switch main             # walk back to safety; the experiment waits
```

### 10.6 Merge vs rebase

You branched at C, made X and Y; meanwhile `main` moved on to E. Combining
has two philosophies:

```
        X ← Y  (feature)                          X' ← Y'  (feature, replayed)
       /                                         /
A ← B ← C ← D ← E  (main)          A ← B ← C ← D ← E  (main)

MERGE: add a new "merge commit"     REBASE: re-apply X and Y on top of E,
with TWO parents (Y and E),         as if you'd started there. Straight-line
weaving both histories together.    history; but X'/Y' are NEW commits.
History = what truly happened.      History = tidied story.
```

- **Merge** is honest and safe: nothing is rewritten; the join is recorded.
  Cost: history becomes a braid, harder to read.
- **Rebase** is tidy: a clean straight line. Cost: it *rewrites* commits
  (new hashes!). **The iron rule: never rebase commits you've already pushed
  and others may have built on** — you'd be swapping out bricks other people
  are standing on.

Either way, if both sides edited the same lines, Git stops and asks you — a
**conflict**. It marks the file with `<<<<<<<` / `=======` / `>>>>>>>` fences
around "your version / their version"; you edit the file into the version you
actually want, delete the fences, `git add` it, and continue. Not an error —
just Git refusing to guess.

### 10.7 The rescue kit: cherry-pick, bisect, reflog

- **`git cherry-pick <hash>`** — "copy that one commit from another branch
  onto mine." Classic use: one urgent fix from a big unfinished branch.
- **`git bisect`** — "it worked last month, it's broken now, 300 commits
  in between." Give Git one good and one bad commit; it checks out the
  midpoint, you say `good` or `bad`, repeat. It's **binary search**
  (CS fundamental 🧱): halving the suspects each round finds the culprit in
  ~9 questions instead of 300. log₂(n) beats n — an idea we'll meet again in
  database indexes (Phase 6).
- **`git reflog`** — the safety net under the safety net. Git privately logs
  *every* place HEAD has been, even through "history-destroying" mistakes.
  Deleted a branch? Botched a rebase? `git reflog`, find the hash from before
  the disaster, `git switch -c rescue <hash>`. **Almost nothing committed is
  ever truly lost in Git.** Commit early, commit often — commits are your
  save points.

### 10.8 Remotes and GitHub

Everything so far lived on your machine. A **remote** is another copy of the
repository elsewhere; **GitHub** is a company hosting remotes (plus reviews,
issues, CI — Phase 18). The verbs:

- `git clone <url>` — copy a remote repo to your machine.
- `git push` — send my new commits up.
- `git fetch` — download their new commits, *don't* touch my files yet.
- `git pull` — fetch **and** merge into my branch (= fetch + merge).

The default remote is nicknamed **`origin`**. The one-time
`git push -u origin main` means "push `main` to `origin` and remember the
pairing (`-u`)" — after that, plain `git push` suffices. In this project,
every phase ends with a push, so GitHub holds the full journey — and any
machine can resume it.

### 10.9 Workflows and version numbers (the 5-minute cultural tour)

How teams *use* branches, two schools:
- **GitFlow:** long-lived `develop` branch, `release/` branches, `hotfix/`
  branches — a formal pipeline. Suits shipped/versioned software (mobile
  apps, desktop software).
- **Trunk-based:** everyone merges small changes into `main` ("trunk")
  quickly — daily or faster; unfinished features hide behind feature flags
  (Phase 18). Suits continuously deployed web services — like LinkBoard.
  It's what we'll practice: short-lived work, frequent merges to `main`.

And **semantic versioning (semver)** — the meaning behind `2.4.1` =
`MAJOR.MINOR.PATCH`: bump **PATCH** for bug fixes (safe to upgrade),
**MINOR** for new features that break nothing, **MAJOR** for breaking
changes (upgrading requires work from users). One glance answers "is this
upgrade dangerous?" You'll rely on this reading every dependency from
Phase 4 onward.

---

## 11. The code I wrote for you — walkthrough

All in [concepts/phase-00-tools-of-the-trade/playground/](playground/). Each
file is heavily commented — **the comments are part of the lesson; read them.**

| File | What it's for |
|---|---|
| `make_logs.sh` | Generates `server.log` — ~800 lines of realistic fake web-server traffic (with planted patterns: an error burst, one attacker IP, one slow endpoint) for you to hunt with grep/awk/sed. |
| `exercises.md` | The guided hunt: 12 investigation tasks against `server.log`, each with a collapsible answer. |
| `runaway.sh` | Deliberately pins a CPU core so you can practice find-and-kill with `top`, `pgrep`, `kill`. |
| `heartbeat.sh` | Tiny script that appends a timestamped line to `heartbeat.log` — your cron exercise target. |
| `git_xray.sh` | After your first commit: dissects `.git/` and shows the actual blob/tree/commit objects and the branch pointer file. Section 10 made visible. |

Things to notice while reading them:
- Every script starts with the shebang + `set -euo pipefail` (section 9).
- Every script **narrates what it does** in `[STEP]`-style log lines — the
  logging-as-teaching habit this whole course uses, starting now.
- `make_logs.sh` seeds its randomness (`RANDOM=42`) so your file and my
  expected outputs match closely.

---

## 12. Run it & watch the logs

> Reminder of our contract: **you** run everything; I never do. Do the parts
> in order; paste anything surprising back to me and I'll interpret it.
> **Part A (git init / GitHub / first push) is in the chat message that
> accompanies this lesson — do that first.** Then continue here.

### Part B — one-time: install WSL (your Linux)

In **PowerShell (run as Administrator)**:

```powershell
wsl --install
```
*What it does:* installs WSL and Ubuntu Linux (the most common beginner
distribution). **Expect:** progress messages, then a request to **reboot**.
After reboot, an Ubuntu window opens and asks you to pick a Linux username
and password (this is separate from Windows; you'll use the password for
`sudo`). **Success looks like:** a prompt such as `aiman@YOURPC:~$`.
**If it says WSL is already installed:** run `wsl --install -d Ubuntu` to add
Ubuntu, or just `wsl` to enter it. **If virtualization errors appear:**
virtualization may be disabled in BIOS — tell me the exact message.

From now on, "in Linux" means: open Windows Terminal → `wsl` (or open the
Ubuntu app).

### Part C — enter the playground

```bash
cd /mnt/d/Projects/linkboard/concepts/phase-00-tools-of-the-trade/playground
ls -l
```
*What it does:* navigates to the playground **via WSL's window into your D:
drive** and lists it. **Expect:** the five files from section 11. Note the
permissions column — the `.sh` files likely do **not** show `x` yet.

```bash
chmod +x make_logs.sh runaway.sh heartbeat.sh git_xray.sh
ls -l
```
*What it does:* marks the scripts executable (section 6). **Expect:** `x`
appearing in the permissions, e.g. `-rwxr-xr-x`.

### Part D — generate the log file and hunt

```bash
./make_logs.sh
```
**Expect (annotated):**
```
[STEP] Generating fake web-server traffic into server.log ...
[STEP] Planting an ERROR burst around 11:42 ...          ← you'll FIND this with grep
[STEP] Planting a suspicious IP (198.51.100.66) ...      ← and this with awk|sort|uniq
[STEP] Planting a slow endpoint (/search) ...            ← and this with awk arithmetic
[DONE] Wrote ~800 lines to server.log — happy hunting.
```
**Success check:** `wc -l server.log` prints roughly 800. **Failure signs:**
`Permission denied` → chmod step skipped; `bad interpreter: /bin/bash^M` →
Windows line endings snuck in — tell me, the fix is one command (`sed -i
's/\r$//' *.sh`), and our `.gitattributes` prevents it for good.

Then open **`exercises.md`** and work the 12 hunts. Try each before expanding
the answer. This is the heart of the phase — budget an unhurried hour.

### Part E — the runaway process

Open **two** WSL terminals side by side.

Terminal 1:
```bash
./runaway.sh
```
**Expect:** `[RUNAWAY] I am PID 12345 and I am about to waste CPU...` then
silence (it's busy!).

Terminal 2:
```bash
top                          # find the culprit: ~100% CPU, name "runaway.sh" — note its PID; q quits
pgrep -f runaway.sh          # the same PID, found by name
kill <PID>                   # polite SIGTERM
```
**Expect:** Terminal 1 prints `[RUNAWAY] Caught SIGTERM — cleaning up
politely. Goodbye.` and exits — *graceful shutdown, visible*. Run it once
more and this time `kill -9 <PID>`: Terminal 1 just prints `Killed` — no
goodbye, no cleanup. That difference **is** section 4.3.

### Part F — cron heartbeat

```bash
sudo service cron start        # WSL doesn't auto-start services; expect: "Starting periodic command scheduler cron" or "already running"
crontab -e                     # first time: pick an editor — choose nano (easiest)
```
Add this line at the bottom (adjust the path if your repo lives elsewhere),
save (in nano: `Ctrl+O`, Enter, `Ctrl+X`):
```
* * * * * /mnt/d/Projects/linkboard/concepts/phase-00-tools-of-the-trade/playground/heartbeat.sh >> /tmp/heartbeat.log 2>&1
```
*What it does:* every minute, cron runs heartbeat.sh and appends its output
(both hoses — section 2.5) to /tmp/heartbeat.log. Now watch it live:
```bash
tail -f /tmp/heartbeat.log
```
**Expect:** within ~60s, lines start appearing:
```
[HEARTBEAT] 2026-07-15 18:42:01 — cron ran me. Beat #1
[HEARTBEAT] 2026-07-15 18:43:01 — cron ran me. Beat #2
```
Each line proves: cron woke up, ran your script with no terminal attached,
and the redirection captured the evidence. After 2–3 beats, `Ctrl+C` the
tail, then **remove the job** (don't leave it beating forever):
`crontab -e`, delete the line, save. **Failure signs:** nothing after 2
minutes → `service cron status` (started?), and check the path in the cron
line is exactly right (cron + relative paths = the classic gotcha from
section 8).

### Part G — git x-ray (after Part A's first commit exists)

```bash
cd /mnt/d/Projects/linkboard
concepts/phase-00-tools-of-the-trade/playground/git_xray.sh
```
**Expect:** a narrated dissection — your latest **commit** object (with its
parent, or "no parent — the root commit!"), the **tree** it points to, one
**blob**'s actual content, and the single-line file that *is* the `main`
branch. Read it next to section 10.4 and the model clicks into place.

---

## 13. Break it / observe it

Optional experiments — each makes a concept *felt*. Nothing here can hurt
anything outside the playground.

1. **Feel `rm`'s finality:** `touch victim.txt && rm victim.txt` — no
   confirmation, no recycle bin. Now you know why seasoned admins fear
   `rm -rf` with wildcards. (Never run `rm -rf` on a path you haven't
   `ls`-ed first. This reflex will save you one day.)
2. **Feel the two hoses:** `ls playground /nope 2>/dev/null` — the error
   about `/nope` vanishes (stderr redirected into the void `/dev/null`) while
   the listing still prints (stdout untouched). Then swap: `ls playground
   /nope 1>/dev/null` — now only the error shows.
3. **Feel SIGKILL's bluntness:** already done in Part E — but try it a third
   time and `Ctrl+C` instead. Note runaway.sh says goodbye for SIGINT too
   (it handles both politely).
4. **Break a script with CRLF on purpose:** in the playground run
   `sed -i 's/$/\r/' heartbeat.sh && ./heartbeat.sh` — enjoy the cryptic
   `bad interpreter` error, then fix it: `sed -i 's/\r$//' heartbeat.sh`.
   You've just pre-lived the #1 Windows-meets-Linux bug and its cure.
5. **Watch Git notice everything:** edit one character in `README.md`, run
   `git status` and `git diff`, then restore it (`git restore README.md`).
   The working directory is a sandbox; the album is untouched.
6. **Prove commits are tamper-evident:** run `git log --oneline`, note the
   hash. Then `git commit --amend -m "same content, new message"` and look
   again — a **different hash**, because the commit's content changed.
   (Amending the *last, unpushed* commit is fine; amending pushed ones
   violates the iron rule of 10.6.)
7. **Time-travel with reflog:** after experiment 6, `git reflog` shows both
   the old and the amended commit. The "lost" one is still there. Nothing
   committed ever really dies.

---

## 14. Glossary (terms this phase introduced)

- **Operating system (OS):** the conductor program managing hardware and all other programs.
- **Linux:** the open-source OS running most of the world's servers.
- **WSL:** Windows Subsystem for Linux — a real Linux running inside Windows.
- **Terminal / shell / prompt:** the window you type in / the program interpreting your commands (bash) / its "ready" marker.
- **Flag / argument:** a `-x` switch modifying a command / the thing the command acts on.
- **Path (absolute/relative):** a file's address from the root `/` / from where you stand.
- **stdin / stdout / stderr:** a program's standard input, output, and error "hoses."
- **Pipe (`|`):** connect one program's stdout to the next one's stdin.
- **Redirection (`>`, `>>`, `2>&1`):** send output into files; `>>` appends; `2>&1` merges error into output.
- **Unix philosophy:** small single-purpose tools, composed.
- **Regular expression (regex):** a pattern language for matching text shapes.
- **Process / PID:** a running program / its ID number.
- **Signal / SIGTERM / SIGKILL / SIGINT:** OS-to-process messages: "please stop" / "you're gone" / "interrupt" (Ctrl+C).
- **Graceful shutdown:** finishing current work when asked (SIGTERM) before exiting.
- **Permissions / chmod / 755:** per-file read/write/execute rights; the command to change them; the numeric notation (r=4,w=2,x=1).
- **root / sudo:** the all-powerful admin account / "run this one command as root."
- **SSH / key pair (public/private):** encrypted remote terminal / padlock you distribute + key you guard.
- **scp / rsync:** copy files over SSH / copy only the *differences*.
- **cron / crontab:** the scheduler service / your table of scheduled commands.
- **Shebang (`#!`):** first line of a script naming its interpreter.
- **Exit code / `$?`:** a command's success (0) or failure (non-0) number / where the shell keeps the last one.
- **Version control / Git:** keeping every historical state of a project / the dominant tool for it.
- **Hash / content-addressed:** a fixed-size fingerprint of data / storing things under their fingerprint as the name.
- **Blob / tree / commit:** Git's objects — file content / folder listing / snapshot record with parent pointer.
- **Working directory / staging area / repository:** your editable files / the composed next snapshot / the permanent history.
- **Branch / HEAD:** a movable pointer (sticky note) to a commit / the pointer to where *you* are.
- **Merge / rebase / conflict:** weave histories with a 2-parent commit / replay commits onto a new base / Git asking you to resolve overlapping edits.
- **cherry-pick / bisect / reflog:** copy one commit over / binary-search history for a bug / Git's private log of everywhere HEAD has been.
- **Remote / origin / push / pull / fetch / clone:** a repo copy elsewhere / its default nickname / send commits / fetch+merge / download only / copy a repo down.
- **GitFlow / trunk-based:** branch-heavy formal workflow / merge-small-into-main-fast workflow.
- **Semantic versioning:** MAJOR.MINOR.PATCH = breaking / new-but-safe / fix-only.
- **Binary search:** find a target in a sorted range by repeated halving — log₂(n) steps.

---

## 15. Challenges & Questions

Purely optional; think as long or short as you like, answers are one click
away. Nothing is graded, ever.

### Challenge 1: Design the pipeline
Using only `grep`, `awk`, `sort`, `uniq`, `head` and pipes: how would you
find the **top 3 slowest requests** in `server.log`?

<details>
<summary>Show answer</summary>

Sort by the duration column (8th), numerically, descending — then take three:

```bash
sort -k8 -rn server.log | head -3
```

`-k8` = sort by column 8, `-rn` = numeric, reversed. (It works even with the
"ms" suffix because numeric sort reads the leading digits.) An awk-flavored
alternative that prints just what you care about:

```bash
awk '{print $8, $5, $6}' server.log | sort -rn | head -3
```
</details>

### Challenge 2: The silent cron job
Your cron job "doesn't work." You have no output, no errors, nothing. Name
three distinct things you'd check, in order.

<details>
<summary>Show answer</summary>

1. **Is cron even running?** `service cron status` (on WSL it doesn't
   auto-start).
2. **Is the schedule/entry right?** `crontab -l` — is the line there, are
   the five fields what you meant?
3. **Would the command run at all outside cron?** Paste the exact command
   from the crontab into a shell. If it works there but not in cron, it's
   almost always the minimal-environment gotcha: relative paths or missing
   PATH. Absolute paths fix it — and adding `>> /tmp/job.log 2>&1` gives
   cron a voice so this is never silent again.
</details>

### Challenge 3: Why can't you "undo" a push the way you undo a commit?
Amending or rebasing local commits is routine. Why is rewriting *pushed*
history dangerous?

<details>
<summary>Show answer</summary>

Rewriting creates commits with **new hashes** (a commit's hash covers its
content and parent). Anyone who pulled the old commits has built new work *on
top of the old hashes*. Your rewrite makes the remote disagree with their
foundations — their next push is rejected, and untangling it requires manual
surgery on every collaborator's machine. Local history is your draft;
pushed history is a published book others are citing.
</details>

### Challenge 4: Merge or rebase?
Your teammate says "always rebase, merge commits are ugly." When is that
advice *wrong*?

<details>
<summary>Show answer</summary>

Wrong whenever the commits are **shared**: rebasing pushed commits rewrites
history others depend on (Challenge 3). Also wrong when the true shape of
history matters — a merge commit records "these two lines of work joined
here," which can be valuable for auditing ("which release did the fix land
in?"). Reasonable etiquette: rebase your own unpushed work to keep it tidy;
merge (or squash-merge) shared work.
</details>

### Challenge 5: The fingerprint intuition
Git stores a file's content under its hash. Suppose two *different* files in
your project have *identical* content. How many blobs does Git store?

<details>
<summary>Show answer</summary>

**One.** Identical content ⇒ identical hash ⇒ same object name ⇒ stored
once. Both tree entries (the two filenames) point at the same blob. This is
content-addressing paying rent — and the same dedupe-by-fingerprint idea
shows up later in Docker image layers (Phase 9) and CDN caching (Phase 8).
</details>

### Challenge 6 (stretch): kill -9 and the database
Phase 6 will run PostgreSQL. Based on section 4.3, why might `kill -9` on a
database be worse than on our runaway script?

<details>
<summary>Show answer</summary>

SIGKILL gives the process zero chance to finish what it's doing. A database
may be mid-way through writing data structures to disk; killing it
instantly can leave files half-written. Real databases defend against
exactly this with a write-ahead log they replay on startup (Phase 15!) — but
recovery takes time, and you've still risked whatever wasn't logged.
SIGTERM lets it flush and stop cleanly. General rule: `-9` is the last
resort for anything that owns data.
</details>

---

**Next:** once you've done the run sections and we've wrapped this phase
(commit + push), Phase 1 opens the machine itself: binary, CPUs, memory,
processes for real, and the blocking-I/O idea that explains why servers are
built the way they are.
