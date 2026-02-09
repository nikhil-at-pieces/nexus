# Nexus — Twitter / Social Listening (Handoff)

This repository contains the **handoff package** for Nexus: a Twitter listening / social listening tool. It is a short reference for setup, architecture, and code patterns — not the full application.

**Start here:** [nexus/README.md](nexus/README.md)

## Contents

- **[nexus/](nexus/)** — Documentation and code reference
  - **HANDOFF.md** — Overview, quick start, checklist
  - **ARCHITECTURE.md** — Components, data flow, project layout
  - **SETUP.md** — Prerequisites, env, migrations
  - **RUNNING.md** — API, worker, scheduler, CLI
  - **env.example** — Example environment variables
  - **code/** — Key modules (config, app, main, celery_app, build_search_query)

## Repo

- **GitHub:** [github.com/nikhil-at-pieces/nexus](https://github.com/nikhil-at-pieces/nexus)
- **Stack:** Python 3.11+, FastAPI, Celery, Redis, PostgreSQL

The full application codebase lives elsewhere; this repo is for handoff and reference only.
