from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional, Dict, List, Annotated
from pydantic import BaseModel, Field

from makers.apps.auth.schemas import UserInDB
from makers.apps.commons.decorators import as_form
from makers.apps.courses.constants import CONSTANTS

@as_form
class CourseBaseModel(BaseModel):
    title: str = Field(title=CONSTANTS.COURSE_TITLE)
    description: str = Field(title=CONSTANTS.SHORT_DESCRIPTION)
    duration: int = Field(title=CONSTANTS.DURATION)
    start_date: datetime = Field(title=CONSTANTS.START_COURSE)
    price: int = Field(title=CONSTANTS.PRICE)

    class Config:
        orm_mode = True

