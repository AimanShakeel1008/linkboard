# Phase 0 — Tools of the Trade: Linux & Git

> **Covers:** M23 (Linux), M28 (Git)
> **Why this comes first:** every phase after this one happens inside a
> terminal, and every phase ends with saving your work using Git. These two
> tools are the pencil and the notebook of the whole journey. If they feel
> comfortable, everything else gets easier.

**How to read this lesson:** slowly, with a terminal open next to it. Every
time you see a **Try it now** block, actually type it. Nothing in this lesson
can damage your computer. If any sentence doesn't make sense, tell me — I will
explain it again, more simply, in smaller pieces. That is the deal for this
whole course.

---

## 0. What you'll be able to do by the end of this phase

- Open a terminal and feel at home: move around, look inside files, search them.
- Investigate a log file (a server's diary) using search-and-count tools.
- Find a misbehaving program on your machine and stop it.
- Understand what file permissions are and how to change them.
- Understand what SSH and cron are for.
- Read and write small shell scripts.
- Understand what Git actually does under the hood — not just which commands
  to type, but what happens when you type them.
- Put this project on GitHub with your first push.

**Zero knowledge is assumed.** If you already know a section, skim it — but
don't skip the Git half; we go deeper than most tutorials ever do.

---

## 1. First, your machine: Windows, and the Linux inside it

### 1.1 What is an operating system? (CS fundamental 🧱)

Your computer is a box of parts: a chip that does calculations (the CPU),
fast temporary memory (RAM), a disk that stores files, a network card. Here
is the problem: none of these parts know how to work together. And when you
run three programs at once, someone has to decide which program gets to use
the CPU *right now*, which parts of memory belong to which program, and who
is allowed to touch which file.

The program that makes all of those decisions is called the **operating
system** (OS for short). It starts the moment you power on the computer, and
it stays in charge until you shut down. Think of it as the **building
manager** of the computer: programs are tenants, and the OS decides who gets
which room (memory), who gets the elevator next (CPU time), and who is
allowed into which office (files).

Windows is one operating system. macOS is another. **Linux** is a third one —
and it is the one this course cares about most, for one simple reason:
**almost every server on the internet runs Linux.** A "server" is just a
computer whose job is to answer requests from other computers — when LinkBoard
eventually runs "in the cloud", it will really be running on Linux machines
in a big building somewhere. So we learn to speak Linux now.

(Why did Linux win the server world? It's free, anyone can inspect and fix
its code, it runs for years without a restart, and it was designed from the
start to be controlled remotely by typing text — no screen needed. Each of
those reasons will make more sense as the course goes on.)

### 1.2 How do we practice Linux on your Windows laptop?

Windows 11 has a feature called **WSL**, which stands for *Windows Subsystem
for Linux*. In plain words: **a real Linux system running inside your Windows
machine, at the same time as Windows.** You open a terminal window, type
`wsl`, and from that moment you are "inside Linux" — real Linux commands,
real Linux behavior — without restarting your computer or buying a second one.

**Analogy:** WSL is like a fully equipped workshop built inside your house.
The house is Windows. The workshop is Linux. You walk in when you want to use
its tools, and you walk out when you're done. One place where this analogy is
*too* separate: the workshop can actually see your house's belongings — your
Windows `D:\` drive appears inside Linux under the folder `/mnt/d/`. So you
can work on the same project files from both sides.

We will install WSL in this phase's "Run it & watch the logs" section
(Part B). Two reasons it's worth doing now rather than later:

1. Some things in this phase (like `cron`, the task scheduler) only exist on
   real Linux — they can't be practiced on plain Windows.
2. **Docker**, a tool we adopt in Phase 9, runs on top of WSL on Windows
   anyway. Installing WSL now is an investment, not a detour.

> **Small fallback note:** when you installed Git on Windows, it came with a
> program called "Git Bash" — a mini terminal that imitates Linux. Most
> *text* commands in this lesson (`grep`, `ls`, `cat`) also work there. But
> the scheduler (`cron`) and the process tools don't. Use Git Bash in a
> pinch; use WSL for the full lesson.

---

## 2. The terminal: a conversation with the operating system

### 2.1 What a terminal actually is

Before computers had mice, windows, and icons, people controlled them by
**typing sentences at them**. That way of working never went away — in fact
it is still how every server on the internet is managed, because servers
don't have screens or mice attached. It is also, once you're used to it,
*faster* and *more precise* than clicking.

Three words you'll hear constantly, and what each one means:

- The **terminal** is the window you type into. Just the window — nothing more.
- The **shell** is the program listening on the other side of that window.
  It reads what you typed, runs it, and prints the answer back. On Linux the
  standard shell is called **bash**. (There are others, like `zsh` — same
  ideas, tiny differences.)
- The **prompt** is the short piece of text the shell prints when it is ready
  for your next command. It usually looks something like:

  ```
  aiman@laptop:~$
  ```

  Reading it left to right: you are user `aiman`, on the machine `laptop`,
  currently standing in the folder `~` (we'll decode `~` in a moment), and
  the `$` means "I'm ready — type something."

**Analogy:** the shell is an extremely literal-minded assistant standing at a
counter. You state a command; it does *exactly* that — no more, no less, no
guessing what you meant — and reports back. That literalness feels harsh in
week one and becomes the thing you love by week three: it never surprises you.

### 2.2 Anatomy of a command

Here is a typical command. Don't run it yet — first let's read it:

```bash
ls -l /var/log
```

It has three parts:

1. `ls` — the **command**: the name of a small program to run. `ls` is short
   for "list" — it lists the files in a folder.
2. `-l` — a **flag** (also called an *option*): a switch that changes how the
   command behaves. `-l` means "long format — show details, not just names."
   Flags start with one dash for short names (`-l`) or two dashes for long
   names (`--help`).
3. `/var/log` — an **argument**: the thing to operate on. Here, which folder
   to list.

So the whole command reads as a sentence: *"List, in detail, the contents of
the folder /var/log."*

Two lifelines when you're lost, and they work for almost every command:

- `ls --help` — prints a short usage summary.
- `man ls` — opens the full **man**ual page (press `q` to quit it).

### 2.3 The file system is a tree (CS fundamental 🧱)

Every file on the computer lives inside a folder; folders live inside other
folders. If you drew that, you'd get a tree shape — one trunk, many branches.
On Linux the trunk (the topmost folder) is written as a single slash: `/`,
called the **root**. Everything on the machine lives somewhere under it:

```
/                        ← the root: the top of everything
├── home/
│   └── aiman/           ← your personal folder, called your "home"
├── etc/                 ← system configuration files live here
├── var/
│   └── log/             ← programs write their diaries ("logs") here
├── tmp/                 ← scratch space; the OS wipes it on reboot
└── mnt/
    └── d/               ← in WSL: your Windows D:\ drive appears here!
```

The `~` you saw in the prompt is simply a shortcut meaning "my home folder"
(`/home/aiman`).

A **path** is the written address of a file in this tree. There are two ways
to write one:

- An **absolute path** starts from the root and spells out the whole route:
  `/home/aiman/notes.txt`. It works no matter where you're standing.
- A **relative path** starts from *the folder you are currently in*: if you
  are standing in `/home/aiman`, then `notes.txt` means the same file.

Two special names you'll use constantly: `.` means "the folder I'm standing
in", and `..` means "the folder one level up from here."

### 2.4 The everyday commands

You will use these dozens of times a day. Read the table, then do the
try-it-now below to make them real.

| Command | Plain-language meaning |
|---|---|
| `pwd` | "Where am I standing right now?" (print working directory) |
| `ls` | "What's in this folder?" — `ls -l` adds details; `ls -a` also shows hidden files |
| `cd somewhere` | "Walk into that folder." `cd ..` = go up one. `cd ~` = go home. |
| `mkdir name` | "Make a new folder." |
| `cat file` | "Print the whole file onto the screen." |
| `less file` | "Open the file in a scrollable viewer" (arrow keys to move, `q` to quit). |
| `head -20 file` | "Show me just the first 20 lines." |
| `tail -20 file` | "Show me just the last 20 lines." |
| `cp a b` | "Copy a, name the copy b." |
| `mv a b` | "Move (or rename) a to b." |
| `rm file` | "Delete the file." ⚠️ **There is no recycle bin. Deleted is gone.** |
| `touch file` | "Create an empty file with this name." |
| `echo hello` | "Print the word hello." (Sounds useless; becomes essential in scripts.) |
| `history` | "Show me the commands I've typed recently." |

About **hidden files**: on Linux, any file whose name starts with a dot —
like `.gitignore` — is treated as "hidden", meaning `ls` doesn't show it
unless you ask with `ls -a`. That's the entire mechanism. Nothing is secret
about them; they're just tucked away to reduce clutter.

**Try it now** (in WSL, once it's installed — or in Git Bash meanwhile):

```bash
pwd                  # where am I?
mkdir practice       # make a folder
cd practice          # step into it
echo "hello there" > note.txt    # create a file containing one line (the > is explained next!)
cat note.txt         # read it back
cd ..                # step back out
rm practice/note.txt # delete the file
rmdir practice       # delete the (now empty) folder
```

### 2.5 The superpower: pipes and redirection

This section is the single most important idea in the Linux half of this
lesson. Take it slowly.

**Step 1 — every program has three standard "hoses" attached.**

When any Linux program runs, the OS plugs three data hoses into it:

- **stdin** ("standard input") — the hose it *reads* from. Normally connected
  to your keyboard.
- **stdout** ("standard output") — the hose its normal answers flow out of.
  Normally connected to your screen.
- **stderr** ("standard error") — a *separate* hose just for complaints and
  error messages. Also connected to your screen by default — which is why
  output and errors look mixed together, even though they travel separately.

Why have two output hoses instead of one? So that you can split them: send
the useful output into a file, while errors still show on screen (or the
other way around). You'll do exactly that below.

**Step 2 — redirection: point a hose at a file instead of the screen.**

The `>` symbol means "send stdout into this file instead of the screen":

```bash
echo "first line" > diary.txt     # creates diary.txt containing that line
echo "second line" > diary.txt    # ⚠️ > OVERWRITES — diary.txt now has ONLY this line
echo "third line" >> diary.txt    # >> APPENDS — adds to the end, keeps what was there
cat diary.txt                     # shows: second line, third line
```

Remember the difference: one arrow `>` replaces the file, two arrows `>>` add
to the end of it.

**Step 3 — the hoses have numbers.**

The OS numbers the three hoses: stdin is `0`, stdout is `1`, stderr is `2`.
Plain `>` is actually shorthand for `1>` ("redirect hose number 1"). Which
means you can redirect the *error* hose specifically by writing `2>`:

**Try it now:**

```bash
ls /nope
# ls complains: "cannot access '/nope': No such file or directory"
# That complaint came out of hose 2 (stderr).

ls /nope 2> errors.txt
# Now the screen shows nothing — the complaint went into the file instead.
cat errors.txt   # there it is
```

One more spelling you will meet constantly in real commands: `2>&1`. Decoded
piece by piece: `2>` means "redirect hose 2 (errors)…", and `&1` means
"…into wherever hose 1 (normal output) is currently pointing." So:

```bash
some_command > everything.txt 2>&1
# stdout goes into the file, AND stderr is merged into the same file.
# Translation: "capture absolutely everything this command says."
```

We'll use exactly this in the cron exercise later, so the scheduler's
silent-by-default runs leave evidence behind.

**Step 4 — pipes: plug one program's output hose into another program's
input hose.**

The vertical bar `|` (called a **pipe**) connects the stdout of the command
on its left to the stdin of the command on its right:

```bash
cat server.log | grep ERROR | wc -l
```

Read it left to right, like water flowing:

1. `cat server.log` — pour the whole file out.
2. `| grep ERROR` — the pour flows into `grep`, which lets through *only*
   the lines containing "ERROR" (we meet grep properly in section 3).
3. `| wc -l` — those surviving lines flow into `wc -l`, which counts them.

Final output: a single number — how many error lines the log contains.

**Analogy:** an assembly line in a factory. Each worker (program) does ONE
small job well, then passes the item down the belt. `grep` only filters.
`sort` only sorts. `wc` only counts. The deep idea: **ten small tools that
can be freely combined are more powerful than one giant tool that can't.**
This has a name — the **Unix philosophy** — and here is a spoiler for the
whole course: good system design is the same idea at a bigger scale. Small
components, each doing one job, connected by clean interfaces.

---

## 3. Slicing text: grep, awk, sed & friends

Why does a whole section of this course care about searching text files?
Because **servers narrate their lives into text files called logs** — one
line per event — and when something goes wrong at 2 a.m., the log is the
witness you interrogate. Being fast at interrogating logs is *the* everyday
superpower of people who run systems.

Our playground includes a script that generates a realistic fake web-server
log for you, called `server.log`. Its lines look like this:

```
2026-07-15 10:23:01 [INFO]  203.0.113.42  GET  /links   200  23ms
2026-07-15 10:23:04 [ERROR] 198.51.100.7  POST /links   500  812ms
```

Let's read the first line out loud, column by column: *on July 15 at
10:23:01, an ordinary event (INFO = information, nothing wrong) — the visitor
whose internet address is 203.0.113.42 asked to GET (fetch) the page called
/links; the server answered with code 200 (which means "OK, here you go"),
and the whole thing took 23 milliseconds.*

Don't worry about what an IP address, GET, or code 200 *really* are — each
gets its own full lesson in Phases 2 and 3. For today they are simply columns
of text to practice on.

### 3.1 `grep` — keep only the matching lines

Plain words: *"show me only the lines that contain this text."* (The odd
name is a historical abbreviation from the 1970s; just think "filter.")

```bash
grep ERROR server.log        # only the lines containing ERROR
grep -c ERROR server.log     # -c = don't show them, just Count them
grep -v INFO server.log      # -v = inVert: lines that do NOT contain INFO
grep -n 500 server.log       # -n = also show each line's Number in the file
grep -i error server.log     # -i = ignore case: matches ERROR, error, Error
```

`grep` can also match *patterns* instead of exact text — "any number here",
"starts with this" — using a mini-language called **regular expressions**
(or **regex**). Example: `grep -E " 5[0-9][0-9] "` finds a space, then a 5,
then any digit, then any digit, then a space — i.e. any status code from 500
to 599. Regex is deep; we'll pick up pieces only as we need them.

### 3.2 `awk` — think in columns

Plain words: *"treat each line as a row of columns, and let me pick and
compute with the columns."*

`awk` automatically splits every line wherever there are spaces, and names
the pieces `$1` (first column), `$2` (second), and so on. `$0` means the
whole line. For our log file that gives us:

`$1`=date, `$2`=time, `$3`=level, `$4`=IP address, `$5`=method, `$6`=path,
`$7`=status code, `$8`=duration.

```bash
awk '{print $6}' server.log
# For every line, print only column 6 → a long list of just the paths.

awk '$7 == 500 {print $4, $6}' server.log
# The part before { } is a CONDITION: "only for lines where column 7 equals 500".
# For those lines, print columns 4 and 6 → who hit an error, and on which page.

awk '{sum += $8; n++} END {print sum/n " ms average"}' server.log
# This one runs a little calculation:
#   for every line: add column 8 (the duration) into a running total called sum,
#                   and add 1 to a counter called n;
#   END means "after the last line": print the total divided by the count.
# Result: the average response time of the whole log, in one command.
# (Handy detail: when awk does math on "23ms" it just reads the number 23
#  and ignores the letters.)
```

That last command is a real production task — "what's our average response
time?" — answered without opening a spreadsheet.

### 3.3 `sed` — find & replace, applied to a whole file

Plain words: *"replace this text with that text, on every line."* The name
means stream editor, but the only form you need for a long time is:

```bash
sed 's/ERROR/PROBLEM/' server.log
# s/old/new/  → on each line, replace the FIRST "ERROR" with "PROBLEM".
# This PRINTS the modified text to the screen. The file is NOT changed.

sed 's/ERROR/PROBLEM/g' server.log
# the extra g ("global") → replace EVERY occurrence on each line, not just the first.

sed -i 's/foo/bar/g' file.txt
# -i ("in place") → actually rewrite the file. Use with care; no undo.
```

Memorize the shape `s/old/new/` — "substitute old with new" — and you know
90% of the `sed` used in real life.

### 3.4 `sort`, `uniq`, `wc` — the counting crew

Three tiny tools: `sort` puts lines in order, `uniq -c` collapses repeated
neighboring lines and counts them, `wc -l` counts lines. Alone, each is
boring. Piped together, they answer real questions:

```bash
wc -l server.log
# How many lines = how many requests did the server handle?

awk '{print $4}' server.log | sort | uniq -c | sort -rn | head -5
```

That second pipeline is *the* classic — you will type variants of it for the
rest of your career. Walk it slowly, stage by stage:

1. `awk '{print $4}'` — reduce every line to just its IP address column.
2. `sort` — put identical IPs next to each other. (This step exists because
   `uniq` only merges *neighboring* duplicates — so we group them first.)
3. `uniq -c` — collapse each group into one line, prefixed with its count:
   `137 203.0.113.42`.
4. `sort -rn` — sort those lines as **n**umbers, **r**eversed (biggest
   first).
5. `head -5` — keep the top five.

Translation of the whole thing: *"who are my top 5 visitors?"* Swap `$4` for
`$6` and it becomes "top 5 most-requested pages." This one pattern answers
top-anything questions forever.

### 3.5 `find` — search for files (not inside them)

`grep` searches *inside* files. `find` searches *for* files, by name, type,
age, size:

```bash
find . -name "*.log"          # every file ending in .log, starting from here (.)
find . -type d                # only directories (folders)
find /var/log -mtime -1       # files modified within the last 1 day
find . -name "*.tmp" -delete  # find AND delete — always run it WITHOUT -delete first, to see what would go
```

### 3.6 `tail -f` — watch a log grow, live

You already know `tail file` shows the last lines of a file. Adding `-f`
("follow") changes its personality: it shows the last lines *and then keeps
waiting*, printing every new line the moment it is added to the file.

```bash
tail -f server.log
```

This is how you watch a live server breathe. From Phase 2 onward you'll
often have two terminals open: one running the app, one following its log.
To stop it, press `Ctrl+C` — and that's worth stating as a general rule:
**`Ctrl+C` stops whatever program is currently running in your terminal.**

---

## 4. Processes: programs in motion

### 4.1 What a process is (CS fundamental 🧱)

A program sitting on your disk — `chrome.exe`, `python` — is just a file: a
recipe, doing nothing. When you *run* it, the OS loads it into memory, gives
it CPU time, and it starts actually doing things. A running instance of a
program is called a **process**.

The recipe/dish distinction matters: open Chrome three times and you have
ONE program but THREE processes — three separately running instances. The OS
gives every process a unique ID number, its **PID** (process ID) — think of
it as the ticket number the OS uses to refer to that specific running
instance. (Phase 1 goes much deeper into processes: threads, scheduling,
what "using the CPU" physically means.)

### 4.2 Seeing what's running

```bash
ps aux
# A snapshot ("ps" = processes) of everything running right now, one line each.

ps aux | grep python
# The same snapshot, piped through grep → only lines mentioning python.
# (Notice: you already know both halves of this. Pipes compose everything.)

top
# A LIVE dashboard that refreshes every few seconds. Press q to quit.
```

In `ps aux`, the columns worth reading: `USER` (who started it), `PID` (its
ticket number), `%CPU` and `%MEM` (how much of the machine it's using), and
the command itself at the end of the line. In `top`, processes are sorted
with the biggest CPU user on top — so a misbehaving process literally rises
to the top of the screen. A process showing 100% is fully using one CPU core.

### 4.3 Stopping a process: signals

You don't stop a process by deleting something — you send it a **signal**: a
tiny standardized message the OS delivers to the process. The two you need:

```bash
kill 1234        # sends the signal SIGTERM to the process whose PID is 1234
kill -9 1234     # sends the signal SIGKILL to it
```

Despite the scary name, `kill` just means "send a signal", and the two
signals differ enormously:

- **SIGTERM** ("terminate, please") is a *request*. The process receives it
  and gets a chance to react: finish what it was writing, close its files,
  say goodbye, and exit cleanly. A well-written program always handles this.
- **SIGKILL** (`-9`) is not a request and is not deliverable *to* the
  program at all — the OS simply erases the process from existence,
  mid-sentence. The process gets no chance to react. Nothing can catch or
  ignore SIGKILL; that is its entire purpose.

**Analogy:** SIGTERM is a tap on the shoulder — "we're closing, please wrap
up." SIGKILL is security lifting the person out of their chair — instant,
but whatever they were in the middle of is lost.

**Rule: always try plain `kill` first.** Reach for `-9` only when a process
ignores the polite version. (One more relative: pressing `Ctrl+C` sends a
cousin signal called SIGINT, "interrupt" — also polite.)

Two helper commands so you don't have to hunt PIDs by eye:

```bash
pgrep -f runaway.sh    # print the PID(s) of processes whose command matches "runaway.sh"
pkill -f runaway.sh    # find them AND send SIGTERM, in one step
```

Why this matters beyond today: the idea of a program *reacting to SIGTERM by
finishing its current work before exiting* is called **graceful shutdown**,
and it is a big deal in real systems — every time Kubernetes (Phase 19)
updates your app, it stops the old copy by sending exactly this signal. The
playground's `runaway.sh` lets you *watch* the difference: it says a polite
goodbye when SIGTERMed, and vanishes silently when SIGKILLed.

---

## 5. Talking to networks (a first taste — Phase 2 covers this deeply)

Two commands to meet today because we'll use them in every phase from here on:

**`curl` — make a web request from the terminal.** When your browser opens a
page, it sends a request over the network and draws the response nicely.
`curl` sends the same kind of request but shows you the raw, undecorated
response — which is exactly what you want when learning or debugging.

```bash
curl https://example.com       # fetch that page; print its raw HTML text
curl -i https://example.com   # -i: also show the response HEADERS (the metadata that rides along)
curl -v https://example.com   # -v (verbose): show the ENTIRE conversation, both directions
```

From Phase 4 onward, `curl` is how you'll poke LinkBoard's API directly, no
browser needed.

**`dig` — look something up in the internet's phone book.** Humans use names
like `example.com`; computers actually connect to numeric addresses (IP
addresses). The worldwide system that translates names into numbers is called
**DNS**, and `dig example.com` performs one lookup and shows you the answer.
The full story — who maintains the phone book, how answers get cached — is a
highlight of Phase 2.

Also in the toolbox for later: `ping some-site.com` ("are you reachable, and
how many milliseconds away?") and `ss -tlnp` ("which programs on *my* machine
are currently listening for network connections?" — this becomes essential
from Phase 2 on, e.g. to answer "is something already using port 8000?").

---

## 6. Permissions: who may do what to a file

Every file on Linux carries a little rulebook: who owns it, and who may do
what with it. `ls -l` shows the rulebook at the start of each line:

```
-rwxr-xr--  1 aiman aiman  512 Jul 15 10:00 make_logs.sh
```

Focus on that first block, `-rwxr-xr--`, and read it in four pieces:

- The first character: `-` means "ordinary file", `d` would mean directory.
- Then three groups of three characters, each answering "may they **r**ead /
  **w**rite / e**x**ecute?" for a different audience:

| Characters | Who they apply to | Meaning in this example |
|---|---|---|
| `rwx` | the file's **owner** (aiman) | may read it, change it, and run it |
| `r-x` | the owner's **group** | may read and run it, but not change it |
| `r--` | **everyone else** | may only read it |

A `-` in any slot means "not allowed."

"Execute" (`x`) deserves a note: for a script or program it means "allowed to
run it." A freshly created script is NOT executable — Linux makes you say so
explicitly:

```bash
chmod +x make_logs.sh    # chmod = "change mode" → add the execute permission
./make_logs.sh           # now it runs
```

(Why the `./` in front? For safety, the shell only auto-runs commands from a
few trusted system folders. Writing `./make_logs.sh` says "run the one right
*here*, in this folder — yes, I mean it.")

**The numbers you'll see everywhere (`chmod 755`):** each three-character
group can be written as one digit by adding up r=4, w=2, x=1. So:

- `rwx` = 4+2+1 = `7`
- `r-x` = 4+1 = `5`
- `r--` = 4 = `4`
- `---` = `0`

`chmod 755 file` therefore means: owner may do everything (7), group may
read+run (5), everyone else may read+run (5) — the standard setting for
scripts. `chmod 600` means: owner may read+write (6), everyone else nothing
(0) — the standard for secret files. (SSH, coming next, actually *refuses*
to use a key file unless it's 600 — a nice example of a tool enforcing good
hygiene.)

Two more commands in this family: `chown user file` changes who owns a file,
and `sudo some-command` runs one command as **root** — the all-powerful
administrator account (**s**uper **u**ser **do**). Linux asks for your
password when you `sudo`, and a small jolt of caution every time you type it
is healthy.

---

## 7. SSH, scp, rsync — working on machines you can't touch

Real servers live in data centers you will never visit. So how do you type
commands into them? **SSH** ("Secure Shell") gives you a terminal *on a
remote machine*, over an encrypted connection:

```bash
ssh aiman@some-server-address
```

After that line, the prompt you see belongs to the *remote* machine — every
command you type runs there, not on your laptop. Everything you've learned in
this lesson works identically over SSH; that is a big part of why terminal
skills matter.

**How SSH logs you in without a password — the key pair.** This idea returns
in Phase 7 (cryptography) and is used by GitHub, so let's get the picture
right now. You generate a pair of mathematically linked files:

- The **public key** works like a *padlock*. You can hand copies to anyone —
  you put one on each server you want access to (or upload it to GitHub).
  A padlock can only lock things; owning it grants nothing.
- The **private key** is the only key that opens that padlock. It stays on
  your machine, never leaves, never gets shared. (This is the file that must
  be `chmod 600`.)

When you connect, the server snaps your padlock shut around a random
challenge and says "open this." Only your private key can. You open it,
identity proven — and no password ever traveled over the network at all.

Copying files rides on top of SSH:

- `scp report.txt aiman@server:/home/aiman/` — simple copy of a file to the
  remote machine. Copies the whole file every time.
- `rsync -avz myfolder/ aiman@server:/backup/` — the smart mover: it compares
  both sides first and transfers **only what changed**. Run it twice in a row
  and the second run finishes almost instantly, because nothing changed.

Tuck that rsync idea away: *"only ship the difference"* is a trick you will
see again and again in system design — database replication, CDNs, Docker
image layers all use a version of it.

We don't have a remote server yet, so SSH stays conceptual today (you may
optionally create a key for GitHub in the setup; the HTTPS login works fine
too). It becomes hands-on in the cloud phases.

---

## 8. cron — the machine's alarm clock

Some work needs to happen on a schedule with no human present: "back up the
database every night at 2 a.m.", "delete old temp files every hour." Linux's
built-in scheduler for this is a background service called **cron**.

Each user has a personal schedule table, their **crontab** ("cron table").
Two commands manage it:

```bash
crontab -l    # list my scheduled jobs
crontab -e    # edit them (opens an editor)
```

Each line of the table is: **five time fields, then the command to run.**
The five fields, in order:

```
┌───────── minute        (0–59)
│ ┌─────── hour          (0–23)
│ │ ┌───── day of month  (1–31)
│ │ │ ┌─── month         (1–12)
│ │ │ │ ┌─ day of week   (0–7; both 0 and 7 mean Sunday)
* * * * *   command-to-run
```

A `*` in a field means "every." Examples, decoded:

- `* * * * *` — every minute of every hour of every day: run constantly.
- `30 2 * * *` — at minute 30 of hour 2, every day: daily at 02:30.
- `0 9 * * 1` — at 9:00, only when the weekday is 1: every Monday morning.

(The website crontab.guru decodes any line you paste into it — handy while
learning.)

Two famous gotchas — you will meet both in the exercise, on purpose:

1. **Cron runs your command in a stripped-down environment.** The
   conveniences of your interactive shell (your current folder, your custom
   settings) are absent. The practical rule: **always write absolute paths**
   in crontab lines — both to the script and inside the script.
2. **Cron is silent.** Your job runs with no terminal attached; anything it
   prints simply evaporates unless you capture it. The practical rule: end
   the crontab line with `>> /some/file.log 2>&1` — which you can now decode
   yourself from section 2.5: *append normal output to the file, and merge
   the error hose into it too.* That file becomes your evidence.

Why learn a 50-year-old scheduler? Because its ideas — and even its exact
five-field syntax — live on inside every modern "run this on a schedule"
system: GitHub Actions schedules (Phase 18), Kubernetes CronJobs (Phase 19),
Airflow pipelines (Phase 23).

> **WSL note:** WSL doesn't always start background services by itself. The
> run section includes the one command to start cron and the check to confirm
> it's alive.

---

## 9. Shell scripting: gluing commands into programs

A shell script is nothing more mysterious than **commands saved in a file,
executed top to bottom**. Anything you can type interactively can be
scripted. Here is a tour of every feature used in the playground scripts —
read it now, and the scripts will read like plain prose afterward.

```bash
#!/usr/bin/env bash
# ↑ Line 1 of every script, called the "shebang". When you run the file,
#   the OS reads this line to learn WHICH program should interpret the rest.
#   This exact spelling means "find bash and use it."

set -euo pipefail
# Three safety switches, worth putting in every script you ever write:
#   -e            if any command fails, STOP the script immediately
#                 (instead of blindly continuing into chaos)
#   -u            using a variable that was never defined is an ERROR
#                 (catches typos in variable names)
#   -o pipefail   in a pipeline like a | b | c, if ANY stage fails the
#                 whole pipeline counts as failed (normally only the last
#                 stage's result matters — a surprising default)

NAME="LinkBoard"        # a variable. IMPORTANT: no spaces around the = sign.
echo "Hello from $NAME" # read a variable with $. Double quotes: $ works inside.
echo 'Hello from $NAME' # single quotes: everything is literal → prints $NAME as-is.

TODAY=$(date +%F)
# $( ... ) is "command substitution": run the command inside the parentheses,
# and use whatever it PRINTS as a value. Here: TODAY becomes e.g. 2026-07-16.

if [ -f server.log ]; then     # [ ... ] is a test. -f asks "does this file exist?"
  echo "the log exists"
else
  echo "no log yet"
fi

for i in 1 2 3; do             # a loop: runs the body once per item
  echo "round $i"
done

greet() {                      # a function: a named, reusable block
  echo "hi, $1"                # inside a function, $1 is its first argument
}
greet "aiman"                  # prints: hi, aiman
```

### 9.1 Exit codes: how programs report success or failure (CS fundamental 🧱)

This small idea quietly powers a lot of what comes later in the course, so
let's take it properly.

When any program finishes, it hands one final number back to the shell
before disappearing. That number is called its **exit code**. The universal
convention:

- **0 means "success — everything went fine."**
- **Any other number (1–255) means "something went wrong."** (Different
  numbers can encode different kinds of failure; what matters is zero vs
  not-zero.)

Why report success as a *number* instead of a message? Because numbers can be
checked *automatically by other programs*. A human can read "No such file or
directory"; a script cannot — but a script can trivially check "was the exit
code 0?"

The shell keeps the exit code of the most recent command in a special
variable spelled `$?`. **Try it now:**

```bash
ls /home
echo $?        # prints 0 — ls succeeded

ls /folder-that-does-not-exist
echo $?        # prints 2 — ls failed, and said so via its exit code
```

Now connect this to things you've already seen — each of these is secretly
built on exit codes:

- **`if` statements.** That `[ -f server.log ]` from above? `[` is actually a
  program. It exits with 0 if the test is true and 1 if false — and `if`
  simply runs the `then` branch on exit code 0. `if` never "understands"
  your test; it only reads the number.
- **`set -e`.** Now you can state precisely what it does: "the moment any
  command exits with a non-zero code, stop the script."
- **The `&&` you'll see in git commands** like
  `git add -A && git commit -m "..."`: the `&&` means "run the second command
  *only if* the first exited with 0."
- **And later (Phase 18):** your automated pipeline will decide whether to
  deploy LinkBoard by running the test suite and reading a single number —
  its exit code. Tests exit 0 → ship it. Tests exit non-zero → stop.

One convention, used identically from a two-line script to a company's
deployment system.

---

## 10. Git from the inside out

Most people learn Git as a list of spells to memorize: `add`, `commit`,
`push`, and pray. We're going to do the opposite — understand the simple
machine underneath, so every command becomes obvious instead of magic. This
half of the lesson is the longest. Take breaks.

### 10.1 The problem Git solves

You've lived this problem: `essay_final.doc`, `essay_final_v2.doc`,
`essay_FINAL_really_v3.doc`. Now scale it up to a software project: hundreds
of files that change together, months of work, and questions like:

- "It worked yesterday. *What changed?*"
- "Can I try a risky idea without endangering the working version?"
- "Can two people edit the project at the same time without overwriting each
  other?"
- "What did this file look like three months ago, and *why* was it changed?"

A **version control system** is a tool that answers all of these by keeping
*every* saved state of the project, forever, with labels, dates, and reasons.
**Git**, written in 2005 by Linus Torvalds (the creator of Linux, to manage
Linux's own development), is the version control system that won — it is
effectively universal today. **GitHub** (which we set up in this phase) is a
website that *hosts* Git projects online; Git is the tool, GitHub is a home
for its output.

A Git-managed project folder is called a **repository** (or "repo"): your
project files, plus a hidden folder named `.git/` where Git keeps the entire
history. That hidden folder is the actual repository; your visible files are
just the current working copy. We're going to look inside `.git/` with our
own eyes before this lesson is over.

### 10.2 Mental model #1: Git stores snapshots, not changes

Question: when you "save a version" of your project, what should the tool
actually record?

Intuition says: record the *changes* — "line 12 was edited, line 40 deleted."
Git does something different, and it's the key to everything else:

> **Every commit is a complete snapshot of your entire project** — every
> file, in full, as it looked at that moment.

**Analogy:** Git is a photographer with an infinite photo album. Every time
you say "commit," it photographs your *whole desk* — not just the thing you
moved — and files the photo in the album with a date and your note about it.

Your immediate objection is correct: "If every snapshot contains every file,
doesn't the album become enormous? If I change one file out of a thousand,
does Git store the other 999 again?!"

No — and the trick Git uses is genuinely beautiful. It needs one new concept
first.

**What is a hash? (CS fundamental 🧱 — this idea returns in Phases 4, 6, 7,
8 and 15, so it repays the next three minutes.)**

A **hash function** is a little machine with one job: you feed it any data —
a word, a file, a whole hard drive — and it outputs a short, fixed-length
scramble of characters called a **hash** (or *fingerprint*, which is the
better mental image). For example, feeding the text `hello` to the hash
function Git uses produces:

```
aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
```

Three properties make hashes useful, and all three matter to Git:

1. **Same input → always the same fingerprint.** Hash `hello` tomorrow, on
   any computer on Earth, and you get exactly the string above.
2. **Tiny change → completely different fingerprint.** Hash `hellp` (one
   letter off) and you get a string that shares nothing with the one above.
   (You'll verify both of these yourself in the experiments section.)
3. **One-way.** From the fingerprint you cannot reconstruct the input, any
   more than you can reconstruct a person from a fingerprint.

Now the trick. Git stores every piece of content in its album **under its
fingerprint, used as its filename.** When you commit, Git fingerprints each
file's content and checks: *"do I already have an object with this
fingerprint in the album?"*

- Already there → **don't store anything.** The new snapshot just *points* to
  the existing object. (Property 1 guarantees this is safe: same fingerprint
  = same content.)
- Not there → store it once, under its fingerprint.

So a snapshot of 1,000 files where one file changed stores exactly **one**
new object plus a small updated table of contents. The other 999 entries
point at objects the album already had. Full snapshots, almost no
duplication. This scheme has a name — **content-addressed storage**: things
are filed under *what they are* (their fingerprint) instead of under an
arbitrary name.

Bonus you get for free: if a stored file is ever corrupted on disk, its
content no longer matches the fingerprint it's filed under — so Git can
detect the damage instantly.

### 10.3 Mental model #2: the three areas (working directory, staging, repository)

Between "I edited a file" and "it's saved in history forever" Git inserts one
deliberate step. There are three places your work can be:

```
   WORKING DIRECTORY        →  git add  →     STAGING AREA        →  git commit  →     REPOSITORY
  (your actual files,                     (the list of exactly                      (the permanent album
   which you edit freely)                  what the NEXT photo                       of snapshots, inside
                                           will include)                             the .git/ folder)
```

**Analogy, continuing the photographer:** the working directory is your messy
desk — work in progress, half-finished thoughts, everything. `git add` is you
placing chosen items onto the photo table: "these are going in the next
shot." The staging area *is* that photo table. `git commit` clicks the
shutter: whatever was on the table becomes a permanent photo in the album,
labeled with your message.

Why have a photo table at all? Why not photograph the whole desk every time?
Because it lets each snapshot be a *curated, meaningful* unit. Suppose you
fixed a bug in one file and also started an unrelated experiment in another.
Stage and commit only the bug fix — "Fix login crash" — and leave the
experiment on the desk for later. Each commit tells one story, which makes
history readable.

The everyday loop you'll repeat for years:

```bash
# ...edit files...
git status                      # "What's changed on my desk? What's on the photo table?"
git diff                        # "Show me the exact edits I haven't staged yet."
git add file1 file2             # put specific files on the table   (git add -A = everything)
git commit -m "Fix login crash" # click the shutter, with a label
git log --oneline               # flip through the album, one line per photo
```

### 10.4 Inside the album: blobs, trees, and commits

Let's open the `.git/` folder conceptually. (Physically, you'll do it with
the playground's `git_xray.sh` script right after your first commit.)
Everything Git stores is one of three kinds of object — each filed under its
fingerprint, as promised:

1. A **blob** holds *file content* — just the bytes inside a file. Notably,
   a blob does **not** know its own filename. Content only.
2. A **tree** holds a *folder listing*: "this folder contains a file named
   README.md whose content is blob `a1b2c3...`, and a subfolder named
   project which is tree `d4e5f6...`". Trees are where filenames live.
3. A **commit** is the *snapshot record*. It contains: the fingerprint of one
   tree (the top-level folder listing — from which the entire snapshot can be
   reached), your name and email, the date, your message — and one more thing
   that turns out to be crucial: **the fingerprint of the previous commit**,
   called its **parent**.

That last field — the parent — is what turns isolated snapshots into
*history*. Each commit points back at the commit that came before it, so the
album is a chain:

```
[first commit] ← [second commit] ← [third commit] ← [fourth commit]
```

Each arrow means "my parent is." To read history, Git starts at the newest
commit and follows parent pointers backwards. (When branches enter the
picture, the chain can fork into diverging paths and later rejoin — you'll
see that shape in section 10.6.)

**One profound consequence — history is tamper-evident.** Walk through it
slowly:

- A commit's fingerprint is computed over everything inside it — *including
  its parent's fingerprint.*
- Now imagine someone secretly alters an old commit. Changed content →
  changed fingerprint (property 2 of hashes).
- But the *next* commit recorded the old fingerprint as its parent. That
  stored value no longer matches anything that exists. To hide the tampering,
  the next commit must be rewritten too — which changes *its* fingerprint —
  which breaks the one after it — and so on, all the way to the newest
  commit.

In other words: **you cannot quietly change the past.** Any alteration to
history is instantly visible, because every commit's fingerprint vouches for
everything behind it. Keep this "chain where each link seals all previous
links" picture; the same construction reappears as Kafka's log (Phase 11) and
the database write-ahead log (Phase 15).

### 10.5 Branches: what they are for, and what they actually are

**The purpose first.** You're building LinkBoard, and it works. You want to
try a risky idea — say, a dark color scheme — without endangering the working
version. What you want is a *parallel line of history*: keep committing your
experiment over here, while the trusted version stays untouched over there.
That parallel line is a **branch**. Every repository starts with one default
branch, conventionally named **main**, and you create more whenever you want
to work on something in isolation:

```bash
git switch -c dark-mode   # -c = create a branch named dark-mode, and move onto it
# ...edit, commit, edit, commit — main is completely unaffected...
git switch main           # step back to the trusted version; your experiment waits
```

**Now the mechanism — and it's simpler than you expect.** Here's the
question that reveals it: when you type `git switch main`, how does Git know
which commit "main" refers to?

Answer: inside the `.git/` folder there is a folder of tiny text files, one
per branch. The file for main is literally at `.git/refs/heads/main`, and its
entire content is **one line: the fingerprint of a commit.**

```
$ cat .git/refs/heads/main
9fceb02c0d5fda1b2c3d4e5f6a7b8c9d0e1f2a3b
```

That's the whole branch. Not a copy of your files, not a folder of history —
a one-line file saying *"the branch named main currently means THIS commit."*

**Analogy:** the commits are pages in the photo album; a branch is a **sticky
note** on one page, with a name written on it. The note for `main` is stuck
on the newest trusted photo. The note for `dark-mode` is stuck wherever your
experiment currently ends.

And here's the part that makes Git feel alive: **when you commit, Git moves
the sticky note for you.** Say `main` points at a commit we'll call
`snapshot-5`. You make a new commit. Git (a) creates `snapshot-6` with
`snapshot-5` as its parent, and (b) rewrites that one-line file so `main` now
points at `snapshot-6`. The sticky note slides forward to the newest page,
automatically, every time.

This explains something that surprises people coming from other tools:
creating a branch in Git is *instant and free*, no matter how big the
project — because it just writes one 41-character line into a new tiny file.
Nothing is copied. So make branches casually, for anything.

### 10.6 HEAD: "you are here"

One more sticky note and the picture is complete. With several branches in
the album, Git needs to know **which branch you are currently working on** —
so that when you commit, it knows *which* sticky note to move.

That's **HEAD**: a single special file (`.git/HEAD`) whose content is
essentially "the current branch is main" (or dark-mode, or whatever).
It's the *"you are here"* arrow on a mall map. `git switch dark-mode` does
two things: points HEAD at the dark-mode note, and rearranges the files in
your working directory to match the photo that note is stuck on.

Vocabulary check — you now know all three layers:
- **commit** = a photo (permanent snapshot),
- **branch** = a named sticky note on some photo, which slides forward as
  you commit,
- **HEAD** = the note marking which sticky note is currently *yours*.

### 10.7 Combining branches: merge vs rebase

**The story.** Monday morning: LinkBoard's `main` branch ends at some commit
— call that commit `C` (we only name it so we can point at it in diagrams).
You create the branch `dark-mode` and start working. By Wednesday you've made
two commits on it — call them `X` and `Y`.

Meanwhile, `main` did not stand still: an urgent bug was fixed on it —
whether by a teammate or by you, switching over for an afternoon — adding two
commits to main, call them `D` and `E`.

Draw the album now (time flows left to right; each commit's parent is the
commit to its left):

```
A --- B --- C --- D --- E     ← the sticky note "main" is on E
             \
              X --- Y         ← the sticky note "dark-mode" is on Y
```

History has **diverged**: two lines of work grew out of commit `C`. The
dark-mode work is done and you want main to include it. There are two ways to
combine the lines, and the difference between them is one of Git's most
discussed topics. Both start from the same picture above.

**Way 1: merge — tie the two lines together, honestly.**

```bash
git switch main          # stand on main
git merge dark-mode      # "bring dark-mode's work into main"
```

Git creates one new commit — a **merge commit**, call it `M` — which is
special in exactly one way: it has **two parents**, `E` and `Y`. It's the
photo of the two lines joining:

```
A --- B --- C --- D --- E --- M     ← main is now on M
             \               /
              X --- Y ------          (dark-mode still points at Y)
```

Merge's character: **honest and safe.** Every commit that ever existed is
still there, untouched; the join itself is recorded as a fact ("these two
lines met here"). The cost: after many merges, history looks like braided
rope — lots of crossing lines — which can be harder to read.

**Way 2: rebase — replay your work on top of theirs, for a straight line.**

```bash
git switch dark-mode     # stand on your branch
git rebase main          # "re-apply my commits as if I had STARTED from main's tip"
```

Git takes your commits `X` and `Y`, and *replays* them, one at a time, on top
of `E` — as if you had started your work Wednesday from the current main
instead of Monday's. The result is a straight line:

```
A --- B --- C --- D --- E --- X' --- Y'     ← dark-mode now ends at Y'
```

Notice the marks: `X'` and `Y'`, not `X` and `Y`. This is the crucial fine
print. The replayed commits contain the same *edits*, but they are **new
commits with new fingerprints** — necessarily so: a commit's fingerprint
covers its parent, and `X'`'s parent is `E` where `X`'s parent was `C`.
Different content → different fingerprint. **Rebase does not move your
commits; it re-creates them and abandons the originals.**

Rebase's character: **tidy but revisionist.** You get a clean, easy-to-read
straight line — at the price of rewriting history to tell a story that
didn't quite happen that way.

**The one iron rule that follows.** Rewriting *your own private* commits is
harmless. But suppose you had already **pushed** `X` and `Y` to GitHub, and
someone else had already pulled them and built their own commits on top.
Their work records `Y` as a parent. If you now rebase, `Y` is abandoned in
favor of `Y'` — and their work sits on top of a commit that the branch no
longer contains. Untangling that means manual repair on every affected
person's machine. Hence the rule, worth memorizing verbatim:

> **Never rebase commits that have been pushed and that others may have
> built on.** Rebase your private drafts freely; treat published history as
> permanent.

**Either way: conflicts can happen.** Whether merging or rebasing, if the two
lines edited *the same lines of the same file* differently, Git stops and
asks you — it refuses to guess which version you want. This is called a
**conflict**, and despite its reputation it is not an error and nothing is
broken. Git marks the disputed spot in the file like this:

```
<<<<<<< HEAD
the version from the branch you're on
=======
the version from the branch being brought in
>>>>>>> dark-mode
```

Your job: edit the file into whatever it *should* say (usually keeping one
side, sometimes blending both), delete the three marker lines, then
`git add` the file and continue (`git commit` for a merge, `git rebase
--continue` for a rebase). That's the whole procedure.

### 10.8 The rescue kit: cherry-pick, bisect, reflog

Three tools you'll rarely use — and be *very* glad to know when the day
comes. A story for each.

**`git cherry-pick` — copy one commit from another branch.**
The situation: your big `dark-mode` branch is half-finished — not ready to
merge. But one commit in the middle of it happens to fix a bug that `main`
needs *today*. You don't want the whole branch; you want that one photo.

```bash
git switch main
git cherry-pick <fingerprint-of-that-one-commit>
```

Git re-applies just that commit's changes onto main, as a new commit. (You
find the fingerprint with `git log dark-mode --oneline` — the short code at
the start of each line.)

**`git bisect` — find which commit broke things, fast.**
The situation: a feature worked a month ago. It's broken today. Three hundred
commits happened in between, and you have no idea which one is guilty.
Checking all 300 one by one would take days.

First, a tiny detour that's a genuine CS fundamental 🧱: **binary search.**
Think of the guessing game "I'm thinking of a number between 1 and 100."
You don't guess 1, 2, 3… You guess 50. "Too low." Now you know it's in
51–100 — *half the possibilities eliminated by one question.* Guess 75, halve
again. Any number in 1–100 falls in at most 7 guesses. Halving is
devastatingly efficient: each question removes half of whatever remains, so
even 300 suspects need only about 9 questions (versus 300 one-by-one checks).
Remember this trick — it is the exact reason database indexes are fast, in
Phase 6.

`git bisect` plays that game against your history. You tell it one commit
where things worked and one where they're broken:

```bash
git bisect start
git bisect bad                  # the current commit is broken
git bisect good <old-fingerprint>   # this old one was fine
```

Git checks out the commit *halfway between them* and asks: does it work? You
test, answer `git bisect good` or `git bisect bad`, and Git halves the range
again. Nine or so rounds later it announces the exact commit that introduced
the bug. (`git bisect reset` returns you to the present.)

**`git reflog` — the safety net under the safety net.**
First, understand how a commit can *seem* lost. Remember: a branch is a
sticky note pointing at a commit, and you find history by starting from
sticky notes and walking parent pointers backward. Now suppose you delete
the branch `dark-mode`. The commits `X` and `Y` still physically exist in the
album — deleting a branch only peels off the sticky note — but **no note
points at them anymore**, so no ordinary command will show them to you. They
are photos with no bookmark: present, but unfindable. The same "orphaning"
happens to the original `X` and `Y` after a rebase, or to a commit you
dropped with a careless reset.

Here's the rescue: **Git keeps a private diary of every place HEAD has
pointed.** Every commit, every branch switch, every merge, rebase, or reset
— each one adds a line to this diary: "HEAD moved from here to there, because
of this command." The diary is called the **reflog** ("reference log"), and:

```bash
git reflog
```

prints it, newest first, with a fingerprint on every line. So after almost
any disaster, the recovery recipe is the same three steps:

1. `git reflog` — find the line from *just before* things went wrong.
2. Copy the fingerprint on that line.
3. `git switch -c rescue <fingerprint>` — stick a brand-new sticky note on
   that photo. Everything reachable from it is instantly "found" again.

The takeaway, and it should genuinely lower your shoulders: **in Git, almost
nothing you have ever committed can be truly lost.** Uncommitted work has no
such protection — which turns into practical advice: *commit early, commit
often.* Commits are save points, and they're free.

### 10.9 Remotes and GitHub: taking history online

Everything so far happened inside `.git/` on your machine. A **remote** is
simply *another copy of the repository, somewhere else* — typically on a
hosting service like **GitHub**. Having a remote gives you: an offsite backup,
a way to work from multiple machines, and (later) a way to collaborate.

The four verbs between you and a remote:

- `git clone <url>` — "copy that whole remote repository onto my machine"
  (done once, at the start; you won't need it since your repo starts locally).
- `git push` — "send my new commits *up* to the remote."
- `git fetch` — "download any new commits *from* the remote, but don't touch
  my working files yet — just let me look."
- `git pull` — fetch **and** immediately merge what arrived into my current
  branch. (Literally: pull = fetch + merge.)

Your repository keeps a little address book of remotes, each under a
nickname. The conventional nickname for your primary remote is **`origin`** —
when you run `git remote add origin <url>` in the setup steps, you are
writing exactly one address-book entry: "origin means this URL."

One flag to decode in advance, because you'll type it in Part A: the first
push is `git push -u origin main`, meaning "push my branch main to the remote
origin — and (`-u`) remember this pairing." After that one time, plain
`git push` knows where to go.

In this course, **every phase ends with a push**, so GitHub will hold the
complete story of the project — and any machine anywhere can pick it up and
resume.

### 10.10 How teams use branches, and what version numbers mean

Two short cultural notes to round out Git — no mechanics here, just the
vocabulary you'll encounter.

**Branching workflows.** Teams need a convention for *how* branches flow
together. Two famous schools:

- **GitFlow:** a formal system with a long-lived `develop` branch where work
  accumulates, plus dedicated `release/` and `hotfix/` branches feeding a
  ceremonial `main`. Suits software shipped in versions — mobile apps,
  desktop programs — where "release 2.4" is an event.
- **Trunk-based development:** everyone merges small changes into `main`
  (the "trunk") quickly — daily or faster. Unfinished features are hidden
  behind switches in the code ("feature flags", Phase 18) rather than parked
  on long-lived branches. Suits web services that deploy continuously —
  which is what LinkBoard is, so this is the style we'll practice: short
  branches, frequent merges into main.

**Semantic versioning ("semver").** You'll soon depend on other people's
software libraries, each with a version like `2.4.1`. Those three numbers are
a message, read as `MAJOR.MINOR.PATCH`:

- **PATCH** bump (2.4.1 → 2.4.2): bug fixes only. Upgrading is safe.
- **MINOR** bump (2.4.1 → 2.5.0): new features, but nothing existing breaks.
  Upgrading is safe.
- **MAJOR** bump (2.4.1 → 3.0.0): **breaking changes** — things that worked
  before may now behave differently or be gone. Upgrading requires reading
  the release notes and possibly changing your code.

One glance at which number moved answers "is this upgrade dangerous?" —
you'll use this reading constantly from Phase 4 onward.

---

## 11. The code I wrote for you — walkthrough

Everything lives in
[concepts/phase-00-tools-of-the-trade/playground/](playground/). Each file is
heavily commented — **the comments are part of the lesson; read every file
top to bottom.**

| File | What it's for |
|---|---|
| `make_logs.sh` | Generates `server.log` — ~800 lines of realistic fake web traffic, with three planted mysteries (an error burst, one suspicious visitor, one slow page) for you to uncover with grep/awk/sed. |
| `exercises.md` | The guided hunt: 12 investigation tasks against `server.log`, each with a collapsible answer. |
| `runaway.sh` | Deliberately hogs a CPU core so you can practice the full hunt-and-stop workflow with `top`, `pgrep`, `kill` — and see graceful shutdown vs SIGKILL with your own eyes. |
| `heartbeat.sh` | A tiny script that appends one time-stamped line per run — your cron exercise target. |
| `git_xray.sh` | Run after your first commit: it opens `.git/` and shows you the actual commit, tree, and blob objects, and the one-line branch file — section 10, made physical. |

Things to notice as you read them:

- Every script starts with the shebang line and `set -euo pipefail`
  (section 9 — you can now decode all four words).
- Every script **narrates what it is doing** in `[STEP]`-style output lines.
  This is the "logging as a teaching tool" habit the whole course uses, and
  it starts here.
- `make_logs.sh` seeds its random generator (`RANDOM=42`) so that everyone
  who runs it gets nearly the same file — meaning the expected outputs I
  quote will closely match what you actually see.

---

## 12. Run it & watch the logs

> Our contract, restated: **you** run everything; I never do. Work the parts
> in order, and paste anything surprising back to me — interpreting output
> together is part of the course.
> **Part A (git init / GitHub / first push) was given in the chat — do that
> first if you haven't.** Then continue here.

### Part B — one-time: install WSL (your Linux)

Open **PowerShell as Administrator** (right-click the Start button →
"Terminal (Admin)"), then:

```powershell
wsl --install
```

*What it does:* installs WSL together with Ubuntu Linux (the most popular
beginner-friendly Linux flavor).
**Expect:** download/progress messages, then a request to **restart your
computer**. After the restart, an Ubuntu window opens on its own and asks you
to choose a Linux username and password. This account is separate from
Windows; the password is what `sudo` will ask for. **Success looks like:** a
prompt such as `aiman@YOURPC:~$`.
**If it says WSL is already installed:** run `wsl --install -d Ubuntu` to add
Ubuntu, or just type `wsl` to enter it.
**If you see an error about virtualization:** it may be disabled in your
machine's firmware — paste me the exact message and we'll fix it together.

From here on, "in Linux" means: open Windows Terminal → type `wsl` → Enter
(or open the "Ubuntu" app from the Start menu).

### Part C — enter the playground

```bash
cd /mnt/d/Projects/linkboard/concepts/phase-00-tools-of-the-trade/playground
ls -l
```

*What it does:* walks to the playground folder — note the path: this is your
Windows `D:\Projects\linkboard`, seen from inside Linux via `/mnt/d/` —
and lists it in long format.
**Expect:** the five files from section 11. Look at the permissions column
(section 6): the `.sh` files likely show **no `x`** yet — they aren't
executable until you say so:

```bash
chmod +x make_logs.sh runaway.sh heartbeat.sh git_xray.sh
ls -l
```

**Expect:** `x` appearing in the permission blocks, e.g. `-rwxr-xr-x`.

### Part D — generate the log file and start the hunt

```bash
./make_logs.sh
```

**Expect (annotated):**

```
[STEP] Generating fake web-server traffic into server.log ...
[STEP] Planting an ERROR burst around 11:42 ...           ← you'll find this with grep
[STEP] Planting a suspicious IP (198.51.100.66) ...       ← and this with the top-5 pipeline
[STEP] Planting a slow endpoint (/search) ...             ← and this with awk arithmetic
[DONE] Wrote 800 lines to server.log — happy hunting. Open exercises.md next.
```

**Success check:** `wc -l server.log` prints roughly 800.
**Failure signs:** `Permission denied` → the chmod step was skipped.
`bad interpreter: /bin/bash^M` → Windows-style line endings crept into the
file; the fix is one command (`sed -i 's/\r$//' *.sh` — and you can now read
it: "strip a trailing \r character from every line, in place") and our
`.gitattributes` file prevents it from recurring.

Then open **`exercises.md`** and work the 12 hunts. Genuinely try each one in
the terminal before expanding its answer. This is the heart of the Linux half
— give it an unhurried hour.

### Part E — the runaway process

Open **two** WSL terminals side by side.

**Terminal 1:**

```bash
./runaway.sh
```

**Expect:** `[RUNAWAY] I am PID 12345 and I am about to waste CPU in a busy
loop.` — followed by silence (it's busy!). Your PID number will differ.

**Terminal 2:**

```bash
top                      # the culprit sits at the very top: ~100% CPU, command "runaway.sh".
                         # Note its PID, press q to quit top.
pgrep -f runaway.sh      # confirms: the same PID, found by name
kill <PID>               # the polite request — SIGTERM (section 4.3)
```

**Expect:** Terminal 1 prints `[RUNAWAY] Caught SIGTERM — cleaning up
politely. Goodbye.` and exits. That is graceful shutdown, live.
Now run it once more — and this time use `kill -9 <PID>`. **Expect:**
Terminal 1 just shows `Killed`. No goodbye, no cleanup — the process never
saw it coming. You have now *seen* the entire content of section 4.3.

### Part F — cron heartbeat

```bash
sudo service cron start
```

*What it does:* starts the cron scheduler service (WSL doesn't auto-start
services). **Expect:** `Starting periodic command scheduler cron` — or a
note that it's already running. Either is fine.

```bash
crontab -e
```

*What it does:* opens your personal schedule table in an editor. First time,
it asks which editor — **choose nano** (the easiest). Add this line at the
bottom (adjust the path only if your repo lives elsewhere), then save and
exit nano with: `Ctrl+O`, `Enter`, `Ctrl+X`:

```
* * * * * /mnt/d/Projects/linkboard/concepts/phase-00-tools-of-the-trade/playground/heartbeat.sh >> /tmp/heartbeat.log 2>&1
```

You can decode every piece of that line yourself now: five stars = "every
minute" (section 8); the absolute path = cron's stripped-down environment
rule; `>> ... 2>&1` = "append everything it says, output and errors both, to
this file" (section 2.5). Now watch the evidence arrive:

```bash
tail -f /tmp/heartbeat.log
```

**Expect:** within at most 60 seconds, lines begin appearing:

```
[HEARTBEAT] 2026-07-16 18:42:01 — cron ran me. Beat #1
[HEARTBEAT] 2026-07-16 18:43:01 — cron ran me. Beat #2
```

Each line proves the full chain: cron woke up on schedule → ran your script
with no terminal attached → your redirection captured what it printed. After
two or three beats, press `Ctrl+C`, then **remove the job** so it doesn't
beat forever: `crontab -e`, delete the line, save.
**Failure signs:** nothing after 2+ minutes → check `service cron status`
(is it running?) and re-check the path in the crontab line character by
character (a wrong path inside silent cron is *the* classic failure —
section 8, gotcha #1).

### Part G — the git x-ray (after Part A's first commit exists)

```bash
cd /mnt/d/Projects/linkboard
concepts/phase-00-tools-of-the-trade/playground/git_xray.sh
```

**Expect:** a narrated dissection of your repository, in four acts: your
newest **commit** object printed in full (spot the `tree` line, and either a
`parent` line or the note that this is the root commit); the **tree** it
points to (spot your filenames, each next to a blob fingerprint); the actual
content of one **blob**; and finally the one-line file that *is* the `main`
branch. Read it side by side with sections 10.4–10.5 — this is the moment
the model clicks.

---

## 13. Break it / observe it

Optional experiments — each turns a claim from the lesson into something you
watch happen. Nothing here can damage anything outside the playground.

1. **Feel `rm`'s finality:** `touch victim.txt && rm victim.txt` — no
   confirmation, no recycle bin, no undo. Respect it accordingly: never
   delete with a wildcard (`rm *.log`) without first running `ls *.log` to
   see exactly what would match.
2. **See the two hoses split (section 2.5):** run `ls playground /nope`.
   You get a listing (stdout) *and* an error (stderr), mixed. Now run
   `ls playground /nope 2> /dev/null` — the error vanishes (redirected into
   `/dev/null`, the system's built-in trash chute that discards whatever is
   written to it) while the listing remains. Now swap: `ls playground /nope
   1> /dev/null` — only the error remains. Two hoses, independently
   pluggable. You've proven it.
3. **See hash property 2 (tiny change → totally different fingerprint):**
   ```bash
   echo "hello" | sha1sum
   echo "hellp" | sha1sum
   ```
   One letter differs between the inputs; compare the two fingerprints —
   nothing matches. This is the property that makes Git's storage and its
   tamper-evidence work (sections 10.2 and 10.4).
4. **Break a script with Windows line endings, on purpose:** in the
   playground, run `sed -i 's/$/\r/' heartbeat.sh` (append a `\r` to every
   line — exactly what Windows editors can do silently), then
   `./heartbeat.sh` and enjoy the cryptic `bad interpreter` error. Fix it:
   `sed -i 's/\r$//' heartbeat.sh`. You have now pre-lived the single most
   common Windows-meets-Linux bug, and you own its cure.
5. **Watch Git see everything (section 10.3):** change one character in
   `README.md`, then run `git status` and `git diff` — Git names the file
   and shows the exact edit. Undo it with `git restore README.md`. Lesson:
   the working directory is a sandbox; the album never changed.
6. **Prove that commits can't be secretly edited (section 10.4):** run
   `git log --oneline -1` and note the short fingerprint. Now run
   `git commit --amend -m "same files, different message"` and look again:
   the fingerprint **changed**, because the commit's content (its message)
   changed. Amending your *latest, unpushed* commit like this is a normal,
   safe operation — but you've just seen why amending *pushed* history
   violates the iron rule of section 10.7: the old fingerprint everyone else
   knew is gone.
7. **Meet the reflog (section 10.8):** right after experiment 6, run
   `git reflog`. Top two lines: the amended commit, and — still there — the
   "old" one you supposedly replaced. Nothing committed ever really
   disappears; the diary sees all.

---

## 14. Glossary (terms this phase introduced)

- **Operating system (OS):** the manager program that runs all other programs and shares out the hardware.
- **Linux:** the free, open-source OS that runs most of the world's servers.
- **Server:** a computer whose job is answering requests from other computers.
- **WSL:** Windows Subsystem for Linux — a real Linux running inside Windows.
- **Terminal / shell / prompt:** the window you type into / the program (bash) that interprets what you type / its "ready for input" marker.
- **Command / flag / argument:** the program to run / a `-x` switch changing its behavior / the thing it acts on.
- **Root (folder):** `/`, the top of the Linux folder tree. (Also the name of the admin account — same word, two meanings.)
- **Path (absolute / relative):** a file's address, from `/` / from where you're standing. `.` = here, `..` = one level up, `~` = your home folder.
- **Hidden file:** any file whose name starts with a dot; `ls -a` reveals them.
- **stdin / stdout / stderr:** a program's three standard hoses — input (0), normal output (1), errors (2).
- **Redirection (`>`, `>>`, `2>`, `2>&1`):** pointing hoses at files — overwrite / append / errors only / merge errors into output.
- **`/dev/null`:** the discard chute — anything written to it vanishes.
- **Pipe (`|`):** connect one program's output hose to the next program's input hose.
- **Unix philosophy:** many small single-purpose tools, freely combined.
- **Log (file):** a program's diary — one line per event.
- **Regular expression (regex):** a mini-language for matching text patterns.
- **Process / PID:** a running instance of a program / its ID number.
- **Signal / SIGTERM / SIGKILL / SIGINT:** a message the OS delivers to a process / "please stop" / "erased immediately, uncatchable" / "interrupt" (Ctrl+C).
- **Graceful shutdown:** a program reacting to SIGTERM by finishing its current work before exiting.
- **Permissions / chmod / 755:** each file's read-write-execute rulebook / the command that edits it / the digit form (r=4, w=2, x=1 summed per group).
- **root (account) / sudo:** the all-powerful admin user / "run this one command as root."
- **SSH / key pair:** an encrypted terminal on a remote machine / padlock (public key, shareable) + only-key (private key, never leaves your machine).
- **scp / rsync:** copy files over SSH / copy only the *differences*.
- **cron / crontab:** the schedule-runner service / your personal table of scheduled commands (5 time fields + command).
- **Shebang (`#!`):** a script's first line, naming which program interprets it.
- **Exit code / `$?`:** the number every program hands back on finishing — 0 = success, non-zero = failure / the shell variable holding the most recent one.
- **Version control / Git / GitHub:** keeping every historical state of a project / the dominant tool for doing so / a website that hosts Git repositories.
- **Repository (repo):** a project folder managed by Git; the history lives in its hidden `.git/` folder.
- **Snapshot:** a complete record of every file at one moment — what a commit stores.
- **Hash / fingerprint:** a fixed-length scramble uniquely identifying a piece of content; same input → same hash, tiny change → totally different hash, not reversible.
- **Content-addressed storage:** filing content under its own fingerprint — so identical content is stored exactly once.
- **Blob / tree / commit:** Git's three object types — file content / folder listing (where filenames live) / snapshot record with author, message, and parent pointer.
- **Parent (of a commit):** the commit that came directly before it; parent pointers turn snapshots into history.
- **Working directory / staging area / repository:** your editable files (the desk) / what the next snapshot will include (the photo table) / the permanent album.
- **Branch:** a named, movable pointer to a commit — physically a one-line file; it slides forward automatically as you commit.
- **HEAD:** the pointer that marks which branch you're currently on — the "you are here" arrow.
- **Merge / merge commit:** combining two branches with a new commit that has two parents; nothing rewritten.
- **Rebase:** replaying your commits on top of another branch — a straight line, but the replayed commits are new commits with new fingerprints.
- **Conflict:** Git pausing to ask you which version to keep when both branches edited the same lines; resolved by editing the marked file.
- **cherry-pick:** copy a single commit from another branch onto yours.
- **bisect:** find the commit that introduced a bug by binary search over history.
- **Binary search:** finding a target by repeatedly halving the possibilities — ~9 questions cover 300 suspects.
- **reflog:** Git's private diary of every position HEAD has ever had — the recovery tool of last resort.
- **Remote / origin:** a copy of the repository elsewhere / the conventional nickname for your main remote.
- **clone / push / fetch / pull:** copy a remote repo down (once) / send commits up / download commits without applying / fetch + merge in one step.
- **GitFlow / trunk-based development:** formal multi-branch workflow for versioned releases / small changes merged into main quickly (our style).
- **Semantic versioning (semver):** version numbers as MAJOR.MINOR.PATCH = breaking changes / new-but-compatible features / bug fixes only.

---

## 15. Challenges & Questions

Purely optional, never graded, answers one click away. Think as long or as
short as you like.

### Challenge 1: Design the pipeline
Using only tools from section 3 and pipes: how would you find the **top 3
slowest requests** in `server.log`?

<details>
<summary>Show answer</summary>

Sort the whole log by the duration column (column 8), as numbers, biggest
first — then keep three lines:

```bash
sort -k8 -rn server.log | head -3
```

`-k8` = "sort by column 8", `-r` = reversed (descending), `-n` = compare as
numbers, not alphabetically. (It works despite the "ms" suffix because
numeric sorting reads the leading digits and stops.) A variant that prints
only the columns you care about:

```bash
awk '{print $8, $5, $6}' server.log | sort -rn | head -3
```
</details>

### Challenge 2: The silent cron job
Your cron job "doesn't work." There's no output and no error anywhere. Name
three distinct things you'd check, in a sensible order.

<details>
<summary>Show answer</summary>

1. **Is the cron service itself running?** `service cron status`. (On WSL it
   doesn't start automatically — section 8's note.)
2. **Is the schedule line actually there and correct?** `crontab -l` — is
   the entry present? Do the five time fields say what you intended?
3. **Does the command work at all, outside cron?** Copy the exact command
   from the crontab line and paste it into a normal shell. If it works there
   but not under cron, the culprit is almost always cron's stripped-down
   environment — usually a relative path that only worked from your shell's
   current folder. Absolute paths fix it. And adding `>> /tmp/job.log 2>&1`
   to the line gives cron a voice, so the next failure won't be silent.
</details>

### Challenge 3: Why is rewriting *pushed* history dangerous?
Amending or rebasing commits that only exist on your machine is routine and
safe. What exactly goes wrong when the commits were already pushed?

<details>
<summary>Show answer</summary>

Rewriting a commit creates a **new commit with a new fingerprint** — the old
one is abandoned (section 10.7). If others already pulled the old commit,
their new work records the *old* fingerprint as a parent. After your
rewrite, their work is built on top of a commit your branch no longer
contains — the two histories disagree at the foundation, pushes start
getting rejected, and repairing it requires manual surgery on every affected
person's copy. Rule of thumb: local history is your private draft — edit
freely; pushed history is a published book others may be citing — never
alter it.
</details>

### Challenge 4: Merge or rebase?
A teammate says "always rebase — merge commits clutter the history." When is
that advice wrong?

<details>
<summary>Show answer</summary>

Twice. First, whenever the commits are **shared**: rebasing pushed commits
rewrites history others depend on — Challenge 3's disaster. Second, when the
true shape of events matters: a merge commit permanently records "these two
lines of work joined here," which can be exactly what an investigation needs
later ("did the fix make it into that release?"). Reasonable etiquette:
rebase your own unpushed drafts to keep them tidy; merge shared work.
</details>

### Challenge 5: The fingerprint intuition
Two *different* files in your project happen to have *identical* content.
After you commit, how many blobs does Git store for them?

<details>
<summary>Show answer</summary>

**One.** Identical content produces the identical fingerprint (hash property
1), so both files resolve to the same object name — and Git stores each
object exactly once. The two *filenames* live separately in the tree
(section 10.4), and both tree entries point at the same single blob. This
"identical content stored once, found by fingerprint" trick reappears later
in Docker's image layers (Phase 9) and in caching (Phase 8).
</details>

### Challenge 6 (stretch): `kill -9` and the database
Phase 6 will introduce PostgreSQL, a database. Using section 4.3, reason out
why `kill -9` on a database is riskier than on our little runaway script.

<details>
<summary>Show answer</summary>

SIGKILL gives the process no chance to finish anything (section 4.3). Our
runaway script was doing nothing of value, so nothing was lost. A database,
however, may be *mid-way through writing your data to disk* — kill it at
that instant and files can be left half-written and inconsistent. Real
databases defend against exactly this with a "write-ahead log" they replay
on startup to repair themselves (that's a Phase 15 topic — and notice it's
the append-only diary idea again). But recovery takes time and only covers
what was logged. So: for anything that owns data, SIGTERM first, always;
`-9` is the last resort.
</details>

---

**Next up:** once you've worked the run sections and we wrap this phase
(commit + push), Phase 1 opens the machine itself: what binary is, what the
CPU and RAM actually do, and the one idea — blocking I/O — that explains why
servers are architected the way they are.
