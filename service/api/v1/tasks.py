"""Service write-heavy tasks."""

from celery import shared_task

from service.db import get_client
from service.schemas import Event
from service.core.config import settings


@shared_task(name="tasks.create_event_task")
def create_event_task(event: Event) -> Event:
    with get_client() as client:
        db = client[settings.DB_NAME]
        db.events.insert_one({key: val for key, val in event.items() if key != "id"})
    return Event(**event).dict()
