# pylint: disable=missing-module-docstring
from fastapi import APIRouter

from service.api.health import router as health_router
from service.api.v1.routes import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router)
router.include_router(health_router)
