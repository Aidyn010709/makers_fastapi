from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, and_, update
from sqlalchemy.exc import NoResultFound
from makers.apps.courses.models import Course
from makers.apps.courses import schemas
from makers.apps.mentor.models import Mentor


async def create_course(db: AsyncSession,
                        data: schemas.CourseBaseModel,
                        mentor: Mentor
):
    course = Course(**data.dict(), user=mentor)
    db.add(course)
    await db.flush()

    await db.commit()
    return course
