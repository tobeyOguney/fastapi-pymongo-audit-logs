"""Schema module."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID, uuid4

from bson import ObjectId
from pydantic import BaseModel, Extra, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class JobStatusEnum(str, Enum):
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    RETRY = "RETRY"
    REVOKED = "REVOKED"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"


class TaskID(BaseModel):
    taskId: UUID = Field(default_factory=uuid4)


class TaskResponse(BaseModel):
    taskId: UUID = Field(default_factory=uuid4)
    status: JobStatusEnum
    result: Any = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Event(BaseModel):
    """
    The explicitly defines invariant fields in an event.
    Also extendable to accomodate specific event types with extra fields w/o modification.
    """

    id: Optional[PyObjectId] = Field(alias="_id")
    eventType: str = Field(
        ..., description="an unrestricted enum of event type values."
    )
    createdAt: datetime = Field(..., description="Timestamp for event creation.")

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
