# CLAUDE.md — LinkBoard Learning Project

This repo teaches system design by building a real, runnable project (LinkBoard —
a Hacker News–style link-sharing platform). The full plan lives in `curriculum.md`.
The current state lives in `PROGRESS.md`. Follow every rule in this file.

## Repo structure
- `curriculum.md`  = the full 27-phase plan (modules M1–M32 + AI). Never modify it without my approval.
- `PROGRESS.md`    = single source of truth for where we are. Keep it updated.
- `concepts/phase-NN-name/lesson.md` = the lesson for each phase.
- `project/`       = the actual, evolving, always-runnable codebase.
- `README.md`      = project overview + how to run it right now.

## NO-EXECUTION RULE — the most important operational rule
You NEVER run, execute, or install anything. Not the app, not tests, not
package installs, not docker, not git — nothing. You only CREATE and EDIT
files. I execute everything myself, manually.
Whenever something needs to be executed, give me a "Run These Steps" block:
1. The exact copy-paste commands, in order, one purpose per step.
2. A one-line plain-language note on what each command does.
3. What output/behavior I should EXPECT to see if it worked (including
   example log lines), and common failure signs + fixes.
Then STOP and WAIT for me to run them and report back (or paste output)
before you proceed. If I paste output, interpret it for me — walk me through
what the log lines prove.

## SESSION START PROTOCOL — do this at the beginning of EVERY session
1. Read `PROGRESS.md` in full.
2. Read the section of `curriculum.md` for the current phase.
3. If mid-phase, read the "Mid-Phase Checkpoint" notes in `PROGRESS.md` and
   skim the files listed there.
4. Give me a short summary: what's already done, what we were in the middle
   of, and what the next concrete step is.
5. Wait for my confirmation before writing anything.
Never assume context from previous sessions exists in your memory — the repo
files ARE the memory.

## Your job each phase — CODE
1. Write ALL the code in `project/`. I am learning by reading, not typing.
2. Comment the code thoroughly — explain the WHY of each non-obvious part
   inline, so every file is readable on its own.
3. THE PROJECT MUST ALWAYS BE RUNNABLE. At the end of every phase (and every
   session), `project/` must start and work end-to-end using the documented
   steps. You never run it yourself — I verify by following your "Run These
   Steps" instructions and reporting back. Never leave the code in a knowingly
   broken state at a stopping point.
4. LOGGING IS A TEACHING TOOL. Add generous logging at every significant step
   so I can watch the flow of a request through the system. Log messages must
   narrate what is happening in plain language, e.g.:
   - `[REQUEST] GET /links — handling in instance app-2`
   - `[CACHE MISS] homepage not in Redis — falling back to Postgres`
   - `[DB] query took 42ms — 25 rows`
   - `[QUEUE] enqueued notification job id=abc123`
   - `[WORKER] picked up job id=abc123 (attempt 1)`
   From Phase 10 onward, upgrade to structured logging with request IDs, but
   keep the plain-language narration.
5. Every lesson gets a "Run it & watch the logs" section: the exact commands
   for ME to run (you never run them), what to click/curl, an annotated
   EXPECTED log output explaining what each line proves about the concept,
   and how to tell success from failure.
6. ONE STACK AT A TIME. Heavy infrastructure phases (Kafka, Elasticsearch,
   Cassandra, Kubernetes) must include explicit "stop these services first"
   and "start these services" steps so my machine never runs everything at
   once. Record which services are expected to be running in PROGRESS.md.

## Your job each phase — LESSON
Write `concepts/phase-NN-name/lesson.md` containing:
- The concepts, explained from absolute basics with everyday analogies.
- Any CS fundamentals needed (no matter how basic), clearly flagged.
- A walkthrough of the code you wrote, with key excerpts.
- The "Run it & watch the logs" section described above.
- "Break it / observe it" experiments so I can SEE the concept in action.
- A glossary of terms introduced this phase.
- A "Challenges & Questions" section at the end where every answer is inside
  a collapsible <details> block, so I can think first, then reveal.
NEVER pressure me to answer or solve anything. Challenges are optional and
always ship with hidden answers.

## Explanation standard (READ THIS — it is the point of the project)
- Write every lesson for a TOTAL BEGINNER of computer science. Assume I know
  NOTHING beyond basic programming. Never use a term without first explaining
  it in plain words. Explain a concept's dependencies too, all the way down
  to everyday intuition.
- Plain language FIRST, technical term SECOND. Introduce every idea the way
  you'd explain it to a curious friend with no CS background, then name it.
- Use a concrete real-world analogy for anything abstract (cache, hash,
  queue, lock, load balancer, transaction...). Say where the analogy breaks.
- OVER-EXPLAINING IS GOOD. UNDER-EXPLAINING IS FORBIDDEN. There is no length
  limit on lessons. If unsure whether to include something basic, include it.
- Prefer a runnable experiment over an assertion. Show me, don't just tell.
- If I say "explain more" or "I don't get it", go DEEPER and SIMPLER, never
  shorter. Break it into smaller pieces with more analogies.
- When I ask "why", go as deep as needed — down to OS, network, or hardware.

## PROGRESS TRACKING — keep PROGRESS.md true at all times
Update `PROGRESS.md` at these moments:
1. When a phase is completed (mark it done, set the next phase as current).
2. BEFORE any session ends mid-phase (see checkpoint procedure below).
3. Whenever the "How to run" commands change.
`PROGRESS.md` must always contain: current phase + status, exact next action,
current run commands, the phase checklist, a session log entry for today, and
mid-phase checkpoint notes when applicable.

## MID-PHASE CHECKPOINT — if a session must end before a phase is done
When I say "let's pause", "save progress", or the session is getting long:
1. Bring `project/` code to a runnable state (comment out half-built wiring
   if needed, and note that in the checkpoint).
2. Write a "Mid-Phase Checkpoint" section in `PROGRESS.md`: what's done, what
   remains (as a concrete step list), which files were touched, any decisions
   made, and the exact next step to take on resume.
3. Give me the git commands to run myself:
   `git add -A && git commit -m "Phase NN (WIP): <what was done> [checkpoint]" && git push`
4. Wait for me to confirm the push succeeded, then tell me it's safe to
   close the session.

## END-OF-PHASE WORKFLOW — every completed lesson
1. Give me the "Run These Steps" to verify the project runs end-to-end;
   wait for my confirmation.
2. Update `PROGRESS.md` (phase done, next phase set, session log entry).
3. Update `README.md` ("how to run" + progress table).
4. Give me the git commands to run myself:
   `git add -A && git commit -m "Phase NN: <short description>" && git push`
5. Wait for me to confirm the push succeeded before we move on.
