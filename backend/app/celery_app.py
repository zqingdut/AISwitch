"""
Celery 配置
异步任务队列
"""

from celery import Celery
from app.config import settings

# 创建 Celery 实例
celery_app = Celery(
    "aiswitch",
    broker=settings.CELERY_BROKER_URL or settings.REDIS_URL or "redis://localhost:6379/0",
    backend=settings.CELERY_RESULT_BACKEND or settings.REDIS_URL or "redis://localhost:6379/0"
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 分钟超时
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# 自动发现任务
celery_app.autodiscover_tasks(["app.tasks"])
