from typing import List, Optional
from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from sqlalchemy.orm import selectinload, joinedload

from makers.apps.auth.models import User
from makers.apps.courses.models import Course



async def get_courses(db: AsyncSession,
                      *,
                      user,
                      filter_data: dict,
                      limit: int,
                      offset: int):
    courses = (
        select(Course).options(
            joinedload(Course.user)
        )
    ).order_by(desc(Course.created_at)).limit(limit).offset(offset)


    for field, value in filter_data.items():
        courses = courses.filter(getattr(Course, field) == value)

    courses_list = await db.execute(courses)
    return courses_list.scalars().all()
    