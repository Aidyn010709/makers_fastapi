from sqlalchemy.ext.asyncio import AsyncSession

from makers.apps.mentor.profiles import schemas
from makers.apps.mentor.models import Experience

async def create_work_experience(
    db: AsyncSession,
    *,
    data_in: schemas.MentorExperience,
    mentor_id: int
) -> Experience:
    dict_user_experience: dict = data_in.dict()
    dict_user_experience["mentor_id"] = mentor_id

    user_experience = Experience(**dict_user_experience)
    db.add(user_experience)
    await db.commit()
    return user_experience
