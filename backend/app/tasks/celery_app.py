"""
Celery configuration and initialization
"""
from celery import Celery
from ..config import settings

# Check if Redis is configured
if settings.CELERY_BROKER_URL and settings.CELERY_BROKER_URL.strip():
    # Production mode with Redis
    celery_app = Celery(
        "tradescope",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=["app.tasks.backtest_tasks"]
    )
    
    # Celery configuration for production
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes max
        task_soft_time_limit=25 * 60,  # 25 minutes soft limit
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=50,
    )
else:
    # Local development mode (eager execution, no Redis needed)
    celery_app = Celery(
        "tradescope",
        include=["app.tasks.backtest_tasks"]
    )
    
    # Eager mode: execute tasks immediately in-process
    celery_app.conf.update(
        task_always_eager=True,  # Execute tasks immediately
        task_eager_propagates=True,  # Propagate exceptions
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
    )
    
    print("⚠️  Celery running in EAGER mode (no Redis) - tasks execute immediately")
