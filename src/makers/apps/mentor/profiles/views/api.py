from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from makers.apps.mentor.models import Mentor
from makers.apps.db.deps import get_db_session
from makers.apps.mentor.profiles import schemas, services
from makers.apps.mentor.deps import get_mentor_session


router = APIRouter()


@router.post("/experience", status_code=status.HTTP_201_CREATED, response_model=schemas.MentorExperience)
async def create_work_experience(
    db: AsyncSession = Depends(get_db_session),
    *,
    mentor: Mentor = Depends(get_mentor_session),
    data: schemas.MentorExperience
) -> schemas.MentorExperience:
    return await services.create_work_experience(db, data_in=data, mentor_id=mentor.id)
