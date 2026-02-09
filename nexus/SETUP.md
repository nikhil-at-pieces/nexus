# Nexus — Setup Guide

This guide covers **environment and dependency setup** for running the **Nexus Twitter listening / social listening** tool locally. Follow these steps before running the API and worker (see RUNNING.md).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Clone and Enter Project](#1-clone-and-enter-project)
3. [Python Environment](#2-python-environment)
4. [PostgreSQL and Redis](#3-postgresql-and-redis)
5. [Environment Variables](#4-environment-variables)
6. [Database Migrations](#5-database-migrations)
7. [Verify Setup](#6-verify-setup)
8. [Optional: Full Stack with Docker Compose](#optional-full-stack-with-docker-compose)
9. [Optional: Frontend](#optional-frontend)

---

## Prerequisites

- **Python 3.11 or newer** (recommended: 3.11 or 3.12).  
- **PostgreSQL** (e.g. 15) — installed locally or via Docker.  
- **Redis** — installed locally or via Docker.  
- **Git** — for cloning the repo.

---

## 1. Clone and Enter Project

```bash
git clone https://github.com/nikhil-at-pieces/nexus.git
cd nexus
```

---

## 2. Python Environment

Create a virtual environment and install the project in editable mode:

```bash
python3.11 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# Windows:  .venv\Scripts\activate

pip install -e .
```

This installs dependencies from the root `pyproject.toml`. If you need a constraints file or extra dependencies, add them after `pip install -e .`.

---

## 3. PostgreSQL and Redis

**Option A — Docker Compose (recommended for local dev):**

```bash
docker compose up -d postgres redis
```

Defaults from `docker-compose.yml`: Postgres on `localhost:5432`, database `nexus`, user `nexus`, password `nexus`. Redis on `localhost:6379`.

**Option B — Local install:**

Install and start Postgres and Redis with your OS package manager. Create a database (e.g. `nexus`) and note the connection URL and Redis URL for the next step.

---

## 4. Environment Variables

Copy the example env file to the **project root** (not inside `nexus/`) and edit it:

```bash
cp nexus/env.example .env
```

Edit `.env` and set at least:

| Variable | Example | Description |
|----------|---------|-------------|
| **NEXUS_SECRET_KEY** | Long random string (32+ chars) | Required for the app. |
| **DATABASE_URL** | `postgresql+asyncpg://nexus:nexus@localhost:5432/nexus` | PostgreSQL URL (asyncpg driver). |
| **REDIS_URL** | `redis://localhost:6379/0` | Redis for app cache/session. |
| **CELERY_BROKER_URL** | `redis://localhost:6379/1` | Redis DB for Celery broker. |
| **CELERY_RESULT_BACKEND** | `redis://localhost:6379/2` | Redis DB for Celery results. |

Other variables in `nexus/env.example` are optional (e.g. `GOOGLE_API_KEY` for AI analysis, Slack/Sheets, Clerk). **Do not commit `.env` or real secrets to the repo.**

---

## 5. Database Migrations

From the project root with your venv activated:

```bash
alembic upgrade head
```

This applies all migrations in `alembic/versions/`. Run after every pull that includes new migration files.

---

## 6. Verify Setup

- **Postgres:** Connect with `psql` or a GUI using `DATABASE_URL`.  
- **Redis:** `redis-cli ping` should return `PONG`.  
- **App:** Start the API with `nexus run --host 0.0.0.0 --port 8000` and open http://localhost:8000/docs or hit `/health` or `/api/v1/health`. See RUNNING.md.

---

## Optional: Full Stack with Docker Compose

To run API, worker, scheduler, Postgres, and Redis in containers:

```bash
# Ensure .env exists and is correct for Docker:
# DATABASE_URL with host "postgres", REDIS_URL with host "redis"
docker compose up -d
```

Then check logs for `nexus-api` and `nexus-worker` to confirm they start without errors.

---

## Optional: Frontend

The repo includes `nexus-frontend/` (Next.js). To run it:

```bash
cd nexus-frontend
npm install
npm run dev
```

Configure its env (e.g. `NEXT_PUBLIC_API_URL`, Clerk keys) as needed; see frontend README if present.

---

*This document is part of the Nexus documentation.*
