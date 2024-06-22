import string
import secrets

from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from makers.apps.mentor.models import Mentor
from makers.apps.mentor.schemas import RegisteredMentorSchema


async def create_mentor(db: AsyncSession,
                        *,
                        mentor_data: RegisteredMentorSchema,
                        ):
    mentor = Mentor(**mentor_data.dict(exclude={"subject_ids"}))
    
    db.add(mentor)
    await db.commit()
    await db.refresh(mentor)
    return mentor


async def check_mentor_is_active(mentor: Mentor) -> bool:
    return mentor.is_active