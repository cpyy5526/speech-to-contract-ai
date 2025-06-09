from __future__ import annotations

import logging
from celery import Celery
from app.core.config import settings

import nltk
nltk.data.path.append(settings.NLTK_DATA_PATH) # NLTK 리소스 경로 추가
try: nltk.data.find("tokenizers/punkt")
except LookupError: nltk.download("punkt", download_dir=settings.NLTK_DATA_PATH)
try: nltk.data.find("tokenizers/punkt_tab")
except LookupError: nltk.download("punkt_tab", download_dir=settings.NLTK_DATA_PATH)
try: nltk.data.find("corpora/stopwords")
except LookupError: nltk.download("stopwords", download_dir=settings.NLTK_DATA_PATH)


from app.core.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

from app.models import (
    user, token, contract, transcription, generation, suggestion
)

# Celery 인스턴스 생성
celery_app: Celery = Celery(
    "ai_contract_generator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.transcriptions", "app.tasks.generations"],
)

# 기본 설정값
celery_app.conf.update(
    task_track_started=True,
    task_time_limit=60 * 30,           # 30분 제한
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_max_tasks_per_child=100,    # 메모리 누수 방지
)

logger.info("Celery app initialized (broker: %s)", settings.CELERY_BROKER_URL)
