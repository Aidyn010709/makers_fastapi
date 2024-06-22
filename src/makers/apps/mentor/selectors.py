from typing import List, Optional
from sqlalchemy import select, and_, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from makers.apps.mentor.models import Mentor


async def get_mentor_by_email(db: AsyncSession, *, email: str) -> Mentor | None:
    query = select(Mentor).filter(Mentor.email == email)
    user = await db.execute(query)
    return user.scalar_one_or_none()


async def get_org_mentor_detail(
    db: AsyncSession,
    *,
    pk: int,
) -> Mentor | None:
    query = select(Mentor).filter(and_(Mentor.id == pk,
                                       Mentor.is_active.is_(True)))
    org_mentor = await db.execute(query)
    mentor = org_mentor.scalar_one_or_none()
    
    return mentor


async def get_mentor_detail(db: AsyncSession, *, mentor_id: int) -> Optional[Mentor]:
    query = select(Mentor).options(
        selectinload(Mentor.experience)
    ).filter(Mentor.id == mentor_id)
    mentor = await db.execute(query)
    return mentor.scalar_one_or_none()


async def get_all_mentors(db: AsyncSession) -> List[Mentor]:
    query = select(Mentor).order_by(desc(Mentor.id))
    mentors = await db.execute(query)
    return mentors.scalars().all()
