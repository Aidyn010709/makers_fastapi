from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from makers.apps.commons import constants
from makers.apps.mentor.constants import EnglishLevel
from makers.apps.auth.schemas import BaseUserSchema

class MentorExperience(BaseModel):
    position: str = Field(title="Должность")
    company: str = Field(title="Название компании")
    start_date: datetime = Field(title="Дата начала")
    end_date: Optional[datetime] = Field(title="Дата окончания")
    is_present: Optional[bool] = Field(title="По настоящее время")

    class Config:
        orm_mode = True

class MentorProfileResponse(BaseUserSchema):
    avatar: Optional[str] = Field(title="Аватар пользователя")
    role: str = Field(default=constants.RolesEnum.user.value, title="Роль")
    time_he_can_spend: Optional[int] = Field(title="Сколько времени он может уделять")
    english_level: Optional[EnglishLevel] = Field(title="Уровень английского")
    about_me: Optional[str] = Field(title="О себе")
    experience: Optional[List[MentorExperience]] = None

    class Config:
        orm_mode = True
