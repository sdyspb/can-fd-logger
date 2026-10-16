# agent-ask-rules.md — when an AI agent MUST ask the user instead of deciding

> Rule set for AI agents working in this repository (and generally). The
> session-26 postmortem (`CONTEXT-26.md`): the `ramroot-installer.sh` was not
> run on firefly1tb because (1) the repo is private and the server had no
> GitHub credential, (2) the server was a different distro than the installer
> was written/tested for, and (3) the agent went "manual" on its own and made
> the NFS-export bug. In all three cases the agent SHOULD have asked first.
> This file encodes those lessons as rules.

## Core principle

When an action is **irreversible, state-changing, or depends on an
assumption that could be wrong**, the agent asks a short question (with 2–4
concrete options) **before** acting. Asking is cheap; a wrong guess on a
private server, a wiped disk, or a wrong branch is expensive. Prefer asking
over assuming; prefer a 30-second question over a 30-minute rollback.

Do NOT ask for trivial, reversible, or clearly-determined things (a file
read, a `git status`, a syntax check, a formatting fix). The goal is to ask
exactly when the downside of guessing is non-trivial.

## Rule 1 — Credentials / access to private resources (ASK)

If a task needs access the agent does not clearly have (a private repo, a
service token, a database, a server login):
- **Ask** how to obtain it, with concrete options (e.g. "provide a token",
  "I'll push the files over the LAN", "use a public mirror", "run it on a
  machine that already has access").
- **Never** proceed on a silent assumption that a credential is present
  (the session-26 trap: `GITHUB_TOKEN` appeared "set" in a login shell but
  was empty in the non-interactive ssh shell the agent used).
- If the only way forward is to work around the missing access (e.g. copy
  files manually), that workaround is a **decision** — ask first.

## Rule 2 — Environment / version differs from what the tool/docs assume (ASK)

If the target environment differs from what the script/docs were written for
(a different distro, a different package version, a different U-Boot/kernel,
a different board):
- **Detect** the difference first (read-only: `cat /etc/os-release`,
  `dpkg -l <pkg>`, `uname -a`, the unit file, the config).
- **Ask** whether to adapt the tool to the new environment (and how) or to
  use the known-good path, when the adaptation is non-trivial.
- Do not silently "fix" a mismatch by trial-and-error across many
  combinations unless the user has approved that exploratory approach.

## Rule 3 — Going off the canonical tool to a manual path (ASK)

If the repo has a canonical tool (an installer, a build script, a deploy
script) and the agent considers bypassing it with manual steps:
- **Ask** why (what blocks the canonical path) and whether manual is OK.
- State the specific divergence the manual path introduces.
- (Session-26: the manual path introduced the NFS-export bug — the installer
  itself was correct.)

## Rule 4 — Destructive / state-changing / irreversible actions (ASK or confirm)

- Wiping a disk/SD, dropping data, overwriting a deployment, `git push` to a
  shared branch, deleting a release asset, restarting a production service:
  **confirm** the exact target and scope before executing.
- The user saying "do it" for a known action is enough; do not re-confirm
  every trivial step, but DO confirm the **target** (e.g. which `/dev/sdX`)
  and any **scope expansion** beyond what was asked.
- For long, hard-to-reverse operations, state what will be done and the
  rollback path first.

## Rule 5 — Scope / goal ambiguity (ASK)

If "done" is not clearly defined, or the request could mean several
different things, ask which one is intended (with options). Do not pick the
most likely interpretation and run with it if the alternatives are
materially different.

## Rule 6 — Multiple viable solutions with different tradeoffs (ASK)

When there are 2+ reasonable approaches and the choice affects the result
(performance, maintainability, compatibility, cost), present the options and
let the user choose. Do not silently pick one unless the user's prior
instructions clearly favor it.

## Rule 7 — When NOT to ask (avoid question fatigue)

Do not ask when:
- The action is read-only or trivially reversible.
- The user already gave a clear directive covering the action.
- The decision is dictated by repo conventions/docs (follow the convention;
  only ask if the convention is missing/contradictory).
- You can verify the assumption with a cheap read-only check instead of
  asking (e.g. "is the repo reachable?" → just probe it).
Ask once, with concrete options; do not re-ask the same question.

## Rule 8 — How to ask (format)

- One focused question (not a wall of them).
- Give 2–4 concrete options (not an open "what do you want?").
- State the default you will take if the user does not answer, and the risk
  of the current path in one line.
- Keep it short; the user may be non-technical (match their language —
  Russian in this project unless told otherwise).

## Rule 9 — After acting: report the assumptions you made

Whenever the agent proceeded on an assumption (even a reasonable one), it
must call it out in the final summary: "I assumed X; if that is wrong, do Y."
This turns a silent guess into a visible, correctable decision.

## Quick decision checklist (run before each non-trivial action)

1. Is this read-only / trivially reversible? → act, no ask.
2. Does it need access I don't clearly have? → **ask** (Rule 1).
3. Does the environment differ from what the tool/docs assume? → **ask**
   (Rule 2).
4. Am I about to bypass the canonical tool? → **ask** (Rule 3).
5. Is it destructive/irreversible/state-changing? → **confirm** target/scope
   (Rule 4).
6. Is the goal or the solution ambiguous? → **ask** (Rules 5/6).
7. Did I make an assumption? → **report** it (Rule 9).
