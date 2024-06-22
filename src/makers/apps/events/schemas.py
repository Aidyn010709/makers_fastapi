from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, validator


class EventTypes(str, Enum):
    INVITE = "Invite"
    REQUEST_TO_JOIN = "Request to join"
    SIGN_UP = "Sign Up"
    ACCEPT = "Accept"
    REJECT = "Reject"


class EventBase(BaseModel):
    """
    Базовая схема для описания события
    """
    user_id: int = Field(..., title="ID пользователя")
    user_name: str = Field(..., title="Имя пользователя")

    team_id: int | None = Field(title="ID команды")
    team_name: str | None = Field(title="Название команды")

    event_type: EventTypes = Field(..., title="Тип события")
    application_id: int = Field(..., title="ID заявки")
    created_at: datetime = Field(..., title="Дата создания события")

    @validator("created_at")
    def validate_datetime(cls, v: datetime):
        if v and isinstance(v, datetime):
            return datetime.strftime(v, "%Y-%m-%d %H:%M")
        return v
