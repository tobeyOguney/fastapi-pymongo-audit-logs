from celery import Celery

from service.core.config import settings

celery = Celery(__name__, include=["service.api.v1.tasks"])
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
