from typing import Optional, List
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from makers.apps.auth.models import User
from makers.apps.mentor.deps import get_mentor_session
from makers.apps.mentor.models import Mentor
from makers.apps.db.deps import get_db_session
from makers.apps.auth.deps import get_user_session
from makers.apps.courses import schemas, services, selectors
from makers.apps.courses.constants import CONSTANTS


router = APIRouter()


@router.post("/course",
             status_code=status.HTTP_200_OK,
             response_model=schemas.CourseBaseModel)
async def create_course(
    db: AsyncSession = Depends(get_db_session),
    *,
    data: schemas.CourseBaseModel = Depends(schemas.CourseBaseModel.as_form),
    mentor: Mentor = Depends(get_mentor_session), # noqa
):
    return await services.create_course(db,
                                        data=data,
                                        mentor=mentor,)


@router.get("/my-courses",
            response_model=List[schemas.CourseBaseModel],
            status_code=status.HTTP_200_OK)
async def get_my_courses_list(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_mentor_session),  # noqa
    limit: int = Query(8),
    offset: int = Query(0)
):
    filter_data = {}  # Define your filter data here if needed
    courses = await selectors.get_courses(db, user=user, filter_data=filter_data, limit=limit, offset=offset)
    return courses