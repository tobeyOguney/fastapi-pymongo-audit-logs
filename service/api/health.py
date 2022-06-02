"""Contains definition of health check endpoint controller."""

from fastapi import APIRouter
from starlette.responses import Response

from service.core.config import settings
from service.db import get_client

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=204)
def health() -> Response:
    """Health check endpoint controller."""

    with get_client() as client:
        db = client[settings.DB_NAME]
        matching_users = db.users.find({"username": "johndoe"})

        if not matching_users:
            return Response(status_code=503)

    return Response(status_code=204)
