# Phase 0 Playground

Small, disposable exercises for the Linux half of Phase 0. Everything here is
driven by `../lesson.html` (open it in your browser) — read that first; its
"Run it & watch the logs" section tells you when to use each file.

| File | Purpose |
|---|---|
| `make_logs.sh` | Generates `server.log` (~800 lines of fake web traffic with planted mysteries). |
| `exercises.md` | 12 guided log-hunt exercises with collapsible answers. |
| `runaway.sh` | A CPU-hogging process for you to find and kill. Demonstrates graceful shutdown. |
| `heartbeat.sh` | The cron exercise target — appends one timestamped line per run. |
| `git_xray.sh` | Dissects the repo's newest commit into blob/tree/commit objects. |

Generated files (`server.log`, `anonymized.log`) are git-ignored — regenerate
them any time with `./make_logs.sh`.
