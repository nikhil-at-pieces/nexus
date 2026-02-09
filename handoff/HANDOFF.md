# Nexus — Handoff Document

This document describes **Nexus**: a **Twitter listening / social listening** tool you can run locally or on a single server. It is intended for handoff to another developer or team who will run, maintain, or extend it.

---

## Table of Contents

1. [What This System Is](#what-this-system-is)
2. [Key Features](#key-features)
3. [Repository and Scope](#repository-and-scope)
4. [What You Need to Run It](#what-you-need-to-run-it)
5. [Quick Start](#quick-start)
6. [Handoff Checklist](#handoff-checklist)
7. [Support and Contact](#support-and-contact)

---

## What This System Is

Nexus is a **Twitter listening / social listening** application that:

- **Monitors Twitter/X** for keywords, hashtags, and mentions using [twscrape](https://github.com/vladkens/twscrape) (cookie-based, no official API key required for search).
- Runs **AI-powered analysis** on conversations (relevance scoring, engagement opportunities, suggested replies) via an LLM (e.g. Google Gemini).
- Exposes an **HTTP API** (FastAPI) for creating campaigns, starting listening runs, and polling progress.
- Uses **background workers** (Celery + Redis) so Twitter search and AI analysis run asynchronously without blocking the API.
- Uses a **scheduler** (APScheduler) for periodic or scheduled listening runs.
- Stores **persistent data** in PostgreSQL (campaigns, runs, organizations, users) and uses **Redis** for caching, run progress, and as the Celery broker.

The codebase in this repo is the full application. It is designed to run **locally or on a single server** (e.g. developer machine or small VPS), not as a hosted multi-tenant SaaS.

---

## Key Features

| Feature | Description |
|--------|-------------|
| **Keyword / hashtag listening** | Define campaigns with keywords; system searches Twitter/X and collects tweets. |
| **Conversation threads** | Builds full reply threads for each tweet for context. |
| **AI analysis** | Each conversation is analyzed (relevance, insights, suggested replies). |
| **Opportunities** | High-relevance results can be exported (e.g. Google Sheets) or notified (e.g. Slack). |
| **Scheduled runs** | Scheduler can trigger listening runs on a schedule. |
| **CLI** | One-off Twitter search via `nexus twitter-search` for testing or scripts. |
| **Optional frontend** | Next.js app in `nexus-frontend/` for UI (run separately). |

---

## Repository and Scope

- **Repository:** [github.com/nikhil-at-pieces/nexus](https://github.com/nikhil-at-pieces/nexus)
- **Language:** Python 3.11+
- **Key stack:** FastAPI, Celery, Redis, PostgreSQL, Docker (optional)

### Handoff package (this folder)

| File | Purpose |
|------|--------|
| `README.md` | Index of handoff docs (this folder). |
| `HANDOFF.md` | This file — overview and handoff notes. |
| `ARCHITECTURE.md` | High-level components, data flow, project layout. |
| `SETUP.md` | Environment and dependency setup. |
| `RUNNING.md` | How to run API, worker, scheduler; CLI; Docker. |
| `env.example` | Example environment variables (no secrets). |

This handoff focuses on **system structure, setup, and operations** so you can run and extend the Twitter listening tool.

---

## What You Need to Run It

**Required:**

1. **Python 3.11+** and a virtual environment.
2. **PostgreSQL** (e.g. 15) — for the main database.
3. **Redis** — for cache and Celery broker.
4. **Environment variables** — copy `handoff/env.example` to project root as `.env` and set at least: `NEXUS_SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`.
5. **Database migrations** — run `alembic upgrade head` after first setup (see RUNNING.md).

**Optional:**

- **Docker / Docker Compose** — to run Postgres, Redis, API, and worker as containers.
- **Google API key** — for AI conversation analysis (Gemini).
- **Slack / Google Sheets** — for notifications and exports (configure in org credentials or env).
- **Frontend** — `nexus-frontend/`; run and configure it separately if needed.
- **Twscrape accounts** — add Twitter cookies (via API or UI) for search; no API key needed.

---

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/nikhil-at-pieces/nexus.git && cd nexus

# 2. Create venv and install
python3.11 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

# 3. Start Postgres and Redis (e.g. via Docker)
docker compose up -d postgres redis

# 4. Copy env and set required variables
cp handoff/env.example .env
# Edit .env: NEXUS_SECRET_KEY (32+ chars), DATABASE_URL, REDIS_URL, CELERY_*

# 5. Run migrations
alembic upgrade head

# 6. Start API and worker (separate terminals)
nexus run --host 0.0.0.0 --port 8000
nexus worker
# Optional: nexus scheduler
```

- **API:** http://localhost:8000  
- **Docs:** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health or http://localhost:8000/api/v1/health  

See **RUNNING.md** for full details.

---

## Handoff Checklist

- [ ] Read **ARCHITECTURE.md** for component overview.
- [ ] Follow **SETUP.md** to install dependencies and configure `.env`.
- [ ] Run database migrations: `alembic upgrade head`.
- [ ] Start API, worker, and (optional) scheduler; confirm health via `/health` or `/api/v1/health`.
- [ ] Confirm Redis and Postgres connectivity from the app.
- [ ] If using Docker Compose, run full stack and verify `nexus-api` and `nexus-worker` logs.
- [ ] Optionally add a twscrape account (Twitter cookies) and run a test campaign or `nexus twitter-search`.

---

## Support and Contact

For questions about this handoff or the repository, contact the previous maintainer or open an issue in the GitHub repo: [github.com/nikhil-at-pieces/nexus](https://github.com/nikhil-at-pieces/nexus).

---

*Last updated: February 2025*
