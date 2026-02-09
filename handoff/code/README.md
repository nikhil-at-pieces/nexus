# Code Reference

This folder contains key modules from the Nexus codebase so you can see the real structure and patterns. The full runnable project lives at the repo root (`nexus/`, `pyproject.toml`, etc.). Use `nexus run`, `nexus worker`, and `nexus scheduler` from the repo root to run the application.

| File | Description |
|------|-------------|
| `config.py` | Core settings (env-based): app, DB, Redis, Celery. Mirrors `nexus/core/config.py`. |
| `app.py` | FastAPI app factory and health route. Mirrors `nexus/api/app.py` pattern. |
| `main.py` | CLI entry: `run`, `worker`, `twitter-search`. Mirrors `nexus/main.py`. |
| `celery_app.py` | Celery app creation and a sample task. Mirrors `nexus/workers/celery_app.py` and `nexus/workers/tasks.py`. |
| `build_search_query.py` | Twitter/X search query builder and tweet-to-dict helper. Used by CLI and connectors. |

These are the same patterns and structure used in the live codebase.
