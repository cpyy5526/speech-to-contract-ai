from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "contracts_worker",
    broker=settings.redis_url,
    backend=settings.redis_url
)
celery_app.conf.update(task_serializer="json", result_serializer="json")