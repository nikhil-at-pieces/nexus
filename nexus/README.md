# Nexus — Documentation

This folder contains the **documentation** for **Nexus**, a **Twitter listening / social listening** tool. Use these docs to understand, set up, and run the system (e.g. locally or on a small server).

---

## Contents

| File | Description |
|------|-------------|
| **[HANDOFF.md](HANDOFF.md)** | Overview, what the system is, quick start, handoff checklist |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Components, data flow, project layout, deployment model |
| **[SETUP.md](SETUP.md)** | Prerequisites, clone, Python env, Postgres/Redis, env vars, migrations |
| **[RUNNING.md](RUNNING.md)** | How to run API, worker, scheduler; CLI; Docker; troubleshooting |
| **[env.example](env.example)** | Example environment variables (copy to project root as `.env`) |
| **[code/](code/)** | Key modules from the codebase: `config.py`, `app.py`, `main.py`, `celery_app.py`, `build_search_query.py` |

---

## What Nexus Is

- **Twitter / X listening** — Monitor keywords, hashtags, and mentions via [twscrape](https://github.com/vladkens/twscrape)
- **AI analysis** — Analyze conversations for relevance and engagement (e.g. Google Gemini)
- **API + workers** — FastAPI backend, Celery workers, APScheduler for scheduled runs
- **Storage** — PostgreSQL for campaigns/runs, Redis for cache and Celery broker
- **Optional** — Slack notifications, Google Sheets export, Next.js frontend

---

## Quick Start

```bash
git clone https://github.com/nikhil-at-pieces/nexus.git && cd nexus
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e .
docker compose up -d postgres redis
cp nexus/env.example .env   # then edit .env
alembic upgrade head
nexus run --host 0.0.0.0 --port 8000   # terminal 1
nexus worker                            # terminal 2
```

API: **http://localhost:8000** · Docs: **http://localhost:8000/docs**

---

## Repository

- **Repo:** [github.com/nikhil-at-pieces/nexus](https://github.com/nikhil-at-pieces/nexus)
- **Stack:** Python 3.11+, FastAPI, Celery, Redis, PostgreSQL, Docker

For full details, start with **[HANDOFF.md](HANDOFF.md)**.
