# Nexus — Architecture Overview

This document describes the architecture of **Nexus** as a **Twitter listening / social listening** tool run locally. It covers the main components, data flow, and where to find things in the codebase.

---

## Table of Contents

1. [High-Level Components](#high-level-components)
2. [Components in Detail](#components-in-detail)
3. [Data Flow](#data-flow)
4. [Project Layout](#project-layout)
5. [External Services](#external-services)
6. [Deployment Model](#deployment-model)

---

## High-Level Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   HTTP API      │     │  Background     │     │   Scheduler     │
│   (FastAPI)     │────▶│  Worker         │     │   (APScheduler) │
│   Port 8000     │     │  (Celery)       │     │   (in-process)  │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Redis (broker + cache)                       │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PostgreSQL (persistent data)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components in Detail

### 1. API Server

- **Framework:** FastAPI  
- **Entry:** `nexus run` or `uvicorn` against `nexus.api.app`  
- **Role:** Serves HTTP endpoints for campaigns, listening runs, progress, health, and CRUD. All heavy work (Twitter search, conversation building, AI analysis) is delegated to the worker via Celery tasks.  
- **Config:** Environment variables (see SETUP.md); main config in `nexus.core.config` (`Settings`).  
- **Key routes (conceptually):** Organizations, campaigns, runs (create run, get progress), health, optional Slack OAuth and twscrape account management. OpenAPI docs at `/docs`.

### 2. Background Worker

- **Stack:** Celery with Redis as broker and result backend.  
- **Entry:** `nexus worker`  
- **Role:** Picks up tasks from Redis: executes Twitter/X search (twscrape), builds conversation threads, runs AI analysis, writes opportunities/results to DB and optionally to Slack/Sheets. Keeps the API responsive.  
- **Config:** Same `.env` as API; `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` (often same Redis host, different DB index).

### 3. Scheduler

- **Stack:** APScheduler (in-process).  
- **Entry:** `nexus scheduler`  
- **Role:** Runs periodic or scheduled listening jobs; enqueues Celery tasks for Twitter search and analysis.  
- **Config:** Same `.env` as API/worker.

### 4. Redis

- **Role:** Celery message broker, result backend, run progress cache, and general app cache/session store.  
- **Default port:** 6379. Use different DB numbers for broker, results, and app cache if desired (see env.example).

### 5. PostgreSQL

- **Role:** Primary persistent store: organizations, users, campaigns, runs, and related data.  
- **Migrations:** Alembic; migrations live under `alembic/`. Always run `alembic upgrade head` after pulling or before first run.

---

## Data Flow

1. **Client → API:** Create campaign or start a listening run (e.g. POST with campaign id, options).  
2. **API → Worker:** API enqueues a Celery task (Twitter search + analysis) and returns a run id; client can poll progress.  
3. **Worker:** Picks up task from Redis, runs twscrape search, builds conversations, runs AI analysis, writes to DB/Redis, marks task complete. Progress is written to Redis for live polling.  
4. **Scheduler:** On a schedule, enqueues Celery tasks for scheduled listening runs.  
5. **Storage:** Persistent state (campaigns, runs, opportunities) in PostgreSQL; run progress and cache in Redis.

---

## Project Layout

Relevant paths for running and understanding the system:

| Path | Description |
|------|-------------|
| `nexus/` | Main Python package. |
| `nexus/api/` | FastAPI app, routes (campaigns, runs, health, etc.). |
| `nexus/api/v1/` | Versioned API endpoints. |
| `nexus/core/` | Config (`config.py`), database, logging. |
| `nexus/workers/` | Celery app and task definitions (listening runs, Twitter search). |
| `nexus/scheduler/` | Scheduler entry and scheduled listening jobs. |
| `nexus/platform_connectors/x/` | Twitter/X listening: keyword search, analysis, twscrape integration. |
| `nexus/services/` | Run service, campaign service, AI analysis, Slack, Google Sheets, twscrape accounts, etc. |
| `nexus/models/` | SQLAlchemy models (used by API and worker). |
| `alembic/` | Database migrations. |
| `nexus/` | This documentation set. |
| `docker-compose.yml` | Optional full stack (API, worker, scheduler, Postgres, Redis). |
| `nexus-frontend/` | Optional Next.js frontend (run separately). |

---

## External Services

| Service | Purpose | Required? |
|---------|---------|-----------|
| **Twitter/X (twscrape)** | Search tweets, conversation context. | Yes for listening; uses cookies (no API key). |
| **Google Gemini (or other LLM)** | Conversation analysis, relevance, suggestions. | Optional but typical for “AI analysis” runs. |
| **Slack** | Notifications (e.g. run complete, top opportunities). | Optional. |
| **Google Sheets** | Export opportunities/conversations. | Optional. |
| **Clerk (or similar)** | Auth for frontend; backend validates tokens. | Optional if using frontend. |

---

## Deployment Model

This handoff assumes a **local or single-machine** deployment:

- One API process.  
- One or more worker processes (you can run multiple workers for throughput).  
- One scheduler process.  
- One Redis instance.  
- One PostgreSQL instance.

For production-like setups, use environment variables to point to external Postgres/Redis; the same code and docs apply. This handoff does not describe multi-tenant or SaaS-specific architecture.

---

*This document is part of the Nexus documentation.*
