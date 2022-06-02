"""Service API routes."""

from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from service.api.v1.services import get_current_active_user
from service.api.v1.tasks import create_event_task
from service.core.config import settings
from service.db import get_client
from service.schemas import Event, JobStatusEnum, TaskID, TaskResponse, User

router = APIRouter(prefix="/v1")


@router.get("/event/", response_model=List[Event])
def get_events(current_user: User = Depends(get_current_active_user)):
    with get_client() as client:
        db = client[settings.DB_NAME]
        events = list(db.events.find())
    return events


@router.post("/event/", response_model=TaskID)
def create_event(
    event: Event, current_user: User = Depends(get_current_active_user)
) -> TaskID:
    task = create_event_task.delay(event=event.dict())
    return TaskID(taskId=task.id)


@router.get("/task", response_model=TaskResponse)
def get_event_task_result(
    taskId: str, current_user: User = Depends(get_current_active_user)
) -> TaskResponse:
    result = AsyncResult(taskId)
    response = TaskResponse(taskId=taskId, status=result.status, result=result.result)

    if response.status in [JobStatusEnum.SUCCESS, JobStatusEnum.FAILURE]:
        result.forget()

    if response.status == JobStatusEnum.FAILURE:
        response.result = str(response.result)

    return response
