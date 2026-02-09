# Nexus — Running the System

How to run the Nexus **Twitter / social listening** stack locally: API, worker, and scheduler. Prerequisites (Postgres, Redis, `.env`, migrations) are covered in SETUP.md.

---

## Table of Contents

1. [Overview](#overview)
2. [Start PostgreSQL and Redis](#1-start-postgresql-and-redis)
3. [Run Database Migrations](#2-run-database-migrations)
4. [Start the API](#3-start-the-api)
5. [Start the Worker](#4-start-the-worker)
6. [Start the Scheduler (Optional)](#5-start-the-scheduler-optional)
7. [Full Stack with Docker Compose](#6-full-stack-with-docker-compose)
8. [CLI: Twitter Search](#cli-twitter-search-no-api)
9. [Health and Docs Endpoints](#health-and-docs-endpoints)
10. [Troubleshooting](#troubleshooting)

---

## Overview

Nexus runs as three processes:

1. **API** — HTTP server for campaigns, runs, and listening jobs (FastAPI).  
2. **Worker** — Celery worker that executes Twitter search and analysis tasks.  
3. **Scheduler** — APScheduler for periodic/scheduled listening jobs.

You need **PostgreSQL** and **Redis** running first (see SETUP.md).

---

## 1. Start PostgreSQL and Redis

If using Docker Compose:

```bash
docker compose up -d postgres redis
```

Otherwise ensure Postgres and Redis are running and that `DATABASE_URL` and `REDIS_URL` in `.env` point to them.

---

## 2. Run Database Migrations

From the project root with your virtualenv activated:

```bash
alembic upgrade head
```

Run this after cloning or after pulling new migration files.

---

## 3. Start the API

```bash
nexus run --host 0.0.0.0 --port 8000
```

With auto-reload (development):

```bash
nexus run --reload
```

- **API base:** http://localhost:8000  
- **Interactive docs:** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health or http://localhost:8000/api/v1/health  

---

## 4. Start the Worker

In a **separate terminal**, with the same `.env` and virtualenv activated:

```bash
nexus worker
```

The worker consumes tasks from Redis (Celery). Listening runs and Twitter search jobs are executed here.

---

## 5. Start the Scheduler (Optional)

For scheduled listening runs, in another terminal:

```bash
nexus scheduler
```

---

## 6. Full Stack with Docker Compose

To run API, worker, scheduler, Postgres, and Redis in containers:

```bash
# Ensure .env exists; for Docker, use hostnames "postgres" and "redis"
# in DATABASE_URL and REDIS_URL
docker compose up -d
```

Check logs:

```bash
docker compose logs -f nexus-api
docker compose logs -f nexus-worker
docker compose logs -f nexus-scheduler
```

---

## CLI: Twitter Search (No API)

You can run a one-off Twitter/X search from the command line (uses twscrape; org-scoped accounts):

```bash
nexus twitter-search --org-id <ORG_UUID> -k "keyword1" -k "keyword2" --last-hours 48 --limit 50 --output table
```

Output formats: `table`, `json`, `jsonl`. Requires at least one twscrape account configured for the given org (e.g. via API or Settings).

---

## Health and Docs Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` or `GET /api/v1/health` | Basic health check. |
| `GET /docs` | Swagger UI for the API. |
| `GET /openapi.json` | OpenAPI schema. |

Use these to confirm the API is up and to explore endpoints.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| **API won’t start** | `NEXUS_SECRET_KEY` set (min 32 chars); `DATABASE_URL` and `REDIS_URL` correct and reachable. |
| **Worker not picking up jobs** | `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` point to Redis; worker uses same `.env` as API. |
| **Migrations** | After pulling, run `alembic upgrade head` before starting the API. |
| **Twscrape / Twitter search fails** | Ensure at least one twscrape account (Twitter cookies) is configured for the org. |
| **AI analysis not running** | Optional: set `GOOGLE_API_KEY` (or other LLM config) if you want conversation analysis. |

---

*This document is part of the Nexus documentation.*
