# pylint: disable=missing-module-docstring
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from service.api import router
from service.api.v1.services import authenticate_user, create_access_token
from service.core.config import settings
from service.db import get_client
from service.schemas import Token
from service.worker import celery


def create_application() -> FastAPI:  # pylint: disable=missing-function-docstring
    application = FastAPI(title=settings.PROJECT_NAME)
    application.include_router(router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_application()
celery_app = celery


@app.on_event("startup")
def create_first_user() -> None:
    with get_client() as client:
        db = client[settings.DB_NAME]
        user = db.users.find_one({"username": "johndoe"})

        # create dummy user if it doesn't already exist
        if not user:
            db.users.insert_one(
                dict(
                    username="johndoe",
                    full_name="John Doe",
                    email="johndoe@example.com",
                    hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                    disabled=False,
                )
            )


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
