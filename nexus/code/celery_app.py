"""
Celery application for background task processing.
Creates and configures the Celery app; used by nexus worker.
"""
from celery import Celery
import os


def get_celery_config():
    """Get Celery configuration from settings or environment."""
    try:
        from nexus.core.config import get_settings
        settings = get_settings()
        return {
            "broker_url": settings.celery_broker_url,
            "result_backend": settings.celery_result_backend,
            "timezone": "UTC",
            "task_soft_time_limit": 1800,
            "task_time_limit": 3600,
        }
    except Exception:
        return {
            "broker_url": os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1"),
            "result_backend": os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2"),
            "timezone": "UTC",
            "task_soft_time_limit": 1800,
            "task_time_limit": 3600,
        }


def create_celery_app() -> Celery:
    """Create and configure Celery application."""
    config = get_celery_config()
    celery_app = Celery(
        "nexus",
        broker=config["broker_url"],
        backend=config["result_backend"],
    )
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone=config["timezone"],
        enable_utc=True,
        task_soft_time_limit=config["task_soft_time_limit"],
        task_time_limit=config["task_time_limit"],
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        task_routes={"nexus.workers.tasks.*": {"queue": "default"}},
        imports=["nexus.workers.tasks"],
    )
    return celery_app


app = create_celery_app()
celery_app = app
