from __future__ import annotations

import logging

from celery import Celery

from app.core.config import settings

logger = logging.getLogger(__name__)

# Celery 인스턴스 생성
celery_app: Celery = Celery(
    "ai_contract_generator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.jobs"],
)

# 기본 설정값
celery_app.conf.update(
    task_track_started=True,
    task_time_limit=60 * 30,           # 30분 제한
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=False,
    worker_max_tasks_per_child=100,    # 메모리 누수 방지
)

logger.info("Celery app initialized (broker: %s)", settings.CELERY_BROKER_URL)

__all__ = ["celery_app"]
